import dash
import dash_core_components as dcc
import dash_html_components as html
import MoodleAnalysisLibrary
import pandas as pd

prueba = (MoodleAnalysisLibrary.MoodleAnalysisLibrary("logs_G668_1819_20191223-1648.csv",
                                                      "C:/Users/sal8b/OneDrive/Escritorio/Beca", ['0', '323','231']))
usuarios = (pd.DataFrame({'Nombre completo del usuario': ['Sanchez Barreiro, Pablo',"CUADRIELLO GALDÓS, ÁNGELA","CUEVAS RODRIGUEZ, SARA","DE SÁDABA IGAREDA, CELIA","SAL SARRIA, SAÚL","DE SANTIAGO ABASCAL, GABRIELA","CIDÓN HOFFMAN, JAIME"]}))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Log Curso 2018-2019',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-family': 'sa'
        }
    ),
    html.H2(
        children='Métodos de Desarrollo',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-family': 'sa'
        }
    ),
    dcc.Graph(
        id='EventosPorRecurso',
        figure={
            'data': [
                {'x': prueba.events_per_resource(prueba.dataframe)['Recurso'],
                 'y': prueba.events_per_resource(prueba.dataframe)['Número de eventos'], 'type': 'bar'},
            ],
            'layout': {
                'title': 'Recurso por rango de eventos',
                # 'yaxis': {'automargin': True},
                # 'xaxis': {'automargin': True},
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        },
    ),
    html.Div(children=[
        html.Div(
            dcc.Graph(
                figure={
                    'data': [
                        {'labels': ['Participantes', 'No Participantes'],
                         'values': [
                             prueba.num_participants_nonparticipants(prueba.dataframe, usuarios)['Participantes'][0],
                             prueba.num_participants_nonparticipants(prueba.dataframe, usuarios)['No participantes'][
                                 0]], 'type': 'pie',
                         'automargin': True,
                         'textinfo': 'none'},
                    ],
                    'layout': {
                        'title': 'Eventos por recurso',
                    }
                }
            ), style={'display': 'inline-block'}
        ),

        html.Div(children=[
            html.H3(
                children='Usuarios no participantes',
                style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'font-family': 'sa'
                }
            ),
            html.Iframe(srcDoc=prueba.list_nonparticipant(prueba.dataframe, usuarios).to_html(index=False)),
        ],
        style={'display': 'inline-block', 'white-space': 'nowrap'}, )
    ], style={'text-align': 'center'}),

    dcc.Graph(id='graph-events-per-day-students'),

    html.Div(children='Introduce el rango de fechas deseado ', style={
        'textAlign': 'left',
        'color': colors['text'],
        'font-size': '15px', },
             ),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        display_format='D/M/Y',
        min_date_allowed=prueba.events_per_day(prueba.dataframe)['Fecha'].min(),
        max_date_allowed=prueba.events_per_day(prueba.dataframe)['Fecha'].max(),
        start_date=prueba.events_per_day(prueba.dataframe)['Fecha'].min(),
        end_date=prueba.events_per_day(prueba.dataframe)['Fecha'].max(),
    ),

])

@app.callback(
    dash.dependencies.Output('graph-events-per-day-students', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    dfaux5 = prueba.events_between_dates(prueba.dataframe, start_date, end_date, True)
    return {
        'data': [
            {'x': dfaux5['Fecha'], 'y': dfaux5['Número de eventos'], 'type': 'scatter'},
        ],
        'layout': {
            'title': 'Eventos por rango de días',
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            }
        },
    }

if __name__ == '__main__':
    app.run_server(debug=True)
