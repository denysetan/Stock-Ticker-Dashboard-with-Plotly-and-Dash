# Stock Ticker Dashboard

# Import packages
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web # requires v0.6.0 or later
from datetime import datetime

# Create the application
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# Create dash layout
app.layout = html.Div([

    dbc.NavbarSimple(
    brand="Stock Ticker Dashboard",
    color="dark",
    dark=True
    ),

    dbc.Jumbotron([

    # Title
    html.H1('Stocks Tracker'),

    # Input Ticker Component
    html.Div([html.P('Enter a stock ticker:', style={'paddingRight':'30px'}),
                dbc.Input(
                    id='my_ticker_symbol',
                    value='TSLA',
                    style={'fontSize':15, 'width':150}
                )],style={'display':'inline-block','verticalAlign':'top'}),
    
    # Date Picker Range Component
    html.Div([html.P('Select a start and end date:'),
                dcc.DatePickerRange(
                            id='my_date_picker',
                            min_date_allowed=datetime(2015,1,1),
                            max_date_allowed=datetime.today(),
                            start_date=datetime(2020,1,1),
                            end_date=datetime.today()
                )], 
                style={'display':'inline-block'}),

    # Button Component
    html.Div([dbc.Button('Submit',
                          color="dark",
                          className="mr-1",
                          id='submit-button',
                          n_clicks=0,
                )], 
                style={'display':'inline-block','paddingLeft':'30px'})
    ]),

    # Graph Component
    dcc.Graph(id='my_graph')
])

# Dash Callback function to display the graph
@app.callback(Output('my_graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('my_ticker_symbol','value'),
               State('my_date_picker','start_date'),
               State('my_date_picker','end_date')               
              ])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    # Reformat datetime string to object
    start = datetime.strptime(start_date[:10],'%Y-%m-%d')
    end = datetime.strptime(end_date[:10],'%Y-%m-%d')

    # Grab the stock data from yahoo API
    df = web.DataReader(stock_ticker,'yahoo', start, end)
    
    # Process the graph chart
    fig = {'data':[
            {'x':df.index,
             'y':df['Adj Close']}], 
            'layout':{'title': stock_ticker}}
    return fig

# Server Clause
if __name__ == '__main__':
    app.run_server()