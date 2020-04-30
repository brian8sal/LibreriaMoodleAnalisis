import unittest
import Maadle
import numpy as np

FECHA = 'Fecha'
RECURSO = 'Recurso'

prueba1Rows = (Maadle.Maadle("TestingLog1Row.csv", "", "PrezConfig1.xlsx", []))
prueba99Rows = (Maadle.Maadle("TestingLog99Rows.csv", "", "PrezConfig2.xlsx", ['1']))
prueba99RowsSinUsuarios = (Maadle.Maadle("TestingLog99Rows.csv", "", "PrezConfig.xlsx", []))
prueba99RowsTodosUsuarios = (Maadle.Maadle("TestingLog99RowsTodosUsuarios.csv", "", "PrezConfig1.xlsx", []))


class Test_Maadle(unittest.TestCase):

    def test_createDataFrame(self):
        self.assertEqual(0,0)

    def test_createDataFrameFileName(self):
        dataframe = prueba1Rows.create_data_frame_file_fame("TestingLog1Row.csv")
        self.assertEqual(len(dataframe), 1)
        dataframe = prueba99Rows.create_data_frame_file_fame("TestingLog99Rows.csv")
        self.assertEqual(len(dataframe), 99)

    def test_addIDColumn(self):
        dataframe=prueba1Rows.add_ID_column() #Ya la tiene en el constructor, probada borrándolo y añadiéndolo aquí
        self.assertTrue(Maadle.ID_USUARIO in dataframe.columns)
        dataframe=prueba99Rows.add_ID_column() #Ya la tiene en el constructor, probada borrándolo y añadiéndolo aquí
        self.assertTrue(Maadle.ID_USUARIO in dataframe.columns)

    def test_deleteColumns(self):
        dataframe=prueba1Rows.delete_columns([Maadle.DESCRIPCION])
        self.assertFalse(Maadle.DESCRIPCION in dataframe.columns)

    def test_deleteByID(self):
        dataframe=prueba1Rows.dataframe
        self.assertTrue("0" in dataframe[Maadle.ID_USUARIO].values)
        dataframe=prueba1Rows.delete_by_ID(["0"])
        self.assertTrue("0" not in dataframe[Maadle.ID_USUARIO].values)

    def test_changeHoraType(self):
        dataframe=prueba1Rows.dataframe
        self.assertEqual(dataframe[Maadle.FECHA_HORA].dtype, 'datetime64[ns]')# Se hace en el constructor
        dataframe=prueba99Rows.dataframe
        self.assertEqual(dataframe[Maadle.FECHA_HORA].dtype, 'datetime64[ns]')# Se hace en el constructor

    def test_betweenDates(self):
        ini = np.datetime64('2019-08-01')
        fin = np.datetime64('2019-08-29')
        self.assertEqual(len(prueba99Rows.between_dates(ini, fin)), 1)
        ini = np.datetime64('2019-09-01')
        fin = np.datetime64('2019-09-10')
        self.assertEqual(len(prueba99Rows.between_dates(ini, fin)), 5)


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
        self.assertTrue(prueba1Rows.num_events() == 1)
        self.assertTrue(prueba99Rows.num_events() == 53)

    def test_numTeachers(self):
        self.assertTrue(prueba1Rows.num_teachers() == 1)
        self.assertTrue(prueba99Rows.num_teachers() == 1)


    def test_numParticipantsPerSubject(self):
        self.assertTrue((prueba1Rows.num_participants_per_subject() == 0))
        self.assertTrue((prueba99Rows.num_participants_per_subject() == 12))


    def test_numEventsPerParticipant(self):
        self.assertTrue((((prueba1Rows.num_events_per_participant())[Maadle.NUM_EVENTOS][0]) == 1))

    def test_num_participants_nonparticipants(self):
        self.assertTrue((prueba99Rows.num_participants_nonparticipants())[
                            Maadle.PARTICIPANTES][0] == 13)
        self.assertTrue((prueba99Rows.num_participants_nonparticipants())[
                            Maadle.NO_PARTICIPANTES][0] == 4)

        self.assertTrue((prueba99RowsSinUsuarios.num_participants_nonparticipants())[
                            Maadle.PARTICIPANTES][0] == 13)
        self.assertTrue((prueba99RowsTodosUsuarios.num_participants_nonparticipants())[
                            Maadle.NO_PARTICIPANTES][0] == 0)



    def test_list_nonparticipant(self):
        self.assertTrue((prueba99Rows.list_nonparticipant())[
                            Maadle.NOMBRE_USUARIO][0] == 'Sanchez Barreiro, Pablo')
        self.assertTrue((prueba99Rows.list_nonparticipant())[
                            Maadle.NOMBRE_USUARIO][1] == 'Pedro')
        self.assertTrue((prueba99Rows.list_nonparticipant())[
                            Maadle.NOMBRE_USUARIO][2] == 'JAVI')
        self.assertTrue((prueba99Rows.list_nonparticipant())[
                            Maadle.NOMBRE_USUARIO][3] == 'RODRIGUEZ PÉREZ, DANIEL')
        self.assertTrue('TODOS HAN PARTICIPADO' in (prueba99RowsTodosUsuarios.list_nonparticipant().columns))


    def test_eventsPerMonth(self):
        self.assertEqual(0,0)

    def test_eventsPerWeek(self):
        self.assertEqual(0,0)

    def test_eventsPerDay(self):
        self.assertEqual(0,0)

    def test_eventsPerResource(self):
        self.assertEqual(prueba99Rows.events_per_resource().iloc[0][Maadle.NUM_EVENTOS], 32)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[0][RECURSO], "Curso: G000 - Curso de Testing - Curso 2018-2019")

        self.assertEqual(prueba99Rows.events_per_resource().iloc[1][Maadle.NUM_EVENTOS], 13)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[1][RECURSO], "Foro: Noticias de clase")

        self.assertEqual(prueba99Rows.events_per_resource().iloc[2][Maadle.NUM_EVENTOS], 4)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[2][RECURSO], "Carpeta: Recursos del Alumnado")

        self.assertEqual(prueba99Rows.events_per_resource().iloc[3][Maadle.NUM_EVENTOS], 1)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[3][RECURSO], "Carpeta: Entrega inicial")

        self.assertEqual(prueba99Rows.events_per_resource().iloc[4][Maadle.NUM_EVENTOS], 1)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[4][RECURSO], "Carpeta: Exámenes")

        self.assertEqual(prueba99Rows.events_per_resource().iloc[5][Maadle.NUM_EVENTOS], 1)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[5][RECURSO], "Carpeta: Papeleo")

        self.assertEqual(prueba99Rows.events_per_resource().iloc[6][Maadle.NUM_EVENTOS], 1)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[6][RECURSO], "Tarea: Entrega inicial")

        self.assertEqual(prueba1Rows.events_per_resource().iloc[0][Maadle.NUM_EVENTOS], 1)
        self.assertEqual(prueba1Rows.events_per_resource().iloc[0][RECURSO], "Curso: G000 - Curso de Testing - Curso 2018-2019")

    def test_events_between_dates(self):
        ini = np.datetime64('2019-08-01')
        fin = np.datetime64('2019-08-29')
        dataframe=prueba99Rows.events_between_dates(ini, fin)
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-08-01'][Maadle.NUM_EVENTOS].to_string(index=False), " 1")
        ini = np.datetime64('2019-09-01')
        fin = np.datetime64('2019-09-10')
        dataframe=prueba99Rows.events_between_dates(ini, fin)
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09-09'][Maadle.NUM_EVENTOS].to_string(index=False), " 3")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09-05'][Maadle.NUM_EVENTOS].to_string(index=False), " 1")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09-02'][Maadle.NUM_EVENTOS].to_string(index=False), " 1")
        ini = np.datetime64('2019-09-09')
        fin = np.datetime64('2019-09-23')
        dataframe=prueba99Rows.events_between_dates(ini, fin)
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09-09'][Maadle.NUM_EVENTOS].to_string(index=False), " 3")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09-22'][Maadle.NUM_EVENTOS].to_string(index=False), " 4")
        self.assertEqual(len(dataframe), 2)
        dataframe=prueba99Rows.events_between_dates(ini, fin,True)
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09-09'][Maadle.NUM_EVENTOS].to_string(index=False), " 3")
        self.assertEqual(len(dataframe), 1)

    def test_participants_per_resource(self):
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[0][
                             Maadle.NUM_PARTICIPANTES], 13)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[0][RECURSO], "Curso: G000 - Curso de Testing - Curso 2018-2019")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[1][
                             Maadle.NUM_PARTICIPANTES], 2)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[1][RECURSO], "Carpeta: Recursos del Alumnado")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[2][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[2][RECURSO], "Carpeta: Entrega inicial")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[3][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[3][RECURSO], "Carpeta: Exámenes")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[4][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[4][RECURSO], "Carpeta: Papeleo")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[5][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[5][RECURSO], "Foro: Noticias de clase")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[6][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[6][RECURSO], "Tarea: Entrega inicial")


    def test_eventsPerHour(self):
        self.assertEqual(0,0)

    def test_resourcesByNumberOfEvents(self):
        self.assertEqual(0,0)

    def test_averageEventsPerParticipant(self):
        self.assertEqual(0,0)

if __name__ == '__main__':
    unittest.main()
