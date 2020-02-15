import os
import pandas as pd
import re
import matplotlib.pyplot as plt
from datetime import date
from sklearn import preprocessing
import numpy

###############
##Ejercicio 1##
###############

# Le pasas el nombre del archivo y el directorio en el que buscarlo
# Obviamente se le podría pasar la ruta completa y utilizar directamente
# la función de pandas para leer convertir csv en DataFrame
def createDataFrame(name, path) -> pd.DataFrame:
    for root, directories, files in os.walk(path): # Nombres en un directorio árbol
        if name in files:
            return pd.read_csv(os.path.join(root, name)) # Concatena la dirección con el nombre del archivo

# print(createDataFrameRute("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca"))

def createDataFrameFileName(name) -> pd.DataFrame:
    return pd.read_csv(name)

# print(createDataFrameFileName("logs_G668_1819_20191223-1648.csv"))


###############
##Ejercicio 2##
###############

df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")

def addIDColumn(dataframe) -> pd.DataFrame:
    dataframe['IDUsuario'] = dataframe['Descripción'].str.extract('[i][d]\s\'(\d*)\'', expand=True)
    return dataframe


# print(addIDColumn(df)['IDUsuario'])

###############
##Ejercicio 3##
###############

df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")

def deleteColumns(dataframe, columns) -> pd.DataFrame:
    dataframe = dataframe.drop(columns, axis='columns') # ¿Mejor un del?
    return dataframe

# print(deleteColumns(df,list(df)))

###############
##Ejercicio 4##
###############

df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
df = addIDColumn(df)

def deleteByID(dataframe, idList) -> pd.DataFrame:
    for ele in idList:
        dataframe = dataframe[~dataframe['IDUsuario'].isin([ele])]
    return dataframe

listIDs = ["6844", "20105"]
# print(deleteByID(df,listIDs))

###############
##Ejercicio 5##
###############

df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
df = addIDColumn(df)

def graphicEventsPerUser(dataframe):
    groups = dataframe.groupby(['IDUsuario']).size()
    groups.plot.bar()
    plt.show()
# graphicEventsPerUser(df)

###############
##Ejercicio 6##
###############

df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
df = addIDColumn(df)

def graphicEventsPerContext(dataframe):
     groups = dataframe.groupby(['Contexto del evento']).size()
     groups.plot.bar()
     plt.show()

# graphicEvents(df)

###############
##Ejercicio 7##
###############

df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
df = addIDColumn(df)

def changeHoraType(dataframe):
    dataframe['Hora']=pd.to_datetime(dataframe['Hora'])
    return dataframe

# changeHoraType(df).info()

###############
##Ejercicio 8##
###############

df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
df = addIDColumn(df)
df = changeHoraType(df)

def betweenDates(dataframe, initial, final):
    result = (dataframe['Hora']>initial)&(dataframe['Hora']<=final)
    dataframe = df.loc[result]
    return dataframe

ini =  pd.Timestamp(2019,8,1)
fin = pd.Timestamp(2019,8,29)
#print(betweenDates(df,ini,fin))

###############
##Ejercicio 9##
###############

df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
df = addIDColumn(df)
df = changeHoraType(df)

def addMontDayHourColumns(dataframe):
    dataframe['DíaSeparado'] = pd.DatetimeIndex(dataframe['Hora']).day
    dataframe['MesSeparado'] = pd.DatetimeIndex(dataframe['Hora']).month
    dataframe['HoraSeparada'] = pd.DatetimeIndex(dataframe['Hora']).time
    return dataframe

# print(addMontDayHourColumns(df))

###############
##Ejercicio 10#
###############

df = createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
df = addIDColumn(df)
df = changeHoraType(df)

def addDiaNormalizadoColumn(dataframe):
    dataframe = dataframe.sort_values(by=['Hora'])
    #dataframe.index = dataframe['Hora']
    dataframe['DíaNormalizado']=dataframe['Hora'].dt.dayofyear
    #dataframe.set_index(pd.Index(['DíaNormalizado']))
    return dataframe

# print(addDiaNormalizadoColumn(df.sample(10)))
