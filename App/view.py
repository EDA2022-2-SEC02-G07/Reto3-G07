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
    print("3- ")
    print("4- ")
    print("5- ")
    print("6- ")
    print("7- ")
    print("8- ")
    print("9- ")

catalog = None
size = "-small"
"""
Menu principal
"""
def printreq1(catalog):
    map = catalog["model"]["MapByPlatform"]
    list_ = catalog["model"]["GamesList"]
    print("Altura:",str(om.height(map)))
    print("Numero de nodos:",str(om.size(map)))
    print("Numero de elemtos:",str(lt.size(list_)))
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        catalog = controller.newController()
        controller.loadData(catalog,size)
        print("Cargando información de los archivos ....")

    elif int(inputs[0]) == 2:
        printreq1(catalog)

    else:
        sys.exit(0)
sys.exit(0)
