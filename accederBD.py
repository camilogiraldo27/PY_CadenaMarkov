# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 17:15:14 2021

@author: Juan Camilo Giraldo-Juan pablo gutierrez
"""
import mysql.connector
import pandas as pd

mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pymodelacion"
    )

df=pd.read_sql_query('SELECT * FROM clientes', mysql)