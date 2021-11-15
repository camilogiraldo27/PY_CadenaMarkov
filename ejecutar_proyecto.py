# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 11:27:56 2020

@author: juan camilo giraldo
"""

import subprocess

scripts_paths =("C:/Users/ASUS/Documents/Proyecto_Final_MS/app.py","C:/Users/ASUS/Documents/Proyecto_Final_MS/grafica/grafica.py" )


procesos=[subprocess.Popen(["python", script]) for script in scripts_paths]
salir = [proceso.wait() for proceso in procesos]

if not any(salir):
    print("Todos los procesos terminaron con éxito")
else:
    print("Algunos procesos terminaron de forma inesperada.")

