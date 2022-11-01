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


from platform import platform
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
import time

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {"GamesList":lt.newList("ARRAY_LIST"),
                "CategoryList":lt.newList("ARRAY_LIST"),
                "Id_Name_Dict" : {},
                "Id_Genres_Dict" : {},
                "Id_Platforms_Dict" : {},
                "MapByPlatform":mp.newMap(),
                'MapByPlayers':mp.newMap(),
                "MapByRuns":om.newMap(),
                "MapByTime_0":om.newMap()}
    return catalog
# Funciones para agregar informacion al catalogo
def add_contentCategory(catalog, content):
    content["Num_Runs"] = int(content["Num_Runs"])
    for player in content['Players_0'].split(','):
        player = player.strip()
        if mp.contains(catalog['MapByPlayers'], player) == False:
            mp.put(catalog['MapByPlayers'], player, om.newMap(omaptype='RBT', comparefunction=compareTime0))
        map_times = me.getValue(mp.get(catalog['MapByPlayers'], player))
        if om.contains(map_times, content['Time_0']) == False:
            mp.put(map_times, content['Time_0'], lt.newList('ARRAY_LIST'))
        lt.addLast(me.getValue(mp.get(map_times, content['Time_0'])), content)
    if om.contains(catalog["MapByRuns"],content["Num_Runs"]) == False: #Mapa por # de runs
        om.put(catalog["MapByRuns"],content["Num_Runs"],om.newMap(omaptype="RBT",comparefunction=compareRuns))
    map_runs = me.getValue(om.get(catalog["MapByRuns"],content["Num_Runs"]))
    if om.contains(map_runs,content["Time_0"]) == False:
        om.put(map_runs,content["Time_0"],lt.newList("ARRAY_LIST"))
    lt.addLast(me.getValue(om.get(map_runs,content["Time_0"])),content)
    if om.contains(catalog["MapByTime_0"],content["Time_0"]) == False:
        om.put(catalog["MapByTime_0"],content["Time_0"],lt.newList("ARRAY_LIST"))
    lt.addLast(me.getValue(om.get(catalog["MapByTime_0"],content["Time_0"])),content)
    lt.addLast(catalog['CategoryList'], content)

def add_contentGames(catalog, content):
    for platform in content["Platforms"].split(","):
        platform = platform.strip()
        if mp.contains(catalog["MapByPlatform"],platform) == False:
            mp.put(catalog["MapByPlatform"],platform,{"map":om.newMap(omaptype="RBT",comparefunction=comparedates),"size":0})
        map_dict = me.getValue(mp.get(catalog["MapByPlatform"],platform))
        if om.contains(map_dict["map"],content["Release_Date"]) == False:
            om.put(map_dict["map"],content["Release_Date"],lt.newList("ARRAY_LIST"))
        lt.addLast(me.getValue(om.get(map_dict["map"],content["Release_Date"])),content)
        map_dict["size"] += 1
    lt.addLast(catalog["GamesList"],content)
    catalog["Id_Name_Dict"][content["Game_Id"]] = content["Name"]
    catalog["Id_Genres_Dict"][content["Game_Id"]] = content["Genres"]
    catalog["Id_Platforms_Dict"][content["Game_Id"]] = content["Platforms"]

    

# Funciones para creacion de datos

# Funciones de consulta
def GamesByPlatform(catalog,platform,date1,date2): #Función Pricipal Requerimiento 1
    platformMapDict = me.getValue(mp.get(catalog["MapByPlatform"],platform))
    datesList = om.values(platformMapDict["map"],date1,date2)
    return platformMapDict["size"],datesList

def BestTimesbyPlayer(catalog, player): #Función Pricipal Requerimiento 2
    playerMapDict = me.getValue(mp.get(catalog['MapByPlayers'], player))
    valuesPlayer = om.valueSet(playerMapDict)
    total_num_runs = 0
    for value in lt.iterator(valuesPlayer):
        total_num_runs += lt.lastElement(value)['Num_Runs']
    return playerMapDict, total_num_runs

def BestTimesbyAttemptsRange(catalog,Lim_inferior,Lim_superior): #Función Pricipal Requerimiento 3
    RunsInRange = om.values(catalog["MapByRuns"],float(Lim_inferior),float(Lim_superior))
    CategoryList = lt.newList("ARRAY_LIST")
    for i in lt.iterator(RunsInRange):
        lt.addLast(CategoryList,om.valueSet(i))
    return CategoryList
def WorstTimesbyDateRange(Fecha_inferior,Fecha_superior): #Función Pricipal Requerimiento 4
    pass
def RecentAttemptsbyRecordTimeRange(catalog,Tiempo_inferior,Tiempo_superior): #Función Pricipal Requerimiento 5
    AttemptsinRange = om.values(catalog["MapByTime_0"],Tiempo_inferior,Tiempo_superior)
    TimeList = lt.newList("ARRAY_LIST")
    for i in lt.iterator(AttemptsinRange):
        for e in lt.iterator(i):
            lt.addLast(TimeList)
    return TimeList

def HistogramofTimesbyYear(N_segmentos,N_niveles,anio,tiempo_012): #Función Pricipal Requerimiento 6
    pass
def TopFiveStreamingGames(Platform): #Función Pricipal Requerimiento 7
    pass
def RecordsbyCountry(Anio__publicacion,Tiempo_inferior,Tiempo_superior): #Función Pricipal Requerimiento 7
    pass
# Funciones utilizadas para comparar elementos dentro de una lista
def comparedates(date1,date2):
    if len(date1) == 8:
        date1 = time.strptime(date1, "%y-%m-%d")
    else:
        date1 = time.strptime(date1, "%Y-%m-%d")
    if len(date2) == 8:
        date2 = time.strptime(date2, "%y-%m-%d")
    else:
        date2 = time.strptime(date2, "%Y-%m-%d")

    if date1 > date2:
        return 1
    elif date1 < date2:
        return -1
    else:
        return 0
def compareRuns(run1,run2):
    run1,run2 = float(run1),float(run2)
    if run1 > run2:
        return 1
    elif run1 < run2:
        return -1
    else:
        return 0
def compareTime0(time1, time2):
    if time1 > time2:
        return 1
    elif time1 < time2:
        return -1
    else:
        return 0
# Funciones de ordenamiento

