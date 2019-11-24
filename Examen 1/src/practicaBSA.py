# encoding:utf-8

import urllib.request, re
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import sqlite3

from numpy.core import string_

categorias_diferentes = set();

def abrir_url(url, file):
    f = urllib.request.urlretrieve(url, file)
    return file


def extraer_datos(url):
    fichero = "peliculas"
    if abrir_url(url, fichero):
        f = open(fichero, encoding="latin-1")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser");

        allElements = soup.findAll('ul', class_="elements")[0];
        temas = allElements.find_all('li')
        return temas


def extraer_datos_de_una_pelicula(url):
    fichero = "pelicula"
    if abrir_url(url, fichero):
        f = open(fichero, encoding="latin-1")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser");

        elements = soup.find('p', class_="categorias").findAll("a");
        categorias = []
        for c in elements:
            categorias.append(c.contents[0])
            categorias_diferentes.add(c.contents[0])
        return categorias

def almacenar_bd():
    conn = sqlite3.connect('defensa.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS ESTRENOS")
    conn.execute('''CREATE TABLE ESTRENOS
              (ID INTEGER PRIMARY KEY  AUTOINCREMENT, TITULO TEXT NOT NULL,
              ENLACE TEXT NOT NULL, FECHA TEXT NOT NULL, GENEROS TEXT NOT NULL, PAIS TEXT NOT NULL);''')
    conn.execute("DROP TABLE IF EXISTS GENEROS")
    conn.execute('''CREATE TABLE GENEROS
                    (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
                    TITULO               TEXT NOT NULL);''')

    for i in range(2):
        if(i==str(1)):
            url = "https://www.elseptimoarte.net/estrenos";
        else:
            url = "https://www.elseptimoarte.net/estrenos/"+str(i);

        urllib.request.urlretrieve(url, "peliculas")
        f = open("peliculas", "r")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser")
        elements = soup.find("ul", "elements")
        list_of_elements = elements.find_all("li")
        for i in list_of_elements:
            enlace = "https://www.elseptimoarte.net/peliculas" + i.find("h3").find("a").get('href')
            urllib.request.urlretrieve(enlace, "estreno")
            e = open("estreno", "r")
            p = e.read()
            soup2 = BeautifulSoup(p, 'html.parser')
            dds = soup2.find_all("dd")
            titulo = dds[0].contents[0]
            pais = dds[2].find("a").contents[0]
            if len(dds) ==11:
                fecha = dds[3].contents[0]
            else:
                fecha = dds[4].contents[0]
            generos = soup2.find("div", "wrapper cinema1").find("p", "categorias").find_all("a")
            categorias = []
            for c in generos:
                categorias.append(c.contents[0])
                categorias_diferentes.add(c.contents[0])
            g = 0
            generos_en_string = ""
            while g < len(categorias):
                generos_en_string = generos_en_string + categorias[g]
                if g != len(categorias) - 1:
                    generos_en_string = generos_en_string + ", "
                g = g + 1

            conn.execute(
                """INSERT INTO ESTRENOS (TITULO, ENLACE, FECHA, GENEROS, PAIS) VALUES (?,?,?,?,?)""",
                (titulo, enlace, fecha, generos_en_string, pais))

    for c in categorias_diferentes:
        conn.execute("""INSERT INTO GENEROS (TITULO) VALUES (?)""", (c,));

    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM ESTRENOS")
    messagebox.showinfo("Base Datos",
                        "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()

def cargar_datos_bd():
    conn = sqlite3.connect('test.db')
    conn.text_factory = str  # para evitar problemas con el conjunto de caracteres que maneja la BD
    conn.execute("DROP TABLE IF EXISTS PELICULAS")
    conn.execute('''CREATE TABLE PELICULAS
         (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
         TITULO               TEXT NOT NULL,
         ENLACE              TEXT NOT NULL,
         FECHA                TEXT NOT NULL,
         GENERO        TEXT NOT NULL);''')


    peliculas = extraer_datos("https://www.elseptimoarte.net/estrenos")
    for pelicula in peliculas:
        url = "https://www.elseptimoarte.net/peliculas" + pelicula.h3.a.get('href')
        print(url)
        if pelicula.find('p', class_='generos').contents[0].find(",")!= -1:
            print(extraer_datos_de_una_pelicula(url))
        else:
            print(pelicula.find('p', class_='generos').contents[0])
            categorias_diferentes.add(pelicula.find('p', class_='generos').contents[0])




    for c in categorias_diferentes:
        conn.execute("""INSERT INTO GENEROS (TITULO) VALUES (?)""", (c,));

    conn.commit()


def buscar_por_fecha_bd():
    return False;


def buscar_por_genero_bd():
    master = Tk()
    conn = sqlite3.connect('test.db')
    generos = conn.execute("SELECT TITULO FROM GENEROS")

    res = list(map(lambda x: x[0], generos.fetchall()));

    w = Spinbox(master, values=res)
    w.pack()
    w.grid(row=0, column=0)
    buscar = Button(master, text="Buscar", command=lambda: show_data_by_genero(w.get()))
    buscar.grid(row=1, column=0)

    mainloop()

def show_data_by_genero(data):
    conn = sqlite3.connect('defensa.db')
    print('%'+data+'%')
    cursor = conn.execute("""SELECT TITULO,ENLACE, FECHA, GENEROS, PAIS FROM ESTRENOS WHERE GENEROS LIKE ?""",
                          ('%'+data+'%',))

    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        lb.insert(END, "Titulo: " + row[0])
        lb.insert(END, "Enlace: " + row[1])
        lb.insert(END, "Fecha de estreno: " + row[2])
        lb.insert(END, "Genero: " + row[3])
        lb.insert(END, "Pais: " + row[4])
        lb.insert(END, '')
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def buscar_por_pais_bd():
    def listar_busqueda(event):
        conn = sqlite3.connect('defensa.db')
        conn.text_factory = str
        s = "%"+en.get()+"%"
        cursor = conn.execute("""SELECT TITULO,ENLACE, FECHA, GENEROS, PAIS FROM ESTRENOS WHERE PAIS LIKE ?""",(s,)) # al ser de tipo string, el ? le pone comillas simples
        imprimir_etiqueta(cursor)
        conn.close()
    v = Toplevel()
    lb = Label(v, text="Introduzca el pais: ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)

def imprimir_etiqueta(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor.fetchall():
        lb.insert(END, "Titulo: " + row[0])
        lb.insert(END, "Enlace: " + row[1])
        lb.insert(END, "Fecha de estreno: " + row[2])
        lb.insert(END, "Genero: " + row[3])
        lb.insert(END, "Pais: " + row[4])
        lb.insert(END,'')
    lb.pack(side = LEFT, fill = BOTH)
    sc.config(command = lb.yview)




def ventana_principal():
    top = Tk()
    menubar = Menu(top)
    datosMenu = Menu(menubar, tearoff=0)
    datosMenu.add_command(label="Cargar", command=almacenar_bd)
    datosMenu.add_separator()
    datosMenu.add_command(label="Salir", command=top.quit)

    menubar.add_cascade(label="Datos", menu=datosMenu)

    buscarMenu = Menu(menubar, tearoff=0)
    buscarMenu.add_command(label="Fecha", command=buscar_por_fecha_bd)
    buscarMenu.add_command(label="Peliculas por genero", command=buscar_por_genero_bd)
    buscarMenu.add_command(label="País", command=buscar_por_pais_bd)

    menubar.add_cascade(label="Buscar", menu=buscarMenu)



    top.config(menu=menubar)
    top.mainloop()


if __name__ == "__main__":
    ventana_principal()