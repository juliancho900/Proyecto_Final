#!/usr/bin/python
#-*- coding: utf-8 -*-


from __future__ import print_function
import Pyro4
from bs4 import BeautifulSoup
import bs4 as bs
from requests import get
import json
import MySQLdb
etiquetas_imagenes= list()
import mysql.connector
import string
import re
import ast

HOST = '30.10.1.84'
USER = 'root'
PASSWORD = ''
DATABASE = 'final_sp'

#from bs4 import BeautifulSoup
#from requests import get
#etiquetas_imagenes=list

@Pyro4.expose
class conexion():
    @Pyro4.expose
    def validar(self,usuario):
        if usuario == "Administrador":
            return (True)
        else:
            return (False)

    @property
    def menu_p(self):
        lista = [
            "\n1. Agregar pagina \n2. Listar pagina \n3. Eliminar pagina \n4. Informacion SEO \n5. Ranking \n6. Listado de paginas Penalizadas\n7. Salir"]
        cadena = json.dumps(lista)
        return cadena

    @property
    def menu_admin(self):
        lista = [
            "\n1. Agregar Empresa \n2. Agregar Palabras Claves \n3. Salir"]
        cadena = json.dumps(lista)
        return cadena

    @property
    def conectar(self):
        try:
            conexion = mysql.connector.connect(host=HOST,
                                               database=DATABASE,
                                               user=USER,
                                               password=PASSWORD)
            cursor = conexion.cursor()
            if cursor:
                return "Conexion con exito"
        except mysql.connector.Error as e:
            return e


    def run_query(self, query):
        conexion = (HOST, USER, PASSWORD, DATABASE)

        conn = MySQLdb.connect(*conexion)
        cursor = conn.cursor()
        cursor.execute(query)

        if query.upper().startswith('SELECT'):
            data = cursor.fetchall()
        else:
            conn.commit()
            data = None

        cursor.close()
        conn.close()

        return data

    @Pyro4.expose
    def agregar_pagina(self, pagina):
        # pass #insertar Datos
        query = "INSERT INTO pag_web (pagina) VALUES ('%s')" %(pagina)
        self.run_query(query)
        return "Pagina Web Adicionada Satisfactoriamente"

    @property
    def listar_paginas(self):
        # Listar Datos
        query = "SELECT * FROM pag_web "
        result = self.run_query(query)
        cadena = json.dumps(result)
        return cadena

    @Pyro4.expose
    def eliminar_pagina(self, pagina):
        query = "DELETE FROM pag_web WHERE pagina =  '%s'" % (pagina)
        self.run_query(query)
        return "Pagina Web Eliminada Satisfactoriamente"






    def contar_enlaces(self,pagina):
        enlaces=pagina.find_all('a')
        i=0
        for enlace in enlaces:
            i += 1
        print ("La cantidad de enlaces que tiene la pagina " + str(URL) + " es: " + str(i))



    @Pyro4.expose
    def contar_imagen(self, URL):
        # URL = 'http://www.eltiempo.com/'  # Direccion de la pag Web
        recurso = get(URL)  # Captura el codigo # Conexion puerto
        pagina = BeautifulSoup(recurso.text, 'html.parser')
        enlaces = pagina.find_all('img')
        for enlace in enlaces:
            etiquetas = enlace.get('alt')
            if (etiquetas != None and etiquetas != ""):
                etiquetas_imagenes.append(etiquetas.upper())
        # for imagenes in etiquetas_imagenes:
        imagenes=(len(etiquetas_imagenes))
        return " la cantidad de imagenes de la pagina  " + str(URL) + " es: " + str(imagenes)


    @Pyro4.expose
    def comprobar_enlaces(self, pagina):
        url = pagina
        lista=["enlaces de la pagina"]
        recurso = get(url)
        pagina = BeautifulSoup(recurso.text, 'html.parser')
        links = (pagina.find_all(href = re.compile("http[s]?://www.")))
        for i in links:
            lista +=[i.get('href')]
        return lista



    def pag_web(self,URL):
        try:
            recurso=get(URL)
            if (recurso.status_code==200):
                pagina=BeautifulSoup((recurso.text),'html.parser')
                a=self.contar_enlaces(pagina)
                return "La cantidad de enlaces que posee la pagina"+str(URL)+"es:"+str(a)
        except:
            return "El recurso solicitado no existe"


    @Pyro4.expose
    def palabra(self,URL):
        recurso = get(URL)
        texto = BeautifulSoup(recurso.text, 'html.parser').get_text()
        palabrasArray = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto).split()
        numero = 0
        for i in sorted(set(palabrasArray)):
            if (i.isalpha() == True):
                numero += 1
        return " la cantidad de palabras de la pagina  " + str(URL) + " es: " + str(numero)


    @Pyro4.expose
    def redes(self,URL):
        recurso=get(URL)
        texto=BeautifulSoup(recurso.text,'html.parser').get_text()
        palabrasArray=re.sub('[%s]'%re.escape(string.punctuation),'',texto).split()
        Redes=["Redes Sociales:"]
        lista=["Instagram","Facebook","Twitter","Youtube"]
        for i in sorted(set(palabrasArray)):
            if (i.isalpha()==True):
                for j in range(len(lista)):
                    if i==lista[j]:
                        Redes+=[i]
        return (Redes)



    @Pyro4.expose
    def enlaces_inex(self,pagina):
        lista=[]
        url=pagina
        recurso=get(url)
        pagina=BeautifulSoup(recurso.text,'html.parser')
        cont=0
        conte=0
        links=pagina.find_all('a',attrs={'href':re.compile("http[s]?://www.")})
        for i in links:
            cont+=1
            print (i)

        lista=["La cantidad de enlaces Externos que posee la pagina"+str(url)+"es:"+str(cont)]
        links1=pagina.find_all('a',attrs={'href':re.compile("#")})
        for i in links1:
            conte+=1
            print (i)
        lista.append("La cantidad de enlaces Internos que posee la pagina"+str(url)+"es:"+str(conte))
        return (lista)


    @Pyro4.expose
    def diccionario(self, URL):
        lista = ["Tecnologia","Avances","Nuevo","Actualizacion","Software","Hardware","Sistemas","Ios","Android","Virus","AMD"]
        recurso = get(URL)
        texto = BeautifulSoup(recurso.text, 'html.parser').get_text()
        palabrasArray = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto).split()
        cla=["Palabras que coinciden:"]
        for i in sorted(set(palabrasArray)):
            if (i.isalpha()==True):
                for j in range(len(lista)):

                    if (i==lista[j]):
                        cla.append(str(lista[j]))
                    else:
                        cla.append("No hay coincidencia")
        return (cla)


    @Pyro4.expose
    def analisis(self,URL):
        recurso=get(URL)
        pagina=BeautifulSoup(recurso.text,'html.parser')

                #titulo=(pagina.tittle)

        meta_descripcion=pagina.findAll(attrs={"name":"description"})
        descripcion=meta_descripcion[0]['content'].encode('utf-8')

        meta_a=pagina.findAll(attrs={"name":"author"})
        autor=meta_a[0]['content'].encode('utf-8')

        ing_clave=pagina.findAll(attrs={"name":"keywords"})
        password=ing_clave[0]['content'].encode('utf-8')

        imagen=self.contar_imagen(URL)
        externos=self.enlaces_inex(URL)

        #a=("Titulo:"+str(titulo))
        b=("Descripcion de pagina"+descripcion)
        c=("Palabras claves"+password)
        d=("Hemos encontrado"+str(imagen)+"imagenes en la pagina")
        #e=("Enlaces: Internos - Externos"+str(externos))
        g=("Autor:"+autor)
        lista=[g,b,c]

        return (lista)
                #return ("Ya")


    @Pyro4.expose
    def keywords(self,URL):
        recurso=get(URL)
        if (recurso.status_code==200):
            pagina=BeautifulSoup(recurso.text,'html.parser')
            ing_clave=pagina.findAll(attrs={"name":"keywords"})
            clave=ing_clave[0]['content'].encode('utf-8')
            password=("Palabras claves"+clave)
            return (password)



    @Pyro4.expose
    def enlazar_pagina(self,URL):
        lista="HTTP://WWW.APPLESFERA.COM"
        recurso = get(URL)  # Captura el codigo # Conexion puerto
        pagina = BeautifulSoup(recurso.text, 'html.parser')
        enlaces = pagina.find_all('a')
        for enlace in enlaces:
            etiquetas = enlace.get('href')
            if (etiquetas != None and etiquetas != ""):
                etiquetas_imagenes.append(etiquetas.upper())

        for i in etiquetas_imagenes:
            if (i==lista):
                return ("Puntuacion extra obtenida(Pagina guardada)")
            else:
                return ("No hay Puntuacion)")



    @Pyro4.expose
    def penalizar_pagina(self,URL):
        query = "SELECT (pagina_no_apta) FROM no_apta"
        result = self.run_query(query)
        cadena = json.dumps(result)
        lista_1 = []
        lista_2 = []

        recurso = get(URL)
        texto = BeautifulSoup(recurso.text, 'html.parser').get_text()

        # Remplazo todos los caracteres ASCII de puntuacion por espacios e inicializa el Array
        palabrasArray = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto).split()
        claves = ["Pagina web: " + str(URL) + " Penalizada (Contenido No Apto): "]
        # Ordenacion sin repeticion de todos los elementos del Array
        for i in sorted(set(palabrasArray)):
            # Imprime solo las palabras con caracteres alfabeticos.
            if (i.isalpha() == True):
                lista_1 += [i]

        lista = json.loads(cadena)
        for i in lista:
            lista_2 += (ast.literal_eval(json.dumps(i)))
        con = 0
        for j in lista_1:
            for i in range(len(lista_2)):
                # print (lista_2[i])
                if (lista_2[i] == j):
                    claves += [j]
                    con += 1

        if con > 0:
            query = "INSERT INTO no_apta(pagina_no_apta)VALUES('%s')" % (URL)
            self.run_query(query)

            return (claves)
        else:
            return (0)


    @Pyro4.expose
    def analizar_enlaces(self,pagina):
        url=pagina
        lista=["Enlaces Externos"]
        recurso=get(url)
        pagina=BeautifulSoup(recurso.text,'html.parser')

        for link in pagina.find_all(href=re.compile("http[s]?://")):
            lista+=[link.get('href')]
        return (lista)


    @property
    def paginas_penalizada(self):
        query ="SELECT * FROM no_apta"
        resultado=self.run_query(query)
        cadena=json.dumps(resultado)
        return cadena


    @Pyro4.expose
    def posicionamiento(self,redes_sociales,imagenes,enlace_int,enlace_ext,palabra_clave,pag_apta,pag_url):
        query="INSERT INTO posicionamiento(redes_sociales,imagenes,enlace_int,enlace_ext,palabra_clave,pag_apta,pag_url)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',)"%(redes_sociales,imagenes,enlace_int,enlace_ext,palabra_clave,pag_apta,pag_url)
        self.run_query(query)
        return ("La pagina Web ha sido añadida satisfactoriamente")

    @Pyro4.expose
    def agregar_empresa(self, empresa):
        # pass #insertar Datos
        query = "INSERT INTO reg_empresa (empresa) VALUES ('%s')" % (empresa)
        self.run_query(query)
        return "Empresa Adicionada Satisfactoriamente"

    def agregar_palabra(self, pal_clave):
        # pass #insertar Datos
        query = "INSERT INTO palabra_clave (pal_clave) VALUES ('%s')" % (pal_clave)
        self.run_query(query)
        return "Palabra Adicionada Satisfactoriamente"


def main():
    david = conexion()
    HOST_IP="30.10.1.132"
    HOST_PORT=9092
    with Pyro4.Daemon(host=HOST_IP, port=HOST_PORT) as daemon:
        uri=daemon.register(david)
        print (uri)
        with Pyro4.locateNS() as ns:
            ns.register("example.conexion.David", uri)
        print ("Conexion exitosa")
        daemon.requestLoop()


if __name__ == '__main__':
    main()