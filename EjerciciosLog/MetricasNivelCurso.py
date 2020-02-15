import EjerciciosLog
import pandas as pd

df1 = EjerciciosLog.createDataFrameFileName("logs_G668_1819_20191223-1648.csv")
df2 = EjerciciosLog.createDataFrameFileName("2logs_G668_1819_20191223-1648.csv")
df1 = EjerciciosLog.changeHoraType(df1)
df2 = EjerciciosLog.changeHoraType(df2)
coursedf = [df1,df2]

def numEvents(course):
    result = 0
    for c in course:
        result = len(c)+result
    return result

# print("Número total de eventos "+str(numEvents(coursedf)))

def numTeachers(dataframe):
    result = 0
    for d in dataframe['Nombre completo del usuario'].unique():
        if(d.isupper()==False and d!='-'):
            result = result +1
    return result

# print(numTeachers(df1))


def numParticipantsPerSubject(dataframe):
    return(dataframe['Nombre completo del usuario'].nunique()-numTeachers(dataframe))

# print(numParticipantsPerSubject(df2))

def numParticipantsPerCourse(course):
    result=0
    for c in course:
        result = numParticipantsPerSubject(c) + result
    return result

# print(numParticipantsPerCourse(coursedf))

def averageEventsPerParticipant(course):
    result=0
    for c in course:
        result = c.groupby(['Nombre completo del usuario']).size()+result
    resultdf = (pd.DataFrame(data=((result/len(course)).values),index=(result/len(course)).index,columns=['Media de eventos']))
    resultdf['Participante'] = resultdf.index
    resultdf.reset_index(drop=True, inplace=True)# El íncide es el participante si hace esto es para que sea el número y mejorar la apariencia
    # resultdf.index.name = "Participante"
    resultdf = resultdf.sort_values(by=['Media de eventos'])
    return resultdf

#print(averageEventsPerParticipant(coursedf))

def eventsPerMonth(course):
    result = 0
    for c in course:
        c = c.sort_values(by=['Hora'])
        #result = c['Hora'].groupby(c.Hora.dt.to_period("M")).agg('count') + result
        #result = c['Hora'].groupby(c['Hora'].dt.month).agg('count') +result
        result = c['Hora'].groupby(c.Hora.dt.strftime('%Y-%m')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index,columns=["Número de eventos"]))
    resultdf['Fecha'] = resultdf.index
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf

#print(eventsPerMonth(coursedf))

def eventsPerWeek(course):
    result = 0
    resultt=0
    for c in course:
        c = c.sort_values(by=['Hora'])
        result = c['Hora'].groupby(c.Hora.dt.strftime('%W')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
    resultdf['Fecha'] = resultdf.index
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf

#print(eventsPerWeek(coursedf))

def eventsPerDay(course):
    result = 0
    for c in course:
        c = c.sort_values(by=['Hora'])
        result = c['Hora'].groupby(c.Hora.dt.strftime('%Y-%m-%d')).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
    resultdf['Fecha'] = resultdf.index
    resultdf['Fecha']=pd.to_datetime(resultdf['Fecha'])
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf

#print(eventsPerDay(coursedf).info())

def eventsBetweenDates(course,initial,final):
    resultdf=eventsPerDay(coursedf)
    result2 = (resultdf['Fecha']>initial)&(resultdf['Fecha']<=final)
    resultdf = resultdf.loc[result2]
    return resultdf

#print(eventsBetweenDates(coursedf,pd.Timestamp(2018,12,22),pd.Timestamp(2018,12,24)))

def eventsPerResource(course):
    result = 0
    for c in course:
        result = c['Nombre evento'].groupby(c['Nombre evento']).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=['Número de eventos']))
    resultdf['Recurso'] = resultdf.index
    resultdf.reset_index(drop=True, inplace=True)
    resultdf = resultdf.sort_values(by=['Número de eventos'])

    return resultdf
#print(eventsPerResource(coursedf))

def resourcesByEvents(course,min,max):
    resultdf=eventsPerResource(coursedf)

    result2 = (resultdf['Número de eventos']>min)&(resultdf['Número de eventos']<=max)
    resultdf = resultdf.loc[result2]
    return resultdf

#print(resourcesByEvents(coursedf,84,100))

def eventsPerHour(course):
    result = 0
    for c in course:
        c = c.sort_values(by=['Hora'])
        result = c['Hora'].groupby((c.Hora.dt.strftime('%H'))).agg('count') + result
        resultdf = (pd.DataFrame(data=result.values, index=result.index, columns=["Número de eventos"]))
    resultdf['Hora'] = resultdf.index
    #resultdf['Fecha']=pd.to_datetime(resultdf['Fecha'])
    resultdf.reset_index(drop=True, inplace=True)
    return resultdf
#print(eventsPerHour(coursedf))



