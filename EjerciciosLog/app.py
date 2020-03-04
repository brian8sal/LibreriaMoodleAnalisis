import pandas as pd
import MoodleAnalysisLibrary

prueba=(MoodleAnalysisLibrary.MoodleAnalysisLibrary("TestingLog99Rows.csv","", []))
print(prueba.dataframe['Hora'][77])
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