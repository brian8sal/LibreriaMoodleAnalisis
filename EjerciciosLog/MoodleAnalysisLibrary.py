import os
import pandas as pd
import matplotlib.pyplot as plt

class MoodleAnalysisLibrary():
    dataframe = pd.DataFrame
    def __init__(self, name, path, userstodelete):
        self.dataframe=MoodleAnalysisLibrary.createDataFrame(self,name, path)
        self.dataframe=MoodleAnalysisLibrary.addIDColumn(self, self.dataframe)
        self.dataframe=MoodleAnalysisLibrary.deleteByID(self.dataframe,userstodelete)
        self.dataframe=MoodleAnalysisLibrary.changeHoraType(self.dataframe)
        self.dataframe=MoodleAnalysisLibrary.addMontDayHourColumns(self.dataframe)
        self.dataframe = self.dataframe.sort_values(by=['Hora'])

    # Crea un dataframe a partir de un archivo csv que se encuentra en determinado path.
    #
    # Recibe como parámetro el nombre del archivo y el path del mismo.
    # Retorna un dataframe.
    def createDataFrame(self,name, path) -> pd.DataFrame:
        for root, directories, files in os.walk(path):
            if name in files:
                return pd.read_csv(os.path.join(root, name))

    # Crea un dataframe a partir de un archivo csv.
    #
    # Recibe como parámetro el nombre del archivo. *Ha de estar en el path del proyecto
    # Retorna un dataframe.
    def createDataFrameFileName(name) -> pd.DataFrame:
        return pd.read_csv(name)

    # Añade una columna con el ID del usuario.
    #
    # Recibe como parámetro el dataframe al que añadir la columna.
    # Retorna un dataframe con la columna añadida.
    def addIDColumn(self, dataframe) -> pd.DataFrame:
        dataframe['IDUsuario'] = dataframe['Descripción'].str.extract('[i][d]\s\'(\d*)\'', expand=True)
        return dataframe

    # Elimina unas columnas del dataframe.
    #
    # Recibe como parámetro el dataframe y las columnas a borrar de este.
    # Retorna un dataframe con las columnas borradas.
    def deleteColumns(self,dataframe, columns) -> pd.DataFrame:
        dataframe = dataframe.drop(columns, axis='columns')
        return dataframe

    # Elimina una lista de usuarios dado su ID.
    #
    # Recibe como parámetro el dataframe del que borrar los usuarios y los IDs de estos.
    # Retorna un dataframe con los usuarios borrados.
    def deleteByID(dataframe, idList) -> pd.DataFrame:
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
    def addMontDayHourColumns(dataframe):
        dataframe['HoraDelDia'] = pd.DatetimeIndex(dataframe['Hora']).time
        dataframe['DíaDelMes'] = pd.DatetimeIndex(dataframe['Hora']).day
        dataframe['MesDelAño'] = pd.DatetimeIndex(dataframe['Hora']).month
        return dataframe

    def addDiaNormalizadoColumn(dataframe):
        #dataframe = dataframe.sort_values(by=['Hora'])
        # dataframe.index = dataframe['Hora']
        dataframe['DíaNormalizado'] = dataframe['Hora'].dt.dayofyear
        # dataframe.set_index(pd.Index(['DíaNormalizado']))
        return dataframe

    # print(addDiaNormalizadoColumn(df.sample(10)))

    # df1 = createDataFrameFileName("logs_G668_1819_20191223-1648.csv")
    # df2 = createDataFrameFileName("2logs_G668_1819_20191223-1648.csv")
    # df1 = changeHoraType(df1)
    # df2 = changeHoraType(df2)
    # coursedf = [df1, df2]

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
        return (dataframe['Nombre completo del usuario'].nunique() - MoodleAnalysisLibrary.numTeachers(self,dataframe))

    # Calcula el número de eventos por participante del dataframe.
    #
    # Recibe como parámetro el dataframe.
    # Retorna un dataframe con una columna con el número de eventos y con otra con el nombre del participante,
    # estando ordenado por la primera.
    def numEventsPerParticipant(self, dataframe):
        result=0
        result = dataframe.groupby(['Nombre completo del usuario']).size() + result
        resultdf = (pd.DataFrame(data=((result).values), index=(result).index, columns=['Número de eventos']))
        resultdf['Participante'] = resultdf.index
        resultdf.reset_index(drop=True,inplace=True)
        resultdf = resultdf.sort_values(by=['Número de eventos'])
        return resultdf

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