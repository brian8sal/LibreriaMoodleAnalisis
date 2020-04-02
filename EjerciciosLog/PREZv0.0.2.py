import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import MoodleAnalysisLibrary
import pandas as pd

prueba = (MoodleAnalysisLibrary.MoodleAnalysisLibrary("logs_G668_1819_20191223-1648.csv",
                                                      "C:/Users/sal8b/OneDrive/Escritorio/Beca", "Usuarios.csv",
                                                      ['0', '323', '231']))

app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    html.H1(
        children='Log Curso 2018-2019',
        style={
            'textAlign': 'center',
            'color': colors['text'],
        }
    ),
    html.H2(
        children='Métodos de Desarrollo',
        style={
            'textAlign': 'center',
            'color': colors['text'],
        }
    ),
    dcc.Graph(
        id='EventosPorRecurso',
        figure={
            'data': [
                {'x': prueba.events_per_resource(prueba.dataframe)['Número de eventos'],
                 'y': prueba.events_per_resource(prueba.dataframe)['Recurso'], 'type': 'bar', 'orientation':'h'},
            ],
            'layout': {
                'title': 'Recursos por número de eventos',
                "titlefont": {
                    "size": 23
                },
                'yaxis': {'automargin': True},
                'xaxis': {'automargin': True},
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        },
    ),
    dcc.Graph(id='graph-events-per-day-students'),

    html.Div(children='Introduce el rango de fechas deseado ', style={
        'textAlign': 'left',
        'color': colors['text'],
        'font-size': '20px'},

             ),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        display_format='D/M/Y',
        style={'font-size': '20px'},
        min_date_allowed=prueba.events_per_day(prueba.dataframe)['Fecha'].min(),
        max_date_allowed=prueba.events_per_day(prueba.dataframe)['Fecha'].max(),
        start_date=prueba.events_per_day(prueba.dataframe)['Fecha'].min(),
        end_date=prueba.events_per_day(prueba.dataframe)['Fecha'].max(),
    ),
    html.Div(
        children=[
            html.Div(
                className='eight columns',
                children=[
                    dcc.Graph(
                        figure={
                            'data': [
                                {'labels': ['Participantes', 'No Participantes'],
                                 'values': [
                                     prueba.num_participants_nonparticipants(prueba.dataframe,
                                                                             prueba.dataframe_Usuarios)[
                                         'Participantes'][0],
                                     prueba.num_participants_nonparticipants(prueba.dataframe,
                                                                             prueba.dataframe_Usuarios)[
                                         'No participantes'][0]], 'type': 'pie',
                                 'automargin': True,
                                 'textinfo': 'none'
                                 },
                            ],
                            'layout': {
                                'title': 'Eventos por recurso',
                                "titlefont": {
                                    "size": 23
                                },
                                'plot_bgcolor': colors['background'],
                                'paper_bgcolor': colors['background'],
                                'font': {
                                    'color': colors['text']
                                }
                            }
                        }
                    )],
            ),

            html.Div(
                children=[
                    html.H3(
                        children='Usuarios no participantes',
                        style={
                            'textAlign': 'center',
                            'color': colors['text'],
                        }
                    ),
                    html.Div(
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in
                                     prueba.list_nonparticipant(prueba.dataframe, prueba.dataframe_Usuarios).columns],
                            data=prueba.list_nonparticipant(prueba.dataframe, prueba.dataframe_Usuarios).to_dict(
                                'records'),
                            style_header={'backgroundColor': colors['background']},
                            style_cell={'textAlign': 'left',
                                        'backgroundColor': 'rgb(50, 50, 50)',
                                        'color': colors['text'],
                                        },
                            style_table={
                                'maxHeight': '200px',
                                'overflowY': 'scroll'
                            },
                        ),
                    ),
                ],
                style={'display': 'inline-block'}, )
        ], style={'text-align': 'center'}),
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
