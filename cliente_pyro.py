#!/usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import Pyro4
import json
import ast
@Pyro4.expose

class cliente(object):
    def __init__(self):
        self.david = set()

def conexion():
    with Pyro4.locateNS() as ns:
        for david1, url in ns.list(prefix="example.conexion.").items():
            cone = Pyro4.Proxy(url)
            usuario = (raw_input("ingrese su usuario"))
            valida_usuario = (cone.validar(usuario))
            if valida_usuario == False:
                while valida_usuario == False:

                    pagina = (cone.menu_p)
                    lista = json.loads(pagina)
                    for i in lista:
                        print(ast.literal_eval(json.dumps(i)))

                    op = int(raw_input("Por favor ingrese una opcion: "))

                    if (op==1):
                        nombre_pagina=raw_input("Ingrese la pagina Web: ")
                        print(cone.agregar_pagina(nombre_pagina))

                    if (op==2):
                        pagina= (cone.listar_paginas)
                        lista=json.loads(pagina)
                        for i in lista:
                            print (ast.literal_eval(json.dumps(i)))

                    if (op==3):
                        nombre_pagina = raw_input("Ingrese la pagina Web: ")
                        print (cone.eliminar_pagina(nombre_pagina))

                    if (op==5):
                        pagina=(cone.ranking_paginas)
                        lista=json.loads(pagina)
                        for i in lista:
                            print (ast.literal_eval(json.dumps(i)))

                    if (op==6):
                        pagina=(cone.paginas_penalizada)
                        lista=json.loads(pagina)
                        for i in lista:
                            print (ast.literal_eval(json.dumps(i)))

                    if (op==7):
                        a = False
                        print("Gracias por utilizar nuestro servicio")

                    if (op==4):
                        a=True
                        while a==True:

                            print("-------------------------------------------")
                            print("\t\tPOSICIONAMIENTO DE PAGINAS WEB\t\t")
                            print("-------------------------------------------")
                            print("(1). Contar palabras")
                            print("(2). Diccionario de palabras claves")
                            print("(3). Contar imagenes")
                            print("(4). Contar enlaces internos y externos")
                            print("(5). Analizar URL")
                            print("(6). Analizar palabras claves")
                            print("(7). Redes sociales")
                            print("(8). Puntuacion extra")
                            print("(9). Estructura del sitio Web")
                            print("(10). Penalizar contenido no apto")
                            print("(11). Penalizacion pagina Web(Dudosa reputacion)")
                            print("(12). Penalizacion pagina Web(Malas practicas)")
                            print("(13). Librerias usadas")
                            print("(14). Comprobar enlaces externos")
                            print("(16). Salir")

                            op1= int(raw_input("Digite una opcion: "))

                            if (op1==1):
                                pagina=raw_input("Ingrese pagina Web:")
                                cadena="http://"+str(pagina)
                                print(cone.palabra(cadena))

                            if (op1==2):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://"+str(pagina)
                                a=(cone.diccionario(cadena))
                                for i in a:
                                    print (i)

                            if (op1==3):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://"+str(pagina)
                                print(cone.contar_imagen(cadena))

                            if (op1==4):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://"+str(pagina)
                                a=(cone.enlaces_inex(cadena)) #pagina_web
                                for i in a:
                                    print(i)

                            if (op1==5):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://"+str(pagina)
                                a=(cone.analisis(cadena))
                                for i in a:
                                    print (i)

                            if (op1==6):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://"+str(pagina)
                                print(cone.keywords(cadena))

                            if (op1 == 7):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://" + str(pagina)
                                a=(cone.redes(cadena))#redessociales
                                for i in a:
                                    print (i)

                            if (op1 == 8):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://" + str(pagina)
                                a=(cone.enlazar_pagina(cadena))#redessociales
                                print (a)

                            if (op1 == 9):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://" + str(pagina)
                                a=(cone.estructura_web(cadena))#redessociales
                                print (a)

                            if (op1 == 10):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://" + str(pagina)
                                a=(cone.penalizar_pagina(cadena))#redessociales
                                if a!=0:
                                    for i in a:
                                        #print (ast.literal_eval(json.dumps(i)))
                                        print (i)

                                else:
                                    print ("Pagina sin Penalizacion")




                            if (op1 == 11):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://" + str(pagina)
                                a=(cone.penalizapa_dudore(cadena))#redessociales
                                print (a)

                            if (op1 == 12):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://" + str(pagina)
                                a=(cone.penalizapa_malapractica(cadena))#redessociales
                                print (a)

                            if (op1 == 13):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://" + str(pagina)
                                a=(cone.libreria_usada(cadena))#redessociales
                                print (a)


                            if (op1 == 14):
                                pagina = raw_input("Ingrese pagina Web:")
                                cadena = "http://" + str(pagina)
                                a=(cone.comprobar_enlaces(cadena))#redessociales
                                print (a)




                            if (op1==16):
                                a=False
                                print ("Gracias por utilizar nuestro servicio")
            else:
                pagina = (cone.menu_admin)
                lista = json.loads(pagina)
                for i in lista:
                    print(ast.literal_eval(json.dumps(i)))
                    op = int(raw_input("Por favor ingrese una opcion: "))

                    if (op == 1):
                        nombre_empresa = raw_input("Ingrese el nombre de la empresa: ")
                        print(cone.agregar_empresa(nombre_empresa))
                    if (op == 2):
                        palabras_clave = raw_input("Ingrese las palabras claves: ")
                        print(cone.agregar_palabra(palabras_clave))

                    if (op == 3):
                        a = False
                        print("Gracias por utilizar nuestro servicio")



def main():
    dastie=cliente()
    dastie.david=conexion()


if __name__ == '__main__':
    main()
