﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from tabulate  import tabulate
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Reportar los 5 videojuegos más recientes de una plataforma")
    print("3- Reportar los registros más veloces de los mejores tiempos de un jugador en específico")
    print("4- Reportar los registros más veloces dentro de un rango de intentos")
    print("5- Reportar los registros más lentos dentro de un rango de fechas")
    print("6- Reportar los registros más recientes en un rango de tiempos récord")
    print("7- Diagramar el histograma de tiempos para un año de publicación")
    print("8- Encontrar los 5 videojuegos más rentables para retransmitir")
    print("9- Mostrar la distribución de récords por país en un año de publicación en un rango de tiempos")
    print("0- Salir")

catalog = None
size = "-small"
"""
Menu principal
"""
def load(catalog):
    printable1 = [["Game_Id","Release_Date","Name","Abbreviation","Platforms","Total_Runs","Genres"]]
    printable2 = [["Game_Id","Record_Date_0","Num_Runs","Name","Category","Subcategory","Country_0","Players_0","Time_0"]]
    games = catalog["model"]["GamesList"]
    first_games = lt.subList(games,1,3)
    last_games = lt.subList(games,lt.size(games)-2,3)
    category = catalog["model"]["CategoryList"]
    first_category = lt.subList(category,1,3)
    last_category = lt.subList(category,lt.size(category)-2,3)
    for i in (lt.iterator(first_games)):
        app = []
        for e in printable1[0]:
            app.append(i[e])
        printable1.append(app)
    for i in (lt.iterator(last_games)):
        app = []
        for e in printable1[0]:
            app.append(i[e])
        printable1.append(app)
    for i in (lt.iterator(first_category)):
        app = []
        for e in printable2[0]:
            if e != "Name":
                app.append(i[e])
            else:
                app.append(catalog["model"]["Id_Name_Dict"][i["Game_Id"]])
        printable2.append(app)
    for i in (lt.iterator(last_category)):
        app = []
        for e in printable2[0]:
            if e != "Name":
                app.append(i[e])
            else:
                app.append(catalog["model"]["Id_Name_Dict"][i["Game_Id"]])
        printable2.append(app)
    print(("Primeros y últimos 3 videojuegos cargados:"))
    print(tabulate(printable1,tablefmt="grid",maxcolwidths=13))
    print("Primeros y ultimos 3 registros cargados")
    print(tabulate(printable2,tablefmt="grid",maxcolwidths=13))
def printreq1(catalog,platform,date1,date2):
    size,list = controller.GamesByPlatform(catalog,platform,date1,date2)
    print("Juegos disponibles para",platform+":",str(size))
    for i in lt.iterator(list):
        print(i)
def printreq2(catalog):
    pass

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        catalog = controller.newController()
        controller.loadData(catalog,size)
        print("Cargando información de los archivos ....")
        load(catalog)

    elif int(inputs[0]) == 2:
        platform = input("Ingrese la plataforma: ")
        date1 = input("Ingrese la primera fecha: ")
        date2 = input("Ingrese la segunda fecha: ")
        printreq1(catalog,platform,date1,date2)

    elif int(inputs[0])==3:
        printreq2(catalog)

    else:
        sys.exit(0)
sys.exit(0)
