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
 """
import config as cf
import model
import csv


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
    return control
# Funciones para la carga de datos
def loadData(control,size):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    catalog = control['model']
    loadContentCategory(catalog,size)
    loadContentGames(catalog,size)
    loadContentRevenue(catalog,size)
def loadContentCategory(catalog,size):
    file = 'Speedruns/category_data_utf-8'+size+'.csv'
    contentfile = cf.data_dir + file
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for content in input_file:
        for key in content:
            if content[key] == "":
                content[key] = "Unknown"
        model.add_contentCategory(catalog, content)
    return catalog
def loadContentGames(catalog,size):
    file = 'Speedruns/game_data_utf-8'+size+'.csv'
    contentfile = cf.data_dir + file
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for content in input_file:
        for key in content:
            if content[key] == "":
                content[key] = "Unknown"
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

def RecentAttemptsbyRecordTimeRange(catalog,Tiempo_inferior,Tiempo_superior): #Función Pricipal Requerimiento 5
    return model.RecentAttemptsbyRecordTimeRange(catalog['model'],Tiempo_inferior,Tiempo_superior)

def HistogramofTimesbyYear(catalog,anio_inferior,anio_superior,N_segmentos,N_niveles,anio,propiedades): #Función Pricipal Requerimiento 6
    return model.HistogramofTimesbyYear(catalog['model'],anio_inferior,anio_superior,N_segmentos,N_niveles,anio,propiedades)
def TopNRevenueGames(catalog,platform,N):
    return model.TopNRevenueGames(catalog["model"],platform,N)