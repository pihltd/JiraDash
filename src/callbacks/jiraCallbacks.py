from dash import Input, Output, State, dash_table
from dash.exceptions import PreventUpdate
from jiraDash import app
import src.functions.jiraFunctions as jf
import pandas as pd
import io


#
#  ACTIVE DATASTORES
#

# Populate active sprint store at startup
@app.callback(
    Output(component_id='activesprintstore', component_property='data'),
    Input(component_id='loadbutton', component_property='n_clicks')
)
def populateActiveSprintStore(n_clicks):
    resjson = jf.getSprints('active')
    if resjson is not None:
        return resjson
    else:
        print('No active sprint returned')
        return None


#Populate the active sprint ticket store
@app.callback(
    Output(component_id='activesprintticketsstore', component_property='data'),
    Input(component_id='activesprintstore', component_property='data'),
    State(component_id='loadbutton', component_property='n_clicks')
)
def populateActiveSprintTicketsStore(sprintdata, n_clicks):
    if n_clicks in [0,None]:
        raise PreventUpdate
    else:
        activeID = sprintdata[0]['id']
        ticket_df = jf.getSprintTickets(activeID)
        return ticket_df.reset_index().to_json(orient='split')
    
    
#
#    ACTVE TAB 1
#
#
#   TOP ROW
@app.callback(
    Output(component_id='activepointsummary', component_property='children'),
    Input(component_id='activesprintticketsstore', component_property='data')
)
def activeSprintPoints(activesprintticketsstore):
    df = pd.read_json(io.StringIO(activesprintticketsstore), orient='split')
    stafflist = df['assignee'].unique().tolist()
    # Need to separate QA points (User Stories) from development points (Tasks)
    pointlist = []
    for staff in stafflist:
        temp_df = df.query('assignee == @staff')
        totalpoints = temp_df['story_points'].sum()
        pointlist.append({'Assignee': staff, 'Points': totalpoints})
    point_df = pd.DataFrame(pointlist)
    return jf.buildBasicTable(df=point_df)

@app.callback(
    Output(component_id='frontbacksummary', component_property='children'),
    Input(component_id='activesprintticketsstore', component_property='data')
)
def activeFrontBackSummary(activesprintticketsstore):
    df = pd.read_json(io.StringIO(activesprintticketsstore), orient='split')
    fblist = df['components'].unique().tolist()
    summarylist = []
    for fb in fblist:
        temp_df = df.query('components == @fb')
        totalpoints = temp_df['story_points'].sum()
        summarylist.append({'Component': fb, 'Points': totalpoints})
    fb_df = pd.DataFrame(summarylist)
    return jf.buildBasicTable(df=fb_df)
#
#
# SECOND ROW
#

@app.callback(
    Output(component_id='activetypestable', component_property='children'),
    Input(component_id='activesprintticketsstore', component_property='data')
)
def activeTypeSummary(activesprintticketsstore):
    df = pd.read_json(io.StringIO(activesprintticketsstore), orient='split')
    return jf.buildBasicTable(df=df.value_counts('issueType').rename_axis('Ticket Types').reset_index(name='Counts'))


@app.callback(
    Output(component_id='activestatustable', component_property='children'),
    Input(component_id='activesprintticketsstore', component_property='data')
)
def activeStatusSummary(activesprintticketsstore):
    df = pd.read_json(io.StringIO(activesprintticketsstore), orient='split')
    return jf.buildBasicTable(df=df.value_counts('status').rename_axis('Ticket Status').reset_index(name='Counts'))



@app.callback(
    Output(component_id='activereleasetable', component_property='children'),
    Input(component_id='activesprintticketsstore', component_property='data')
)
def activeReleasesSummary(activesprintticketsstore):
    df = pd.read_json(io.StringIO(activesprintticketsstore), orient='split')
    return jf.buildBasicTable(df=df.value_counts('release').rename_axis('Ticket Release').reset_index(name='Counts'))





#
#    ACTVE TAB 2
#

# Popuate the full active sprint ticket table 
@app.callback(
    Output(component_id="activesprinttable", component_property="children"),
    Input(component_id="activesprintticketsstore", component_property="data")
)
def populateActiveSprintTicketTable(activesprintticketsstore):
    df = pd.read_json(io.StringIO(activesprintticketsstore), orient='split')
    return jf.buildBasicTable(df=df)




