# encoding:utf-8

import urllib.request, re
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import sqlite3
import os

def abrir_url(url,file):

    f = urllib.request.urlretrieve(url,file)
    return file


def extraer_datos(url):
    fichero="foro"
    if abrir_url(url,fichero):
        f = open (fichero, encoding="latin-1")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser");
        
        temas = soup.findAll('li', class_="threadbit");


        return temas

def datos_bd():
    conn = sqlite3.connect('test.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS TEMAS")   
    conn.execute('''CREATE TABLE TEMAS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
       TITULO           TEXT    NOT NULL,
       LINK           TEXT    NOT NULL,
       FECHA        TEXT NOT NULL,
       RESPUESTAS  TEXT NOT NULL,
       VISITAS    TEXT NOT NULL);''')

    for i in range(1,4):
        pagina = 'page'+str(i)
        print(i)
        if i!=1:
            temas = extraer_datos("https://foros.derecho.com/foro/20-Derecho-Civil-General/"+pagina)
        else:
            temas = extraer_datos("https://foros.derecho.com/foro/20-Derecho-Civil-General")
        
        for li in temas:

            conn.execute("""INSERT INTO TEMAS (TITULO, LINK, FECHA, RESPUESTAS, VISITAS) VALUES (?,?,?,?,?)""",(
                li.find("h3", class_="threadtitle").find("a", class_="title").contents[0],
                'https://foros.derecho.com'+li.find("h3", class_="threadtitle").find("a", class_="title").get('href'),
                li.find("div", class_="threadmeta").find("span", class_="label").contents[2][2:],
                li.find("ul", class_="threadstats td alt").find("li").find("a").contents[0],
                li.find("ul", class_="threadstats td alt").findAll('li')[1].contents[0][-1:]));
    
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM TEMAS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()
    
    
    
def listar_bd():
    conn = sqlite3.connect('test.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TITULO,LINK, FECHA, RESPUESTAS, VISITAS FROM TEMAS")
    imprimir_etiqueta(cursor)
    conn.close()
    
def imprimir_etiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,"Tema: "+row[0])
        lb.insert(END,"Link: "+row[1])
        lb.insert(END,"Fecha: "+row[2])
        lb.insert(END, "Respuestas: " +row[3])
        lb.insert(END,"Visitas: "+ row[4]) 
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)
        
def buscar_tema_bd():
    def listar_busqueda(event):
        conn = sqlite3.connect('test.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        cursor = conn.execute("""SELECT TITULO,LINK,FECHA, RESPUESTAS, VISITAS FROM TEMAS WHERE TITULO LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
            
    v = Toplevel()
    lb = Label(v, text="Introduzca el tema: ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)
    
def buscar_fecha_bd():
    def listar_busqueda(event):
        conn = sqlite3.connect('test.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        cursor = conn.execute("""SELECT TITULO,LINK,FECHA, RESPUESTAS, VISITAS FROM TEMAS WHERE FECHA LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
            
    v = Toplevel()
    lb = Label(v, text="Introduzca una fecha (dd/MM/yyyy hh:mm):  ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)

def estadisticas_populares_bd():
    
    conn = sqlite3.connect('test.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT TITULO,LINK,FECHA, RESPUESTAS, VISITAS FROM TEMAS ORDER BY VISITAS DESC LIMIT 5""") # al ser de tipo string, el ? le pone comillas simples
    imprimir_etiqueta(cursor)
    conn.close()

def estadisticas_activos_bd():
    
    conn = sqlite3.connect('test.db')
    conn.text_factory = str
    cursor = conn.execute("""SELECT TITULO,LINK,FECHA, RESPUESTAS, VISITAS FROM TEMAS ORDER BY RESPUESTAS DESC LIMIT 5""") # al ser de tipo string, el ? le pone comillas simples
    imprimir_etiqueta(cursor)
    conn.close()

    

def ventana_principal():
    top = Tk()
    menubar = Menu(top)
    datosMenu = Menu(menubar, tearoff = 0)
    datosMenu.add_command(label="Cargar", command = datos_bd)
    datosMenu.add_command(label = "Mostrar", command = listar_bd)
    datosMenu.add_separator()
    datosMenu.add_command(label = "Salir", command = top.quit)
    
    menubar.add_cascade(label = "Datos", menu = datosMenu)
    
    buscarMenu = Menu(menubar, tearoff=0)
    buscarMenu.add_command(label="Tema", command = buscar_tema_bd)
    buscarMenu.add_command(label = "Fecha", command = buscar_fecha_bd)
    
    menubar.add_cascade(label = "Buscar", menu = buscarMenu)
    
    stadisticsMenu = Menu(menubar, tearoff=0)
    stadisticsMenu.add_command(label="Temas mas populares", command = estadisticas_populares_bd)
    stadisticsMenu.add_command(label = "Temas mas activos", command = estadisticas_activos_bd)
    
    menubar.add_cascade(label = "Estadisticas", menu = stadisticsMenu)

    top.config(menu = menubar)
    top.mainloop()
    

ventana_principal()