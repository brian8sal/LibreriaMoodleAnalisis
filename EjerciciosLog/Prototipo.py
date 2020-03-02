import dash
import dash_core_components as dcc
import dash_html_components as html
import MoodleAnalysisLibrary

prueba=(MoodleAnalysisLibrary.MoodleAnalysisLibrary("TestingLog99Rows.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca",[]))

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
    html.Div(children='Número de eventos: ' + str(prueba.numEvents(prueba.dataframe)), style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-family': 'sa',
        'font-size': '20px'
    }),
    html.Div(children='Número de participantes: ' + str(prueba.numParticipantsPerSubject(prueba.dataframe)), style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-family': 'sa',
        'font-size': '20px'
    }),
    html.Div(children='Número de eventos por participante ', style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-family': 'sa',
        'font-size': '20px', },
             ),
    html.Div(
        html.Iframe(srcDoc=prueba.numEventsPerParticipant(prueba.dataframe).to_html(index=False, columns=["Nombre completo del usuario", "Número de eventos"]), width='500'),
        style={'textAlign': 'center'}
    ),
    html.Div(children='Número de eventos por recurso ', style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-family': 'sa',
        'font-size': '20px', },
             ),
    html.Div(
        html.Iframe(srcDoc=prueba.eventsPerResource(prueba.dataframe).to_html(index=False, columns=["Recurso", "Número de eventos"]), width='500'),
        style={'textAlign': 'center'}
    ),

    dcc.Graph(
        id='EventosPorMes',
        figure={
            'data': [
                {'x': prueba.eventsPerMonth(prueba.dataframe)['Fecha'], 'y': prueba.eventsPerMonth(prueba.dataframe)['Número de eventos'], 'type': 'scatter'},
            ],
            'layout': {
                'title': 'Eventos por mes',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),

    dcc.Graph(
        id='EventosPorSemana',
        figure={
            'data': [
                {'x': prueba.eventsPerWeek(prueba.dataframe)['Fecha'], 'y': prueba.eventsPerWeek(prueba.dataframe)['Número de eventos'], 'type': 'scatter'},
            ],
            'layout': {
                'title': 'Eventos por semana',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
    dcc.Graph(
        id='EventosPorDia',
        figure={
            'data': [
                {'x': prueba.eventsPerDay(prueba.dataframe)['Fecha'], 'y': prueba.eventsPerDay(prueba.dataframe)['Número de eventos'], 'type': 'plot'},
            ],
            'layout': {
                'title': 'Eventos por día',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
    dcc.Graph(
        id='EventosPorHora',
        figure={
            'data': [
                {'x': prueba.eventsPerHour(prueba.dataframe)['Hora'], 'y': prueba.eventsPerHour(prueba.dataframe)['Número de eventos'], 'type': 'bar'},
            ],
            'layout': {
                'title': 'Eventos por hora',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
    dcc.Graph(id='graph-with-picker'),
    html.Div(children='Introduce el rango de fechas deseado ', style={
        'textAlign': 'left',
        'color': colors['text'],
        'font-size': '15px', },
             ),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        display_format='D/M/Y',
        min_date_allowed=prueba.eventsPerDay(prueba.dataframe)['Fecha'].min(),
        max_date_allowed=prueba.eventsPerDay(prueba.dataframe)['Fecha'].max(),
        start_date=prueba.eventsPerDay(prueba.dataframe)['Fecha'].min(),
        end_date=prueba.eventsPerDay(prueba.dataframe)['Fecha'].max(),
    ),

    dcc.Graph(id='graph-with-range-slider'),

    dcc.RangeSlider(
        id='slider',
        marks={i: '{} eventos'.format(i) for i in prueba.eventsPerResource(prueba.dataframe)['Número de eventos']},
        min=prueba.eventsPerResource(prueba.dataframe)['Número de eventos'].min(),
        max=prueba.eventsPerResource(prueba.dataframe)['Número de eventos'].max(),
        step=None,#Poner paso y quitar marks, muy contiguas
        value=[prueba.eventsPerResource(prueba.dataframe)['Número de eventos'].min(), prueba.eventsPerResource(prueba.dataframe)['Número de eventos'].max()]
    ),
    dcc.Graph(
        figure={
            'data': [
                {'labels': prueba.eventsPerResource(prueba.dataframe)['Recurso'], 'values': prueba.eventsPerResource(prueba.dataframe)['Número de eventos'], 'type': 'pie', 'automargin': True,
                 'textinfo': 'none'},
            ],
            'layout': {
                'title': 'Eventos por recurso',
            }
        }
    ),

])

@app.callback(
    dash.dependencies.Output('graph-with-picker', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    dfaux5 = prueba.eventsBetweenDates(prueba.dataframe, start_date, end_date)
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
@app.callback(
    dash.dependencies.Output('graph-with-range-slider', 'figure'),
    [dash.dependencies.Input('slider', 'value')])
def update_output(selected_range):
    dfaux6 = prueba.resourcesByNumberOfEvents(prueba.dataframe, selected_range[0], selected_range[1])
    return {
        'data': [
            {'x': dfaux6['Número de eventos'], 'y': dfaux6['Recurso'], 'type': 'scatter'},
        ],
        'layout': {
            'title': 'Recurso por rango de eventos',
            'yaxis': {'automargin': True},
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            }
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
