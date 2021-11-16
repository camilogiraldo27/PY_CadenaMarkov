# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 23:05:44 2020

@author: juan camilo giraldo
"""
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from random import choice

# initializations
app = Flask(__name__)

# Mysql Connection
mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pastas de dientes"
)


# settings
app.secret_key = "mysecretkey"

# creating a database
cursor = mysql.cursor()

# routes
@app.route('/')
def index():
    cursor.execute('SELECT * FROM clientes')
    data = cursor.fetchall()
    print('data[0]')
    return render_template('index.html', clientes=data)


@app.route('/add_contact/<id_cliente>', methods=['POST'])
def add_contact(id_cliente):
    
        
    if request.method=='POST':
        marca_ref=['colgate','oralb','sensodine']
        marca_referencia=choice(marca_ref)
        nombre=request.form['nombre']
        id_cedula=request.form['id_cedula']
        marca_compra=request.form['marca_compra']
        cantidad=int(request.form['cantidad'])
        precio=int(request.form['precio'])
        total=int(precio*cantidad)
        
        cursor.execute('INSERT INTO clientes (marca_referencia, nombre, id_cedula, marca_compra, cantidad, precio, total) VALUES ( %s,%s,%s,%s,%s,%s,%s)',
                    (marca_referencia,nombre, id_cedula, marca_compra, cantidad, precio, total))
        mysql.commit()
        flash('Registro de venta agregada sastifactoriamente') 
        return redirect(url_for('index'))
        
        
           
       


@app.route('/edit/<id_cliente>', methods=['POST', 'GET'])
def get_contact(id_cliente):
    cursor.execute(f'SELECT * FROM clientes WHERE id_cliente = {id_cliente}')
    data = cursor.fetchall()
    cursor.close()
    print('data[0]')
    return render_template('editar_tienda.html', producto = data[0])
  


@app.route('/update/<id_cliente>', methods=['GET', 'POST'])
def update_contact(id_cliente):
    
    if request.method =='POST':
        nombre = request.form['nombre']
        id_cedula = request.form['id_cedula']
        marca_compra = request.form['marca_compra']
        cantidad=int(request.form['cantidad'])
        precio=int(request.form['precio'])
        total=int(precio*cantidad)
        cursor.execute(' UPDATE clientes SET  nombre=%s, id_cedula=%s, marca_compra=%s, cantidad=%s, precio=%s, total=%s WHERE id_cliente=%s', ( nombre, id_cedula, marca_compra, cantidad, precio, total, id_cliente))
        mysql.commit()
        mysql.close()
        flash('registro de venta actualizado corractamente.')
        return redirect(url_for('index'))
    
        
@app.route('/delete/<id_cliente>', methods=['POST', 'GET'])
def delete_contact(id_cliente):
    cursor.execute(f'DELETE FROM clientes WHERE id_cliente = {id_cliente}')
    mysql.commit()
    flash('Registro de venta eliminado corectamente')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=1000, debug=True)

    
