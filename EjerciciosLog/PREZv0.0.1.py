import dash
import dash_core_components as dcc
import dash_html_components as html
import MoodleAnalysisLibrary

prueba = (MoodleAnalysisLibrary.MoodleAnalysisLibrary("logs_G668_1819_20191223-1648.csv",
                                                      "C:/Users/sal8b/OneDrive/Escritorio/Beca", ['0', '-1']))

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
                {'x': prueba.eventsPerResource(prueba.dataframe)['Recurso'],
                 'y': prueba.eventsPerResource(prueba.dataframe)['Número de eventos'], 'type': 'bar'},
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
])

if __name__ == '__main__':
    app.run_server(debug=True)