﻿"""
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
 """
import config as cf
import model
import csv
import time
import tracemalloc
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newController():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': model.newCatalog()
    }
    tracemalloc.start()
    return control
# Funciones para la carga de datos
def loadData(control,size):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    catalog = control['model']
    loadContentGames(catalog,size)
    loadContentCategory(catalog,size)
    loadContentRevenue(catalog,size)
def loadContentCategory(catalog,size):
    file = 'Speedruns/category_data_utf-8'+size+'.csv'
    contentfile = cf.data_dir + file
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for content in input_file:
        model.add_contentCategory(catalog, content)
    return catalog
def loadContentGames(catalog,size):
    file = 'Speedruns/game_data_utf-8'+size+'.csv'
    contentfile = cf.data_dir + file
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for content in input_file:
        model.add_contentGames(catalog, content)
    return catalog
def loadContentRevenue(catalog,size):
    file = 'Speedruns/category_data_utf-8'+size+'.csv'
    contentfile = cf.data_dir + file
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for content in input_file:
        model.addcontentStreamReveue(catalog,content)
    return catalog
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def GamesByPlatform(catalog,platform,date1,date2): #Función Pricipal Requerimiento 1
    return model.GamesByPlatform(catalog["model"],platform,date1,date2)

def BestTimesByPlayer(catalog, player):
    return model.BestTimesbyPlayer(catalog['model'], player)
    
def BestTimesbyAttemptsRange(catalog,Lim_inferior,Lim_superior): #Función Pricipal Requerimiento 3
    return model.BestTimesbyAttemptsRange(catalog["model"],Lim_inferior,Lim_superior)

def SlowestTimesByDateRange(catalog, lo, hi): #Función Pricipal Requerimiento 4
    return model.SlowestTimesByDateRange(catalog['model'], lo, hi)

def RecentAttemptsbyRecordTimeRange(catalog,Tiempo_inferior,Tiempo_superior): #Función Pricipal Requerimiento 5
    return model.RecentAttemptsbyRecordTimeRange(catalog['model'],Tiempo_inferior,Tiempo_superior)

def HistogramofTimesbyYear(catalog,li,lo,N,criterio): #Función Principal Requerimiento 6
    return model.HistogramofTimesbyYear(catalog["model"],li,lo,N,criterio)

def TopNRevenueGames(catalog,platform,N):
    return model.TopNRevenueGames(catalog["model"],platform,N)

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)
def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()
def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

def recordsDistributionByCountry(catalog, year, lo, hi):
    return model.RecordsDistributionByCountry(catalog['model'], year, lo, hi)
