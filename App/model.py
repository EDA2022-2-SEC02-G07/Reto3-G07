"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {"GamesList":lt.newList("ARRAY_LIST"),
                "CategoryList":lt.newList("ARRAY_LIST"),
                "Id_Name_Dict" : {},
                "MapByPlatform":mp.newMap(),
                'MapByPlayers':mp.newMap()}
    return catalog
# Funciones para agregar informacion al catalogo
def add_contentCategory(catalog, content):
    players = lt.newList('ARRAY_LIST')
    for player1 in content['Players_0']:
        player1 = player1.strip()
        if mp.contains(catalog['MapByPlayers'], player1) == False:
            mp.put(catalog['MapByPlayers'], player1, om.newMap(omaptype='RBT'))
    for player2 in content['Players_1']:
        player2 = player2.strip()
        if mp.contains(catalog['MapByPlayers'], player2) == False:
            mp.put(catalog['MapByPlayers'], player2, om.newMap(omaptype='RBT'))
    for player3 in content['Players_2']:
        player3 = player3.strip()
        if mp.contains(catalog['MapByPlayers'], player3) == False:
            mp.put(catalog['MapByPlayers'], player3, om.newMap(omaptype='RBT'))
    lt.addLast(catalog['CategoryList'], content)
    #content['Players_0']
    #for player in content['']
    #Mapa ordendo por jugadores con árboles como valores.

def add_contentGames(catalog, content):
    for platform in content["Platforms"].split(","):
        platform = platform.strip()
        if mp.contains(catalog["MapByPlatform"],platform) == False:
            mp.put(catalog["MapByPlatform"],platform,{"map":om.newMap(omaptype="RBT"),"size":0})
        map_dict = me.getValue(mp.get(catalog["MapByPlatform"],platform))
        if om.contains(map_dict["map"],content["Release_Date"]) == False:
            om.put(map_dict["map"],content["Release_Date"],lt.newList("ARRAY_LIST"))
        lt.addLast(me.getValue(om.get(map_dict["map"],content["Release_Date"])),content["Release_Date"])
        map_dict["size"] += 1
    lt.addLast(catalog["GamesList"],content)
    catalog["Id_Name_Dict"][content["Game_Id"]] = content["Name"]
    

# Funciones para creacion de datos

# Funciones de consulta
def GamesByPlatform(catalog,platform,date1,date2): #Función Pricipal Requerimiento 1
    platformMapDict = me.getValue(mp.get(catalog["MapByPlatform"],platform))
    datesList = om.values(platformMapDict["map"],date1,date2)
    print(datesList)
    returnDateList = lt.newList("ARRAY_LIST")
    
    for DateList in lt.iterator(datesList):
        for Date in lt.iterator(DateList):
            lt.addLast(returnDateList,Date)
    return platformMapDict["size"],returnDateList

def BestTimesbyPlayer(catalog, PlayerName): #Función Pricipal Requerimiento 2
    
    pass

def BeyersstTimesbyAttemptsRange(Lim_inferior,Lim_superior): #Función Pricipal Requerimiento 3
    pass
def WorstTimesbyDateRange(Fecha_inferior,Fecha_superior): #Función Pricipal Requerimiento 4
    pass
def RecentAttemptsbyRecordTimeRange(Tiempo_inferior,Tiempo_superior): #Función Pricipal Requerimiento 5
    pass
def HistogramofTimesbyYear(N_segmentos,N_niveles,anio,tiempo_012): #Función Pricipal Requerimiento 6
    pass
def TopFiveStreamingGames(Platform): #Función Pricipal Requerimiento 7
    pass
def RecordsbyCountry(Anio__publicacion,Tiempo_inferior,Tiempo_superior): #Función Pricipal Requerimiento 7
    pass
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
