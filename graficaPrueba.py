# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 17:15:14 2021

@author: Juan Camilo Giraldo-Juan pablo gutierrez
"""
import accederBD as bd
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from sklearn.metrics import confusion_matrix
import numpy as np
from dash import Input, Output 
import DF_To_GSheet as sh

nN=0
df=bd.df
cm=confusion_matrix(df.marca_referencia, df.marca_compra)

def markov(Nnn):
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
    
    for n in range(1,Nnn+1):
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
                
                
    df1 = pd.DataFrame(probabilidades)
    df1.columns = ['probabilidad']
    return x,df1
    

#GRAFICA EN LA WEB LOCALHOST

grafica=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar= dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Registrar venta", href="http://localhost:1000")),
        dbc.NavItem(dbc.NavLink("Analisis", href="https://docs.google.com/spreadsheets/d/14W1i-S93awy2RNUEP1Wlxh8857Po9XBPi7aMiFVJ6GM/edit#gid=0")),
       
    ],
    brand="GRÁFICA",
    brand_href="#",
    color="primary",
    dark=True,
    )





grafica.layout= html.Div([
    
navbar,
dcc.Input(
            id="input_range_2", type="number", placeholder="input with range",value="4",
            min=1, max=100
        ),
html.Div(id='output_container', children=[]),
html.Br(),
dcc.Graph(
    id='life-exp-vs-gdp',
    figure={}
    )
])


@grafica.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='life-exp-vs-gdp', component_property='figure')],
    [Input(component_id='input_range_2', component_property='value')]
)
def update_graph(option_slctd):
    global nN
    trasiciones=['colgate-colgate','oralb-colgate','sensodine-colgate','colgate-oralb','oralb-oralb','sensodine-oralb','colgate-sensodine','oralb-sensodine','sensodine-sensodine']
    print(option_slctd)
    print(type(option_slctd))

    container = "Numero de mes: {}".format(option_slctd)

    Nn = option_slctd
    Nn=int(Nn)
    nN=Nn
    
    x,y=markov(Nn)
    sh.Export_Data_To_Sheets(Nn)
    
         
    
    return(container, {
        'data':[
             
             go.Scatter(
                
                x=x,
                y=y.probabilidad[0+i*Nn:i*Nn+Nn],
                mode='lines+markers',
                opacity=0.8,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                    },
                name=trasiciones[i]
                
                )for i in range(0,9)
                 
            ],
        'layout':{
            'title':'GRÁFICA'
            }
    })

    
    
if __name__ == '__main__':
    grafica.run_server(port=2000, debug=True)
