# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 17:15:14 2021

@author: Juan Camilo Giraldo-Juan pablo gutierrez
"""

import subprocess

scripts_paths =("C:/Users/ASUS/Documents/Proyecto_Final_MS/app.py","C:/Users/ASUS/Documents/Proyecto_Final_MS/graficaPrueba.py" )


procesos=[subprocess.Popen(["python", script]) for script in scripts_paths]
salir = [proceso.wait() for proceso in procesos]

if not any(salir):
    print("Todos los procesos terminaron con éxito")
else:
    print("Algunos procesos terminaron de forma inesperada.")

