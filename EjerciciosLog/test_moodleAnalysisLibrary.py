import unittest
import MoodleAnalysisLibrary

prueba1Rows = (MoodleAnalysisLibrary.MoodleAnalysisLibrary("TestingLog1Row.csv","", []))
prueba99Rows = (MoodleAnalysisLibrary.MoodleAnalysisLibrary("TestingLog99Rows.csv","", []))

class TestMoodleAnalysisLibrary(unittest.TestCase):

    # def test_createDataFrame(self):
    #     dataframe=prueba.createDataFrame("TestingLog1Row.csv","C:/Users/sal8b/OneDrive/Escritorio")
    #     print(dataframe.columns)
    #     # dataframe1=prueba.createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
    #     # print(dataframe1.columns)
    #     self.assertEqual(len(dataframe),1)
    #     # self.assertEqual(len(dataframe1),1842)


    def test_createDataFrameFileName(self):
        dataframe = prueba1Rows.createDataFrameFileName("TestingLog1Row.csv")
        self.assertEqual(len(dataframe), 1)
        dataframe = prueba99Rows.createDataFrameFileName("TestingLog99Rows.csv")
        self.assertEqual(len(dataframe), 99)

    def test_addIDColumn(self):
        dataframe=prueba1Rows.addIDColumn(prueba1Rows.dataframe) #Ya la tiene en el constructor, probada borrándolo y añadiéndolo aquí
        self.assertTrue('IDUsuario' in dataframe.columns)
        dataframe=prueba99Rows.addIDColumn(prueba1Rows.dataframe) #Ya la tiene en el constructor, probada borrándolo y añadiéndolo aquí
        self.assertTrue('IDUsuario' in dataframe.columns)

    def test_deleteColumns(self):
        dataframe=prueba1Rows.deleteColumns(prueba1Rows.dataframe,['Descripción'])
        self.assertFalse('Descripción' in dataframe.columns)

    def test_deleteByID(self):
        dataframe=prueba1Rows.dataframe
        self.assertTrue("0" in dataframe['IDUsuario'].values)
        dataframe=prueba1Rows.deleteByID(prueba1Rows.dataframe,["0"])
        self.assertTrue("0" not in dataframe['IDUsuario'].values)

    def test_changeHoraType(self):
        dataframe=prueba1Rows.dataframe
        self.assertEqual(dataframe['Hora'].dtype,'datetime64[ns]')# Se hace en el constructor
        dataframe=prueba99Rows.dataframe
        self.assertEqual(dataframe['Hora'].dtype,'datetime64[ns]')# Se hace en el constructor

    # def test_betweenDates(self):
    #     self.fail()
    #

    def test_addMontDayHourColumns(self):
        dataframe=prueba1Rows.dataframe
        self.assertTrue(('MesDelAño'in dataframe.columns))# Se hace en el constructor
        self.assertTrue(('DíaDelMes' in dataframe.columns))
        self.assertTrue(('HoraDelDía' in dataframe.columns))
        dataframe=prueba99Rows.dataframe
        self.assertTrue(('MesDelAño'in dataframe.columns))# Se hace en el constructor
        self.assertTrue(('DíaDelMes' in dataframe.columns))
        self.assertTrue(('HoraDelDía' in dataframe.columns))

    # def test_addDiaNormalizadoColumn(self):
    #     self.fail()
    #

    def test_numEvents(self):
        self.assertTrue(prueba1Rows.numEvents(prueba1Rows.dataframe)==1)
        self.assertTrue(prueba99Rows.numEvents(prueba99Rows.dataframe)==99)


    def test_numTeachers(self):
        self.assertTrue(prueba1Rows.numTeachers(prueba1Rows.dataframe)==1)
        self.assertTrue(prueba99Rows.numTeachers(prueba99Rows.dataframe)==1)


    def test_numParticipantsPerSubject(self):
        self.assertTrue((prueba1Rows.numParticipantsPerSubject(prueba1Rows.dataframe)==0))
        print(prueba99Rows.numParticipantsPerSubject(prueba99Rows.dataframe))
        self.assertTrue((prueba99Rows.numParticipantsPerSubject(prueba99Rows.dataframe)==13))#12 +1 de el guión


    def test_numEventsPerParticipant(self):
        self.assertTrue((((prueba1Rows.numEventsPerParticipant(prueba1Rows.dataframe))['Número de eventos'][0])==1))

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
