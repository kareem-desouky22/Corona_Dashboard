from coronaplots import CoronaPlots

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output , State
import dash_table
import os


# data
confirmed_url = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/'
                 'master/csse_covid_19_data/csse_covid_19_time_series/'
                 'time_series_covid19_confirmed_global.csv')
deaths_url = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/'
              'master/csse_covid_19_data/csse_covid_19_time_series/'
              'time_series_covid19_deaths_global.csv')
recovered_url = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19'
                 '/master/csse_covid_19_data/csse_covid_19_time_series/'
                 'time_series_covid19_recovered_global.csv')

country_codes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'country_codes.csv')
country_codes_file = country_codes_path

cp = CoronaPlots(confirmed_url, deaths_url, recovered_url, country_codes_file)

choropleth = cp.build_map()
summary_table = cp.summary_table
summary = f'''
             **Last update**: {cp.last_update}

             **Total confirmed cases**: {cp.total_confirmed_cases}
            '''


# setting up DASH server
app = dash.Dash(
    __name__, external_stylesheets=[
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
    ]
)
server = app.server
app.title = 'COVID-19 Live Dashboard'


# app layout
app.layout = html.Div(id='container',children=[
    # header
    html.H1(["Coronavirus (COVID-19) Live Dashboard", ], id='h1'),
    html.H1(["________________________________________________________________________", ], id='h2'),

    html.Div(id='columns', children=[

        # column: summary and datatable
                html.Div(id='f-col',
                 children=[
                     html.Div([dcc.Markdown([summary])],
                              id='summary'),
                              dcc.Input(
                                placeholder="Enter country",
                                id="country-input",
                                style={"width":"22%"},
                                     ),
                                html.Button(id='search', n_clicks=0, children='Search'),
                                html.Div(id='dummy'),
                                html.H1(["________________________________________________________________________", ], id='h3'),
                     dash_table.DataTable(
                         data=summary_table.to_dict('records'),
                         columns=[{'id': c, 'name': c}
                                  for c in summary_table.columns],
                         fixed_rows={'headers': True},

                         style_cell={
                             'backgroundColor': 'rgb(50, 50, 50)',
                             'color': 'white',
                             'font-family': 'PT Sans',
                             'font-size': '1.4rem',
                         },

                         style_table={
                             'maxHeight': '222px',
                             'max-width': '90%',
                             'overflowY': 'auto',

                         },

                         style_cell_conditional=[

                             {'if': {'column_id': 'Country/Region'},
                              'width': '85px',
                              'textAlign': 'left'},
                             {'if': {'column_id': 'Confirmed'},
                              'width': '85px'},
                         ],
                         #style_data_conditional=[
                         #    {
                          #    'if': {'row_index': 'odd'},
                           #   'backgroundColor': 'rgb(248, 248, 248)'
                            # }
                         #],
                         style_header={
                             'backgroundColor': 'rgb(30, 30, 30)',
                             'fontWeight': 'bold'
                         },
                        # style_as_list_view=True,
                     ),
                 ]), ]),
                 
        # column (map)
        html.Div(id='s-col',
                 children=[
                     dcc.Graph(id="map", config={
                         'displayModeBar': False}, figure=choropleth),
                 ]),


    # footer
    html.Div([dcc.Markdown(('Data source: [COVID-19 (2019-nCoV)'
                            ' Data Repository by Johns Hopkins CSSE]'
                            '(https://github.com/CSSEGISandData/COVID-19)'))],
             id='source'),
    dcc.Markdown(('Developed by Kareem Desouky '
                  ' using [DASH](https://plot.ly/dash/)')),
])

# ------------------------------- CALLBACK---------------------------------------- #

@app.callback(Output("dummy", "children"), [Input("search", "n_clicks")], [State("country-input", "value")])
def new_search(n_clicks, country ):
    if not country:
        return "Please enter the country in a valid format ex : Egypt "
    #return f"Dashboard started working on {country}..."
    #return f"confirmed case {summary_table.loc[summary_table['Country/Region'] == country, 'Confirmed'].item()}..."
    cases = f"Confirmed cases in {country} : {summary_table.loc[summary_table['Country/Region'] == country,'Confirmed'].iloc[0]}"
    if not cases :
        return "Please enter the country in a valid format ex : Egypt "
    return cases

if __name__ == '__main__':
    app.run_server(debug = False)