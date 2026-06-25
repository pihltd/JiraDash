from dash import html, dcc
import src.layouts.jiraStyles as js
import dash_loading_spinners as dls

###########################################################
#    INDIVIDUAL COMPONENTS                                                         
##########################################################

# TODO:  Apparently the points on user stories are only QA points, the tasks have the development points.

#
# Active Tab 1
#
activetableheader = html.Div([
    html.Hr(),
    html.H2("Active Sprint Summary", id='activesprinttitle'),
    html.Hr()
    ]
)

loadbutton = html.Div([
    dcc.Button("Click to load the active sprint",id='loadbutton', n_clicks=0)
])


activePointSummaryTable = html.Div([
    dcc.Loading([
        html.H2('Active Sprint Point Totals'),
        html.Hr(),
        html.Div(id='activepointsummary')
    ])
])

'''
activePointSummaryTable = html.Div([
    dls.Hash([
        html.H2('Active Sprint Point Totals'),
        html.Hr(),
        html.Div(id='activepointsummary')
    ])
])
'''
activeFrontBackSummaryTable = html.Div([
    dcc.Loading([
        html.H2('Active Component Point Totals'),
        html.Hr(),
        html.Div(id='frontbacksummary')
    ])
])

activeTypesTable = html.Div([
    dcc.Loading([
        html.H2('Active Types Ticket Count'),
        html.Hr(),
        html.Div(id='activetypestable')
    ])
])

activeStatusTable = html.Div([
    dcc.Loading([
        html.H2('Active Status Ticket Count'),
        html.Hr(),
        html.Div(id='activestatustable')
    ])
])

activeReleaseTable = html.Div([
    dcc.Loading([
        html.H2('Active Release Ticket Counts'),
        html.Hr(),
        html.Div(id='activereleasetable')
    ])
])

#
#  Active Tab 2
#

activesprinttable = html.Div([
    dcc.Loading([
        html.H2("Active Sprint Deatails"),
        html.Hr(),
        html.Div(id='activesprinttable'),
    ])
])




#
#  Future Tab 1
#

futurePointSummaryTable = html.Div([
    dcc.Loading([
        html.H2('Future Sprint Point Totals'),
        html.Hr(),
        html.Div(id='futurepointsummary')
    ])
])

futureFrontBackSummaryTable = html.Div([
    dcc.Loading([
        html.H2('Future Component Point Totals'),
        html.Hr(),
        html.Div(id='futurefrontbacksummary')
    ])
])

futureTypesTable = html.Div([
    dcc.Loading([
        html.H2('Future Types Ticket Count'),
        html.Hr(),
        html.Div(id='futuretypestable')
    ])
])


futureStatusTable = html.Div([
    dcc.Loading([
        html.H2('Future Status Ticket Count'),
        html.Hr(),
        html.Div(id='futurestatustable')
    ])
])



futureReleaseTable = html.Div([
    dcc.Loading([
        html.H2('Future Release Ticket Counts'),
        html.Hr(),
        html.Div(id='futurereleasetable')
    ])
])

#
#  Future Tab 2
#
futuresprinttable = html.Div([
    dcc.Loading([
        html.H2("Future Sprint Deatails"),
        html.Hr(),
        html.Div(id='futuresprinttable')
    ])
])

###########################################################
#    Group layouts                                                       
##########################################################



activeConglomerate = html.Div([
    dcc.Loading([
        html.Div(
            children=[
                html.Hr(),
                html.Div(activePointSummaryTable)
            ],
            style={'width':'50%', 'display':'inline-block'},
        ),
        html.Div(
            children=[
                html.Hr(),
                html.Div(activeFrontBackSummaryTable)
            ],
            style={'width':'50%', 'display':'inline-block'},
        )
    ])
])


futureConglomerate = html.Div([
    dcc.Loading([
        html.Div(
            children=[
                html.Hr(),
                html.Div(futurePointSummaryTable)
            ],
            style={'width':'50%', 'display':'inline-block'},
        ),
        html.Div(
            children=[
                html.Hr(),
                html.Div(futureFrontBackSummaryTable)
            ],
            style={'width':'50%', 'display':'inline-block'},
        )
    ])
])

activesection = html.Div([
    html.Div(activetableheader),
    html.Hr(),
    html.Div(loadbutton),
    html.Hr(),
    html.Div(activesprinttable)
])




ticketcounts = html.Div([
    dcc.Loading([
        html.Div(
            children=[
                html.Hr(),
                html.Div(activeTypesTable)
            ],
            style={'width':'33%', 'display':'inline-block'},
        ),
        html.Div(
            children=[
                html.Hr(),
                html.Div(activeStatusTable)
            ],
            style={'width':'33%', 'display':'inline-block'},
        ),
        html.Div(
            children=[
                html.Hr(),
                html.Div(activeReleaseTable)
            ],
            style={'width':'33%', 'display':'inline-block'},
        )
    ])
])

futureticketcounts = html.Div([
    dcc.Loading([
        html.Div(
            children=[
                html.Hr(),
                html.Div(futureTypesTable)
            ],
            style={'width':'33%', 'display':'inline-block'},
        ),
        html.Div(
            children=[
                html.Hr(),
                html.Div(futureStatusTable)
            ],
            style={'width':'33%', 'display':'inline-block'},
        ),
        html.Div(
            children=[
                html.Hr(),
                html.Div(futureReleaseTable)
            ],
            style={'width':'33%', 'display':'inline-block'},
        )
    ])
])



sitelayout = html.Div([
    dcc.Tabs(
        id='tabcontainer',
        value='tab-activesummary',
        children=[
            dcc.Tab(
                id='summarytab',
                value = 'tab-activesummary',
                label='Active Sprint Summary',
                style=js.TAB_STYLE,
                selected_style=js.SELECTED_TAB_STYLE,
                children=[loadbutton, activeConglomerate, ticketcounts]
            ),
            dcc.Tab(
                id='activedetails',
                value = 'tab-activedetails',
                label='Active Sprint Details',
                style=js.TAB_STYLE,
                selected_style=js.SELECTED_TAB_STYLE,
                children=[activetableheader, activesprinttable]
            ),
            dcc.Tab(
              id='futuresummary',
              value = 'tab-futuresummary',
              label='Future Sprint Summary',
              style=js.TAB_STYLE,
              selected_style=js.SELECTED_TAB_STYLE,
              children=[futureConglomerate, futureticketcounts]
            ),
            dcc.Tab(
                id='futuredetail',
                value='tab-futuredetail',
                label='Future Sprint Details',
                style=js.TAB_STYLE,
                selected_style=js.SELECTED_TAB_STYLE,
                children=[futuresprinttable]
            )
        ]
    )
])

