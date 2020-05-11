import dash
import dash_html_components as html
import dash_core_components as dcc
import Maadle
import dash_table
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

RECURSO = 'Recurso'
FECHA = 'Fecha'


def clicked_btn_log():
    window.log = filedialog.askopenfilename(initialdir=".", title="Select file",
                                            filetypes=(("csv files", "*.csv"), ("all files", "*.*")))


def clicked_btn_config():
    window.config = filedialog.askopenfilename(initialdir=".", title="Select file",
                                               filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))


def clicked_btn_create():
    window.config = txt_config_name.get()
    if window.config.isspace() or window.config == "":
        messagebox.showerror("Error", "Escriba un nombre para el fichero de configuración")
    else:
        window.config = window.config + '.xlsx'


def clicked_btn_accept():
    if not hasattr(window, 'log') or window.log == "":
        messagebox.showerror("Error", "Seleccione un fichero log")
    elif not isinstance(window.config, str) or window.config=="":
        messagebox.showerror("Error", "Seleccione o cree un fichero de configuración")
    else:
        window.destroy()


window = Tk()

window.title("Prez")

btn_log = Button(window, text="Seleccione el fichero log", command=clicked_btn_log)
btn_config = Button(window, text="Seleccione el fichero de configuración", command=clicked_btn_config)
btn_create = Button(window, text="Crear un fichero de configuración", command=clicked_btn_create)
btn_accept = Button(window, text="Aceptar", command=clicked_btn_accept)

txt_config_name = Entry(window, width=10)

btn_log.pack(fill=X)
txt_config_name.pack(fill=X)
btn_create.pack(fill=X)
btn_config.pack(fill=X)
btn_accept.pack(fill=X)

window.mainloop()

prezz = (Maadle.Maadle(window.log, "", window.config))


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname("C:/Users/sal8b/OneDrive/Escritorio/LibreriaMoodleAnalisis/EjerciciosLog/assets")
    return os.path.join(datadir, filename)


app = dash.Dash(__name__, assets_folder=find_data_file('assets/'))

server = app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'grey': 'rgb(50, 50, 50)'
}

app.layout = html.Div(children=[

    html.H2(
        children=
        prezz.dataframe[prezz.dataframe['Contexto del evento'].str.contains("Curso:")]['Contexto del evento'].iloc[0],
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
            html.Div(children='Introduce el rango de fechas deseado ', style={
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
    html.Div(children=[
        html.Div(children='Seleccione a un usuario ', style={
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
            value=prezz.dataframe_usuarios[Maadle.NOMBRE_USUARIO][0]
        ),
        dcc.Graph(id='graph-events-per-day-per-student')
    ], style={'background': colors['grey']}),
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
            {'x': dfaux6[FECHA], 'y': dfaux6[Maadle.NUM_EVENTOS], 'type': 'scatter'},
        ],
        'layout': {
            'title': 'Eventos por rango de días por alumno',
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['grey'],
            'font': {
                'color': colors['text']
            }
        },
    }


if __name__ == '__main__':
    app.run_server()
