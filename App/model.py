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
import time
from math import log

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
                "Id_ReleaseDate_Dict":{},
                ###7###
                "Number_Of_RegistersRuns_ById":{"Register":{},"Runs":{}},
                "MapByPlatformAndRevenue":mp.newMap(),
                ###7###
                "MapByPlatform":mp.newMap(),
                'MapByPlayers':mp.newMap(),
                "MapByRuns":om.newMap(),
                "MapByTime_0":om.newMap(comparefunction=compareRuns),
                "Platform_count":{}}
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
    ###7###
    if content["Misc"] == "False":
        if content["Game_Id"] not in catalog["Number_Of_RegistersRuns_ById"]["Register"]:
            catalog["Number_Of_RegistersRuns_ById"]["Register"][content["Game_Id"]] = 0
        catalog["Number_Of_RegistersRuns_ById"]["Register"][content["Game_Id"]] += 1    
    ###7###
    for i in catalog["Id_Platforms_Dict"][content["Game_Id"]].split(","):
        i = i.strip()
        if i not in catalog["Platform_count"]:
            catalog["Platform_count"][i] = 0
        catalog["Platform_count"][i] += 1
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
    catalog["Id_ReleaseDate_Dict"][content["Game_Id"]] = content["Release_Date"]
    catalog["Number_Of_RegistersRuns_ById"]["Runs"][content["Game_Id"]] = content["Total_Runs"]
def addcontentStreamReveue(catalog,content):
    if (content["Misc"]) == "False":
        avg,revenue = Revenue(catalog,content)
        content["Time_Avg"] = round(avg,2)
        gt = catalog["Number_Of_RegistersRuns_ById"]["Register"][content["Game_Id"]]
        content["Genres"] = catalog["Id_Genres_Dict"][content["Game_Id"]]
        content["Platforms"] = catalog["Id_Platforms_Dict"][content["Game_Id"]]
        content["Name"] = catalog["Id_Name_Dict"][content["Game_Id"]]
        content["Release_Date"] = catalog["Id_ReleaseDate_Dict"][content["Game_Id"]]
        content["Total_Runs"] = catalog["Number_Of_RegistersRuns_ById"]["Runs"][content["Game_Id"]]
        for platform in (catalog["Id_Platforms_Dict"][content["Game_Id"]]).split(","):
            platform = platform.strip()
            pt = me.getValue(mp.get(catalog["MapByPlatform"],platform))["size"] 
            MarketShare = gt/pt
            stream_revenue = round(revenue*MarketShare,2)
            content["Market_Share"] = round(MarketShare,2)
            content["Stream_Revenue"] = stream_revenue
            if mp.contains(catalog["MapByPlatformAndRevenue"],platform) == False:
                mp.put(catalog["MapByPlatformAndRevenue"],platform,om.newMap())
            map_ = me.getValue(mp.get(catalog["MapByPlatformAndRevenue"],platform))
            if om.contains(map_,stream_revenue) == False:
                om.put(map_,stream_revenue,lt.newList("ARRAY_LIST"))
            lt.addLast(me.getValue(om.get(map_,stream_revenue)),content.copy())
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
    return AttemptsinRange

def HistogramofTimesbyYear(N_segmentos,N_niveles,anio,tiempo_012): #Función Pricipal Requerimiento 6
    pass
def TopFiveStreamingGames(Platform): #Función Pricipal Requerimiento 7
    pass
def TopNRevenueGames(catalog,platform,N): #Función Pricipal Requerimiento 7
    MapByPlatformAndRevenue = catalog["MapByPlatformAndRevenue"]
    MapByRevenue = me.getValue(mp.get(MapByPlatformAndRevenue,platform))
    list_ = lt.newList("ARRAY_LIST")
    print(catalog["Number_Of_RegistersRuns_ById"]["Register"]["180"])
    high = om.maxKey(MapByRevenue)
    low = om.select(MapByRevenue,lt.size(om.keySet(MapByRevenue))-N)
    Values = om.values(MapByRevenue,low,high)
    for i in lt.iterator(Values):
        for e in lt.iterator(i):
            lt.addLast(list_,e)
    if lt.size(list_) > N:
        list_ = lt.subList(list_,lt.size(list_)-N+1,N)
    return reverselist(list_)
def Revenue(catalog,content): #Función Auxiliar Requerimiento 7
    if len(catalog["Id_ReleaseDate_Dict"][content["Game_Id"]]) == 8:
        release_year = int(time.strptime(catalog["Id_ReleaseDate_Dict"][content["Game_Id"]], "%y-%m-%d")[0])
    else:
        release_year = int(time.strptime(catalog["Id_ReleaseDate_Dict"][content["Game_Id"]], "%Y-%m-%d")[0])
    if release_year >= 2018:
        antiquity = release_year - 2017
    elif release_year < 1998:
        antiquity = 5
    else:
        antiquity = (-0.2*release_year) + 404.6
    popularity = log(int(catalog["Number_Of_RegistersRuns_ById"]["Runs"][content["Game_Id"]]))
    sum = 0
    div = 0
    if content["Time_0"] != "":
        sum += float(content["Time_0"])
        div += 1
    if content["Time_1"] != "":
        sum += float(content["Time_1"])
        div += 1
    if content["Time_2"] != "":
        sum += float(content["Time_2"])
        div += 1
    avg = sum/div
    return avg,(popularity*(avg/60))/antiquity
def reverselist(list): #Función para invertir el orden de una lista
    li = 1
    lo = lt.size(list)
    while li <lo:
        lt.exchange(list,li,lo)
        li +=1
        lo -= 1
    return list
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
def compareNumberDescending(uno,dos):
    if uno < dos:
        return True
    elif uno > dos:
        return False
    else:
        return 0
# Funciones de ordenamiento
