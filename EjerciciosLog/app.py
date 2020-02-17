# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import MoodleAnalysisLibrary

prueba=(MoodleAnalysisLibrary.MoodleAnalysisLibrary("logs_G668_1819_20191223-1648.csv", "C:/Users/sal8b/OneDrive/Escritorio/Beca",["323","0"]))
print(prueba.dataframe)
ini = pd.Timestamp(2019, 8, 1)
fin = pd.Timestamp(2019, 8, 29)
print(prueba.betweenDates(prueba.dataframe,ini,fin))
