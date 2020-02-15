# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import EjerciciosLog as el

df = el.createDataFrameFileName("logs_G668_1819_20191223-1648.csv")
#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')


def generateTable(dataframe, maxRows=100):
    return html.Table(
        # Cabecera
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Cuerpo
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), maxRows))]
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Log G668'),
    generateTable(df)
])
if __name__ == '__main__':
    app.run_server(debug=True)