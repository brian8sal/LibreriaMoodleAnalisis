import os
import tarfile
import pandas as pd
import openpyxl
import xml.etree.ElementTree as ET

SECCION = 'Seccion'

EXCLUIDO = 'Excluido'

ID_USUARIO = 'IDUsuario'
ID_RECURSO = 'IDRecurso'
NOMBRE_USUARIO = 'Nombre completo del usuario'
NUM_PARTICIPANTES = 'Número de participantes'
DESCRIPCION = 'Descripción'
FECHA_HORA = 'Hora'
CONTEXTO = 'Contexto del evento'
NUM_EVENTOS = 'Número de eventos'
NO_PARTICIPANTES = 'No participantes'
PARTICIPANTES = 'Participantes'
ID_SESION = 'IDSesion'
ALIAS = 'Alias'
THRESHOLD = 1800


class Maadle:
    dataframe = pd.DataFrame
    dataframe_usuarios = pd.DataFrame
    dataframe_recursos = pd.DataFrame
    nombre_curso = 'Curso de Moodle'

    def __init__(self, name, path, config, backup):

        if path != "":
            self.dataframe = Maadle.create_data_frame(self, name, path)
        else:
            self.dataframe = Maadle.create_data_frame_file_fame(self, name)
        if len(self.dataframe[self.dataframe[CONTEXTO].str.contains("Curso:")][CONTEXTO]) != 0:
            self.nombre_curso = self.dataframe[self.dataframe[CONTEXTO].str.contains("Curso:")][CONTEXTO].iloc[0]
        self.dataframe = Maadle.add_ID_user_column(self)
        self.dataframe = Maadle.add_ID_resource_column(self)
        self.dataframe = self.dataframe[~self.dataframe[NOMBRE_USUARIO].isin(['-'])]
        if backup != "":
            self.dataframe[SECCION] = Maadle.course_structure(self, backup)[SECCION]
        else:
            self.dataframe[SECCION] = 1
        self.dataframe = Maadle.change_hora_type(self)
        self.dataframe = Maadle.add_mont_day_hour_columns(self)
        self.dataframe = self.dataframe.sort_values(by=[FECHA_HORA])
        self.create_config(config)
        self.dataframe = Maadle.create_dynamic_session_id(self)

    def create_config(self, config):
        self.dataframe_usuarios = pd.DataFrame(self.dataframe[NOMBRE_USUARIO].unique(), columns=[NOMBRE_USUARIO])
        self.dataframe_recursos = pd.DataFrame(self.dataframe.groupby([CONTEXTO, ID_RECURSO]).size().reset_index(),
                                               columns=[CONTEXTO, ID_RECURSO])
        self.dataframe_recursos[ALIAS] = self.dataframe_recursos[CONTEXTO]
        self.dataframe_recursos[ID_RECURSO] = self.dataframe_recursos[ID_RECURSO].astype('float')
        self.dataframe_recursos = self.dataframe_recursos.sort_values([ID_RECURSO])
        self.dataframe_recursos[EXCLUIDO] = ''
        self.dataframe_usuarios[EXCLUIDO] = ''
        self.dataframe_usuarios = self.dataframe_usuarios.sort_values([NOMBRE_USUARIO])
        if not os.path.isfile(config):
            with pd.ExcelWriter(config) as writer:
                self.dataframe_usuarios.to_excel(writer, sheet_name='Usuarios', index=False)
                self.dataframe_recursos.to_excel(writer, sheet_name='Recursos', index=False)
                writer.sheets['Usuarios'].set_column('A:A', self.dataframe_usuarios[NOMBRE_USUARIO].map(len).max())
                writer.sheets['Recursos'].set_column('A:C', self.dataframe_recursos[CONTEXTO].map(len).max())
                writer.sheets['Recursos'].set_column('B:B', options={'hidden': True})
        self.dataframe_usuarios = pd.ExcelFile(config).parse('Usuarios')
        self.dataframe_recursos = pd.ExcelFile(config).parse('Recursos')
        for i in range(self.dataframe_recursos[CONTEXTO].size):
            if pd.isna(self.dataframe_recursos[ALIAS][i]):
                self.dataframe_recursos[ALIAS][i] = " "
                self.dataframe[CONTEXTO] = self.dataframe[CONTEXTO].replace(
                    self.dataframe_recursos[CONTEXTO][i], " ")
            else:
                self.dataframe[CONTEXTO] = self.dataframe[CONTEXTO].replace(self.dataframe_recursos[CONTEXTO][i],
                                                                            self.dataframe_recursos[ALIAS][i])
        ele = []
        for i in range(self.dataframe_usuarios[NOMBRE_USUARIO].size):
            if not (pd.isna(self.dataframe_usuarios[EXCLUIDO][i]) or self.dataframe_usuarios[EXCLUIDO][
                i].isspace()):
                ele.append(self.dataframe_usuarios[NOMBRE_USUARIO][i])
        self.dataframe = self.dataframe[~self.dataframe[NOMBRE_USUARIO].isin(ele)]
        self.dataframe_usuarios = self.dataframe_usuarios[~self.dataframe_usuarios[NOMBRE_USUARIO].isin(ele)]
        ele = []
        for i in range(self.dataframe_recursos[ALIAS].size):
            if not (pd.isna(self.dataframe_recursos[EXCLUIDO][i]) or self.dataframe_recursos[EXCLUIDO][
                i].isspace()):
                ele.append(self.dataframe_recursos[ID_RECURSO][i])
        self.dataframe = self.dataframe[~self.dataframe[ID_RECURSO].isin(ele)]
        self.dataframe_recursos = self.dataframe_recursos[~self.dataframe_recursos[ID_RECURSO].isin(ele)]
        self.dataframe_recursos = self.dataframe_recursos[~self.dataframe_recursos[ID_RECURSO].isin(list(
            set(self.dataframe_recursos[ID_RECURSO].dropna().unique()) - set(
                sorted(self.dataframe[ID_RECURSO].dropna().unique()))))]

    def create_data_frame(self, name, path) -> pd.DataFrame:
        """
        Summary line.

        Crea un dataframe a partir de un archivo csv que se encuentra en determinado path.

        Parameters
        ----------
        name : str
            Nombre del fichero.
        path : str
            Dirección del fichero.

        Returns
        -------
        dataframe
            Log.

        """
        for root, directories, files in os.walk(path):
            if name in files:
                return pd.read_csv(os.path.join(root, name))

    def create_data_frame_file_fame(self, name) -> pd.DataFrame:
        """
        Summary line.

        Crea un dataframe a partir de un archivo csv.

        Parameters
        ----------
        name : str
            Nombre del fichero.

        Returns
        -------
        dataframe
            Log.

        """
        return pd.read_csv(name)

    def add_ID_user_column(self) -> pd.DataFrame:
        """
        Summary line.

        Añade una columna con el ID del usuario.

        Parameters
        ----------
        Returns
        -------
        dataframe
            Log con la columna añadida.

        """
        dataframe = self.dataframe
        dataframe[ID_USUARIO] = self.dataframe[DESCRIPCION].str.extract('[i][d]\s\'(\d*)\'', expand=True)
        return dataframe

    def add_ID_resource_column(self) -> pd.DataFrame:
        """
        Summary line.

        Añade una columna con el ID del recurso.

        Parameters
        ----------

        Returns
        -------
        dataframe
            Log con la columna añadida.

        """
        dataframe = self.dataframe
        dataframe[ID_RECURSO] = self.dataframe[DESCRIPCION].str.extract('with course module id\s\'(\d*)\'\.',
                                                                        expand=True)
        dataframe[ID_RECURSO] = pd.to_numeric(dataframe[ID_RECURSO])
        return dataframe

    def delete_columns(self, columns) -> pd.DataFrame:
        """
        Summary line.

        Elimina unas columnas del dataframe.

        Parameters
        ----------
        columns : array
            Columnas que eliminar.

        Returns
        -------
        dataframe
            Log con las columnas eliminadas.

        """
        dataframe = self.dataframe.drop(columns, axis='columns')
        return dataframe

    def delete_by_ID(self, idList) -> pd.DataFrame:
        """
        Summary line.

        Elimina una lista de usuarios dado su ID.

        Parameters
        ----------

        idList : array
            Usuarios que eliminar.

        Returns
        -------
        dataframe
            Log con los usuarios eliminados.

        """
        for ele in idList:
            dataframe = self.dataframe[~self.dataframe[ID_USUARIO].isin([ele])]
        return dataframe

    def graphic_events_per_user(self):
        """
        Summary line.

        Genera una gráfica con los eventos por usuario.

        Parameters
        ----------

        Returns
        -------


        """
        groups = self.dataframe.groupby([ID_USUARIO]).size()
        groups.plot.bar()

    def graphic_events_per_context(self):
        """
        Summary line.

        Genera una gráfica con los eventos por contexto.

        Parameters
        ----------

        Returns
        -------


        """
        groups = self.dataframe.groupby([CONTEXTO]).size
        groups.plot.bar()

    def change_hora_type(self) -> pd.DataFrame:
        """
        Summary line.

        Cambia el tipo de la columna Hora a datetime.

        Parameters
        ----------

        Returns
        -------
        dataframe
            Log con la columna Hora cambiada.

        """
        dataframe = self.dataframe
        dataframe[FECHA_HORA] = pd.to_datetime(self.dataframe[FECHA_HORA], dayfirst=True)
        return dataframe

    def between_dates(self, initial, final) -> pd.DataFrame:
        """
        Summary line.

        Devuelve los eventos que se encuentren entre dos fechas dadas.

        Parameters
        ----------
        initial : Timestamp
            Fecha inicial.
        final : Timestamp
            Fecha final.

        Returns
        -------
        dataframe
            Log con los eventos comprendidos.

        """
        result = (self.dataframe[FECHA_HORA] > initial) & (self.dataframe[FECHA_HORA] <= final)
        dataframe = self.dataframe.loc[result]
        return dataframe

    def add_mont_day_hour_columns(self) -> pd.DataFrame:
        """
        Summary line.

        Añade columnas de hora, día y mes.

        Parameters
        ----------

        Returns
        -------
        DataFrame
            Log con las columnas añadidas.

        """
        dataframe = self.dataframe
        dataframe['HoraDelDía'] = pd.DatetimeIndex(self.dataframe[FECHA_HORA]).time
        dataframe['DíaDelMes'] = pd.DatetimeIndex(self.dataframe[FECHA_HORA]).day
        dataframe['MesDelAño'] = pd.DatetimeIndex(self.dataframe[FECHA_HORA]).month
        return dataframe

    def num_events(self) -> int:
        """
        Summary line.

        Calcula el número de eventos de un dataframe.

        Parameters
        ----------

        Returns
        -------
        int
            Número de eventos en el log.

        """
        return len(self.dataframe)

    """"
    Retorna el número de profesores de un dataframe. ***PASARÁ A SER BORRADO

    Recibe como parámetro el dataframe.
    Retorna el número de profesores del dataframe.
    """""

    def num_teachers(self) -> int:
        result = 0
        for d in self.dataframe[NOMBRE_USUARIO].unique():
            if d.isupper() is False and d != '-':
                result = result + 1
        return result

    def num_participants_per_subject(self) -> int:
        """
        Summary line.

        Calcula el número de participantes de un log, sin contar a profesores.

        Parameters
        ----------

        Returns
        -------
        int
            Número de participantes en el log.

        """
        return self.dataframe[ID_USUARIO].nunique() - Maadle.num_teachers(self)

    def num_participants_nonparticipants(self) -> pd.DataFrame:
        """
        Summary line.

        Calcula el número de usuarios participantes y el de no participantes.

        Parameters
        ----------

        Returns
        -------
        Dataframe
            Dataframe con una columna para el número de participantes y otra para el número que no
            participantes.

        """
        data = {PARTICIPANTES: [0], NO_PARTICIPANTES: [0]}
        df = pd.DataFrame(data)
        df[PARTICIPANTES] = self.dataframe[ID_USUARIO].nunique()
        for fila in self.dataframe_usuarios.iterrows():
            if fila[1][NOMBRE_USUARIO] not in self.dataframe[NOMBRE_USUARIO].values:
                df[NO_PARTICIPANTES] = df[NO_PARTICIPANTES] + 1
        return df

    def list_nonparticipant(self) -> pd.Series:
        """
        Summary line.

        Recoge a los usuarios no participantes

        Parameters
        ----------

        Returns
        -------
        Series
            Lista de todos los usuarios no participantes.

        """
        result = list()
        for fila in self.dataframe_usuarios[NOMBRE_USUARIO]:
            if fila not in self.dataframe[NOMBRE_USUARIO].values:
                result.append(fila)
        if result == []:
            df = pd.DataFrame(result, columns=['TODOS HAN PARTICIPADO'])
            return df
        df = pd.DataFrame(result, columns=[NOMBRE_USUARIO])
        return df

    def num_events_per_participant(self) -> pd.DataFrame:
        """
        Summary line.

        Calcula el número de eventos por participante del log.

        Parameters
        ----------

        Returns
        -------
        DataFrame
            Lista con los participantes y su número de participantes.

        """
        result = pd.DataFrame({NUM_EVENTOS: self.dataframe.groupby([NOMBRE_USUARIO, ID_USUARIO]).size()}).reset_index()
        result = result.sort_values(by=[NUM_EVENTOS])
        return result

    def events_per_month(self) -> pd.DataFrame:
        """
        Summary line.

        Calcula el número de eventos por mes del log.

        Parameters
        ----------

        Returns
        -------
        DataFrame
            Lista con los meses y su número de participantes.

        """
        result = 0
        result = self.dataframe[FECHA_HORA].groupby(self.dataframe.Hora.dt.strftime('%Y-%m')).agg('count') + result
        resultdf = pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS])
        resultdf['Fecha'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def events_per_week(self) -> pd.DataFrame:
        """
        Summary line.

        Calcula el número de eventos por semana del log.

        Parameters
        ----------

        Returns
        -------
        DataFrame
            Lista con las semanas y su número de eventos.

        """
        result = 0
        result = self.dataframe[FECHA_HORA].groupby(self.dataframe.Hora.dt.strftime('%W')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS]))
        resultdf['Fecha'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def events_per_day(self) -> pd.DataFrame:
        """
        Summary line.

        Calcula el número de eventos por día del log.

        Parameters
        ----------

        Returns
        -------
        DataFrame
            Lista con los días y su número de eventos.

        """
        result = 0
        result = self.dataframe[FECHA_HORA].groupby(self.dataframe.Hora.dt.strftime('%Y-%m-%d')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS]))
        resultdf['Fecha'] = resultdf.index
        resultdf['Fecha'] = pd.to_datetime(resultdf['Fecha'])
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def events_per_resource(self) -> pd.DataFrame:
        """
        Summary line.

        Calcula el número de eventos por recurso del dataframe.

        Parameters
        ----------

        Returns
        -------
        DataFrame
            Dataframe con los recursos y su número de eventos.

        """
        result = 0
        result = self.dataframe.groupby([CONTEXTO, ID_RECURSO, SECCION]).size() + result
        result = result.reset_index()
        result.rename(columns={0: NUM_EVENTOS})
        result.columns = ['Recurso', ID_RECURSO, SECCION, NUM_EVENTOS]
        result = result.sort_values(ascending=False, by=[ID_RECURSO])
        return result

    def participants_per_resource(self) -> pd.DataFrame:
        """
        Summary line.

        Calcula el número de participantes por recurso del dataframe.

        Parameters
        ----------

        Returns
        -------
        DataFrame
            DataFrame con los recursos y su número de eventos.

        """
        result = self.dataframe.groupby([CONTEXTO, ID_RECURSO, SECCION])[ID_USUARIO].nunique()
        result = result.reset_index()
        result.rename(columns={0: NUM_PARTICIPANTES})
        result.columns = ['Recurso', ID_RECURSO, SECCION, NUM_PARTICIPANTES]
        result = result.sort_values(ascending=False, by=[ID_RECURSO])
        return result

    def events_per_hour(self) -> pd.DataFrame:
        """
        Summary line.

        Calcula el número de eventos por hora del dataframe.

        Parameters
        ----------

        Returns
        -------
        DataFrame
            Lista con las horas del día y su número de eventos.

        """
        result = 0
        result = self.dataframe[FECHA_HORA].groupby((self.dataframe.Hora.dt.strftime('%H'))).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS]))
        resultdf[FECHA_HORA] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def resources_by_number_of_events(self, min, max) -> pd.DataFrame:
        """
        Summary line.

        Filtra los eventos que se encuentren en un rango determinado de eventos.

        Parameters
        ----------
        min : int
            Límite inferior del rango.
        max : int
            Límite superior del rango.

        Returns
        -------
        dataframe
            Log con los eventos filtrados.

        """
        resultdf = Maadle.events_per_resource(self)
        result2 = (resultdf[NUM_EVENTOS] > min) & (resultdf[NUM_EVENTOS] <= max)
        resultdf = resultdf.loc[result2]
        return resultdf

    def events_between_dates(self, initial, final) -> pd.DataFrame:
        """
        Summary line.

        Calcula el número de eventos en determinado rango de fechas.

        Parameters
        ----------
        initial : int
            Límite inferior del rango.
        final : int
            Límite superior del rango.

        Returns
        -------
        DataFrame
            El número de eventos por cada fecha.

        """
        resultdf = Maadle.events_per_day(self)
        result2 = (resultdf['Fecha'] >= initial) & (resultdf['Fecha'] <= final)
        resultdf = resultdf.loc[result2]
        return resultdf

    def events_per_day_per_user(self, usuario) -> pd.DataFrame:
        """
        Summary line.

        Calcula el número de eventos de un usuario concreto por día del log.

        Parameters
        ----------
        usuario : String
            Nombre del usuario a analizar.

        Returns
        -------
        DataFrame
            Lista con los días y su número de eventos.

        """
        df = self.dataframe[[FECHA_HORA, NOMBRE_USUARIO]]
        df = df[df[NOMBRE_USUARIO].str.contains(usuario)]
        result = df[FECHA_HORA].groupby(df.Hora.dt.strftime('%Y-%m-%d')).agg('count')
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS]))
        resultdf['Fecha'] = resultdf.index
        resultdf['Fecha'] = pd.to_datetime(resultdf['Fecha'])
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def events_per_day_per_resource(self, resource) -> pd.DataFrame:
        """
        Summary line.

        Calcula el número de eventos de un recurso concreto por día del log.

        Parameters
        ----------
        resource : String
            ID del recurso a analizar.

        Returns
        -------
        DataFrame
            DataFrame con el nombre del evento, su recurso y las fechas en las que se interactuó con él.

        """
        df = self.dataframe[[FECHA_HORA, CONTEXTO, ID_RECURSO]]
        df = df[df[ID_RECURSO] == resource]
        result = df[FECHA_HORA].groupby(df.Hora.dt.strftime('%Y-%m-%d')).agg('count')
        resultdf = pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS])
        resultdf['Fecha'] = resultdf.index
        resultdf['Fecha'] = pd.to_datetime(resultdf['Fecha'])
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def create_dynamic_session_id(self) -> pd.DataFrame:
        """
        Summary line.

        Crea un identificador para distinguir la sesión a la que pertenece cada evento en función de un tiempo
        umbral que sirva para aproximarlas.

        Parameters
        ----------

        Returns
        -------
        DataFrame
            DataFrame con una columna para el ID de sesión añadida.

        """
        result = self.dataframe.sort_values(by=[ID_USUARIO, FECHA_HORA])
        previous_row = None
        sessionids = [None] * len(result)
        user_session_counter = 0
        session_counter = 0
        for index, row in result.iterrows():
            if previous_row is not None:
                if row[ID_USUARIO] != previous_row[ID_USUARIO]:
                    user_session_counter = 0
                distance = row[FECHA_HORA] - previous_row[FECHA_HORA]
                if distance.total_seconds() > THRESHOLD:
                    user_session_counter += 1
            sessionid = "{}:{}".format(row[ID_USUARIO], user_session_counter)
            sessionids[session_counter] = sessionid
            session_counter += 1
            previous_row = row
            result[ID_SESION] = sessionids
        return result

    def number_of_sessions_by_user(self) -> pd.DataFrame:
        """
        Summary line.

        Construye un DataFrame con el número de sesiones de cada usuario.

        Parameters
        ----------

        Returns
        -------
        DataFrame
            DataFrame con los usuarios y el número de sesiones de cada uno

        """
        df = Maadle.create_dynamic_session_id(self)
        result = pd.DataFrame(data=df.groupby(ID_USUARIO)[ID_SESION].nunique().values,
                              columns=['Número de sesiones iniciadas'])
        result[NOMBRE_USUARIO] = df[NOMBRE_USUARIO].unique()
        return result

    def sessions_matrix(self) -> pd.DataFrame:
        """
        Summary line.

        Construye la matriz de relación de los recursos.

        Parameters
        ----------

        Returns
        -------
        DataFrame
            Matriz de relación de los recursos.

        """
        df = self.dataframe.dropna()
        dfe = self.dataframe_recursos[ID_RECURSO].dropna().unique()
        lista_recursos = sorted(dfe.tolist())
        rows = len(dfe)
        columns = rows
        matrix = [[0 for _ in range(columns)] for _ in range(rows)]
        for session, event in df.groupby(ID_SESION):
            resource_iterador = 0
            for resource in dfe:
                if resource in event[ID_RECURSO].values:
                    matrix[resource_iterador][resource_iterador] = matrix[resource_iterador][resource_iterador] + 1
                    for recource_in_event in event[ID_RECURSO].unique():
                        if recource_in_event != resource:
                            matrix[resource_iterador][lista_recursos.index(recource_in_event)] = \
                                matrix[resource_iterador][lista_recursos.index(recource_in_event)] + 1
                resource_iterador = resource_iterador + 1
        matrix_result = [[0 for _ in range(columns)] for _ in range(rows)]
        for j in range(columns):
            for i in range(rows):
                aux = matrix[i][j] / matrix[j][j]
                matrix_result[j][i] = aux
        return pd.DataFrame(matrix_result)

    def course_structure(self, backup) -> pd.DataFrame:
        """
        Summary line.

        Añade la sección a la que pertenece cada recurso dentro del curso de Moodle.

        Parameters
        ----------
        str
            Ruta del la copia de seguridad del curso de Moodle en formato mbz

        Returns
        -------
        DataFrame
            DataFrame con una columna columna con la sección a la que pertenece el recurso.

        """
        tarfile.open(backup).extract(member='moodle_backup.xml')
        tree = ET.parse('moodle_backup.xml')
        root = tree.getroot()
        df = pd.DataFrame(columns=[SECCION, ID_RECURSO, 'Recurso'])
        for activity in root.findall('information/contents/activities/activity'):
            df = df.append(
                pd.Series(
                    [activity.find('sectionid').text, activity.find('moduleid').text, activity.find('title').text],
                    index=[SECCION, ID_RECURSO, 'Recurso']), ignore_index=True)
        id_curso = ''
        for activity in root.findall('information/contents/course'):
            id_curso = activity.find('courseid').text
        dfaux = self.dataframe.copy()
        dfaux[SECCION] = id_curso
        for activity, section in zip(df[ID_RECURSO], df[SECCION]):
            dfaux.loc[dfaux[ID_RECURSO] == float(activity)] = dfaux.loc[
                dfaux[ID_RECURSO] == float(activity)].astype(str).replace(id_curso, section)
        os.remove("moodle_backup.xml")
        return dfaux
