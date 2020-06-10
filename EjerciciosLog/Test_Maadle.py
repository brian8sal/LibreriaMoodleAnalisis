import unittest
import Maadle
import numpy as np

FECHA = 'Fecha'
RECURSO = 'Recurso'

prueba1Rows = (Maadle.Maadle("TestingLog1Row.csv", "", "PrezConfig1.xlsx", ""))
prueba99Rows = (Maadle.Maadle("TestingLog99Rows.csv", "", "PrezConfig2.xlsx", ""))
prueba99RowsSinUsuarios = (Maadle.Maadle("TestingLog99Rows.csv", "", "PrezConfig.xlsx", ""))
prueba99RowsTodosUsuarios = (Maadle.Maadle("TestingLog99RowsTodosUsuarios.csv", "", "PrezConfig1.xlsx", ""))


class Test_Maadle(unittest.TestCase):

    def test_create_data_frame(self):
        dataframe = prueba1Rows.create_data_frame("TestingLog1Row.csv", ".")
        self.assertEqual(len(dataframe), 1)
        dataframe = prueba99Rows.create_data_frame("TestingLog99Rows.csv", ".")
        self.assertEqual(len(dataframe), 99)

    def test_create_data_frame_file_name(self):
        dataframe = prueba1Rows.create_data_frame_file_fame("TestingLog1Row.csv")
        self.assertEqual(len(dataframe), 1)
        dataframe = prueba99Rows.create_data_frame_file_fame("TestingLog99Rows.csv")
        self.assertEqual(len(dataframe), 99)

    def test_addID_user_column(self):
        dataframe = prueba1Rows.add_ID_user_column()
        self.assertTrue(Maadle.ID_USUARIO in dataframe.columns)
        dataframe = prueba99Rows.add_ID_user_column()
        self.assertTrue(Maadle.ID_USUARIO in dataframe.columns)

    def test_deleteColumns(self):
        dataframe = prueba1Rows.delete_columns([Maadle.DESCRIPCION])
        self.assertFalse(Maadle.DESCRIPCION in dataframe.columns)

    def test_deleteByID(self):
        dataframe = prueba1Rows.dataframe
        self.assertTrue("0" in dataframe[Maadle.ID_USUARIO].values)
        dataframe = prueba1Rows.delete_by_ID(["0"])
        self.assertTrue("0" not in dataframe[Maadle.ID_USUARIO].values)

    def test_changeHoraType(self):
        dataframe = prueba1Rows.dataframe
        self.assertEqual(dataframe[Maadle.FECHA_HORA].dtype, 'datetime64[ns]')  # Se hace en el constructor
        dataframe = prueba99Rows.dataframe
        self.assertEqual(dataframe[Maadle.FECHA_HORA].dtype, 'datetime64[ns]')  # Se hace en el constructor

    def test_betweenDates(self):
        ini = np.datetime64('2019-08-01')
        fin = np.datetime64('2019-08-29')
        self.assertEqual(len(prueba99Rows.between_dates(ini, fin)), 1)
        ini = np.datetime64('2019-09-01')
        fin = np.datetime64('2019-09-10')
        self.assertEqual(len(prueba99Rows.between_dates(ini, fin)), 5)

    def test_addMontDayHourColumns(self):
        dataframe = prueba1Rows.dataframe
        self.assertTrue(('MesDelAño' in dataframe.columns))  # Se hace en el constructor
        self.assertTrue(('DíaDelMes' in dataframe.columns))
        self.assertTrue(('HoraDelDía' in dataframe.columns))
        dataframe = prueba99Rows.dataframe
        self.assertTrue(('MesDelAño' in dataframe.columns))  # Se hace en el constructor
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
        self.assertTrue('TODOS HAN PARTICIPADO' in prueba99RowsTodosUsuarios.list_nonparticipant().columns)

    def test_events_per_month(self):
        dataframe = prueba99Rows.events_per_month()
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-03'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 5")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-05'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 6")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-06'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 3")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-07'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 12")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-08'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 1")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 17")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-10'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 3")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-12'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 6")

    def test_events_per_week(self):
        dataframe = prueba99Rows.events_per_week()
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '12'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 5")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '17'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 4")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '18'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 1")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '21'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 1")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '22'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 2")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '23'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 1")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '26'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 4")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '27'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 2")

    def test_events_per_day(self):
        dataframe = prueba99Rows.events_per_day()
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-03-26'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 4")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-03-27'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 1")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-05-03'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 4")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-05-07'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 1")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-05-29'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 1")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-06-03'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 2")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-06-16'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 1")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-07-01'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 4")

    def test_eventsPerResource(self):
        self.assertEqual(prueba99Rows.events_per_resource().iloc[0][Maadle.NUM_EVENTOS], 1)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[0][Maadle.ID_RECURSO], 5016.0)

        self.assertEqual(prueba99Rows.events_per_resource().iloc[1][Maadle.NUM_EVENTOS], 1)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[1][Maadle.ID_RECURSO], 5015.0)

        self.assertEqual(prueba99Rows.events_per_resource().iloc[2][Maadle.NUM_EVENTOS], 1)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[2][Maadle.ID_RECURSO], 5014.0)

        self.assertEqual(prueba99Rows.events_per_resource().iloc[3][Maadle.NUM_EVENTOS], 1)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[3][Maadle.ID_RECURSO], 5013.0)

        self.assertEqual(prueba99Rows.events_per_resource().iloc[4][Maadle.NUM_EVENTOS], 2)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[4][Maadle.ID_RECURSO], 5012.0)

        self.assertEqual(prueba99Rows.events_per_resource().iloc[5][Maadle.NUM_EVENTOS], 1)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[5][Maadle.ID_RECURSO], 5011.0)

        self.assertEqual(prueba99Rows.events_per_resource().iloc[6][Maadle.NUM_EVENTOS], 1)
        self.assertEqual(prueba99Rows.events_per_resource().iloc[6][Maadle.ID_RECURSO], 5002.0)

    def test_events_between_dates(self):
        initial = np.datetime64('2019-08-01')
        final = np.datetime64('2019-08-29')
        dataframe = prueba99Rows.events_between_dates(initial, final)
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-08-01'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 1")
        initial = np.datetime64('2019-09-01')
        final = np.datetime64('2019-09-10')
        dataframe = prueba99Rows.events_between_dates(initial, final)
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09-09'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 3")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09-05'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 1")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09-02'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 1")
        initial = np.datetime64('2019-09-09')
        final = np.datetime64('2019-09-23')
        dataframe = prueba99Rows.events_between_dates(initial, final)
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09-09'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 3")
        self.assertEqual(dataframe.loc[dataframe[FECHA] == '2019-09-22'][Maadle.NUM_EVENTOS].to_string(index=False),
                         " 4")
        self.assertEqual(len(dataframe), 2)

    def test_participants_per_resource(self):
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[0][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[0][RECURSO],
                         "Carpeta: Entrega inicial")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[1][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[1][RECURSO], "Tarea: Entrega inicial")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[2][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[2][RECURSO], "Carpeta: Recursos del Alumnado")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[3][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[3][RECURSO], "Carpeta: Papeleo")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[4][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[4][RECURSO], "Carpeta: Recursos del Alumnado")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[5][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[5][RECURSO], "Carpeta: Recursos del Alumnado")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[6][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[6][RECURSO], "Carpeta: Exámenes")

        self.assertEqual(prueba99Rows.participants_per_resource().iloc[7][
                             Maadle.NUM_PARTICIPANTES], 1)
        self.assertEqual(prueba99Rows.participants_per_resource().iloc[7][RECURSO], "Foro: Noticias de clase")

    def test_events_per_day_per_user(self):
        self.assertEqual(prueba99Rows.events_per_day_per_user("CUADRIELLO GALDÓS, ÁNGELA")[Maadle.NUM_EVENTOS][0], 4)
        self.assertEqual(prueba99Rows.events_per_day_per_user("CUADRIELLO GALDÓS, ÁNGELA")[Maadle.NUM_EVENTOS][1], 1)
        self.assertEqual(prueba99Rows.events_per_day_per_user("CUADRIELLO GALDÓS, ÁNGELA")[Maadle.NUM_EVENTOS][2], 1)

        self.assertEqual(prueba99Rows.events_per_day_per_user("CUEVAS RODRIGUEZ, SARA")[Maadle.NUM_EVENTOS][0], 1)

        self.assertEqual(prueba99Rows.events_per_day_per_user("CIMAS CAMPOS, NOIVE")[Maadle.NUM_EVENTOS][0], 2)
        self.assertEqual(prueba99Rows.events_per_day_per_user("CIMAS CAMPOS, NOIVE")[Maadle.NUM_EVENTOS][1], 1)

        self.assertEqual(prueba99Rows.events_per_day_per_user("Pérez González, Docente")[Maadle.NUM_EVENTOS][0], 2)
        self.assertEqual(prueba99Rows.events_per_day_per_user("Pérez González, Docente")[Maadle.NUM_EVENTOS][1], 1)
        self.assertEqual(prueba99Rows.events_per_day_per_user("Pérez González, Docente")[Maadle.NUM_EVENTOS][2], 3)
        self.assertEqual(prueba99Rows.events_per_day_per_user("Pérez González, Docente")[Maadle.NUM_EVENTOS][3], 4)
        self.assertEqual(prueba99Rows.events_per_day_per_user("Pérez González, Docente")[Maadle.NUM_EVENTOS][4], 8)
        self.assertEqual(prueba99Rows.events_per_day_per_user("Pérez González, Docente")[Maadle.NUM_EVENTOS][5], 3)
        self.assertEqual(prueba99Rows.events_per_day_per_user("Pérez González, Docente")[Maadle.NUM_EVENTOS][6], 6)

    def test_events_per_day_per_resource(self):
        self.assertEqual(prueba99Rows.events_per_day_per_resource(5000.0)[Maadle.NUM_EVENTOS][0], 2)
        self.assertEqual(prueba99Rows.events_per_day_per_resource(5000.0)[Maadle.NUM_EVENTOS][1], 3)
        self.assertEqual(prueba99Rows.events_per_day_per_resource(5000.0)[Maadle.NUM_EVENTOS][2], 6)
        self.assertEqual(prueba99Rows.events_per_day_per_resource(5000.0)[Maadle.NUM_EVENTOS][3], 2)

        self.assertEqual(prueba99Rows.events_per_day_per_resource(5002.0)[Maadle.NUM_EVENTOS][0], 1)

        self.assertEqual(prueba99Rows.events_per_day_per_resource(5011.0)[Maadle.NUM_EVENTOS][0], 1)

        self.assertEqual(prueba99Rows.events_per_day_per_resource(5012.0)[Maadle.NUM_EVENTOS][0], 2)

        self.assertEqual(prueba99Rows.events_per_day_per_resource(5013.0)[Maadle.NUM_EVENTOS][0], 1)

        self.assertEqual(prueba99Rows.events_per_day_per_resource(5014.0)[Maadle.NUM_EVENTOS][0], 1)

        self.assertEqual(prueba99Rows.events_per_day_per_resource(5015.0)[Maadle.NUM_EVENTOS][0], 1)

        self.assertEqual(prueba99Rows.events_per_day_per_resource(5015.0)[Maadle.NUM_EVENTOS][0], 1)

        self.assertEqual(prueba99Rows.events_per_day_per_resource(5016.0)[Maadle.NUM_EVENTOS][0], 1)

    def test_create_dynamic_session_id(self):
        dataframe = prueba99Rows.create_dynamic_session_id()
        self.assertTrue(Maadle.ID_SESION in dataframe.columns)
        self.assertEqual(dataframe[Maadle.ID_SESION].loc[dataframe[Maadle.FECHA_HORA] == '2019-07-01 10:30:00'].values,
                         ['1:0'])
        self.assertEqual(dataframe[Maadle.ID_SESION].loc[dataframe[Maadle.FECHA_HORA] == '2019-07-01 10:33:00'].values,
                         ['1:0'])
        self.assertEqual(dataframe[Maadle.ID_SESION].loc[dataframe[Maadle.FECHA_HORA] == '2019-07-12 17:36:00'].values,
                         ['1:1'])
        self.assertEqual(dataframe[Maadle.ID_SESION].loc[dataframe[Maadle.FECHA_HORA] == '2019-07-19 10:13:00'].values,
                         ['1:2'])
        self.assertEqual(dataframe[Maadle.ID_SESION].loc[dataframe[Maadle.FECHA_HORA] == '2019-09-27 19:17:00'].values,
                         ['1:5'])
        self.assertEqual(dataframe[Maadle.ID_SESION].loc[dataframe[Maadle.FECHA_HORA] == '2019-12-23 16:48:00'].values,
                         ['1:8'])

        self.assertEqual(dataframe[Maadle.ID_SESION].loc[dataframe[Maadle.FECHA_HORA] == '2019-03-26 15:22:00'].values,
                         ['1010:0'])
        self.assertEqual(dataframe[Maadle.ID_SESION].loc[dataframe[Maadle.FECHA_HORA] == '2019-08-01 14:49:00'].values,
                         ['1010:1'])
        self.assertEqual(dataframe[Maadle.ID_SESION].loc[dataframe[Maadle.FECHA_HORA] == '2019-09-02 13:34:00'].values,
                         ['1010:2'])

    def test_number_of_sessions_by_user(self):
        dataframe = prueba99Rows.number_of_sessions_by_user()
        self.assertEqual(dataframe['Número de sesiones iniciadas'].loc[
                             dataframe[Maadle.NOMBRE_USUARIO] == 'Pérez González, Docente'].values, 9)
        self.assertEqual(dataframe['Número de sesiones iniciadas'].loc[
                             dataframe[Maadle.NOMBRE_USUARIO] == 'REVUELTA DIAZ, CRISTINA'].values, 1)
        self.assertEqual(dataframe['Número de sesiones iniciadas'].loc[
                             dataframe[Maadle.NOMBRE_USUARIO] == 'CUADRIELLO GALDÓS, ÁNGELA'].values, 3)
        self.assertEqual(dataframe['Número de sesiones iniciadas'].loc[
                             dataframe[Maadle.NOMBRE_USUARIO] == 'CIMAS CAMPOS, NOIVE'].values, 2)

    def test_sessions_matrix(self):
        result_matrix = prueba99Rows.sessions_matrix()
        expected_matrix = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0],
                           [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0]]
        self.assertEqual(result_matrix, expected_matrix)

    def test_events_per_hour(self):
        dataframe = prueba99Rows.events_per_hour()
        self.assertEqual(dataframe[Maadle.NUM_EVENTOS].loc[dataframe[Maadle.FECHA_HORA] == '08'].values, 3)
        self.assertEqual(dataframe[Maadle.NUM_EVENTOS].loc[dataframe[Maadle.FECHA_HORA] == '10'].values, 13)
        self.assertEqual(dataframe[Maadle.NUM_EVENTOS].loc[dataframe[Maadle.FECHA_HORA] == '11'].values, 5)
        self.assertEqual(dataframe[Maadle.NUM_EVENTOS].loc[dataframe[Maadle.FECHA_HORA] == '12'].values, 10)
        self.assertEqual(dataframe[Maadle.NUM_EVENTOS].loc[dataframe[Maadle.FECHA_HORA] == '14'].values, 1)
        self.assertEqual(dataframe[Maadle.NUM_EVENTOS].loc[dataframe[Maadle.FECHA_HORA] == '17'].values, 4)

    def course_structure(self):
        dataframe = prueba99Rows.course_structure()
        self.assertTrue(Maadle.SECCION in dataframe.columns)

    def test_resources_by_number_of_events(self):
        self.assertEqual(0, 0)


if __name__ == '__main__':
    unittest.main()
