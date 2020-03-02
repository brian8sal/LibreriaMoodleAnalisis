import os
import pandas as pd
import matplotlib.pyplot as plt

class MoodleAnalysisLibrary():
    dataframe = pd.DataFrame
    def __init__(self, name, path, userstodelete):
        #self.dataframe=MoodleAnalysisLibrary.createDataFrame(self,name, path)
        self.dataframe=MoodleAnalysisLibrary.createDataFrameFileName(self,name)
        self.dataframe=MoodleAnalysisLibrary.addIDColumn(self, self.dataframe)
        self.dataframe=MoodleAnalysisLibrary.deleteByID(self,self.dataframe,userstodelete)
        self.dataframe=MoodleAnalysisLibrary.changeHoraType(self.dataframe)
        self.dataframe=MoodleAnalysisLibrary.addMontDayHourColumns(self,self.dataframe)
        self.dataframe = self.dataframe.sort_values(by=['Hora'])

    def createDataFrame(self,name, path) -> pd.DataFrame:
        """
        Summary line.

        Crea un dataframe a partir de un archivo csv que se encuentra en determinado path.

        Parameters
        ----------
        arg1 : str
            Nombre del fichero.
        arg2 : str
            Dirección del fichero.

        Returns
        -------
        dataframe
            Log.

        """
        for root, directories, files in os.walk(path):
            if name in files:
                return pd.read_csv(os.path.join(root, name))

    def createDataFrameFileName(self,name) -> pd.DataFrame:
        """
        Summary line.

        Crea un dataframe a partir de un archivo csv.

        Parameters
        ----------
        arg1 : str
            Nombre del fichero.

        Returns
        -------
        dataframe
            Log.

        """
        return pd.read_csv(name)

    def addIDColumn(self, dataframe) -> pd.DataFrame:
        """
        Summary line.

        Añade una columna con el ID del usuario.

        Parameters
        ----------
        arg1 : dataframe
            Log al que añadir la columna.

        Returns
        -------
        dataframe
            Log con la columna añadida.

        """
        dataframe['IDUsuario'] = dataframe['Descripción'].str.extract('[i][d]\s\'(\d*)\'', expand=True)
        return dataframe

    def deleteColumns(self,dataframe,columns) -> pd.DataFrame:
        """
        Summary line.

        Elimina unas columnas del dataframe.

        Parameters
        ----------
        arg1 : dataframe
            Log del que eliminar las columnas.
        arg2 : array
            Columnas que eliminar.

        Returns
        -------
        dataframe
            Log con las columnas eliminadas.

        """
        dataframe = dataframe.drop(columns, axis='columns')
        return dataframe

    def deleteByID(self,dataframe, idList) -> pd.DataFrame:
        """
        Summary line.

        Elimina una lista de usuarios dado su ID.

        Parameters
        ----------
        arg1 : dataframe
            Log del que eliminar los usuarios.
        arg2 : array
            Usuarios que eliminar.

        Returns
        -------
        dataframe
            Log con los usuarios eliminados.

        """
        for ele in idList:
            dataframe = dataframe[~dataframe['IDUsuario'].isin([ele])]
        return dataframe

    # Genera una gráfica con los eventos por usuario.
    #
    # Recibe como parámetro el dataframe a representar.
    def graphicEventsPerUser(self,dataframe):
        groups = dataframe.groupby(['IDUsuario']).size()
        groups.plot.bar()
        plt.show()

    # Genera una gráfica con los eventos por contexto.
    #
    # Recibe como parámetro el dataframe a representar.
    def graphicEventsPerContext(self,dataframe):
        groups = dataframe.groupby(['Contexto del evento']).size()
        groups.plot.bar()
        plt.show()

    # Cambia el tipo de la columna Hora a datetime.
    #
    # Recibe como parámetro el dataframe cuya columna quiere ser cambiada de tipo.
    # Retorna un dataframe con la columna con el tipo cambiado.
    def changeHoraType(dataframe):
        dataframe['Hora'] = pd.to_datetime(dataframe['Hora'])
        return dataframe

    # Devuelve los eventos que se encuentren entre dos fechas dadas.
    #
    # Recibe como parámetro el dataframe y las fechas.
    # Retorna un dataframe con las filas comprendidas entre las fechas.
    def betweenDates(self,dataframe, initial, final):
        result = (dataframe['Hora'] > initial) & (dataframe['Hora'] <= final)
        dataframe = dataframe.loc[result]
        return dataframe

    # Añade columnas de hora, día y mes.
    #
    # Recibe como parámetro el dataframe al que añadir las columnas.
    # Retorna un dataframe con las columna añadidas.
    def addMontDayHourColumns(self,dataframe):
        dataframe['HoraDelDía'] = pd.DatetimeIndex(dataframe['Hora']).time
        dataframe['DíaDelMes'] = pd.DatetimeIndex(dataframe['Hora']).day
        dataframe['MesDelAño'] = pd.DatetimeIndex(dataframe['Hora']).month
        return dataframe

    def addDiaNormalizadoColumn(dataframe):
        #dataframe = dataframe.sort_values(by=['Hora'])
        # dataframe.index = dataframe['Hora']
        dataframe['DíaNormalizado'] = dataframe['Hora'].dt.dayofyear
        # dataframe.set_index(pd.Index(['DíaNormalizado']))
        return dataframe

    # Retorna el número de eventos de un dataframe.
    #
    # Recibe como parámetro el dataframe.
    # Retorna el número de eventos del dataframe.
    def numEvents(self, dataframe):
        return len(dataframe)

    # Retorna el número de profesores de un dataframe.
    #
    # Recibe como parámetro el dataframe.
    # Retorna el número de profesores del dataframe.
    def numTeachers(self,dataframe):
        result = 0
        for d in dataframe['Nombre completo del usuario'].unique():
            if (d.isupper() == False and d != '-'):
                result = result + 1
        return result

    # Retorna el número de participantes de un dataframe.
    #
    # Recibe como parámetro el dataframe.
    # Retorna el número de eventos del dataframe.
    def numParticipantsPerSubject(self,dataframe):
        return (dataframe['IDUsuario'].nunique() - MoodleAnalysisLibrary.numTeachers(self,dataframe))

    # Calcula el número de eventos por participante del dataframe.
    #
    # Recibe como parámetro el dataframe.
    # Retorna un dataframe con una columna con el número de eventos y con otra con el nombre del participante,
    # estando ordenado por la primera.
    def numEventsPerParticipant(self, dataframe):
        result = pd.DataFrame({'Número de eventos': dataframe.groupby(['Nombre completo del usuario', 'IDUsuario']).size()}).reset_index()
        result = result.sort_values(by=['Número de eventos'])
        return result

    # Devuelve el número de eventos por mes del dataframe.
    #
    # Recibe como parámetro el dataframe.
    # Retorna un dataframe ordenado cronológicamente con una columna con el número de eventos y con otra con el mes del año,
    def eventsPerMonth(self, dataframe):
        result = 0
        result = dataframe['Hora'].groupby(dataframe.Hora.dt.strftime('%Y-%m')).agg('count') + result
        resultdf = pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"])
        resultdf['Fecha'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    # Devuelve el número de eventos por mes del dataframe.
    #
    # Recibe como parámetro el dataframe.
    # Retorna un dataframe con una columna con el número de eventos y con otra con la semana del año.
    def eventsPerWeek(self, dataframe):
        result = 0
        result = dataframe['Hora'].groupby(dataframe.Hora.dt.strftime('%W')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
        resultdf['Fecha'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    # Devuelve el número de eventos por día del dataframe.
    #
    # Recibe como parámetro el dataframe.
    # Retorna un dataframe con una columna con el número de eventos y con otra con el día.
    def eventsPerDay(self, dataframe):
        result = 0
        result = dataframe['Hora'].groupby(dataframe.Hora.dt.strftime('%Y-%m-%d')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
        resultdf['Fecha'] = resultdf.index
        resultdf['Fecha'] = pd.to_datetime(resultdf['Fecha'])
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    # Devuelve el número de eventos por recurso del dataframe.
    #
    # Recibe como parámetro el dataframe.
    # Retorna un dataframe con una columna con el número de eventos y con otra con el recurso con el que se interactuó.
    def eventsPerResource(self, dataframe):
        result = 0
        result = dataframe['Contexto del evento'].groupby(dataframe['Contexto del evento']).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=['Número de eventos']))
        resultdf['Recurso'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        resultdf = resultdf.sort_values(by=['Número de eventos'])
        return resultdf

    # Devuelve el número de eventos por hora del dataframe.
    #
    # Recibe como parámetro el dataframe.
    # Retorna un dataframe con una columna con el número de eventos y con otra con la hora.
    def eventsPerHour(self, dataframe):
        result = 0
        result = dataframe['Hora'].groupby((dataframe.Hora.dt.strftime('%H'))).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
        resultdf['Hora'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    def resourcesByNumberOfEvents(self,dataframe, min, max):
        resultdf = MoodleAnalysisLibrary.eventsPerResource(self,dataframe)
        result2 = (resultdf['Número de eventos'] > min) & (resultdf['Número de eventos'] <= max)
        resultdf = resultdf.loc[result2]
        return resultdf

    def eventsBetweenDates(self, dataframe, initial, final):
        resultdf = MoodleAnalysisLibrary.eventsPerDay(self,dataframe)
        result2 = (resultdf['Fecha'] > initial) & (resultdf['Fecha'] <= final)
        resultdf = resultdf.loc[result2]
        return resultdf

    # Calcula la media de eventos por participante del dataframe.
    #
    # Recibe como parámetro el dataframe.
    # Retorna un dataframe con una columna con la media de eventos y con otra con el nombre del participante,
    # estando ordenado por la primera.
    ###########OJO NO TIENE SENTIDO, ESTA MÉTRICA TIENE QUE SER DE CURSO
    def averageEventsPerParticipant(self, dataframe):
        result=0
        result = dataframe.groupby(['Nombre completo del usuario']).size() + result
        resultdf = (pd.DataFrame(data=((result / len(dataframe)).values), index=(result / len(dataframe)).index, columns=['Media de eventos']))
        resultdf['Participante'] = resultdf.index
        resultdf.reset_index(drop=True,inplace=True)
        resultdf = resultdf.sort_values(by=['Media de eventos'])
        return resultdf