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

doc = "foro"


def open_url(url, file):
    urllib.request.urlretrieve(url, file)
    return file


def extract_data(url):
    fichero = "temas"
    if open_url(url,fichero):
        f = open(fichero, encoding="latin1")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser")

        temas = soup.findAll('div', "rating5 nonsticky")

        return temas


def extract_respuestas(url):
    fichero = "respuestas"
    if open_url(url, fichero):
        f = open(fichero, encoding="latin1")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser")

        res = soup.findAll('blockquote', "postcontent")

        return res


def parse_respuestas(texto):
    res = ""
    for text in texto:

        text = text.contents
        listToStr = ' '.join([str(elem) for elem in text])
        listToStr = listToStr.replace("<br/>", "")
        res += listToStr+", "

    return res;




def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return str1.join(s)


def datos_bd():
    if not os.path.exists(doc):
        os.mkdir(doc)

    ix = index.create_in(doc, schema=get_schema())
    writer = ix.writer()
    for i in range(1, 2):
        pagina = 'page' + str(i)
        print(i)
        if i != 1:
            url = "https://foros.derecho.com/foro/34-Derecho-Inmobiliario/" + pagina
            print(url)
            temas = extract_data(url)
        else:
            temas = extract_data("https://foros.derecho.com/foro/34-Derecho-Inmobiliario")

        for li in temas:

            titulo = li.find("a", "title").contents[0]
            link = "https://foros.derecho.com/tema/" + li.find("a", "title").get("href")
            autor = li.find("span", "label").find("a", "username").contents[0]
            fecha = li.find("span", "label").contents[2][2:12]
            respuestas = li.find("ul" , "threadstats td alt").find("a").contents[0]
            visitas = li.find("ul", "threadstats td alt").contents[3].contents[0][9:]

            respuestas_text = parse_respuestas(extract_respuestas(link))

            f = datetime.strptime(fecha, "%d/%m/%Y")
            print(f)
            writer.add_document(title=str(titulo), link=str(link), autor=str(autor), date=f,
                                respuestas=str(respuestas), visitas=str(visitas), respuestasText=str(respuestas_text))

    writer.commit()


def get_schema():
    return Schema(title=TEXT(stored=True), link=TEXT(stored=True), autor=TEXT(stored=True),
                  date=DATETIME(stored=True), respuestas=TEXT(stored=True), visitas=TEXT(stored=True),
                  respuestasText=TEXT(stored=True))


def filter_by_title():
    def listar(e):
        query = en.get()
        with ix.searcher() as searcher:
            query = QueryParser("title", ix.schema).parse(query)
            results = searcher.search(query)
            print_elements(results)

    ix = open_dir(doc)
    v = Toplevel()
    lb = Label(v, text="Introduzca una palabra clave: ")
    lb.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", listar)
    en.pack(side=LEFT)


def filter_by_autor():
    def listar(e):
        query = en.get()
        with ix.searcher() as searcher:
            query = QueryParser("autor", ix.schema).parse(query)
            results = searcher.search(query)
            print_elements(results)

    ix = open_dir(doc)
    v = Toplevel()
    lb = Label(v, text="Introduzca una palabra clave: ")
    lb.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", listar)
    en.pack(side=LEFT)


def filter_by_respuestas():
    def listar(e):
        query = en.get()
        with ix.searcher() as searcher:
            query = QueryParser("respuestasText", ix.schema).parse(query)
            results = searcher.search(query)
            print_elements_respuestas(results)

    ix = open_dir(doc)
    v = Toplevel()
    lb = Label(v, text="Introduzca una palabra clave: ")
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
        lb.insert(END, "Link: "+row['link'])
        lb.insert(END, "Fecha: "+str(row['date'])[:11])
        lb.insert(END, "Autor: " + row['autor'])
        lb.insert(END, "Respuestas: " + row['respuestas'])
        lb.insert(END, "Visitas: " + row['visitas'])
        lb.insert(END, '')

    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def print_elements_respuestas(elements):

    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in elements:
        lb.insert(END, "Titulo: " + row['title'])
        lb.insert(END, "Link: " + row['link'])
        lb.insert(END, "Fecha: " + str(row['date'])[:11])
        lb.insert(END, "Autor: " + row['autor'])
        repuestas = row["respuestasText"].parse(',')
        for res in repuestas:
            lb.insert(END, res)
            lb.insert(END, "")
        lb.insert(END, '')

    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def ventana_principal():

    top = Tk()
    menu = Menu(top)
    datos_menu = Menu(menu, tearoff=0)
    datos_menu.add_command(label="Indexar", command=datos_bd)
    datos_menu.add_separator()
    datos_menu.add_command(label="Salir", command=top.quit)

    menu.add_cascade(label="Inicio", menu=datos_menu)

    buscar_menu = Menu(menu, tearoff=0)

    temas_menu = Menu(menu, tearoff=0)
    temas_menu.add_command(label="Titulo", command=filter_by_title)
    temas_menu.add_command(label="Autor", command=filter_by_autor)

    repuestas_menu = Menu(menu, tearoff=0)
    repuestas_menu.add_command(label="Texto", command=filter_by_respuestas)

    buscar_menu.add_cascade(label="Temas", menu=temas_menu)
    buscar_menu.add_cascade(label="Respuestas", menu=repuestas_menu)

    menu.add_cascade(label="Buscar", menu=buscar_menu)

    top.config(menu=menu)
    top.mainloop()


if __name__ == "__main__":

    ventana_principal()
