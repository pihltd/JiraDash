import requests
import pandas as pd
import os
from dash import dash_table
from dateutil import parser
from dateutil.relativedelta import relativedelta

def trackerGetAPIQuery(endpoint):
    apitoken = os.getenv('JIRAAPI')
    headers = {"accept": "application/json", "Authorization": f"Bearer {apitoken}"}
    baseurl = 'https://tracker.nci.nih.gov/'
    
    try:
        res = requests.get(url=f"{baseurl}{endpoint}", headers=headers)
        if res.status_code == 200:
            return res.json()
        else:
            print(res.content)
            return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return None



def issueParser(jsonobj, key1, key2=None):
    if key2 == None:
        if key1 in jsonobj.keys():
            return jsonobj[key1]
    elif key2 is not None:
        if key1 in jsonobj.keys():
            if key2 in jsonobj[key1].keys():
                return jsonobj[key1][key2]
        else:
            return 'None'
    else:
        return 'None'


def lister(listfield, item):
    finallist = []
    for entry in listfield:
        finallist.append(entry[item])
    return finallist
    
    
def getSprints(status):
    crdcdhboard = 1177
    getactivesprint = f"/rest/agile/1.0/board/{crdcdhboard}/sprint?state={status}"
    resjson = trackerGetAPIQuery(getactivesprint)
    if resjson is not None:
        return resjson['values']
    else:
        return None
    
def getSprintTickets(sprintID, sprintstartdate=None):
    getissues = f"/rest/agile/1.0/sprint/{sprintID}/issue"
    res = trackerGetAPIQuery(getissues)
    ticket_df = pd.DataFrame(res['issues'])
    ticketlist = ticket_df['id'].unique().tolist()
    ticketreport = []
    for ticket in ticketlist:
        singleticket = f"/rest/api/2/issue/{ticket}?expand=changelog"
        singleres = trackerGetAPIQuery(singleticket)
        
        ticketfields = singleres['fields']
        ticketdata = {}
        
        #Get last change time
        lastchange = singleres['changelog']['histories'][-1]
        #lasttime = parser.parse(lastchange['created'])
        lasttime = lastchange['created']
        #Caclulate elapsed time
        if sprintstartdate is not None:
            sprinttime = parser.parse(sprintstartdate)
            ticketime = parser.parse(lasttime)
            elapsed = relativedelta(ticketime, sprinttime).days
        
        ticketdata['ticket'] = issueParser(singleres, 'key')
        ticketdata['ticketID'] = issueParser(singleres, 'id')
        ticketdata['assignee'] = issueParser(ticketfields, 'assignee', 'displayName')
        ticketdata['issueType'] = issueParser(ticketfields, 'issuetype', 'name')
        ticketdata['status'] = issueParser(ticketfields, 'status', 'name')
        ticketdata['reporter'] = issueParser(ticketfields, 'reporter', 'displayName')
        ticketdata['description'] = issueParser(ticketfields, 'description')
        ticketdata['story_points'] = issueParser(ticketfields, 'customfield_10042')
        ticketdata['components'] = str(lister(ticketfields['components'], 'name'))
        ticketdata['comments'] = str(lister(ticketfields['comment']['comments'], 'body'))
        ticketdata['release'] = str(lister(ticketfields['fixVersions'], 'name'))
        # Time stuff
        ticketdata['enddate'] = lasttime
        if sprintstartdate is not None:
            ticketdata['elaped_time'] = elapsed
       # ticketstuff['elapsed_days'] = relativedelta(lasttime, sprintstart).days
        #
        ticketreport.append(ticketdata)
    return pd.DataFrame(ticketreport)
       


def buildBasicTable(df, diffstyle = None):
    if diffstyle is None:
        styles = [{'if':{'row_index':'odd'}, 'backgroundColor': 'rgb(220,220,220)'}]
    else:
        styles = diffstyle
    
    if 'index' in df.columns:
        df = df.drop(['index'], axis=1)

    return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": e, "id": e} for e in (df.columns)],
            style_table={'overflowX':'auto'},
            style_cell={'overflow':'hidden', 'textOverflow':'ellipsis', 'maxWidth':10, 'textAlign':'center'},
            style_data={'color':'black', 'backgroundColor':'white'},
            style_data_conditional=styles,
            style_header={'backgroundColor': 'rgb(210,210,210)', 'color':'black', 'fontWeight':'bold', 'textAlign':'center'},
            tooltip_data=[
                {
                    column:{'value': str(value), 'type':'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_duration=None,
            export_format="csv"
        )