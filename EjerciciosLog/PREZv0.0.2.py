import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import MoodleAnalysisLibrary
import pandas as pd

prueba = (MoodleAnalysisLibrary.MoodleAnalysisLibrary("logs_G668_1819_20191223-1648.csv",
                                                      "C:/Users/sal8b/OneDrive/Escritorio/Beca", "Usuarios.csv",
                                                      ['0', '-1']))
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
                             prueba.num_participants_nonparticipants(prueba.dataframe, prueba.dataframeUsuarios)[
                                 'Participantes'][0],
                             prueba.num_participants_nonparticipants(prueba.dataframe, prueba.dataframeUsuarios)[
                                 'No participantes'][0]], 'type': 'pie',
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
            html.Iframe(
                srcDoc=prueba.list_nonparticipant(prueba.dataframe, prueba.dataframeUsuarios).to_html(index=False)),
        ],
            style={'display': 'inline-block', 'white-space': 'nowrap'}, )
    ], style={'text-align': 'center'}),

])

if __name__ == '__main__':
    app.run_server(debug=True)
