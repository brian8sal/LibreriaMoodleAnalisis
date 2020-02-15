import dash
import dash_core_components as dcc
import dash_html_components as html
import MoodleAnalysisLibrary

df1 = MoodleAnalysisLibrary.createDataFrameFileName("logs_G668_1819_20191223-1648.csv")
df2 = MoodleAnalysisLibrary.createDataFrameFileName("2logs_G668_1819_20191223-1648.csv")
df1 = MoodleAnalysisLibrary.changeHoraType(df1)
df2 = MoodleAnalysisLibrary.changeHoraType(df2)
coursedf = [df1, df2]
dfaux = MoodleAnalysisLibrary.averageEventsPerParticipant(coursedf)
dfaux2 = MoodleAnalysisLibrary.eventsPerMonth(coursedf)
dfaux3 = MoodleAnalysisLibrary.eventsPerWeek(coursedf)
dfaux4 = MoodleAnalysisLibrary.eventsPerDay(coursedf)
dfaux6 = MoodleAnalysisLibrary.eventsPerResource(coursedf)
dfaux7 = MoodleAnalysisLibrary.eventsPerHour(coursedf)


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
    html.Div(children='Número de eventos: ' + str(MoodleAnalysisLibrary.numEvents(coursedf)), style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-family': 'sa',
        'font-size': '20px'
    }),
    html.Div(children='Número de participantes: ' + str(MoodleAnalysisLibrary.numParticipantsPerCourse(coursedf)), style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-family': 'sa',
        'font-size': '20px'
    }),
    html.Div(children='Media de eventos por participante ', style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-family': 'sa',
        'font-size': '20px', },
             ),
    html.Div(
        html.Iframe(srcDoc=dfaux.to_html(index=False, columns=["Participante", "Media de eventos"]), width='500'),
        style={'textAlign': 'center'}
    ),
    html.Div(children='Número de eventos por recurso ', style={
        'textAlign': 'center',
        'color': colors['text'],
        'font-family': 'sa',
        'font-size': '20px', },
             ),
    html.Div(
        html.Iframe(srcDoc=dfaux6.to_html(index=False, columns=["Recurso", "Número de eventos"]), width='500'),
        style={'textAlign': 'center'}
    ),

    dcc.Graph(
        id='EventosPorMes',
        figure={
            'data': [
                {'x': dfaux2['Fecha'], 'y': dfaux2['Número de eventos'], 'type': 'scatter'},
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
                {'x': dfaux3['Fecha'], 'y': dfaux3['Número de eventos'], 'type': 'scatter'},
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
                {'x': dfaux4['Fecha'], 'y': dfaux4['Número de eventos'], 'type': 'plot'},
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
                {'x': dfaux7['Hora'], 'y': dfaux7['Número de eventos'], 'type': 'bar'},
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
        min_date_allowed=dfaux4['Fecha'].min(),
        max_date_allowed=dfaux4['Fecha'].max(),
        start_date=dfaux4['Fecha'].min(),
        end_date=dfaux4['Fecha'].max(),
    ),

    dcc.Graph(id='graph-with-range-slider'),

    dcc.RangeSlider(
        id='slider',
        marks={i: '{} eventos'.format(i) for i in dfaux6['Número de eventos']},
        min=dfaux6['Número de eventos'].min(),
        max=dfaux6['Número de eventos'].max(),
        step=None,#Poner paso y quitar marks, muy contiguas
        value=[dfaux6['Número de eventos'].min(), dfaux6['Número de eventos'].max()]
    ),
    dcc.Graph(
        figure={
            'data': [
                {'labels': dfaux6['Recurso'], 'values': dfaux6['Número de eventos'], 'type': 'pie', 'automargin': True,
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
    dfaux5 = MoodleAnalysisLibrary.eventsBetweenDates(coursedf, start_date, end_date)
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
    dfaux6 = MoodleAnalysisLibrary.resourcesByEvents(coursedf, selected_range[0], selected_range[1])
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
