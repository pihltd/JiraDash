from dash import html, dcc
import src.layouts.jiraStyles as js

activetableheader = html.Div([
    html.Hr(),
    html.H2("Active Sprint Summary", id='activesprinttitle'),
    html.Hr()
    ]
)

activesprinttable = html.Div([
    dcc.Loading([
        html.H2("Active Sprint Table"),
        html.Hr(),
        html.Div(id='activesprinttable'),
    ])
])

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

activeFrontBackSummaryTable = html.Div([
    dcc.Loading([
        html.H2('Active Component Point Totals'),
        html.Hr(),
        html.Div(id='frontbacksummary')
    ])
])

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

activesection = html.Div([
    html.Div(activetableheader),
    html.Hr(),
    html.Div(loadbutton),
    html.Hr(),
    html.Div(activesprinttable)
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

futurereleasetable = html.Div([
    dcc.Loading([
        html.H2('Future Releases'),
        html.Hr(),
        html.Div(id='futurereleasetable')
    ])
])

sitelayout = html.Div([
    dcc.Tabs(
        id='tabcontainer',
        value='summarytab',
        children=[
            dcc.Tab(
                id='summarytab',
                label='Active Sprint Summary',
                style=js.TAB_STYLE,
                selected_style=js.SELECTED_TAB_STYLE,
                #children=[loadbutton, activePointSummaryTable, activeFrontBackSummaryTable,ticketcounts]
                children=[loadbutton, activeConglomerate, ticketcounts]
            ),
            dcc.Tab(
                id='activedetails',
                label='Active Sprint Details',
                style=js.TAB_STYLE,
                selected_style=js.SELECTED_TAB_STYLE,
                children=[activetableheader, activesprinttable]
            ),
            dcc.Tab(
              id='futursummary',
              label='Future Sprint Summary',
              style=js.TAB_STYLE,
              selected_style=js.SELECTED_TAB_STYLE,
              children=[]
            ),
            dcc.Tab(
                id='futuredetail',
                label='Future Sprint Details',
                style=js.TAB_STYLE,
                selected_style=js.SELECTED_TAB_STYLE,
                children=[futurereleasetable]
            )
        ]
    )
])

