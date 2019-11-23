# encoding:utf-8
import urllib.request, re
from tkinter import *
from bs4 import BeautifulSoup
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser
import os, os.path
from whoosh import index
from datetime import datetime, timedelta


doc = "Docs/news"


def open_url(url, file):
    urllib.request.urlretrieve(url, file)
    return file


def extract_data(url):
    fichero = "noticias"
    if open_url(url,fichero):
        f = open(fichero, encoding="utf-8")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser")

        temas = soup.findAll('div', "news-card")

        return temas


def extract_date(url):
    fichero = "date"
    if open_url(url, fichero):
        f = open(fichero, encoding="utf-8")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser")

        date = soup.find('span', class_="titlebar-subtile-txt").contents[2][3:13]

        return date


def extract_description(url):
    fichero = "description"
    if open_url(url, fichero):
        f = open(fichero, encoding="utf-8")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser")

        description = soup.find('p', class_="article-lead").contents[0]

        return description


def datos_bd():
    if not os.path.exists(doc):
        os.mkdir(doc)

    ix = index.create_in(doc, schema=get_schema())
    writer = ix.writer()
    for i in range(1, 2):
        pagina = '?page=' + str(i)
        print(i)
        if i != 1:
            url = "http://www.sensacine.com/peliculas/noticias/" + pagina
            print(url)
            temas = extract_data(url)
        else:
            temas = extract_data("http://www.sensacine.com/peliculas/noticias")

        for li in temas:
            category = li.find("div", "meta-category").text[11:]
            title = li.find("a", "meta-title-link").text
            url = "http://www.sensacine.com" + li.find("a", "meta-title-link").get("href")
            fecha = extract_date(url)
            fecha = fecha.strip()
            description = extract_description(url)
            image_url = li.find("img", "thumbnail-img").get("src")
            if 'gif' in image_url:
                image_url = li.find("img", "thumbnail-img").get("data-src")

            f = datetime.strptime(fecha, "%d/%m/%Y")
            print(f)
            writer.add_document(title=str(title), category=str(category), image=str(image_url), date=f,
                                description=str(description))

    writer.commit()


def get_schema():
    return Schema(title=TEXT(stored=True), category=TEXT(stored=True), image=TEXT(stored=True),
                  date=DATETIME(stored=True), description=TEXT(stored=True))


def filter_by_name_description():
    def listar(e):
        query = en.get()
        with ix.searcher() as searcher:
            query = MultifieldParser(["title", "description"], ix.schema, group=qparser.AndGroup).parse(query)
            results = searcher.search(query)
            print_elements(results)

    ix = open_dir(doc)
    v = Toplevel()
    lb = Label(v, text="Introduzca una palabra clave: ")
    lb.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", listar)
    en.pack(side=LEFT)


def filter_by_date():
    def listar(e):
        f = datetime.strptime(en.get(), "%d/%m/%Y")
        query = f.strftime('%Y%m%d')
        with ix.searcher() as searcher:
            query = QueryParser("date", ix.schema).parse(query)
            results = searcher.search(query)
            print_elements(results)

    ix = open_dir(doc)
    v = Toplevel()
    lb = Label(v, text="Introduzca una fecha DD/MM/AAAA: ")
    lb.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", listar)
    en.pack(side=LEFT)


def print_elements(elements):

    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in elements:
        lb.insert(END, "Titulo: "+row['title'])
        lb.insert(END, "Descripción: "+row['description'])
        lb.insert(END, "Fecha: "+str(row['date'])[:11])
        lb.insert(END, "Categoría: " + row['category'])
        lb.insert(END, "Imagen: " + row['image'])
        lb.insert(END, '')

    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def filter_by_description():
        def listar(e):
            query = en.get()
            with ix.searcher() as searcher:
                query = QueryParser("description", ix.schema).parse(query)
                results = searcher.search(query)
                print_elements(results)

        ix = open_dir(doc)
        v = Toplevel()
        lb = Label(v, text="Introduzca una palabra clave: ")
        lb.pack(side=LEFT)
        en = Entry(v)
        en.bind("<Return>", listar)
        en.pack(side=LEFT)


def ventana_principal():

    top = Tk()
    menu = Menu(top)
    datos_menu = Menu(menu, tearoff=0)
    datos_menu.add_command(label="Cargar", command=datos_bd)
    datos_menu.add_separator()
    datos_menu.add_command(label="Salir", command=top.quit)

    menu.add_cascade(label="Datos", menu=datos_menu)

    buscar_menu = Menu(menu, tearoff=0)
    buscar_menu.add_command(label="Titulo y descripción", command=filter_by_name_description)
    buscar_menu.add_command(label="Fecha", command=filter_by_date)
    buscar_menu.add_command(label="Descripción", command=filter_by_description)

    menu.add_cascade(label="Buscar", menu=buscar_menu)

    top.config(menu=menu)
    top.mainloop()


if __name__ == "__main__":

    ventana_principal()
