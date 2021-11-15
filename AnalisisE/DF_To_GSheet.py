# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 17:39:34 2020

@author: juan camilo giraldo
"""
import mysql.connector
from Google import Create_Service
import pandas as pd
import numpy as np

CLIENT_SECRETS_FILE = 'client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
gsheetId = '14W1i-S93awy2RNUEP1Wlxh8857Po9XBPi7aMiFVJ6GM'


service = Create_Service(CLIENT_SECRETS_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="python")

def Export_Data_To_Sheets():
    df=pd.read_sql_query('SELECT * FROM tienda', mysql)
    df.replace(np.nan, '', inplace=True)
    response_date = service.spreadsheets().values().append(
        spreadsheetId=gsheetId,
        valueInputOption='RAW',
        range='BD!A3',
        body=dict(
            majorDimension='ROWS',
            values=df.T.reset_index().T.values.tolist())
    ).execute()

    rs=df.total
    Resumen=rs.describe()
    response_date = service.spreadsheets().values().append(
        spreadsheetId=gsheetId,
        valueInputOption='RAW',
        range='Analisis_Estadistico_total!A3',
        body=dict(
            majorDimension='ROWS',
            values=Resumen.T.reset_index().T.values.tolist())
    ).execute()
    
    

Export_Data_To_Sheets()