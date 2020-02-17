import os
import pandas as pd
import matplotlib.pyplot as plt

class MoodleAnalysisLibrary():
    dataframe = pd.DataFrame
    def __init__(self, name, path, userstodelete):
        self.dataframe=MoodleAnalysisLibrary.createDataFrame(name, path)
        self.dataframe=MoodleAnalysisLibrary.addIDColumn(self.dataframe)
        self.dataframe=MoodleAnalysisLibrary.deleteByID(self.dataframe,userstodelete)
        self.dataframe=MoodleAnalysisLibrary.changeHoraType(self.dataframe)
        self.dataframe=MoodleAnalysisLibrary.addMontDayHourColumns(self.dataframe)
        self.dataframe = self.dataframe.sort_values(by=['Hora'])



    # Crea un dataframe a partir de un archivo csv que se encuentra en determinado path.
    #
    # Recibe como parámetro el nombre del archivo y el path del mismo.
    # Retorna un dataframe.
    def createDataFrame(name, path) -> pd.DataFrame:
        for root, directories, files in os.walk(path):
            if name in files:
                return pd.read_csv(os.path.join(root, name))

    # print(createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca"))

    # Crea un dataframe a partir de un archivo csv.
    #
    # Recibe como parámetro el nombre del archivo. *Ha de estar en el path del proyecto
    # Retorna un dataframe.
    def createDataFrameFileName(name) -> pd.DataFrame:
        return pd.read_csv(name)

    # print(createDataFrameFileName("logs_G668_1819_20191223-1648.csv"))

    # df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")

    # Añade una columna con el ID del usuario.
    #
    # Recibe como parámetro el dataframe al que añadir la columna.
    # Retorna un dataframe con la columna añadida.
    def addIDColumn(dataframe) -> pd.DataFrame:
        dataframe['IDUsuario'] = dataframe['Descripción'].str.extract('[i][d]\s\'(\d*)\'', expand=True)
        return dataframe

    # print(addIDColumn(df)['IDUsuario'])

    # df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")

    # Elimina unas columnas del dataframe.
    #
    # Recibe como parámetro el dataframe y las columnas a borrar de este.
    # Retorna un dataframe con las columnas borradas.
    def deleteColumns(dataframe, columns) -> pd.DataFrame:
        dataframe = dataframe.drop(columns, axis='columns')
        return dataframe

    # print(deleteColumns(df,list(df)))

    # df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
    # df = addIDColumn(df)

    # Elimina una lista de usuarios dado su ID.
    #
    # Recibe como parámetro el dataframe del que borrar los usuarios y los IDs de estos.
    # Retorna un dataframe con los usuarios borrados.
    def deleteByID(dataframe, idList) -> pd.DataFrame:
        for ele in idList:
            dataframe = dataframe[~dataframe['IDUsuario'].isin([ele])]
        return dataframe

    listIDs = ["6844", "20105"]
    # print(deleteByID(df,listIDs))

    # df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
    # df = addIDColumn(df)

    # Genera una gráfica con los eventos por usuario.
    #
    # Recibe como parámetro el dataframe a representar.
    def graphicEventsPerUser(dataframe):
        groups = dataframe.groupby(['IDUsuario']).size()
        groups.plot.bar()
        plt.show()

    # graphicEventsPerUser(df)

    # df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
    # df = addIDColumn(df)

    # Genera una gráfica con los eventos por contexto.
    #
    # Recibe como parámetro el dataframe a representar.
    def graphicEventsPerContext(dataframe):
        groups = dataframe.groupby(['Contexto del evento']).size()
        groups.plot.bar()
        plt.show()

    # graphicEvents(df)

    # df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
    # df = addIDColumn(df)

    # Cambia el tipo de la columna Hora a datetime.
    #
    # Recibe como parámetro el dataframe cuya columna quiere ser cambiada de tipo.
    # Retorna un dataframe con la columna con el tipo cambiado.
    def changeHoraType(dataframe):
        dataframe['Hora'] = pd.to_datetime(dataframe['Hora'])
        return dataframe

    # changeHoraType(df).info()

    # df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
    # df = addIDColumn(df)
    # df = changeHoraType(df)

    # Devuelve los eventos que se encuentren entre dos fechas dadas.
    #
    # Recibe como parámetro el dataframe y las fechas.
    # Retorna un dataframe con las filas comprendidas entre las fechas.
    def betweenDates(self,dataframe, initial, final):
        result = (dataframe['Hora'] > initial) & (dataframe['Hora'] <= final)
        dataframe = dataframe.loc[result]
        return dataframe

    # ini = pd.Timestamp(2019, 8, 1)
    # fin = pd.Timestamp(2019, 8, 29)
    # print(betweenDates(df,ini,fin))

    # df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
    # df = addIDColumn(df)
    # df = changeHoraType(df)

    # Añade columnas de hora, día y mes.
    #
    # Recibe como parámetro el dataframe al que añadir las columnas.
    # Retorna un dataframe con las columna añadidas.
    def addMontDayHourColumns(dataframe):
        dataframe['HoraDelDia'] = pd.DatetimeIndex(dataframe['Hora']).time
        dataframe['DíaDelMes'] = pd.DatetimeIndex(dataframe['Hora']).day
        dataframe['MesDelAño'] = pd.DatetimeIndex(dataframe['Hora']).month
        return dataframe

    # print(addMontDayHourColumns(df))

    # df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
    # df = addIDColumn(df)
    # df = changeHoraType(df)

    def addDiaNormalizadoColumn(dataframe):
        dataframe = dataframe.sort_values(by=['Hora'])
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

    def numEvents(course):
        result = 0
        for c in course:
            result = len(c) + result
        return result

    # print("Número total de eventos "+str(numEvents(coursedf)))

    def numTeachers(dataframe):
        result = 0
        for d in dataframe['Nombre completo del usuario'].unique():
            if (d.isupper() == False and d != '-'):
                result = result + 1
        return result

    # print(numTeachers(df1))

    def numParticipantsPerSubject(dataframe):
        return (dataframe['Nombre completo del usuario'].nunique() - MoodleAnalysisLibrary.numTeachers(dataframe))

    # print(numParticipantsPerSubject(df2))

    def numParticipantsPerCourse(course):
        result = 0
        for c in course:
            result = MoodleAnalysisLibrary.numParticipantsPerSubject(c) + result
        return result

    # print(numParticipantsPerCourse(coursedf))

    def averageEventsPerParticipant(course):
        result = 0
        for c in course:
            result = c.groupby(['Nombre completo del usuario']).size() + result
        resultdf = (pd.DataFrame(data=((result / len(course)).values), index=(result / len(course)).index,
                                 columns=['Media de eventos']))
        resultdf['Participante'] = resultdf.index
        resultdf.reset_index(drop=True,
                             inplace=True)  # El íncide es el participante si hace esto es para que sea el número y mejorar la apariencia
        # resultdf.index.name = "Participante"
        resultdf = resultdf.sort_values(by=['Media de eventos'])
        return resultdf

    # print(averageEventsPerParticipant(coursedf))

    def eventsPerMonth(course):
        result = 0
        for c in course:
            c = c.sort_values(by=['Hora'])
            # result = c['Hora'].groupby(c.Hora.dt.to_period("M")).agg('count') + result
            # result = c['Hora'].groupby(c['Hora'].dt.month).agg('count') +result
            result = c['Hora'].groupby(c.Hora.dt.strftime('%Y-%m')).agg('count') + result
            resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
        resultdf['Fecha'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    # print(eventsPerMonth(coursedf))

    def eventsPerWeek(course):
        result = 0
        resultt = 0
        for c in course:
            c = c.sort_values(by=['Hora'])
            result = c['Hora'].groupby(c.Hora.dt.strftime('%W')).agg('count') + result
            resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
        resultdf['Fecha'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    # print(eventsPerWeek(coursedf))

    def eventsPerDay(course):
        result = 0
        for c in course:
            c = c.sort_values(by=['Hora'])
            result = c['Hora'].groupby(c.Hora.dt.strftime('%Y-%m-%d')).agg('count') + result
            resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
        resultdf['Fecha'] = resultdf.index
        resultdf['Fecha'] = pd.to_datetime(resultdf['Fecha'])
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf

    # print(eventsPerDay(coursedf).info())

    def eventsBetweenDates(course, initial, final):
        resultdf = MoodleAnalysisLibrary.eventsPerDay(course)
        result2 = (resultdf['Fecha'] > initial) & (resultdf['Fecha'] <= final)
        resultdf = resultdf.loc[result2]
        return resultdf

    # print(eventsBetweenDates(coursedf,pd.Timestamp(2018,12,22),pd.Timestamp(2018,12,24)))

    def eventsPerResource(course):
        result = 0
        for c in course:
            result = c['Nombre evento'].groupby(c['Nombre evento']).agg('count') + result
            resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=['Número de eventos']))
        resultdf['Recurso'] = resultdf.index
        resultdf.reset_index(drop=True, inplace=True)
        resultdf = resultdf.sort_values(by=['Número de eventos'])

        return resultdf

    # print(eventsPerResource(coursedf))

    def resourcesByEvents(course, min, max):
        resultdf = MoodleAnalysisLibrary.eventsPerResource(course)

        result2 = (resultdf['Número de eventos'] > min) & (resultdf['Número de eventos'] <= max)
        resultdf = resultdf.loc[result2]
        return resultdf

    # print(resourcesByEvents(coursedf,84,100))

    def eventsPerHour(course):
        result = 0
        for c in course:
            c = c.sort_values(by=['Hora'])
            result = c['Hora'].groupby((c.Hora.dt.strftime('%H'))).agg('count') + result
            resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
        resultdf['Hora'] = resultdf.index
        # resultdf['Fecha']=pd.to_datetime(resultdf['Fecha'])
        resultdf.reset_index(drop=True, inplace=True)
        return resultdf
    # print(eventsPerHour(coursedf))
