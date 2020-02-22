import unittest
import MoodleAnalysisLibrary

prueba = (MoodleAnalysisLibrary.MoodleAnalysisLibrary("logs_G668_1819_20191223-1648.csv","C:/Users/sal8b/OneDrive/Escritorio/Beca", ["323", "2", "231"]))
class TestMoodleAnalysisLibrary(unittest.TestCase):

    def test_createDataFrame(self):
        dataframe=prueba.createDataFrame("TestingLog99Rows.csv","C:/Users/sal8b/OneDrive/Escritorio")
        dataframe1=prueba.createDataFrame("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca")
        self.assertEqual(len(dataframe),99)
        self.assertEqual(len(dataframe1),1842)

    #
    # def test_createDataFrameFileName(self):
    #     self.fail()
    #

    def test_addIDColumn(self):
        dataframe=prueba.addIDColumn(prueba.dataframe) #Ya la tiene en el constructor, probada borrándolo y añadiéndolo aquí
        self.assertTrue('IDUsuario' in dataframe.columns)

    def test_deleteColumns(self):
        dataframe=prueba.deleteColumns(prueba.dataframe,['Descripción'])
        self.assertFalse('Descripción' in dataframe.columns)

    # def test_deleteByID(self):
    #     self.fail()
    #
    # def test_graphicEventsPerUser(self):
    #     self.fail()
    #
    # def test_graphicEventsPerContext(self):
    #     self.fail()
    #
    # def test_changeHoraType(self):
    #     self.fail()
    #
    # def test_betweenDates(self):
    #     self.fail()
    #
    # def test_addMontDayHourColumns(self):
    #     self.fail()
    #
    # def test_addDiaNormalizadoColumn(self):
    #     self.fail()
    #
    # def test_numEvents(self):
    #     self.fail()
    #
    # def test_numTeachers(self):
    #     self.fail()
    #
    # def test_numParticipantsPerSubject(self):
    #     self.fail()
    #
    # def test_numEventsPerParticipant(self):
    #     self.fail()
    #
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
