# encoding:latin-1

import urllib.request, re
from tkinter import *
from tkinter import messagebox
import sqlite3
import os

def abrir_url(url,file):
    try:
        if os.path.exists(file):
            recarga = input("La página ya ha sido cargada. Desea recargarla (s/n)?")
            if recarga == "s":
                f = urllib.request.urlretrieve(url,file)
        else:
            f = urllib.request.urlretrieve(url,file)
        return file
    except:
        print  ("Error al conectarse a la pÃ¡gina")
        return None

def extraer_datos():
    fichero="noticias"
    if abrir_url("http://www.us.es/rss/feed/portada",fichero):
        f = open (fichero, encoding="utf8")
        s = f.read()
        l = re.findall(r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>.*</description>\s*<author>.*</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>', s)
        f.close()
        return l
 
def almacenar_bd():
    conn = sqlite3.connect('test.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS NOTICIAS")   
    conn.execute('''CREATE TABLE NOTICIAS
       (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
       TITULO           TEXT    NOT NULL,
       LINK           TEXT    NOT NULL,
       FECHA        TEXT NOT NULL);''')
    l = extraer_datos()
    for i in l:
        conn.execute("""INSERT INTO NOTICIAS (TITULO, LINK, FECHA) VALUES (?,?,?)""",(i[0],i[1],i[3]))
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM NOTICIAS")
    messagebox.showinfo( "Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()

def listar_bd():
    conn = sqlite3.connect('test.db')
    conn.text_factory = str  
    cursor = conn.execute("SELECT TITULO,LINK, FECHA FROM NOTICIAS")
    imprimir_etiqueta(cursor)
    conn.close()
    
def imprimir_etiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)

def buscar_bd():
    def listar_busqueda(event):
        conn = sqlite3.connect('test.db')
        conn.text_factory = str
        s = "%"+en.get()+"%" 
        cursor = conn.execute("""SELECT TITULO,LINK,FECHA FROM NOTICIAS WHERE FECHA LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
    
    v = Toplevel()
    lb = Label(v, text="Introduzca una fecha (Xxx): ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)
  
    
def ventana_principal():
    top = Tk()
    almacenar = Button(top, text="Almacenar", command = almacenar_bd)
    almacenar.pack(side = LEFT)
    listar = Button(top, text="Listar", command = listar_bd)
    listar.pack(side = LEFT)
    Buscar = Button(top, text="Buscar", command = buscar_bd)
    Buscar.pack(side = LEFT)
    top.mainloop()
    

if __name__ == "__main__":
    ventana_principal()
