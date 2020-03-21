import os
import pandas as pd
import matplotlib.pyplot as plt

class MoodleAnalysisLibrary():
    dataframe = pd.DataFrame
    def __init__(self, name, path, userstodelete):
        if path!="":
            self.dataframe=MoodleAnalysisLibrary.createDataFrame(self,name, path)
        else:
            self.dataframe=MoodleAnalysisLibrary.createDataFrameFileName(self,name)
        self.dataframe=MoodleAnalysisLibrary.addIDColumn(self, self.dataframe)
        self.dataframe=MoodleAnalysisLibrary.deleteByID(self,self.dataframe,userstodelete)
        self.dataframe = self.dataframe[~self.dataframe['Nombre completo del usuario'].isin(['-'])] #OJO,PODRÍA PASARSE SU ID COMO ARGUMENTO, POR EL MOMENTO DELETEBYID NO CONTEMPLA NEGATIVOS
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
        dataframe['IDUsuario'] = dataframe['Descripción'].str.extract('[i][d]\s\'(\d*)\'', expand=True) #NÚMEROS NEGATIVOS
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

    def graphicEventsPerUser(self,dataframe):
        """
        Summary line.

        Genera una gráfica con los eventos por usuario.

        Parameters
        ----------
        arg1 : dataframe
            Log del que hacer la gráfica.

        Returns
        -------


        """
        groups = dataframe.groupby(['IDUsuario']).size()
        groups.plot.bar()
        plt.show()

    def graphicEventsPerContext(self,dataframe):
        """
        Summary line.

        Genera una gráfica con los eventos por contexto.

        Parameters
        ----------
        arg1 : dataframe
            Log del que hacer la gráfica.

        Returns
        -------


        """
        groups = dataframe.groupby(['Contexto del evento']).size()
        groups.plot.bar()
        plt.show()

    def changeHoraType(dataframe):
        """
        Summary line.

        Cambia el tipo de la columna Hora a datetime.

        Parameters
        ----------
        arg1 : dataframe
            Log cuya columna quiere ser cambiada de tipo.

        Returns
        -------
        dataframe
            Log con la columna Hora cambiada.

        """
        dataframe['Hora'] = pd.to_datetime(dataframe['Hora'],dayfirst=True)
        return dataframe

    def betweenDates(self,dataframe, initial, final):
        """
        Summary line.

        Devuelve los eventos que se encuentren entre dos fechas dadas.

        Parameters
        ----------
        arg1 : dataframe
            Log cuya columna quiere ser cambiada de tipo.
        arg2 : Timestamp
            Fecha inicial.
        arg3 : Timestamp
            Fecha final.

        Returns
        -------
        dataframe
            Log con los eventos comprendidos.

        """
        result = (dataframe['Hora'] > initial) & (dataframe['Hora'] <= final)
        dataframe = dataframe.loc[result]
        return dataframe

    def addMontDayHourColumns(self,dataframe):
        """
        Summary line.

        Añade columnas de hora, día y mes.

        Parameters
        ----------
        arg1 : dataframe
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

    def addDiaNormalizadoColumn(dataframe):
        #dataframe = dataframe.sort_values(by=['Hora'])
        # dataframe.index = dataframe['Hora']
        dataframe['DíaNormalizado'] = dataframe['Hora'].dt.dayofyear
        # dataframe.set_index(pd.Index(['DíaNormalizado']))
        return dataframe

    def numEvents(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos de un dataframe.

        Parameters
        ----------
        arg1 : dataframe
            Log en el que contar los eventos.

        Returns
        -------
        int
            Número de eventos en el log.

        """
        return len(dataframe)

    # Retorna el número de profesores de un dataframe. ***PASARÁ A SER BORRADO
    #
    # Recibe como parámetro el dataframe.
    # Retorna el número de profesores del dataframe.
    def numTeachers(self,dataframe):
        result = 0
        for d in dataframe['Nombre completo del usuario'].unique():
            if (d.isupper() == False and d != '-'):
                result = result + 1
        return result

    def numParticipantsPerSubject(self,dataframe):
        """
        Summary line.

        Calcula el número de participantes de un log, sin contar a profesores.

        Parameters
        ----------
        arg1 : dataframe
            Log en el que contar los participantes.

        Returns
        -------
        int
            Número de participantes en el log.

        """
        return (dataframe['IDUsuario'].nunique() - MoodleAnalysisLibrary.numTeachers(self,dataframe))

    def numEventsPerParticipant(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos por participante del log.

        Parameters
        ----------
        arg1 : dataframe
            Log en el que calcular el número de eventos por participante.

        Returns
        -------
        series??int
            Lista con los participantes y su número de participantes.

        """
        result = pd.DataFrame({'Número de eventos': dataframe.groupby(['Nombre completo del usuario', 'IDUsuario']).size()}).reset_index()
        result = result.sort_values(by=['Número de eventos'])
        return result

    def eventsPerMonth(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos por mes del log.

        Parameters
        ----------
        arg1 : dataframe
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

    def eventsPerWeek(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos por semana del log.

        Parameters
        ----------
        arg1 : dataframe
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

    def eventsPerDay(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos por día del log.

        Parameters
        ----------
        arg1 : dataframe
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

    def eventsPerResource(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos por recurso del dataframe.

        Parameters
        ----------
        arg1 : dataframe
            Log en el que calcular el número de eventos por recurso.

        Returns
        -------
        series??int
            Lista con los recursos y su número de eventos.

        """
        result = 0
        result = dataframe['Contexto del evento'].groupby(dataframe['Contexto del evento']).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=['Número de eventos']))
        resultdf['Recurso'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        resultdf = resultdf.sort_values(ascending=False,by=['Número de eventos'])
        return resultdf

    def eventsPerHour(self, dataframe):
        """
        Summary line.

        Calcula el número de eventos por hora del dataframe.

        Parameters
        ----------
        arg1 : dataframe
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

    def resourcesByNumberOfEvents(self,dataframe, min, max):
        """
        Summary line.

        Filtra los eventos que se encuentren en un rango determinado de eventos.

        Parameters
        ----------
        arg1 : dataframe
            Log del que filtrar los eventos.
        arg1 : int
            Límite inferior del rango.
        arg2 : int
            Límite superior del rango.

        Returns
        -------
        dataframe
            Log con los eventos filtrados.

        """
        resultdf = MoodleAnalysisLibrary.eventsPerResource(self,dataframe)
        result2 = (resultdf['Número de eventos'] > min) & (resultdf['Número de eventos'] <= max)
        resultdf = resultdf.loc[result2]
        return resultdf

    def eventsBetweenDates(self, dataframe, initial, final):
        """
        Summary line.

        Calcula el número de eventos en determinado rango de fechas.

        Parameters
        ----------
        arg1 : dataframe
            Log en el que calcular el número de eventos.
        arg1 : int
            Límite inferior del rango.
        arg2 : int
            Límite superior del rango.

        Returns
        -------
        series??int
            El número de eventos por cada fecha. ??REVISAR DOCUMENTACIÓN.

        """
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