# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 17:15:14 2021

@author: Juan Camilo Giraldo-Juan pablo gutierrez
"""

from Google import Create_Service
import pandas as pd
import numpy as np
import accederBD as bd
from sklearn.metrics import confusion_matrix


CLIENT_SECRETS_FILE = 'client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
gsheetId = '14W1i-S93awy2RNUEP1Wlxh8857Po9XBPi7aMiFVJ6GM'


service = Create_Service(CLIENT_SECRETS_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)



def Export_Data_To_Sheets(Nnn):
    trasiciones=['colgate-colgate','oralb-colgate','sensodine-colgate','colgate-oralb','oralb-oralb','sensodine-oralb','colgate-sensodine','oralb-sensodine','sensodine-sensodine']
    df=bd.df
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
                
                

                
                
    df = pd.DataFrame(probabilidades)
    df.columns = ['probabilidad']
    x=[]
    d=[]
    for i in range(len(probabilidades)):   
        y=df.probabilidad[0+i*Nnn:i*Nnn+Nnn]
        x.append(y)
    df1=pd.DataFrame(x)
    df1.replace(np.nan, '', inplace=True)
    
    for k in range(0,9):
        for j in range(0,Nnn):
            d.append(trasiciones[k])
    df1.columns=d
        
    response_date = service.spreadsheets().values().append(
        spreadsheetId=gsheetId,
        valueInputOption='RAW',
        range='BD!A3',
        body=dict(
            majorDimension='ROWS',
            values=df1.T.reset_index().T.values.tolist())
    ).execute()

    