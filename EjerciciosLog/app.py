import pandas as pd
import MoodleAnalysisLibrary

prueba=(MoodleAnalysisLibrary.MoodleAnalysisLibrary("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca",["323","2","231"]))
print(prueba.dataframe)
prueba.graphicEventsPerContext(prueba.dataframe)
prueba.graphicEventsPerUser(prueba.dataframe)
ini = pd.Timestamp(2019, 8, 1)
fin = pd.Timestamp(2019, 8, 29)
print(prueba.betweenDates(prueba.dataframe,ini,fin))

print(prueba.numEvents(prueba.dataframe))
print(prueba.numTeachers(prueba.dataframe))
print(prueba.numParticipantsPerSubject(prueba.dataframe))
print(prueba.averageEventsPerParticipant(prueba.dataframe))
print(prueba.eventsPerMonth(prueba.dataframe))
print(prueba.eventsPerWeek(prueba.dataframe))
print(prueba.eventsPerDay(prueba.dataframe))
print(prueba.eventsPerResource(prueba.dataframe))
print(prueba.eventsPerHour(prueba.dataframe))