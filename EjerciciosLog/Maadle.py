import os
import pandas as pd
import openpyxl

ID_SESION = 'IDSesion'
CONGIG_PREZ = 'ConfigPrez.xlsx'
ID_USUARIO = 'IDUsuario'
NOMBRE_USUARIO = 'Nombre completo del usuario'
NUM_PARTICIPANTES = 'Número de participantes'
DESCRIPCION = 'Descripción'
FECHA_HORA = 'Hora'
CONTEXTO = 'Contexto del evento'
NUM_EVENTOS = 'Número de eventos'
NO_PARTICIPANTES = 'No participantes'
PARTICIPANTES = 'Participantes'

THRESHOLD = 1800


class Maadle:
    dataframe = pd.DataFrame
    dataframe_usuarios = pd.DataFrame
    dataframe_recursos = pd.DataFrame
    nombre_curso = 'Curso de Moodle'
    def __init__(self, name, path, config):

        if path != "":
            self.dataframe = Maadle.create_data_frame(self, name, path)
        else:
            self.dataframe = Maadle.create_data_frame_file_fame(self, name)
        if len(self.dataframe[self.dataframe['Contexto del evento'].str.contains("Curso:")]['Contexto del evento']) != 0:
            self.nombre_curso = self.dataframe[self.dataframe['Contexto del evento'].str.contains("Curso:")]['Contexto del evento'].iloc[0]
        self.dataframe = Maadle.add_ID_column(self)
        self.dataframe = self.dataframe[~self.dataframe[NOMBRE_USUARIO].isin(['-'])]
        self.dataframe = Maadle.change_hora_type(self)
        self.dataframe = Maadle.add_mont_day_hour_columns(self)
        self.dataframe = self.dataframe.sort_values(by=[FECHA_HORA])
        self.dataframe_usuarios = pd.DataFrame(self.dataframe[NOMBRE_USUARIO].unique(), columns=[NOMBRE_USUARIO])
        self.dataframe_recursos = pd.DataFrame(self.dataframe[CONTEXTO].unique(), columns=[CONTEXTO])
        self.dataframe_recursos['Alias'] = self.dataframe[CONTEXTO].unique()
        self.dataframe_recursos['Excluido'] = ''
        self.dataframe_usuarios['Excluido'] = ''
        self.dataframe_usuarios = self.dataframe_usuarios.sort_values([NOMBRE_USUARIO])
        if not os.path.isfile(config):
            with pd.ExcelWriter(config) as writer:
                self.dataframe_usuarios.to_excel(writer, sheet_name='Usuarios', index=False)
                self.dataframe_recursos.to_excel(writer, sheet_name='Recursos', index=False)
                writer.sheets['Usuarios'].set_column('A:A', self.dataframe_usuarios[NOMBRE_USUARIO].map(len).max())
                writer.sheets['Recursos'].set_column('A:B', self.dataframe_recursos[CONTEXTO].map(len).max())
        self.dataframe_usuarios = pd.ExcelFile(config).parse('Usuarios')
        self.dataframe_recursos = pd.ExcelFile(config).parse('Recursos')
        for i in range(self.dataframe_recursos[CONTEXTO].size):
            if pd.isna(self.dataframe_recursos['Alias'][i]):
                self.dataframe_recursos['Alias'][i] = " "
                self.dataframe[CONTEXTO] = self.dataframe[CONTEXTO].replace(
                    self.dataframe_recursos[CONTEXTO][i], " ")
            else:
                self.dataframe[CONTEXTO] = self.dataframe[CONTEXTO].replace(self.dataframe_recursos[CONTEXTO][i], self.dataframe_recursos['Alias'][i])
        ele = []
        for i in range(self.dataframe_usuarios[NOMBRE_USUARIO].size):
            if not (pd.isna(self.dataframe_usuarios['Excluido'][i]) or self.dataframe_usuarios['Excluido'][i].isspace()):
                ele.append(self.dataframe_usuarios[NOMBRE_USUARIO][i])
        self.dataframe = self.dataframe[~self.dataframe[NOMBRE_USUARIO].isin(ele)]
        self.dataframe_usuarios = self.dataframe_usuarios[~self.dataframe_usuarios[NOMBRE_USUARIO].isin(ele)]
        ele = []
        for i in range(self.dataframe_recursos['Alias'].size):
            if not (pd.isna(self.dataframe_recursos['Excluido'][i]) or self.dataframe_recursos['Excluido'][i].isspace()):
                ele.append(self.dataframe_recursos['Alias'][i])
        self.dataframe = self.dataframe[~self.dataframe[CONTEXTO].isin(ele)]
        self.dataframe_recursos = self.dataframe_recursos[~self.dataframe_recursos['Alias'].isin(ele)]

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

    def add_ID_column(self) -> pd.DataFrame:
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
        dataframe[ID_USUARIO] = self.dataframe[DESCRIPCION].str.extract('[i][d]\s\'(\d*)\'', expand=True) #NÚMEROS NEGATIVOS
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

    def change_hora_type(self):
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

    def between_dates(self, initial, final):
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

    def add_mont_day_hour_columns(self):
        """
        Summary line.

        Añade columnas de hora, día y mes.

        Parameters
        ----------

        Returns
        -------
        dataframe
            Log con las columnas añadidas.

        """
        dataframe = self.dataframe
        dataframe['HoraDelDía'] = pd.DatetimeIndex(self.dataframe[FECHA_HORA]).time
        dataframe['DíaDelMes'] = pd.DatetimeIndex(self.dataframe[FECHA_HORA]).day
        dataframe['MesDelAño'] = pd.DatetimeIndex(self.dataframe[FECHA_HORA]).month
        return dataframe

    """
    def addDiaNormalizadoColumn(dataframe):
        #dataframe = dataframe.sort_values(by=['Hora'])
        # dataframe.index = dataframe['Hora']
        dataframe['DíaNormalizado'] = dataframe['Hora'].dt.dayofyear
        # dataframe.set_index(pd.Index(['DíaNormalizado']))
        return dataframe
    """

    def num_events(self):
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
    def num_teachers(self):
        result = 0
        for d in self.dataframe[NOMBRE_USUARIO].unique():
            if d.isupper() == False and d != '-':
                result = result + 1
        return result

    def num_participants_per_subject(self):
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

    def num_participants_nonparticipants(self):
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

    def list_nonparticipant(self):
        """
        Summary line.

        Recoge a los usuarios no participantes

        Parameters
        ----------

        Returns
        -------
        Dataframe
            Dataframe con una columna con la lista de todos los usuarios no participantes.

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

    def num_events_per_participant(self):
        """
        Summary line.

        Calcula el número de eventos por participante del log.

        Parameters
        ----------

        Returns
        -------
        series??int
            Lista con los participantes y su número de participantes.

        """
        result = pd.DataFrame({NUM_EVENTOS: self.dataframe.groupby([NOMBRE_USUARIO, ID_USUARIO]).size()}).reset_index()
        result = result.sort_values(by=[NUM_EVENTOS])
        return result

    def events_per_month(self):
        """
        Summary line.

        Calcula el número de eventos por mes del log.

        Parameters
        ----------

        Returns
        -------
        series??int
            Lista con los meses y su número de participantes.

        """
        result = 0
        result = self.dataframe[FECHA_HORA].groupby(self.dataframe.Hora.dt.strftime('%Y-%m')).agg('count') + result
        resultdf = pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS])
        resultdf['Fecha'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def events_per_week(self):
        """
        Summary line.

        Calcula el número de eventos por semana del log.

        Parameters
        ----------

        Returns
        -------
        series??int
            Lista con las semanas y su número de eventos.

        """
        result = 0
        result = self.dataframe[FECHA_HORA].groupby(self.dataframe.Hora.dt.strftime('%W')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS]))
        resultdf['Fecha'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def events_per_day(self):
        """
        Summary line.

        Calcula el número de eventos por día del log.

        Parameters
        ----------

        Returns
        -------
        series??int
            Lista con los días y su número de eventos.

        """
        result = 0
        result = self.dataframe[FECHA_HORA].groupby(self.dataframe.Hora.dt.strftime('%Y-%m-%d')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS]))
        resultdf['Fecha'] = resultdf.index
        resultdf['Fecha'] = pd.to_datetime(resultdf['Fecha'])
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def events_per_resource(self):
        """
        Summary line.

        Calcula el número de eventos por recurso del dataframe.

        Parameters
        ----------

        Returns
        -------
        series??int
            Lista con los recursos y su número de eventos.

        """
        result = 0
        result = self.dataframe[CONTEXTO].groupby(self.dataframe[CONTEXTO]).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS]))
        resultdf['Recurso'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        resultdf = resultdf.sort_values(ascending=False, by=[NUM_EVENTOS])
        return resultdf

    def participants_per_resource(self):
        """
        Summary line.

        Calcula el número de participantes por recurso del dataframe.

        Parameters
        ----------

        Returns
        -------
        series??int
            Lista con los recursos y su número de eventos.

        """
        result = self.dataframe.groupby(CONTEXTO)[ID_USUARIO].nunique()
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=[NUM_PARTICIPANTES]))
        resultdf['Recurso'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        resultdf = resultdf.sort_values(ascending=False, by=[NUM_PARTICIPANTES])
        return resultdf

    def events_per_hour(self):
        """
        Summary line.

        Calcula el número de eventos por hora del dataframe.

        Parameters
        ----------

        Returns
        -------
        series??int
            Lista con las horas del día y su número de eventos.

        """
        result = 0
        result = self.dataframe[FECHA_HORA].groupby((self.dataframe.Hora.dt.strftime('%H'))).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS]))
        resultdf[FECHA_HORA] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def resources_by_number_of_events(self, min, max):
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

    def events_between_dates(self, initial, final):
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
        series??int
            El número de eventos por cada fecha. ??REVISAR DOCUMENTACIÓN.

        """
        resultdf = Maadle.events_per_day(self)
        result2 = (resultdf['Fecha'] >= initial) & (resultdf['Fecha'] <= final)
        resultdf = resultdf.loc[result2]
        return resultdf

    def events_per_day_per_user(self, usuario):
        """
        Summary line.

        Calcula el número de eventos de un usuario concreto por día del log.

        Parameters
        ----------
        usuario : String
            Nombre del usuario a analizar.

        Returns
        -------
        series
            Lista con los días y su número de eventos.

        """
        result = 0
        df = self.dataframe[[FECHA_HORA, NOMBRE_USUARIO]]
        df = df[df[NOMBRE_USUARIO].str.contains(usuario)]
        result = df[FECHA_HORA].groupby(df.Hora.dt.strftime('%Y-%m-%d')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS]))
        resultdf['Fecha'] = resultdf.index
        resultdf['Fecha'] = pd.to_datetime(resultdf['Fecha'])
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def events_per_day_per_resource(self, resource):
        """
        Summary line.

        Calcula el número de eventos de un recurso concreto por día del log.

        Parameters
        ----------
        resource : String
            Nombre del recurso a analizar.

        Returns
        -------
        series
            Lista con los días y su número de eventos.

        """
        result = 0
        df = self.dataframe[[FECHA_HORA, CONTEXTO]]
        df = df[df[CONTEXTO].str.contains(resource)]
        result = df[FECHA_HORA].groupby(df.Hora.dt.strftime('%Y-%m-%d')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=[NUM_EVENTOS]))
        resultdf['Fecha'] = resultdf.index
        resultdf['Fecha'] = pd.to_datetime(resultdf['Fecha'])
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def create_dynamic_session_id(self):
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
        result = self.dataframe.sort_values(by=['IDUsuario', 'Hora'])
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

    def number_of_sessions_by_user(self):
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
        result = pd.DataFrame(data=df.groupby(ID_USUARIO)[ID_SESION].nunique().values, columns=['Número de sesiones iniciadas'])
        result[NOMBRE_USUARIO] = df[NOMBRE_USUARIO].unique()
        return result

    def sessions_matrix(self):
        """
        Summary line.

        Construye la matriz de relación de los recursos.

        Parameters
        ----------

        Returns
        -------
        Matrix
            Matriz de relación de los recursos.

        """
        df = Maadle.create_dynamic_session_id(self)
        dfe = self.dataframe[CONTEXTO].unique()
        lista_recursos = dfe.tolist()
        rows = len(dfe)
        columns = rows
        matrix = [[0 for x in range(columns)] for x in range(rows)]
        for session, event in df.groupby(ID_SESION):
            resource_iterador = 0
            for resource in dfe:
                if resource in event[CONTEXTO].values:
                    matrix[resource_iterador][resource_iterador] = matrix[resource_iterador][resource_iterador]+1
                    for recource_in_event in event[CONTEXTO].unique():
                        if recource_in_event != resource:
                            matrix[resource_iterador][lista_recursos.index(recource_in_event)] = matrix[resource_iterador][lista_recursos.index(recource_in_event)] + 1
                resource_iterador = resource_iterador+1
        matrix_result = [[0 for x in range(columns)] for x in range(rows)]
        for j in range(columns):
            for i in range(rows):
                aux = matrix[i][j]/matrix[j][j]
                matrix_result[j][i] = aux
        return matrix_result


    """
    Calcula la media de eventos por participante del dataframe.

    Recibe como parámetro el dataframe.
    Retorna un dataframe con una columna con la media de eventos y con otra con el nombre del participante,
    estando ordenado por la primera.
    ##########OJO NO TIENE SENTIDO, ESTA MÉTRICA TIENE QUE SER DE CURSO
    """
    """
    def average_events_per_participant(self, dataframe):
        result=0
        result = dataframe.groupby([NOMBRE_USUARIO]).size() + result
        resultdf = (pd.DataFrame(data=((result / len(dataframe)).values), index=(result / len(dataframe)).index, 
        columns=['Media de eventos']))
        resultdf['Participante'] = resultdf.index
        resultdf.reset_index(drop=True,inplace=True)
        resultdf = resultdf.sort_values(by=['Media de eventos'])
        return resultdf
    """
