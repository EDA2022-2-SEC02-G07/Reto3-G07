"""
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
from DISClib.DataStructures import mapentry as me
from tabulate  import tabulate
assert cf
from datetime import datetime

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar los videojuegos publicados en un rango de tiempo para una plataforma")
    print("3- Encontrar los 5 registros con menor tiempo para un jugador en específico")
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
    print("Juegos cargados:",str(lt.size(games)))
    print("Records de categoría cargados:",str(lt.size(category)))
    print(("Primeros y últimos 3 videojuegos cargados:"))
    print(tabulate(printable1,tablefmt="grid",maxcolwidths=13))
    print("Primeros y ultimos 3 registros cargados")
    print(tabulate(printable2,tablefmt="grid",maxcolwidths=13))
def printreq1(catalog,platform,date1,date2):
    size,list = controller.GamesByPlatform(catalog,platform,date1,date2)
    print("Juegos disponibles para",platform+":",str(size))
    print_list1 = [["Date","Count","Details"]]
    size_inrange = 0
    if lt.size(list) <= 6:
        for i in lt.iterator(list):
            size_inrange += lt.size(i)
            print_list2 = [["Abbreviation","Name","Platforms","Genres","Total_Runs"]]
            for e in lt.iterator(i):
                Date = e["Release_Date"]
                print_list2.append([e["Abbreviation"],e["Name"],e["Platforms"],e["Genres"],e["Total_Runs"]])
            print_list1.append([Date,lt.size(i),tabulate(print_list2,tablefmt="grid")])
    else:
        first = lt.subList(list,1,3)
        last = lt.subList(list,lt.size(list)-2,3)
        for i in lt.iterator(list):
            size_inrange += lt.size(i)
        for i in lt.iterator(first):
            print_list2 = [["Abbreviation","Name","Platforms","Genres","Total_Runs"]]
            for e in lt.iterator(i):
                Date = e["Release_Date"]
                print_list2.append([e["Abbreviation"],e["Name"],e["Platforms"],e["Genres"],e["Total_Runs"]])
            print_list1.append([Date,lt.size(i),tabulate(print_list2,tablefmt="grid")])
        for i in lt.iterator(last):
            print_list2 = [["Abbreviation","Name","Platforms","Genres","Total_Runs"]]
            for e in lt.iterator(i):
                Date = e["Release_Date"]
                print_list2.append([e["Abbreviation"],e["Name"],e["Platforms"],e["Genres"],e["Total_Runs"]])
            print_list1.append([Date,lt.size(i),tabulate(print_list2,tablefmt="grid")])
    print("Hay",str(size_inrange),"registros en el rango.")
    print(tabulate(print_list1,tablefmt="grid"))

def printreq2(catalog, player):
    mapdict, total_num_runs = controller.BestTimesByPlayer(catalog, player)
    print('\nEl jugador', player, 'tiene', total_num_runs, 'intentos de speedrun.\n')
    print(6*'-','Detalles del jugador',player, 6*'-')
    print('\nEl jugador', player, 'tiene el mejor tiempo de speedruns en', om.size(mapdict), 'registros\n')
    printlist = [['Time_0', 'Record_Date_0', 'Name', 'Players_0', 'Country_0', 'Num_Runs', 'Platforms', 'Genres', 'Category', 'Subcategory']]
    if lt.size(om.keySet(mapdict)) <= 5:
        for time in lt.iterator(om.keySet(mapdict)):
            printlist2 = []
            for value in lt.iterator(me.getValue(om.get(mapdict, time))):
                for title in printlist[0]:
                    if title != 'Name' and title != 'Platforms' and title != 'Genres':
                        if value[title] == '':
                            value[title] = 'Unknown'
                        printlist2.append(value[title])
                    else:
                        printlist2.append(catalog['model']['Id_'+title+'_Dict'][value['Game_Id']])
                printlist.append(printlist2)
        print(tabulate(printlist, tablefmt='grid'))

def printreq3(catalog,lo,lh):
    list = controller.BestTimesbyAttemptsRange(catalog,int(lo),int(lh))
    names = catalog["model"]["Id_Name_Dict"]
    print_list1 = [["Num_Runs","Count","Details"]]
    size = 0
    for i in lt.iterator(list):
        for e in lt.iterator(i):
            size += lt.size(e)
    if lt.size(list) <= 6:
        for i in lt.iterator(list):
            print_list2 = [["Name","Category","Subcategory","Num_Runs","Players_0","Country_0","Time_0","Record_Date_0"]]
            for e in lt.iterator(i):
                for r in lt.iterator(e):
                    xd = []
                    for a in print_list2[0]:
                        if a != "Name":
                            xd.append(r[a])
                        else:
                            xd.append(names[r["Game_Id"]])
                    print_list2.append(xd)
                runs = r["Num_Runs"]
            print_list1.append([runs,lt.size(i),tabulate(print_list2,tablefmt="grid",maxcolwidths=15)])
    else:
        first = lt.subList(list,1,3)
        last = lt.subList(list,lt.size(list)-2,3)
        for i in lt.iterator(first):
            print_list2 = [["Name","Category","Subcategory","Num_Runs","Players_0","Country_0","Time_0","Record_Date_0"]]
            for e in lt.iterator(i):
                for r in lt.iterator(e):
                    xd = []
                    for a in print_list2[0]:
                        if a != "Name":
                            xd.append(r[a])
                        else:
                            xd.append(names[r["Game_Id"]])
                    print_list2.append(xd)
                runs = r["Num_Runs"]
            print_list1.append([runs,lt.size(i),tabulate(print_list2,tablefmt="grid",maxcolwidths=15)])          
        for i in lt.iterator(last):
            print_list2 = [["Name","Category","Subcategory","Num_Runs","Players_0","Country_0","Time_0","Record_Date_0"]]
            for e in lt.iterator(i):
                for r in lt.iterator(e):
                    xd = []
                    for a in print_list2[0]:
                        if a != "Name":
                            xd.append(r[a])
                        else:
                            xd.append(names[r["Game_Id"]])
                    print_list2.append(xd)
                runs = r["Num_Runs"]
            print_list1.append([runs,lt.size(i),tabulate(print_list2,tablefmt="grid",maxcolwidths=15)])
    print("Hay",str(size),"registros en el rango.")
    print("Hay",str(lt.size(list)),"elementos en el rango.")
    print(tabulate(print_list1,tablefmt="grid"))

def printreq4(catalog, lo, hi):
    mapdict, size, times_list = controller.SlowestTimesByDateRange(catalog, lo, hi)
    names = catalog["model"]["Id_Name_Dict"]
    print('Registros más lentos en el rango de fechas:', lo, 'a', hi)
    print('Número de registros en el rango de fechas:', size)
    print_list = [['Time_0', 'Record_Date_0', 'Name', 'Category', 'Subcategory', 'Num_Runs', 'Players_0', 'Country_0']]
    first = lt.subList(times_list, 1, 3)
    last = lt.subList(times_list, lt.size(times_list)-2, 3)
    if lt.size(times_list) >= 6:
        for info in lt.iterator(first):
            for element in lt.iterator(info):
                for register in lt.iterator(element):
                    print_list_2 = []
                    for title in print_list[0]:
                        if title != 'Name':
                            print_list_2.append(register[title])
                        else:
                            print_list_2.append(names[register['Game_Id']])
                print_list.append(print_list_2)
        for info in lt.iterator(last):
            for element in lt.iterator(info):
                for register in lt.iterator(element):
                    print_list_2 = []
                    for title in print_list[0]:
                        if title != 'Name':
                            print_list_2.append(register[title])
                        else:
                            print_list_2.append(names[register['Game_Id']])
                print_list.append(print_list_2)
    else:
        for info in lt.iterator(times_list):
            for element in lt.iterator(info):
                for register in lt.iterator(element):
                    print_list_2 = []
                    for title in print_list[0]:
                        if title != 'Name':
                            print_list_2.append(register[title])
                        else:
                            print_list_2.append(names[register['Game_Id']])
                print_list.append(print_list_2)
    print(tabulate(print_list, tablefmt='grid'))

def printreq5(catalog,Tiempo_inferior,Tiempo_superior):
    lista = controller.RecentAttemptsbyRecordTimeRange(catalog,Tiempo_inferior,Tiempo_superior)
    print_list = [["Time_0","Count","Details"]]
    names = catalog["model"]["Id_Name_Dict"]
    platforms = catalog["model"]["Id_Platforms_Dict"]
    release_dates = catalog["model"]["Id_ReleaseDate_Dict"]
    genres = catalog["model"]["Id_Genres_Dict"]
    if lt.size(lista) <= 6:
        for i in lt.iterator(lista):
            print_list2 = [["Num_Runs","Record_Date_0","Name","Players_0","Country_0","Platforms","Genres","Category",
                                "Subcategory","Release_Date","Num_Runs"]]
            for e in lt.iterator(i):
                list = []
                for r in print_list2[0]:
                    if r not in ["Name","Platforms","Genres","Release_Date"]:
                        list.append(e[r])
                    elif r == "Name":
                        list.append(names[e["Game_Id"]])
                    elif r == "Platforms":
                        list.append(platforms[e["Game_Id"]])
                    elif r == "Genres":
                        list.append(genres[e["Game_Id"]])
                    elif r == "Release_Date":
                        list.append(release_dates[e["Game_Id"]])
                time = e["Time_0"]
                print_list2.append(list)
            print_list.append([time,lt.size(i),tabulate(print_list2,tablefmt="grid",maxcolwidths=15)])
    else:
        first = lt.subList(lista,1,3)
        last = lt.subList(lista,lt.size(lista)-2,3) 
        for i in lt.iterator(first):
            print_list2 = [["Num_Runs","Record_Date_0","Name","Players_0","Country_0","Platforms","Genres","Category",
                                "Subcategory","Release_Date","Num_Runs"]]
            for e in lt.iterator(i):
                list = []
                for r in print_list2[0]:
                    if r not in ["Name","Platforms","Genres","Release_Date"]:
                        list.append(e[r])
                    elif r == "Name":
                        list.append(names[e["Game_Id"]])
                    elif r == "Platforms":
                        list.append(platforms[e["Game_Id"]])
                    elif r == "Genres":
                        list.append(genres[e["Game_Id"]])
                    elif r == "Release_Date":
                        list.append(release_dates[e["Game_Id"]])
                time = e["Time_0"]
                print_list2.append(list)
            print_list.append([time,lt.size(i),tabulate(print_list2,tablefmt="grid",maxcolwidths=15)])
        for i in lt.iterator(last):
            print_list2 = [["Num_Runs","Record_Date_0","Name","Players_0","Country_0","Platforms","Genres","Category",
                                "Subcategory","Release_Date","Num_Runs"]]
            for e in lt.iterator(i):
                list = []
                for r in print_list2[0]:
                    if r not in ["Name","Platforms","Genres","Release_Date"]:
                        list.append(e[r])
                    elif r == "Name":
                        list.append(names[e["Game_Id"]])
                    elif r == "Platforms":
                        list.append(platforms[e["Game_Id"]])
                    elif r == "Genres":
                        list.append(genres[e["Game_Id"]])
                    elif r == "Release_Date":
                        list.append(release_dates[e["Game_Id"]])
                time = e["Time_0"]
                print_list2.append(list)
            print_list.append([time,lt.size(i),tabulate(print_list2,tablefmt="grid",maxcolwidths=15)])
    print(tabulate(print_list,tablefmt="grid"))

def printreq6(catalog,li,lo,N,criterio,x):
    min,max_,size,step,count_list = controller.HistogramofTimesbyYear(catalog,int(li),int(lo),int(N),criterio)
    print("Valor mas alto:",str(round(max_,2)))
    print("Valor más bajo:",str(round(min,2)))
    print("Hay",str(size),"registros.")
    print_table = [["bin","count","lvl","mark"]]
    for i in range(1,int(N)+1):
        lvl = int(lt.getElement(count_list,i)/int(x))
        print_table.append(["("+str(round(min,2))+","+str(round(min+step,2))+"]",lt.getElement(count_list,i),lvl,("*"*lvl)])
        min += step
    print(tabulate(print_table,tablefmt="grid"))
    print("Cada '*' representa",x,"registros.")

def printreq7(catalog,platform,N):
    list,size = controller.TopNRevenueGames(catalog,platform,int(N))
    print("Hay",str(size),"registros para",platform+".")
    print_list = [["Name","Release_Date","Platforms","Genres","Stream_Revenue","Market_Share","Time_Avg","Total_Runs"]]
    for i in lt.iterator(list):
        xd = []
        for e in print_list[0]:
          xd.append(i[e])
        print_list.append(xd)  
    print(tabulate(print_list,tablefmt="grid",maxcolwidths=15))

def printreq8(catalog, year, lo, hi):
    total = controller.recordsDistributionByCountry(catalog, year, lo, hi)
    print('Hay', total, 'registros de espeedrun en el año', year, 'dentro del rango de tiempos', lo, 'y', hi,'.')

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        if catalog == None:
            catalog = controller.newController()
        controller.loadData(catalog,size)
        print("Cargando información de los archivos ....")
        load(catalog)

    elif int(inputs[0]) == 2:
        platform = input("Ingrese la plataforma: ")
        date1 = input("Ingrese la primera fecha: ")
        date2 = input("Ingrese la segunda fecha: ")
        memory1 = controller.getMemory()
        time1 = controller.getTime()
        printreq1(catalog,platform,date1,date2)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria utilizada', deltamemory, 'KB.')

    elif int(inputs[0])==3:
        player = input('Ingrese el nombre del jugador:')
        memory1 = controller.getMemory()
        time1 = controller.getTime()
        printreq2(catalog, player)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')

    elif int(inputs[0]) == 4:
        lo = input("Ingrese el limite inferior: ")
        lh = input("Ingrese el limite superior: ")
        memory1 = controller.getMemory()
        time1 = controller.getTime()
        printreq3(catalog,lo,lh)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria utilizada', deltamemory, 'KB.')
    
    elif int(inputs[0]) == 5:
        lo = datetime.fromisoformat(input('Ingrese el límite inferior de la fecha:hora en que se obtuvo el record:'))
        hi = datetime.fromisoformat(input('Ingrese el límite superior de la fecha:hora en que se obtuvo el record:'))
        memory1 = controller.getMemory()
        time1 = controller.getTime()
        printreq4(catalog,lo,hi)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltamemory = controller.deltaMemory(memory2, memory1)
        deltatime = controller.deltaTime(time2, time1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria utilizada', deltamemory, 'KB.')

    elif int(inputs[0]) == 6:
        lo = input("Ingrese el tiempo inferior: ")
        lh = input("Ingrese el tiempo superior: ")
        memory1 = controller.getMemory()
        time1 = controller.getTime()
        printreq5(catalog,lo,lh)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria utilizada', deltamemory, 'KB.')

    elif int(inputs[0]) == 7:
        li = input("Ingrese el año inferior: ")
        lo = input("Ingrese el año superior: ")
        n = input("ingrese el numero de segmentos: ")
        x = input("Ingrese la división de las marcas: ")
        criterio = input('Ingrese el criterio ("Time_0","Time_1","Time_2","Time_Avg","Num_Runs"): ')
        memory1 = controller.getMemory()
        time1 = controller.getTime()
        printreq6(catalog,li,lo,n,criterio,x)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria utilizada', deltamemory, 'KB.')

    elif int(inputs[0]) == 8:
        platform = input("Ingrese la plataforma: ")
        N = input("Ingrese el numero N: ")
        memory1 = controller.getMemory()
        time1 = controller.getTime()
        printreq7(catalog,platform,N)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria utilizada', deltamemory, 'KB.')

    elif int(inputs[0]) == 9:
        year = input('Ingrese el año de lanzamiento:')
        lo = input('Ingrese el límite inferior del mejor tiempo record:')
        hi = input('Ingrese el límite superior del mejor tiempo record:')
        memory1 = controller.getMemory()
        time1 = controller.getTime()
        printreq8(catalog, year, lo, hi)
        time2 = controller.getTime()
        memory2 = controller.getMemory()
        deltatime = controller.deltaTime(time2, time1)
        deltamemory = controller.deltaMemory(memory2, memory1)
        print('Tiempo de ejecución:', str(deltatime), 'ms.')
        print('Memoria utilizada', deltamemory, 'KB.')
        
    else:
        sys.exit(0)
sys.exit(0)
