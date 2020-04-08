import dash
import dash_html_components as html
import dash_core_components as dcc
import MoodleAnalysisLibrary
import dash_table
import os
import sys

log=input("Introduza el nombre del fichero log, no olvides el .csv ")
usuarios=input("Introduza el nombre del fichero de usuarios, no olvides el .csv ")
print("Introduza los ids de los usuarios a eliminar separados por un espacio ",end="")
idprofesores = list(map(str, input().split()))



prueba = (MoodleAnalysisLibrary.MoodleAnalysisLibrary(log,"",usuarios,idprofesores))

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname("C:/Users/sal8b/OneDrive/Escritorio/Despliegue/assets")
        print(datadir)
    return os.path.join(datadir, filename)


app = dash.Dash(__name__, assets_folder=find_data_file('assets/'))

server = app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
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
                    )], style={'display': 'inline-block'},
            ),

        ], ),
    dcc.Graph(
        id='ParticipantesPorRecurso',
        figure={
            'data': [
                {'x': prueba.events_per_resource(prueba.dataframe)['Número de eventos'],
                 'y': prueba.events_per_resource(prueba.dataframe)['Recurso'], 'type': 'bar', 'orientation': 'h'},
            ],
            'layout': {
                'title': 'Paticipantes por recurso',
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
            dcc.Graph(id='graph-events-per-day-students'),
        ],style={'background': 'rgb(50, 50, 50)'}
    ),

dcc.Graph(
        id='EventosPorRecurso',
        figure={
            'data': [
                {'x': prueba.events_per_resource(prueba.dataframe)['Número de eventos'],
                 'y': prueba.events_per_resource(prueba.dataframe)['Recurso'], 'type': 'bar', 'orientation': 'h'},
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
    dfaux5 = prueba.events_between_dates(prueba.dataframe, start_date, end_date, True)
    return {
        'data': [
            {'x': dfaux5['Fecha'], 'y': dfaux5['Número de eventos'], 'type': 'scatter'},
        ],
        'layout': {
            'title': 'Eventos por rango de días',
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': 'rgb(50, 50, 50)',
            'font': {
                'color': colors['text']
            }
        },
    }


if __name__ == '__main__':
    app.run_server()