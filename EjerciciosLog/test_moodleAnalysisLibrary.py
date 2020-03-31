import unittest
import MoodleAnalysisLibrary
import pandas as pd
import numpy as np


prueba1Rows = (MoodleAnalysisLibrary.MoodleAnalysisLibrary("TestingLog1Row.csv","","UsuariosTest.csv", []))
prueba99Rows = (MoodleAnalysisLibrary.MoodleAnalysisLibrary("TestingLog99Rows.csv","","UsuariosTest.csv", []))
prueba99RowsSinUsuarios = (MoodleAnalysisLibrary.MoodleAnalysisLibrary("TestingLog99Rows.csv","","UsuariosTestVacio.csv", []))




class TestMoodleAnalysisLibrary(unittest.TestCase):

    def test_createDataFrame(self):
        self.assertEqual(0,0)



    def test_createDataFrameFileName(self):
        dataframe = prueba1Rows.create_data_frame_file_fame("TestingLog1Row.csv")
        self.assertEqual(len(dataframe), 1)
        dataframe = prueba99Rows.create_data_frame_file_fame("TestingLog99Rows.csv")
        self.assertEqual(len(dataframe), 99)

    def test_addIDColumn(self):
        dataframe=prueba1Rows.add_ID_column(prueba1Rows.dataframe) #Ya la tiene en el constructor, probada borrándolo y añadiéndolo aquí
        self.assertTrue('IDUsuario' in dataframe.columns)
        dataframe=prueba99Rows.add_ID_column(prueba1Rows.dataframe) #Ya la tiene en el constructor, probada borrándolo y añadiéndolo aquí
        self.assertTrue('IDUsuario' in dataframe.columns)

    def test_deleteColumns(self):
        dataframe=prueba1Rows.delete_columns(prueba1Rows.dataframe, ['Descripción'])
        self.assertFalse('Descripción' in dataframe.columns)

    def test_deleteByID(self):
        dataframe=prueba1Rows.dataframe
        self.assertTrue("0" in dataframe['IDUsuario'].values)
        dataframe=prueba1Rows.delete_by_ID(prueba1Rows.dataframe, ["0"])
        self.assertTrue("0" not in dataframe['IDUsuario'].values)

    def test_changeHoraType(self):
        dataframe=prueba1Rows.dataframe
        self.assertEqual(dataframe['Hora'].dtype,'datetime64[ns]')# Se hace en el constructor
        dataframe=prueba99Rows.dataframe
        self.assertEqual(dataframe['Hora'].dtype,'datetime64[ns]')# Se hace en el constructor

    def test_betweenDates(self):
        ini = np.datetime64('2019-08-01')
        fin = np.datetime64('2019-08-29')
        self.assertEqual(len(prueba99Rows.between_dates(prueba99Rows.dataframe, ini, fin)), 1)
        ini = np.datetime64('2019-09-01')
        fin = np.datetime64('2019-09-10')
        self.assertEqual(len(prueba99Rows.between_dates(prueba99Rows.dataframe, ini, fin)), 5)


    def test_addMontDayHourColumns(self):
        dataframe=prueba1Rows.dataframe
        self.assertTrue(('MesDelAño'in dataframe.columns))# Se hace en el constructor
        self.assertTrue(('DíaDelMes' in dataframe.columns))
        self.assertTrue(('HoraDelDía' in dataframe.columns))
        dataframe=prueba99Rows.dataframe
        self.assertTrue(('MesDelAño'in dataframe.columns))# Se hace en el constructor
        self.assertTrue(('DíaDelMes' in dataframe.columns))
        self.assertTrue(('HoraDelDía' in dataframe.columns))

    def test_numEvents(self):
        self.assertTrue(prueba1Rows.num_events(prueba1Rows.dataframe) == 1)
        self.assertTrue(prueba99Rows.num_events(prueba99Rows.dataframe) == 53)

    def test_numTeachers(self):
        self.assertTrue(prueba1Rows.num_teachers(prueba1Rows.dataframe) == 1)
        self.assertTrue(prueba99Rows.num_teachers(prueba99Rows.dataframe) == 1)


    def test_numParticipantsPerSubject(self):
        self.assertTrue((prueba1Rows.num_participants_per_subject(prueba1Rows.dataframe) == 0))
        self.assertTrue((prueba99Rows.num_participants_per_subject(prueba99Rows.dataframe) == 12))


    def test_numEventsPerParticipant(self):
        self.assertTrue((((prueba1Rows.num_events_per_participant(prueba1Rows.dataframe))['Número de eventos'][0]) == 1))

    def test_num_participants_nonparticipants(self):
        self.assertTrue((prueba99Rows.num_participants_nonparticipants(prueba99Rows.dataframe,prueba99Rows.dataframeUsuarios))['Participantes'][0]==13)
        self.assertTrue((prueba99Rows.num_participants_nonparticipants(prueba99Rows.dataframe,prueba99Rows.dataframeUsuarios))['No participantes'][0]==4)

        self.assertTrue((prueba99Rows.num_participants_nonparticipants(prueba99RowsSinUsuarios.dataframe,prueba99RowsSinUsuarios.dataframeUsuarios))['Participantes'][0]==13)
        self.assertTrue((prueba99Rows.num_participants_nonparticipants(prueba99RowsSinUsuarios.dataframe,prueba99RowsSinUsuarios.dataframeUsuarios))['No participantes'][0]==0)



    def test_list_nonparticipant(self):
        self.assertTrue((prueba99Rows.list_nonparticipant(prueba99Rows.dataframe,prueba99Rows.dataframeUsuarios))['Nombre completo del usuario'][0]=='Sanchez Barreiro, Pablo')
        self.assertTrue((prueba99Rows.list_nonparticipant(prueba99Rows.dataframe,prueba99Rows.dataframeUsuarios))['Nombre completo del usuario'][1]=='Pedro')
        self.assertTrue((prueba99Rows.list_nonparticipant(prueba99Rows.dataframe,prueba99Rows.dataframeUsuarios))['Nombre completo del usuario'][2]=='JAVI')
        self.assertTrue((prueba99Rows.list_nonparticipant(prueba99Rows.dataframe,prueba99Rows.dataframeUsuarios))['Nombre completo del usuario'][3]=='RODRIGUEZ PÉREZ, DANIEL')


        self.assertTrue('TODOS HAN PARTICIPADO' in (prueba99Rows.list_nonparticipant(prueba99RowsSinUsuarios.dataframe, prueba99RowsSinUsuarios.dataframeUsuarios).columns))


    def test_eventsPerMonth(self):
        self.assertEqual(0,0)

    def test_eventsPerWeek(self):
        self.assertEqual(0,0)

    def test_eventsPerDay(self):
        self.assertEqual(0,0)

    def test_eventsPerResource(self):
        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[0]['Número de eventos'], 32)
        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[0]['Recurso'], "Curso: G000 - Curso de Testing - Curso 2018-2019")

        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[1]['Número de eventos'], 13)
        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[1]['Recurso'], "Foro: Noticias de clase")

        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[2]['Número de eventos'], 4)
        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[2]['Recurso'], "Carpeta: Recursos del Alumnado")

        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[3]['Número de eventos'], 1)
        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[3]['Recurso'], "Carpeta: Entrega inicial")

        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[4]['Número de eventos'], 1)
        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[4]['Recurso'], "Carpeta: Exámenes")

        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[5]['Número de eventos'], 1)
        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[5]['Recurso'], "Carpeta: Papeleo")

        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[6]['Número de eventos'], 1)
        self.assertEqual(prueba99Rows.events_per_resource(prueba99Rows.dataframe).iloc[6]['Recurso'], "Tarea: Entrega inicial")

        self.assertEqual(prueba1Rows.events_per_resource(prueba1Rows.dataframe).iloc[0]['Número de eventos'], 1)
        self.assertEqual(prueba1Rows.events_per_resource(prueba1Rows.dataframe).iloc[0]['Recurso'], "Curso: G000 - Curso de Testing - Curso 2018-2019")







    def test_eventsPerHour(self):
        self.assertEqual(0,0)

    def test_resourcesByNumberOfEvents(self):
        self.assertEqual(0,0)

    def test_averageEventsPerParticipant(self):
        self.assertEqual(0,0)

if __name__ == '__main__':
    unittest.main()
