import os
import pandas as pd

CONTEXTO = 'Contexto del evento'
ID_USUARIO = 'IDUsuario'
NOMBRE_USUARIO = 'Nombre completo del usuario'


class MoodleAnalysisLibrary():
    dataframe = pd.DataFrame
    teachers = []
    dataframe_usuarios = pd.DataFrame
    def __init__(self, name, path, usuarioscsv, userstodelete):
        if path!="":
            self.dataframe=MoodleAnalysisLibrary.create_data_frame(self, name, path)
        else:
            self.dataframe=MoodleAnalysisLibrary.create_data_frame_file_fame(self, name)
        self.dataframe=MoodleAnalysisLibrary.add_ID_column(self, self.dataframe)
        # self.dataframe=MoodleAnalysisLibrary.delete_by_ID(self, self.dataframe, userstodelete)
        self.teachers = userstodelete
        self.dataframe = self.dataframe[~self.dataframe[NOMBRE_USUARIO].isin(['-'])]
        self.dataframe=MoodleAnalysisLibrary.change_hora_type(self.dataframe)
        self.dataframe=MoodleAnalysisLibrary.add_mont_day_hour_columns(self, self.dataframe)
        self.dataframe = self.dataframe.sort_values(by=['Hora'])
        self.dataframe_usuarios = pd.read_csv(usuarioscsv)

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

    def add_ID_column(self, dataframe) -> pd.DataFrame:
        """
        Summary line.

        Añade una columna con el ID del usuario.

        Parameters
        ----------
        dataframe : dataframe
            Log al que añadir la columna.

        Returns
        -------
        dataframe
            Log con la columna añadida.

        """
        dataframe[(ID_USUARIO)] = dataframe['Descripción'].str.extract('[i][d]\s\'(\d*)\'', expand=True) #NÚMEROS NEGATIVOS
        return dataframe

    def delete_columns(self, dataframe, columns) -> pd.DataFrame:
        """
        Summary line.

        Elimina unas columnas del dataframe.

        Parameters
        ----------
        dataframe : dataframe
            Log del que eliminar las columnas.
        columns : array
            Columnas que eliminar.

        Returns
        -------
        dataframe
            Log con las columnas eliminadas.

        """
        dataframe = dataframe.drop(columns, axis='columns')
        return dataframe

    def delete_by_ID(self, dataframe, idList) -> pd.DataFrame:
        """
        Summary line.

        Elimina una lista de usuarios dado su ID.

        Parameters
        ----------
        dataframe : dataframe
            Log del que eliminar los usuarios.
        idList : array
            Usuarios que eliminar.

        Returns
        -------
        dataframe
            Log con los usuarios eliminados.

        """
        for ele in idList:
            dataframe = dataframe[~dataframe[ID_USUARIO].isin([ele])]
        return dataframe


    def graphic_events_per_user(self, dataframe):
        """
        Summary line.

        Genera una gráfica con los eventos por usuario.

        Parameters
        ----------
        dataframe : dataframe
            Log del que hacer la gráfica.

        Returns
        -------


        """
        groups = dataframe.groupby([ID_USUARIO]).size()
        groups.plot.bar()

    def graphic_events_per_context(self, dataframe):
        """
        Summary line.

        Genera una gráfica con los eventos por contexto.

        Parameters
        ----------
        dataframe : dataframe
            Log del que hacer la gráfica.

        Returns
        -------


        """
        groups = dataframe.groupby([(CONTEXTO)]).size()
        groups.plot.bar()

    def change_hora_type(dataframe):
        """
        Summary line.

        Cambia el tipo de la columna Hora a datetime.

        Parameters
        ----------
        dataframe : dataframe
            Log cuya columna quiere ser cambiada de tipo.

        Returns
        -------
        dataframe
            Log con la columna Hora cambiada.

        """
        dataframe['Hora'] = pd.to_datetime(dataframe['Hora'],dayfirst=True)
        return dataframe

    def between_dates(self, dataframe, initial, final):
        """
        Summary line.

        Devuelve los eventos que se encuentren entre dos fechas dadas.

        Parameters
        ----------
        dataframe : dataframe
            Log cuya columna quiere ser cambiada de tipo.
        initial : Timestamp
            Fecha inicial.
        final : Timestamp
            Fecha final.

        Returns
        -------
        dataframe
            Log con los eventos comprendidos.

        """
        result = (dataframe['Hora'] > initial) & (dataframe['Hora'] <= final)
        dataframe = dataframe.loc[result]
        return dataframe

    def add_mont_day_hour_columns(self, dataframe):
        """
        Summary line.

        Añade columnas de hora, día y mes.

        Parameters
        ----------
        dataframe : dataframe
            Log al que añadir columnas.

        Returns
        -------
        dataframe
            Log con las columnas añadidas.

        """
        dataframe['HoraDelDía'] = pd.DatetimeIndex(dataframe['Hora']).time
        dataframe['DíaDelMes'] = pd.DatetimeIndex(dataframe['Hora']).day
        dataframe['MesDelAño'] = pd.DatetimeIndex(dataframe['Hora']).month
        return dataframe

    """
    def addDiaNormalizadoColumn(dataframe):
        #dataframe = dataframe.sort_values(by=['Hora'])
        # dataframe.index = dataframe['Hora']
        dataframe['DíaNormalizado'] = dataframe['Hora'].dt.dayofyear
        # dataframe.set_index(pd.Index(['DíaNormalizado']))
        return dataframe
    """

    def num_events(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos de un dataframe.

        Parameters
        ----------
        dataframe : dataframe
            Log en el que contar los eventos.

        Returns
        -------
        int
            Número de eventos en el log.

        """
        return len(dataframe)
    """"
    Retorna el número de profesores de un dataframe. ***PASARÁ A SER BORRADO

    Recibe como parámetro el dataframe.
    Retorna el número de profesores del dataframe.
    """""
    def num_teachers(self, dataframe):
        result = 0
        for d in dataframe[NOMBRE_USUARIO].unique():
            if (d.isupper() == False and d != '-'):
                result = result + 1
        return result

    def num_participants_per_subject(self, dataframe):
        """
        Summary line.

        Calcula el número de participantes de un log, sin contar a profesores.

        Parameters
        ----------
        dataframe : dataframe
            Log en el que contar los participantes.

        Returns
        -------
        int
            Número de participantes en el log.

        """
        return (dataframe[ID_USUARIO].nunique() - MoodleAnalysisLibrary.num_teachers(self, dataframe))

    def num_participants_nonparticipants(self, dataframe, dataframeusuarios):
        """
        Summary line.

        Calcula el número de usuarios participantes y el de no participantes.

        Parameters
        ----------
        dataframe : dataframe
            Log en el que contar los participantes.

        dataframeusuarios : dataframe
            Dataframe en el que contar todos los usuarios (participantes y no participantes).

        Returns
        -------
        Dataframe
            Dataframe con una columna para el número de participantes y otra para el número que no
            participantes.

        """
        data={'Participantes':[0],'No participantes':[0]}
        df=pd.DataFrame(data)
        df['Participantes']=dataframe[ID_USUARIO].nunique()
        for fila in dataframeusuarios.iterrows():
            if fila[1][NOMBRE_USUARIO] not in dataframe[NOMBRE_USUARIO].values:
                df['No participantes']=df['No participantes']+1
        return df

    def list_nonparticipant(self, dataframe, dataframeusuarios):
        """
        Summary line.

        Recoge a los usuarios no participantes

        Parameters
        ----------
        dataframe : dataframe
            Log en el que contar los participantes.

        dataframeusuarios : dataframe
            Dataframe con todos los usuarios (participantes y no participantes).

        Returns
        -------
        Dataframe
            Dataframe con una columna con la lista de todos los usuarios no participantes.

        """
        result=list()
        for fila in dataframeusuarios[NOMBRE_USUARIO]:
            if fila not in dataframe[NOMBRE_USUARIO].values:
                result.append(fila)
        if(result==[]):
            df = pd.DataFrame(result, columns=['TODOS HAN PARTICIPADO'])
            return df
        df=pd.DataFrame(result,columns=[NOMBRE_USUARIO])
        return df

    def num_events_per_participant(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos por participante del log.

        Parameters
        ----------
        dataframe : dataframe
            Log en el que calcular el número de eventos por participante.

        Returns
        -------
        series??int
            Lista con los participantes y su número de participantes.

        """
        result = pd.DataFrame({'Número de eventos': dataframe.groupby([NOMBRE_USUARIO, ID_USUARIO]).size()}).reset_index()
        result = result.sort_values(by=['Número de eventos'])
        return result

    def events_per_month(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos por mes del log.

        Parameters
        ----------
        dataframe : dataframe
            Log en el que calcular el número de eventos por mes.

        Returns
        -------
        series??int
            Lista con los meses y su número de participantes.

        """
        result = 0
        result = dataframe['Hora'].groupby(dataframe.Hora.dt.strftime('%Y-%m')).agg('count') + result
        resultdf = pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"])
        resultdf['Fecha'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def events_per_week(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos por semana del log.

        Parameters
        ----------
        dataframe : dataframe
            Log en el que calcular el número de eventos por semana.

        Returns
        -------
        series??int
            Lista con las semanas y su número de eventos.

        """
        result = 0
        result = dataframe['Hora'].groupby(dataframe.Hora.dt.strftime('%W')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
        resultdf['Fecha'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def events_per_day(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos por día del log.

        Parameters
        ----------
        dataframe : dataframe
            Log en el que calcular el número de eventos por día.

        Returns
        -------
        series??int
            Lista con los días y su número de eventos.

        """
        result = 0
        result = dataframe['Hora'].groupby(dataframe.Hora.dt.strftime('%Y-%m-%d')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
        resultdf['Fecha'] = resultdf.index
        resultdf['Fecha'] = pd.to_datetime(resultdf['Fecha'])
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf


    def events_per_resource(self, dataframe):
        """
        Summary line. SPRINT00

        Calcula el número de eventos por recurso del dataframe.

        Parameters
        ----------
        dataframe : dataframe
            Log en el que calcular el número de eventos por recurso.

        Returns
        -------
        series??int
            Lista con los recursos y su número de eventos.

        """
        result = 0
        result = dataframe[CONTEXTO].groupby(dataframe[CONTEXTO]).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=['Número de eventos']))
        resultdf['Recurso'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        resultdf = resultdf.sort_values(ascending=False,by=['Número de eventos'])
        return resultdf

    def participants_per_resource(self, dataframe):
        """
        Summary line. SPRINT02

        Calcula el número de participantes por recurso del dataframe.

        Parameters
        ----------
        dataframe : dataframe
            Log en el que calcular el número de participantes por recurso.

        Returns
        -------
        series??int
            Lista con los recursos y su número de eventos.

        """
        result = dataframe.groupby(CONTEXTO)[ID_USUARIO].nunique()
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=['Número de participantes']))
        resultdf['Recurso'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        resultdf = resultdf.sort_values(ascending=False, by=['Número de participantes'])
        return resultdf

    def events_per_hour(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos por hora del dataframe.

        Parameters
        ----------
        dataframe : dataframe
            Log en el que calcular el número de eventos por hora.

        Returns
        -------
        series??int
            Lista con las horas del día y su número de eventos.

        """
        result = 0
        result = dataframe['Hora'].groupby((dataframe.Hora.dt.strftime('%H'))).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
        resultdf['Hora'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def resources_by_number_of_events(self, dataframe, min, max):
        """
        Summary line.

        Filtra los eventos que se encuentren en un rango determinado de eventos.

        Parameters
        ----------
        dataframe : dataframe
            Log del que filtrar los eventos.
        min : int
            Límite inferior del rango.
        max : int
            Límite superior del rango.

        Returns
        -------
        dataframe
            Log con los eventos filtrados.

        """
        resultdf = MoodleAnalysisLibrary.events_per_resource(self, dataframe)
        result2 = (resultdf['Número de eventos'] > min) & (resultdf['Número de eventos'] <= max)
        resultdf = resultdf.loc[result2]
        return resultdf

    def events_between_dates(self, dataframe, initial, final, onlystudents=False):
        """
        Summary line. SPRINT01

        Calcula el número de eventos en determinado rango de fechas.

        Parameters
        ----------
        dataframe : dataframe
            Log en el que calcular el número de eventos.
        initial : int
            Límite inferior del rango.
        final : int
            Límite superior del rango.
        onlystudents : bool
            Indica si deben contarse solo estudiantes o profesores también

        Returns
        -------
        series??int
            El número de eventos por cada fecha. ??REVISAR DOCUMENTACIÓN.

        """
        if onlystudents:
            resultdf = MoodleAnalysisLibrary.delete_by_ID(self, dataframe, self.teachers)
            resultdf = MoodleAnalysisLibrary.events_per_day(self, resultdf)
        else:
            resultdf = MoodleAnalysisLibrary.events_per_day(self, dataframe)
        result2 = (resultdf['Fecha'] >= initial) & (resultdf['Fecha'] <= final)
        resultdf = resultdf.loc[result2]
        return resultdf


    """
    Calcula la media de eventos por participante del dataframe.

    Recibe como parámetro el dataframe.
    Retorna un dataframe con una columna con la media de eventos y con otra con el nombre del participante,
    estando ordenado por la primera.
    ##########OJO NO TIENE SENTIDO, ESTA MÉTRICA TIENE QUE SER DE CURSO
    """
    def average_events_per_participant(self, dataframe):
        result=0
        result = dataframe.groupby([NOMBRE_USUARIO]).size() + result
        resultdf = (pd.DataFrame(data=((result / len(dataframe)).values), index=(result / len(dataframe)).index, columns=['Media de eventos']))
        resultdf['Participante'] = resultdf.index
        resultdf.reset_index(drop=True,inplace=True)
        resultdf = resultdf.sort_values(by=['Media de eventos'])
        return resultdf