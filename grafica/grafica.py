# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 00:24:15 2021

@author: Juan Camilo Giraldo Céspedes y juan Pablo gutierrez
"""

import mysql.connector
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from sklearn.metrics import confusion_matrix
import numpy as np


mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pymodelacion"
)


df=pd.read_sql_query('SELECT * FROM clientes', mysql)
cm=confusion_matrix(df.marca_referencia, df.marca_compra)
sumaT=[]
for i in range(len(cm)):
    suma=0
    for j in range(len(cm)):
        suma=suma+ cm[i][j]
    sumaT.append(suma)
    

a = []
for i in range(3):
     a.append([])
     for j in range(3):
           
         a[i].append(cm[i][j]/sumaT[i])
         
cm_nva = np.array(a)


## Esta parte del codigo en adelante ya es lo de markov
an=[]
N=3
for n in range(1,N+1):
    bn=np.linalg.matrix_power(cm_nva,n)
    an.append(bn)
    
x=np.arange(0,len(an))

for i in range(len(an)):
    print("estado del tiempo en la hora "+str(i+1)+" : ")
    print(an[i])
    

probabilidades=[]

for m in range(len(a)):
    for j in range(len(a)):
        for i in range(len(x)):
            probabilidades.append(an[i][j][m])
            
posicion=0
            
df = pd.DataFrame(probabilidades)
df.columns = ['probabilidad']

#GRAFICA EN LA WEB LOCALHOST
grafica=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar= dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Registrar venta", href="http://localhost:1000")),
        dbc.NavItem(dbc.NavLink("Análisis", href="https://docs.google.com/spreadsheets/d/14W1i-S93awy2RNUEP1Wlxh8857Po9XBPi7aMiFVJ6GM/edit#gid=0")),
       
    ],
    brand="GRÁFICA",
    brand_href="#",
    color="primary",
    dark=True,
    )



posicion=posicion+N
grafica.layout= html.Div([
    
navbar,
dcc.Input(
            id="input_range_2", type="number", placeholder="input with range",
            min=1, max=100
        ),
dcc.Graph(
    id='life-exp-vs-gdp',
    figure={
        
        'data':[
             
             go.Scatter(
                
                x=x,
                y=df.probabilidad[0+i*3:i*3+N],
                mode='lines+markers',
                opacity=0.8,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                    },
                name=i
                
                )for i in range(0,9)
                 
            ],
        'layout':{
            'title':'GRÁFICA'
            }
        }
    )
])




    
if __name__ == '__main__':
    grafica.run_server(port=2000, debug=True)
