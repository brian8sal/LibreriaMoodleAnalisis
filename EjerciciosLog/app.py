import pandas as pd
import MoodleAnalysisLibrary

prueba=(MoodleAnalysisLibrary.MoodleAnalysisLibrary("TestingLog99Rows.csv","", []))
print(prueba.dataframe['Hora'][77])
prueba.graphic_events_per_context(prueba.dataframe)
prueba.graphic_events_per_user(prueba.dataframe)
ini = pd.Timestamp(2019, 8, 1)
fin = pd.Timestamp(2019, 8, 29)

print(prueba.num_events(prueba.dataframe))
print(prueba.num_teachers(prueba.dataframe))
print(prueba.num_participants_per_subject(prueba.dataframe))
print(prueba.average_events_per_participant(prueba.dataframe))
print(prueba.events_per_month(prueba.dataframe))
print(prueba.events_per_week(prueba.dataframe))
print(prueba.events_per_day(prueba.dataframe))
print(prueba.events_per_resource(prueba.dataframe))
print(prueba.events_per_hour(prueba.dataframe))