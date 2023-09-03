from copy import copy
from collections import defaultdict
from functools import reduce
from itertools import product
from typing import Generator

from parametros import RUTA_PELICULAS, RUTA_GENEROS
from utilidades import (
    Pelicula, Genero, obtener_unicos, imprimir_peliculas,
    imprimir_generos, imprimir_peliculas_genero
)


# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------
import csv

def cargar_peliculas(ruta: str) -> Generator:
    # TODO: Completar
    separador = ","
    with open(ruta, encoding="utf-8") as archivo:
        next(archivo)  # Omitir encabezado del archivo
        for linea in archivo:
            linea = linea.rstrip("\n")  # Quitar salto de línea
            columnas = linea.split(separador)
            yield int(columnas[0]),str(columnas[1]),str(columnas[2]),int(columnas[3]),float(columnas[4])


def cargar_generos(ruta: str) -> Generator:
    # TODO: Completar
    separador = ","
    with open(ruta, encoding="utf-8") as archivo:
        next(archivo)  # Omitir encabezado del archivo
        for linea in archivo:
            linea = linea.rstrip("\n")  # Quitar salto de línea
            columnas = linea.split(separador)
            yield (str(columnas[0]),int(columnas[1]))

# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_directores(generador_peliculas: Generator) -> set:
    # TODO: Completar
    mapeo = map(lambda x: x.director, generador_peliculas)
    _set = obtener_unicos(mapeo)
    return _set

def obtener_str_titulos(generador_peliculas: Generator) -> str:
    # TODO: Completar
    mapeo = map(lambda x: x.titulo, generador_peliculas)
    mapeo = ", ".join(mapeo)
    return mapeo

def filtrar_peliculas(
    generador_peliculas: Generator,
    director: str | None = None,
    rating_min: float | None = None,
    rating_max: float | None = None
) -> filter:
    # TODO: Completar
    if director is not None:
        generador_peliculas = filter(lambda x: x.director == director, generador_peliculas)
    if rating_min is not None:
        generador_peliculas = filter(lambda x: x.rating >= rating_min, generador_peliculas)
    if rating_max is not None:
        generador_peliculas = filter(lambda x: x.rating <= rating_max, generador_peliculas)
    return generador_peliculas


def filtrar_peliculas_por_genero(
    generador_peliculas: Generator,
    generador_generos: Generator,
    genero: str | None = None
) -> Generator:
    # TODO: Completar
    producto = product(generador_peliculas, generador_generos)
    mismo_id = filter(lambda p: p[0].id_pelicula == p[1].id_pelicula, producto)
    if genero is not None:
        mismo_id = filter(lambda p: p[1].genero == genero, mismo_id)
    return mismo_id


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class DCCMax:
    def __init__(self, peliculas: list) -> None:
        self.peliculas = peliculas

    def __iter__(self):
        # TODO: Completar
        return IteradorDCCMax(self.peliculas)


class IteradorDCCMax:
    def __init__(self, iterable_peliculas: list) -> None:
        self.peliculas = copy(iterable_peliculas)
        self.peliculas.sort(key = lambda pelicula: (pelicula.estreno, -pelicula.rating))
        self.indices = 0 

        '''
        La idea de los índices fue sacada de:
        https://tinchicus.com/2021/12/09/python-iterador-personalizado/
        Y el sort(key = lambda) fue aprendido de:
        https://sparkbyexamples.com/python/sort-using-lambda-in-python/
        y 
        https://blogboard.io/blog/knowledge/python-sorted-lambda/
        
        '''

    def __iter__(self):
        # TODO: Completar
        return self

    def __next__(self) -> tuple:
        # TODO: Completar
        if self.indices < len(self.peliculas):
            valor = self.peliculas[self.indices]
            self.indices += 1
            return valor
        else:
            # Se levanta la excepción correspondiente
            raise StopIteration()


if __name__ == '__main__':
    print('> Cargar películas:')
    imprimir_peliculas(cargar_peliculas(RUTA_PELICULAS))
    print()

    print('> Cargar géneros')
    imprimir_generos(cargar_generos(RUTA_GENEROS), 5)
    print()

    print('> Obtener directores:')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(list(obtener_directores(generador_peliculas)))
    print()

    print('> Obtener string títulos')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(obtener_str_titulos(generador_peliculas))
    print()

    print('> Filtrar películas (por director):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(
        generador_peliculas, director='Christopher Nolan'
    ))
    print('\n> Filtrar películas (rating min):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_min=9.1))
    print('\n> Filtrar películas (rating max):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_max=8.7))
    print()

    print('> Filtrar películas por género')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    generador_generos = cargar_generos(RUTA_GENEROS)
    imprimir_peliculas_genero(filtrar_peliculas_por_genero(
        generador_peliculas, generador_generos, 'Biography'
    ))
    print()

    print('> DCC Max')
    for (estreno, pelis) in DCCMax(list(cargar_peliculas(RUTA_PELICULAS))):
        print(f'\n{estreno:^80}\n')
        imprimir_peliculas(pelis)
