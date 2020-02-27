import unittest
import MoodleAnalysisLibrary

prueba = (MoodleAnalysisLibrary.MoodleAnalysisLibrary("TestingLog1Row.csv","", []))
class TestMoodleAnalysisLibrary(unittest.TestCase):

    # def test_createDataFrame(self):
    #     dataframe=prueba.createDataFrame("TestingLog1Row.csv","C:/Users/sal8b/OneDrive/Escritorio")
    #     print(dataframe.columns)
    #     # dataframe1=prueba.createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
    #     # print(dataframe1.columns)
    #     self.assertEqual(len(dataframe),1)
    #     # self.assertEqual(len(dataframe1),1842)


    def test_createDataFrameFileName(self):
        dataframe = prueba.createDataFrameFileName("TestingLog1Row.csv")
        self.assertEqual(len(dataframe), 1)

    def test_addIDColumn(self):
        dataframe=prueba.addIDColumn(prueba.dataframe) #Ya la tiene en el constructor, probada borrándolo y añadiéndolo aquí
        self.assertTrue('IDUsuario' in dataframe.columns)

    def test_deleteColumns(self):
        dataframe=prueba.deleteColumns(prueba.dataframe,['Descripción'])
        self.assertFalse('Descripción' in dataframe.columns)

    def test_deleteByID(self):
        dataframe=prueba.dataframe
        self.assertTrue("0" in dataframe['IDUsuario'].values)
        dataframe=prueba.deleteByID(prueba.dataframe,["0"])
        self.assertTrue("0" not in dataframe['IDUsuario'].values)

    def test_changeHoraType(self):
        dataframe=prueba.dataframe
        self.assertEqual(dataframe['Hora'].dtype,'datetime64[ns]')# Se hace en el constructor

    # def test_betweenDates(self):
    #     self.fail()
    #
    def test_addMontDayHourColumns(self):
        dataframe=prueba.dataframe
        self.assertTrue(('MesDelAño'in dataframe.columns))# Se hace en el constructor
        self.assertTrue(('DíaDelMes' in dataframe.columns))
        self.assertTrue(('HoraDelDía' in dataframe.columns))


    # def test_addDiaNormalizadoColumn(self):
    #     self.fail()
    #
    def test_numEvents(self):
        self.assertTrue(prueba.numEvents(prueba.dataframe)==1)

    def test_numTeachers(self):
        self.assertTrue(prueba.numTeachers(prueba.dataframe)==1)

    def test_numParticipantsPerSubject(self):
        self.assertTrue((prueba.numParticipantsPerSubject(prueba.dataframe)==0))

    def test_numEventsPerParticipant(self):
        self.assertTrue((((prueba.numEventsPerParticipant(prueba.dataframe))['Número de eventos'][0])==1))

    # def test_eventsPerMonth(self):
    #     self.fail()
    #
    # def test_eventsPerWeek(self):
    #     self.fail()
    #
    # def test_eventsPerDay(self):
    #     self.fail()
    #
    # def test_eventsPerResource(self):
    #     self.fail()
    #
    # def test_eventsPerHour(self):
    #     self.fail()
    #
    # def test_resourcesByNumberOfEvents(self):
    #     self.fail()
    #
    # def test_eventsBetweenDates(self):
    #     self.fail()
    #
    # def test_averageEventsPerParticipant(self):
    #     self.fail()

if __name__ == '__main__':
    unittest.main()
