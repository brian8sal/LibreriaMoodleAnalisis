from tkinter import filedialog
from tkinter import messagebox
from tkinter import *


def clicked_btn_log():
    windowLog.log = filedialog.askopenfilename(initialdir=".", title="Select file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))


def clicked_btn_config():
    windowConfig.config = filedialog.askopenfilename(initialdir=".", title="Select file",
                                                     filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))


def clicked_btn_create():
    windowCreateConfig.config = filedialog.asksaveasfilename(initialdir=".", title="Select file",
                               filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))
    windowCreateConfig.config = windowCreateConfig.config + '.xlsx'
    windowCreateConfig.destroy()


def clicked_btn_accept():
    if not isinstance(windowConfig.config, str) or windowConfig.config == "":
        if windowCreateConfig.config != "":
            windowConfig.config = windowCreateConfig.config
            windowConfig.destroy()
        else:
            messagebox.showerror("Error", "Seleccione un fichero de configuración")
    else:
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