#
#  FUTURE DATASTORES
#
 
# Populate the future sprint store
@app.callback(
    Output(component_id='futuresprintstore', component_property='data'),
    Input(component_id='loadbutton', component_property='n_clicks')
)
def populateFutureSprintStore(n_clicks):
    resjson = jf.getSprints('future')
    if resjson is not None:
        temp_df = pd.DataFrame(resjson)
        future_df = temp_df.query('state == "future" and name.str.startswith("CRDC-DH Sprint")')
        return future_df.reindex().to_json(orient='split')


# Populate the future sprint ticket store
@app.callback(
    Output(component_id='futuresprintticketstore', component_property='data'),
    Input(component_id='futuresprintstore', component_property='data'),
    State(component_id='loadbutton', component_property='n_clicks')
)
def populateFutureSprintTicketStore(sprintdata, n_clicks):
    if n_clicks in [0, None]:
        raise PreventUpdate
    else:
        future_df = pd.read_json(io.StringIO(sprintdata), orient='split')
        final_df = pd.DataFrame()
        for index, row in future_df.iterrows():
            sprint_df = jf.getSprintTickets(row['id'])
            final_df = pd.concat([final_df, sprint_df])
        return final_df.reset_index().to_json(orient='split')


#
# FUTURE TAB 1  ROW 1
#
@app.callback(
    Output(component_id='futurepointsummary', component_property='children'),
    Input(component_id='futuresprintticketstore', component_property='data')
)
def futureSprintPoints(futuresprintticketstore):
    df = pd.read_json(io.StringIO(futuresprintticketstore), orient='split')
    stafflist = df['assignee'].unique().tolist()
    pointlist = []
    for staff in stafflist:
        temp_df = df.query('assignee == @staff')
        totalpoints = temp_df['story_points'].sum()
        pointlist.append({'Assignee': staff, 'Points': totalpoints})
    point_df = pd.DataFrame(pointlist)
    return jf.buildBasicTable(df=point_df)


@app.callback(
    Output(component_id='futurefrontbacksummary', component_property='children'),
    Input(component_id='futuresprintticketstore', component_property='data')
)
def futureFrontBackSummary(futuresprintticketstore):
    df = pd.read_json(io.StringIO(futuresprintticketstore), orient='split')
    fblist = df['components'].unique().tolist()
    summarylist = []
    for fb in fblist:
        temp_df = df.query('components == @fb')
        totalpoints = temp_df['story_points'].sum()
        summarylist.append({'Component': fb, 'Points': totalpoints})
    fb_df = pd.DataFrame(summarylist)
    return jf.buildBasicTable(df=fb_df)


#
# FUTURE TAB 1  ROW 2
#

@app.callback(
    Output(component_id='futuretypetable', component_property='children'),
    Input(component_id='futuresprintticketstore', component_property='data')
)
def futureTypeSummary(futuresprintticketstore):
    df = pd.read_json(io.StringIO(futuresprintticketstore), orient='split')
    return jf.buildBasicTable(df=df.value_counts('issueType').rename_axis('Ticket Type').reset_index(name='Counts'))


@app.callback(
    Output(component_id='futurestatustable', component_property='children'),
    Input(component_id='futuresprintticketstore', component_property='data')
)
def futureStatusSummary(futuresprintticketstore):
    df = pd.read_json(io.StringIO(futuresprintticketstore), orient='split')
    return jf.buildBasicTable(df=df.value_counts('status').rename_axis('Ticket Status').reset_index(name='Counts'))


@app.callback(
    Output(component_id='futurereleasetable', component_property='children'),
    Input(component_id='futuresprintticketstore', component_property='data')
)
def futureReleaseeSummary(futuresprintticketstore):
    df = pd.read_json(io.StringIO(futuresprintticketstore), orient='split')
    return jf.buildBasicTable(df=df.value_counts('release').rename_axis('Ticket Realease').reset_index(name='Counts'))


#
# FUTURE TAB 2
#



@app.callback(
    Output(component_id='futuresprinttable', component_property='children'),
    Input(component_id='futuresprintticketstore', component_property='data')
)
def populateFutureSprintTable(futuresprintticketstore):
    df = pd.read_json(io.StringIO(futuresprintticketstore), orient='split')
    return jf.buildBasicTable(df=df)
