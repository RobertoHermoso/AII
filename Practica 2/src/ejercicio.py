# encoding:utf-8
import urllib.request, re
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import sqlite3

def abrir_url(url,file):

    f = urllib.request.urlretrieve(url,file)
    return file


def extraer_datos(url):
    fichero="productos"
    if abrir_url(url,fichero):
        f = open (fichero, encoding="utf-8")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser");
        
        temas = soup.findAll('div', class_='grid__item m-one-whole t-one-third d-one-third dw-one-quarter | js-product-grid-grid');

        return temas

def almacenar_bd():
    conn = sqlite3.connect('test.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS PRODUCTOS")   
    conn.execute('''CREATE TABLE PRODUCTOS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
       MARCA               TEXT NOT NULL,
       NOMBRE              TEXT NOT NULL,
       LINK                TEXT NOT NULL,
       PRECIOACTUAL        TEXT NOT NULL,
       PRECIOANTERIOR      TEXT);''')

    temas = extraer_datos("https://www.ulabox.com/en/campaign/productos-sin-gluten?v=g")

    for li in temas:

        if li.find('del', class_='product-item__price product-item__price--old product-grid-footer__price--old nano | flush--bottom'):
            precioAnterior = li.find('del', class_='product-item__price product-item__price--old product-grid-footer__price--old nano | flush--bottom').contents[0]
        else:
            precioAnterior = NONE
        print()
        conn.execute("""INSERT INTO PRODUCTOS (MARCA, NOMBRE, LINK, PRECIOACTUAL, PRECIOANTERIOR) VALUES (?,?,?,?,?)""",(
            li.find('article').get('data-product-brand'),
            li.find('article').get('data-product-name'),
            'https://www.ulabox.com' + li.find('a', class_='product-item__image nauru js-pjax js-article-link').get('href'),
            li.find('article').get('data-price'),
            precioAnterior));
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM PRODUCTOS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " productos")
    conn.close()


def mostrar_bd():

    master = Tk()
    conn = sqlite3.connect('test.db')
    marcas = conn.execute("SELECT DISTINCT MARCA FROM PRODUCTOS")

    res = list(map(lambda x:x[0], marcas.fetchall()));

    w = Spinbox(master, values =res )
    w.pack()
    w.grid(row = 0, column=0)
    buscar = Button(master, text="Buscar", command=lambda: show_data(w.get()))
    buscar.grid(row=1, column=0)
 
    mainloop()
    

def show_data(data):
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("""SELECT NOMBRE,PRECIOACTUAL FROM PRODUCTOS WHERE MARCA LIKE ?""",(data,)) # al ser de tipo string, el ? le pone comillas simples
    
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,"Nombre: "+row[0])
        lb.insert(END,"Precio Final: "+row[1] + " €")
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)


def buscar_bd():
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("""SELECT NOMBRE,PRECIOACTUAL, PRECIOANTERIOR FROM PRODUCTOS WHERE PRECIOANTERIOR NOT LIKE 'none'""")  # al ser de tipo string, el ? le pone comillas simples
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END, "Nombre: " + row[0])
        lb.insert(END, "Precio actual: " + row[1] + " €")
        lb.insert(END, "Precio anterior: " + row[2][1:] + " €")
        lb.insert(END, '')
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)
    

def ventana_principal():
    top = Tk()
    almacenar = Button(top, text="Almacenar productos", command = almacenar_bd)
    almacenar.pack(side = LEFT)
    listar = Button(top, text="Mostrar marca", command = mostrar_bd)
    listar.pack(side = LEFT)
    buscar = Button(top, text="Buscar ofertas", command = buscar_bd)
    buscar.pack(side = LEFT)
    top.mainloop()
    

if __name__ == "__main__":
    ventana_principal()
