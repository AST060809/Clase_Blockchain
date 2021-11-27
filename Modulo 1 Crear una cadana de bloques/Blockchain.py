# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 21:33:48 2021

@author: Alexander
"""

# Modulo 1 Como crear una cadena de bloques

# Para instalar:
# flask ==0.12.2: pip install Flask==0.12.2
# Cliente HTTP Postman: https://www.getpostman.com/

# Importar las librerias

import datetime #para manejar fechas
import hashlib # es la libreria para crear los hash
import json #para crear objetos json
from flask import Flask, jsonify

#Parte 1 Crear la Cadena de Bloques

class Blockchain:
    
    def __init__(self): #creando el constructor, el parametro self hace referencia al objeto creado, es como el this en JS
        self.chain = [] #creando el objeto chain
        self.create_block(proof = 1, prev_hash = '0')
        
    def create_block(self, proof, prev_hash):
        block = {
            
            }
        
    
     
    
    


#Parte 2 Minado de un bloque de la Cadena