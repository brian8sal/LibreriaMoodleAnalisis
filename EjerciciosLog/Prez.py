import dash
import dash_html_components as html
import dash_core_components as dcc
import Maadle
import dash_table
import os
import webbrowser
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

RECURSO = 'Recurso'
FECHA = 'Fecha'


def clicked_btn_log():
    windowLog.log = filedialog.askopenfilename(initialdir=".", title="Select file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))


def clicked_btn_config():
    windowConfig.config = filedialog.askopenfilename(initialdir=".", title="Select file",
                                                     filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))


def clicked_btn_create():
    windowCreateConfig.config = txt_config_name.get()
    if windowCreateConfig.config.isspace() or windowCreateConfig.config == "":
        messagebox.showerror("Error", "Escriba un nombre para el fichero de configuración")
    else:
        windowCreateConfig.config = windowCreateConfig.config + '.xlsx'
        windowCreateConfig.destroy()


def clicked_btn_accept():
    if not isinstance(windowConfig.config, str) or windowConfig.config == "":
        if windowCreateConfig.config != "":
            windowConfig.config = windowCreateConfig.config
            webbrowser.open_new("http://localhost:8080")
            windowConfig.destroy()
        else:
            messagebox.showerror("Error", "Seleccione un fichero de configuración")
    else:
        webbrowser.open_new("http://localhost:8080")
        windowConfig.destroy()


def clicked_btn_siguiente():
    if not hasattr(windowLog, 'log') or windowLog.log == "":
        messagebox.showerror("Error", "Seleccione un fichero log")
    else:
        windowLog.destroy()


def clicked_btn_skip():
    windowCreateConfig.config = ""
    windowCreateConfig.destroy()


def on_closing():
    if messagebox.askokcancel("Cancelar", "¿Seguro que quiere cancelar el análisis?"):
        windowConfig.destroy()


windowLog = Tk()
windowLog.title("Prez")
windowLog.iconbitmap("assets/favicon.ico")

mensaje_log = Text(windowLog, width=40, height=14)
mensaje_log.insert(INSERT, "Bienvenido a Prez. Le acompañaremos en la configuración de su análisis. \n"
                           "\nEn primer lugar, pulse  'Seleccione el fichero log' y elija el fichero "
                           "log del curso que quiera analizar. "
                           "Si actualmente no lo tiene, acceda a la sección de informes de Moodle y descargue, en"
                           " formato .csv, el log del curso deseado. \n"
                           "\nUna vez seleccionado el fichero, pulse 'Siguiente'.")
btn_log = Button(windowLog, text="Seleccione el fichero log", command=clicked_btn_log)
btn_siguiente = Button(windowLog, text="Siguiente", command=clicked_btn_siguiente)

mensaje_log.pack(fill=X)
btn_log.pack(fill=X)
btn_siguiente.pack(fill=X)

windowLog.mainloop()

windowCreateConfig = Tk()
windowCreateConfig.title("Prez")
windowCreateConfig.iconbitmap("assets/favicon.ico")

mensaje_create = Text(windowCreateConfig, width=40, height=14)
mensaje_create.insert(INSERT, "Prez le permite proporcionar fichero Excel de configuración con datos adicionales del"
                              " curso.\n \nSi actualmente no dispone de este fichero, proporcione un nombre para "
                              "el mismo, pulse 'Crear' y uno será creado (en la carpeta de instalación de Prez)"
                              " y utilizado automáticamente en el análisis.\n"
                              "\nSi ya dispone de un fichero Excel de configuración pulse 'Saltar este paso'.")
btn_create = Button(windowCreateConfig, text="Crear", command=clicked_btn_create)
btn_skip = Button(windowCreateConfig, text="Saltar este paso", command=clicked_btn_skip)

mensaje_create.pack(fill=X)
txt_config_name = Entry(windowCreateConfig)
txt_config_name.pack(fill=X)
btn_create.pack(fill=X)
btn_skip.pack(fill=X)

windowCreateConfig.mainloop()

windowConfig = Tk()
windowConfig.title("Prez")
windowConfig.iconbitmap("assets/favicon.ico")

mensaje_config = Text(windowConfig, width=40, height=14)
mensaje_config.insert(INSERT, "Para terminar, si no ha creado un fichero de configuración en el paso previo pulse "
                              "'Seleccione el fichero de configuración y elija el fichero on el que quiera realizar "
                              "el análisis.\n \nUna vez creado o seleccionado el fichero de configuración, pulse "
                              "'Aceptar' y el análisis será mostrado en su navegador web.")

btn_config = Button(windowConfig, text="Seleccione el fichero de configuración", command=clicked_btn_config)
btn_accept = Button(windowConfig, text="Aceptar", command=clicked_btn_accept)
windowConfig.protocol("WM_DELETE_WINDOW", on_closing)

mensaje_config.pack(fill=X)
btn_config.pack(fill=X)
btn_accept.pack(fill=X)

windowConfig.mainloop()

prezz = (Maadle.Maadle(windowLog.log, "", windowConfig.config))


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

app.layout = html.Div(children=[

    html.H2(
        children=prezz.nombre_curso,
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
            value=prezz.dataframe[Maadle.NOMBRE_USUARIO].unique()[0]
        ),
        dcc.Graph(id='graph-events-per-day-per-student')
    ], style={'background': colors['grey']}),

    html.Div(children=[
        html.Div(children='Seleccione un recurso ', style={
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
