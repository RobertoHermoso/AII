# encoding:utf-8
from tkinter import *
import urllib.request, re
from bs4 import BeautifulSoup
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser
import os, os.path
from whoosh import index
from datetime import datetime, timedelta
from tkinter import messagebox
from whoosh.qparser.dateparse import DateParserPlugin

doc = "events"

categoriasTotales = set()

def open_url(url, file):
    urllib.request.urlretrieve(url, file)
    return file


def extract_data(url):
    fichero = "eventos"
    if open_url(url,fichero):
        f = open(fichero, encoding="utf-8")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser")

        temas = soup.findAll('article', "vevent tileItem")

        return temas


def datos_bd():
    if not os.path.exists(doc):
        os.mkdir(doc)

    ix = index.create_in(doc, schema=get_schema())
    writer = ix.writer()
    eventos = extract_data("https://www.sevilla.org/ayuntamiento/alcaldia/comunicacion/calendario/agenda-actividades")
    cont = 0
    for li in eventos:
        titulo = li.find("span", "summary").text

        if li.find('p', class_="description") is not None:
            description = li.find('p', class_="description").text
        else:
            description = "None"

            # SCRAPING CATEGORIAS, EL ATRIBUTO A GUARDAR ES categorias
        lista_categorias = li.find('li', class_="category")
        categorias = ""
        if lista_categorias is not None:
            cat = lista_categorias.find_all('span')
            for c in cat:
                categ = str(c.text)
                categoriasTotales.add(categ)
                if c == cat[-1]:
                    categorias = categorias + c.text
                else:
                    categorias = categorias + c.text + ", "
        else:
            categorias = "None"


        try:
            dtstart = li.find("abbr","dtstart").get("title")
            fecha1 = datetime.fromisoformat(dtstart)
        except:
            fecha = li.find("div","documentByLine").contents[0].strip()
            fecha1 = datetime.strptime(fecha,'%d/%m/%Y')
        try:
            dtend = li.find("abbr","dtend").get("title")
            fecha2 = datetime.fromisoformat(dtend);
        except:
            fecha2 = None

        writer.add_document(titulo=str(titulo), fechaInicio=fecha1, fechaFin=fecha2,
                            descripcion=str(description), categorias=str(categorias))
        cont = cont + 1
    writer.commit()
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(cont)+ " noticias")


def get_schema():
    return Schema(titulo=TEXT(stored=True), fechaInicio=DATETIME(stored=True), fechaFin=DATETIME(stored=True),
                  descripcion=TEXT(stored=True), categorias=TEXT(stored=True))


def buscar_cateogria():
    def listar(e):
        query = w.get()
        with ix.searcher() as searcher:
            query = QueryParser("categorias", ix.schema, group=qparser.OrGroup).parse(query)
            results = searcher.search(query)
            print_elements(results)
    ix = open_dir(doc)
    v = Toplevel()
    w = Spinbox(v, values=list(categoriasTotales))
    w.pack()
    w.grid(row=0, column=0)
    buscar = Button(v, text="Buscar", command=lambda: listar(w.get()))
    buscar.grid(row=1, column=0)

    mainloop()


def print_elements(elements):

    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in elements:
        lb.insert(END, "Titulo: "+row['titulo'])
        lb.insert(END, "Descripción: "+row['descripcion'])
        lb.insert(END, "Fechas: " + str(row['fechaInicio']) + " - "+ str(row['fechaFin']))
        lb.insert(END, "Categorías: " + row['categorias'])

        lb.insert(END, '')

    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def busqueda_titulo_descripcion():
    def mostrar_lista(event):
        lb.delete(0,END)
        ix=open_dir(doc)
        with ix.searcher() as searcher:
            entry = str(en.get()).split()
            query = str(en.get())
            for e in entry:
                query = query + ' titulo:' + e.strip()
            query = QueryParser('descripcion', ix.schema, group=qparser.AndGroup).parse(query)
            results = searcher.search(query)
            for r in results:
                lb.insert(END,r['titulo'])
                lb.insert(END,r['fechaInicio'])
                lb.insert(END,r['fechaFin'])
                lb.insert(END,'')

    v = Toplevel()
    v.title("Busqueda por título y descripción")
    f = Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca una o varias palabras:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview)



def search_date(entry):
    ix = index.open_dir("events")
    tk = Tk()
    scrollbar = Scrollbar(tk, orient="vertical")
    lb = Listbox(tk, width=50, height=20, yscrollcommand=scrollbar.set)
    scrollbar.config(command=lb.yview)

    scrollbar.pack(side="right", fill="y")
    lb.pack(side="left", fill="both", expand=True)
    date = str(entry)
    myquery = "date:<= " + date
    print("Myquery " + myquery)
    qp = QueryParser('fechaInicio', ix.schema)
    qp.add_plugin(DateParserPlugin())

    t = qp.parse(u"date:"+date)
    print(t)
    with ix.searcher() as s:
        results_t = s.search(t, limit=None)
        for r in results_t:
            lb.insert(END, "Categorias: " + r["categorias"], "Título: " + r["titulo"], "Fecha: " + r["fechaInicio"], "")

    tk.mainloop()

def w_date_search():
    window = Tk()
    lbl = Label(window, text="Fecha: ").grid(row=0)

    e1 = Entry(window)
    e1.grid(row=0, column=1)
    e1.insert(0, 'dd/mm/yyyy')
    btn1 = Button(window, text='Show', command=lambda: search_date(e1.get())).grid(row=3, column=0, sticky=W, pady=4)
    btn2 = Button(window, text='Quit', command=window.quit).grid(row=3, column=1, sticky=W, pady=4)

    window.mainloop()

def ventana_principal():

    top = Tk()
    menu = Menu(top)
    datos_menu = Menu(menu, tearoff=0)
    datos_menu.add_command(label="Cargar", command=datos_bd)
    datos_menu.add_separator()
    datos_menu.add_command(label="Salir", command=top.quit)

    menu.add_cascade(label="Datos", menu=datos_menu)

    buscar_menu = Menu(menu, tearoff=0)
    buscar_menu.add_command(label="Titulo y descripción", command=busqueda_titulo_descripcion)
    buscar_menu.add_command(label="Fecha", command=w_date_search)
    buscar_menu.add_command(label="Categoría", command=buscar_cateogria)

    menu.add_cascade(label="Buscar", menu=buscar_menu)

    top.config(menu=menu)
    top.mainloop()


if __name__ == "__main__":

    ventana_principal()
