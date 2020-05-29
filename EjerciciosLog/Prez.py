import Maadle
import PrezGUI
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import os
from tkinter import *
import webbrowser

RECURSO = 'Recurso'
FECHA = 'Fecha'

prezz = (Maadle.Maadle(PrezGUI.windowLog.log, "", PrezGUI.windowConfig.config))


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.realpath('.')
    return os.path.join(datadir, filename)


app = dash.Dash(__name__, assets_folder=find_data_file('assets/'))
app.title = 'Prez'
server = app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'grey': 'rgb(50, 50, 50)'
}
webbrowser.open_new("http://localhost:8080")

app.layout = html.Div(
    style={'margin': '3%'},
    children=[
        html.Div(
            id="header",
            style={'align-items': 'center'},
            className="row flex-display",
            children=[
                html.Div(
                    className="one-third column",
                    children=[
                        html.Img(
                            id="UC-logo", src="assets/logo_UC.png",
                            style={
                                'height': '100px',
                                'width': 'auto',
                                'margin-bottom': '25px'
                            })
                    ]),
                html.H2(
                    className="two-third column",
                    children=prezz.nombre_curso,
                    style={
                        'textAlign': 'center',
                        'color': colors['text'],
                    }
                ),
                html.Div(
                    className="one-third column",
                    children=[
                        html.Img(
                            id="ISTR-logo",
                            src="assets/logo_ISTR.png",
                            style={
                                'height': '80px',
                                'width': 'auto',
                                'margin-bottom': '25px'
                            })
                    ]),
            ]),

        html.Div(
            children=[
                html.Div(
                    className='four columns',
                    children=[
                        html.H3(
                            children='Usuarios no participantes',
                            style={
                                'textAlign': 'center',
                                'color': colors['text'],
                            }
                        ),
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in
                                     prezz.list_nonparticipant().columns],
                            data=prezz.list_nonparticipant().to_dict(
                                'records'),
                            style_header={'backgroundColor': colors['background']},
                            style_cell={'textAlign': 'left',
                                        'backgroundColor': colors['grey'],
                                        'color': colors['text'],
                                        },
                            style_table={
                                'maxHeight': '200px',
                                'maxWidth': '400px',
                                'overflowY': 'scroll'
                            },
                        ),
                    ],
                    style={'marginLeft': '150px'}
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id='pie-chart-participants-users',
                            figure={
                                'data': [
                                    {'labels': [Maadle.PARTICIPANTES, Maadle.NO_PARTICIPANTES],
                                     'values': [
                                         prezz.num_participants_nonparticipants()[
                                             Maadle.PARTICIPANTES][0],
                                         prezz.num_participants_nonparticipants()[
                                             Maadle.NO_PARTICIPANTES][0]], 'type': 'pie',
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
                        )], style={'display': 'inline-block'},
                ),

            ], ),
        dcc.Graph(
            id='ParticipantesPorRecurso',
            figure={
                'data': [
                    {'x': prezz.participants_per_resource()[Maadle.NUM_PARTICIPANTES],
                     'y': prezz.participants_per_resource()[RECURSO], 'type': 'bar', 'orientation': 'h'},
                ],
                'layout': {
                    'title': 'Participantes por recurso',
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
        html.Div(
            children=[
                html.Div(
                    children='Introduce el rango de fechas deseado ',
                    style={
                        'textAlign': 'left',
                        'color': colors['text'],
                        'font-size': '20px'},
                ),
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    display_format='D/M/Y',
                    style={'font-size': '20px'},
                    first_day_of_week=1,
                    min_date_allowed=prezz.events_per_day()[FECHA].min(),
                    max_date_allowed=prezz.events_per_day()[FECHA].max(),
                    start_date=prezz.events_per_day()[FECHA].min(),
                    end_date=prezz.events_per_day()[FECHA].max(),
                ),
                dcc.Graph(id='graph-events-per-day-students'),
            ], style={'background': colors['grey']}
        ),

        dcc.Graph(
            id='EventosPorRecurso',
            figure={
                'data': [
                    {'x': prezz.events_per_resource()[Maadle.NUM_EVENTOS],
                     'y': prezz.events_per_resource()[RECURSO], 'type': 'bar', 'orientation': 'h'},
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
        html.Div(
            children=[
                html.Div(
                    children='Seleccione a un usuario ',
                    style={
                        'textAlign': 'left',
                        'color': colors['text'],
                        'font-size': '20px'},
                ),
                dcc.Dropdown(
                    id='users-dropdown',
                    options=[{'label': i, 'value': i} for i in prezz.dataframe[Maadle.NOMBRE_USUARIO].unique()
                             ],
                    searchable=True,
                    placeholder="Seleccione a un usuario",
                    value=prezz.dataframe[Maadle.NOMBRE_USUARIO].unique()[0]
                ),
                dcc.Graph(id='graph-events-per-day-per-student')
            ], style={'background': colors['grey']}),

        html.Div(
            children=[
                html.Div(
                    children='Seleccione un recurso ',
                    style={
                        'textAlign': 'left',
                        'color': colors['text'],
                        'font-size': '20px'},
                ),
                dcc.Dropdown(
                    id='resources-dropdown',
                    options=[{'label': i, 'value': i} for i in prezz.dataframe[Maadle.CONTEXTO].unique()
                             ],
                    searchable=True,
                    placeholder="Seleccione a un usuario",
                    value=prezz.dataframe_recursos[Maadle.CONTEXTO][0]
                ),
                dcc.Graph(id='graph-events-per-day-per-resource')
            ], style={'background': colors['background']}),
dcc.Graph(
            id='EventosPorRecurso',
            figure={
                'data': [
                    {'x': prezz.events_per_resource()[Maadle.NUM_EVENTOS],
                     'y': prezz.events_per_resource()[RECURSO], 'type': 'bar', 'orientation': 'h'},
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

    ])


@app.callback(
    dash.dependencies.Output('graph-events-per-day-students', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    dfaux5 = prezz.events_between_dates(start_date, end_date)
    return {
        'data': [
            {'x': dfaux5[FECHA], 'y': dfaux5[Maadle.NUM_EVENTOS], 'type': 'scatter'},
        ],
        'layout': {
            'title': 'Eventos por rango de días',
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['grey'],
            'font': {
                'color': colors['text']
            }
        },
    }


@app.callback(
    dash.dependencies.Output('graph-events-per-day-per-student', 'figure'),
    [dash.dependencies.Input('users-dropdown', 'value')])
def update_output(value):
    dfaux6 = prezz.events_per_day_per_user(value)
    return {
        'data': [
            {'x': dfaux6[FECHA], 'y': dfaux6[Maadle.NUM_EVENTOS], 'type': 'bar'},
        ],
        'layout': {
            'title': 'Eventos por rango de días por alumnos',
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['grey'],
            'font': {
                'color': colors['text']
            }
        },
    }


@app.callback(
    dash.dependencies.Output('graph-events-per-day-per-resource', 'figure'),
    [dash.dependencies.Input('resources-dropdown', 'value')])
def update_output(value):
    dfaux7 = prezz.events_per_day_per_resource(value)
    return {
        'data': [
            {'x': dfaux7[FECHA], 'y': dfaux7[Maadle.NUM_EVENTOS], 'type': 'bar'},
        ],
        'layout': {
            'title': 'Eventos por rango de días por recurso',
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            }
        },
    }


if __name__ == '__main__':
    app.run_server(port=8080)
