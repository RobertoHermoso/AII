#encoding: utf-8

import urllib.request, re
import os.path



def extraer_lista(file):
    f = open (file, "r",encoding='utf-8')
    s = f.read()
    l = re.findall(r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>.*</description>\s*<author>.*</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>', s)
    f.close()
    return l

def imprimir_lista(l):
    for t in l:
        print ("Título:", str(t[0]))
        print ("Link:", t[1])
        f=formatear_fecha(t[3])
        print ("Fecha: {0:2s}/{1:2s}/{2:4s}\n".format(f[0],f[1],f[2]))
 

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
        print  ("Error al conectarse a la página")
        return None

def buscar_fecha(l):
    mes = input("Introduzca el mes (mm):")
    enc=False
    for t in l:
        f =formatear_fecha(t[3])
        if mes == f[1]:
            print ("Título:", str(t[0]))
            print ("Link:", t[1])
            print ("Fecha: {0:2s}/{1:2s}/{2:4s}\n".format(f[0],f[1],f[2]))
            enc = True
    if not enc:
        print ("No hay noticias para ese mes")
        
def formatear_fecha(s):
    meses={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    fecha = re.match(r'.*(\d\d)\s*(.{3})\s*(\d{4}).*', s)
    l = list(fecha.groups())
    l[1] = meses[l[1]]
    return tuple(l)

if __name__ == "__main__":
    fichero="noticias"
    if abrir_url("http://www.us.es/rss/feed/portada",fichero):
        l=extraer_lista(fichero)
    if l:
        imprimir_lista(l)
        buscar_fecha(l)

