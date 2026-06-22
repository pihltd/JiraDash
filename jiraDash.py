from dash import Dash, html, dcc
from src.layouts.jiraLayout import *

app = Dash(
    __name__,
    #external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    update_title="Updating..."
)
app.title ="Data Hub Jira Report"

app.layout = html.Div([
    dcc.Store(id='activesprintstore'),
    dcc.Store(id='activesprintticketsstore'),
    dcc.Store(id='futuresprintstore'),
    dcc.Store(id='futuresprintticketstore'),
    #activesection
    sitelayout
])


from src.callbacks.jiraCallbacks import *



if __name__ == "__main__":
    app.run(port=8050, debug=True)
