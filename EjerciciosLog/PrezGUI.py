from tkinter import filedialog
from tkinter import messagebox
from tkinter import *


def clicked_btn_log():
    windowLog.log = filedialog.askopenfilename(initialdir=".", title="Select file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))


def clicked_btn_config():
    windowConfig.config = filedialog.askopenfilename(initialdir=".", title="Select file",
                                                     filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))


def clicked_btn_backup():
    windowBackup.backup = filedialog.askopenfilename(initialdir=".", title="Select file",
                                                     filetypes=(("mbz files", "*.mbz"), ("all files", "*.*")))


def clicked_btn_create():
    windowCreateConfig.config = filedialog.asksaveasfilename(initialdir=".", title="Select file",
                                                             filetypes=(("xlsx files", "*.xlsx"), ("all files", "*.*")))
    windowCreateConfig.config = windowCreateConfig.config + '.xlsx'
    windowCreateConfig.destroy()


def clicked_btn_skip_select_config():
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


def clicked_btn_skip_create_config():
    windowCreateConfig.config = ""
    windowCreateConfig.destroy()


def clicked_btn_accept():
    if not hasattr(windowBackup, 'backup'):
        windowBackup.backup = ""
    windowBackup.destroy()


def on_closing():
    if messagebox.askokcancel("Cancelar", "¿Seguro que quiere cancelar el análisis?"):
        windowBackup.destroy()


windowLog = Tk()
windowLog.title("Prez")
windowLog.iconbitmap("assets/favicon.ico")

mensaje_log = Text(windowLog, wrap=WORD, font='Helvetica', width=40, height=14)
mensaje_log.insert(INSERT, "Bienvenido a Prez. Le acompañaremos en la configuración de su análisis. \n"
                           "\nEn primer lugar, pulse  'Seleccione el fichero log' y elija el fichero "
                           "log del curso que quiera analizar. "
                           "Si actualmente no lo tiene, acceda a la sección de informes de Moodle y descargue, en"
                           " formato .csv, el registro del curso deseado. \n"
                           "\nUna vez seleccionado el fichero, pulse 'Siguiente'.")

mensaje_log.config(state=DISABLED)

btn_log = Button(windowLog, text="Seleccionar el fichero log", command=clicked_btn_log)
btn_siguiente = Button(windowLog, text="Siguiente", command=clicked_btn_siguiente)

mensaje_log.pack(fill=X)
btn_log.pack(fill=X)
btn_siguiente.pack(fill=X)

windowLog.mainloop()

windowCreateConfig = Tk()
windowCreateConfig.title("Prez")
windowCreateConfig.iconbitmap("assets/favicon.ico")

mensaje_create = Text(windowCreateConfig, wrap=WORD, font='Helvetica', width=40, height=14)
mensaje_create.insert(INSERT, "Prez le permite proporcionar fichero Excel de configuración con datos adicionales del"
                              " curso.\n \nSi actualmente no dispone de este fichero pulse 'Crear' y proporcione un"
                              " nombre y un lugar para que uno sea generado con los datos por defecto. De generarlo"
                              " en este punto, no hace falta que seleccione ninguno en el siguiente paso\n"
                              "\nSi ya dispone de un fichero Excel de configuración pulse 'Saltar este paso'.")
mensaje_create.config(state=DISABLED)
btn_create = Button(windowCreateConfig, text="Crear", command=clicked_btn_create)
btn_skip = Button(windowCreateConfig, text="Saltar este paso", command=clicked_btn_skip_create_config)

mensaje_create.pack(fill=X)
btn_create.pack(fill=X)
btn_skip.pack(fill=X)

windowCreateConfig.mainloop()

windowConfig = Tk()
windowConfig.title("Prez")
windowConfig.iconbitmap("assets/favicon.ico")

mensaje_config = Text(windowConfig, wrap=WORD, font='Helvetica', width=40, height=14)
mensaje_config.insert(INSERT, "Si no ha creado un fichero de configuración en el paso previo pulse "
                              "'Seleccionar el fichero de configuración' y elija el fichero on el que quiera realizar "
                              "el análisis.\n \nUna vez creado o seleccionado el fichero de configuración, pulse "
                              "'Siguiente'.")

mensaje_config.config(state=DISABLED)
btn_config = Button(windowConfig, text="Seleccionar el fichero de configuración", command=clicked_btn_config)
btn_accept = Button(windowConfig, text="Siguiente", command=clicked_btn_skip_select_config)

mensaje_config.pack(fill=X)
btn_config.pack(fill=X)
btn_accept.pack(fill=X)

windowConfig.mainloop()

windowBackup = Tk()
windowBackup.title("Prez")
windowBackup.iconbitmap("assets/favicon.ico")

mensaje_backup = Text(windowBackup, wrap=WORD, font='Helvetica', width=40, height=14)
mensaje_backup.insert(INSERT,
                      "Para terminar, si quiere disponer de alguna funcionalidad adicional, pulse "
                      "'Seleccionar la copia de seguridad' y adjunte la copia "
                      "de seguridad del curso de Moodle, se encuentra debajo de la sección de informes en la que se "
                      "descarga el registro previamente proporcionado. \n \n"
                      "Tras esto, pulse 'Aceptar' y el análisis será mostrado en su navegador web."
                      "")

mensaje_backup.config(state=DISABLED)
btn_backup = Button(windowBackup, text="Seleccionar la copia de seguridad", command=clicked_btn_backup)
btn_accept = Button(windowBackup, text="Aceptar", command=clicked_btn_accept)
windowBackup.protocol("WM_DELETE_WINDOW", on_closing)

mensaje_backup.pack(fill=X)
btn_backup.pack(fill=X)
btn_accept.pack(fill=X)

windowBackup.mainloop()
