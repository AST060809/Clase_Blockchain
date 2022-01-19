# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 17:00:27 2022

@author: Alexander
"""

# Modulo 2 Crear una crypto moneda

# Para instalar:
# flask ==0.12.2: pip install Flask==0.12.2
# Cliente HTTP Postman: https://www.getpostman.com/
# requests==2.25.1: pip install requests==2.25.1

# Importar las librerias

import datetime #para manejar fechas
import hashlib # es la libreria para crear los hash
import json #para crear objetos json
from flask import Flask, jsonify, request
import requests # libreria requests para hacer peticiones 
from uuid import uuid4
from urllib.parse import urlparse
 
#Parte 1 Crear la Cadena de Bloques

class Blockchain:
    
    def __init__(self): #creando el constructor, el parametro self hace referencia al objeto creado, es como el this en JS
        self.chain = [] #creando el objeto chain en una lista vacia
        self.transactions=[] # Creando la lista de transacciones, que se iran guardando hasta crear un nuevo bloque
        self.create_block(proof = 1, prev_hash = '0')# Invocando la función crear bloque dentro del constructor, se le pasan los parametros del primer bloque.
        self.nodes = set{} # los nodos los creo como un conjunto xq no tendran un orden, como un lista
    # Creación da la función crear bloque.    
    def create_block(self, proof, prev_hash):  # la proof en la preuba de trabajo, demostrando que el bloque fue minado. LLamando asi a la funcion despues de haber minado el bloque.
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()), # esto me devuelve la fecha en la que fue minado el bloque. (llamamos a la libreira datatime, con la funcion datetime y el metodo now()), le hago un casting a string ya que lo voy aguardar en formato json.
                 'proof':proof, # la prueba de trabajo que se creo el bloque.
                 'prev_hash':prev_hash  
                 'transaction': self.transactions}
        self.transactions = [] # despues que minamos el bloque tenemos que vaciar la lista de transacciones.
        self.chain.append(block) #añadimos el bloque a la cadena)
        return block
    
    
    # La función para obtener el bloque previo, es decir el ultimo de la cadena
    def get_prev_block(self):
        return self.chain[-1] # -1 para obtener el ultimo elemento de la cadena, en este caso el hash de la anterior.
    
    def proof_of_work(self, prev_proof): # función que vamos a utilizar para comprobar que el valor es valido para minar el bloque
        new_proof = 1 # esta variable la utilizaremos para determinar si es la solución y se ira incrementando de 1 en 1
        check_proof = False # caundo se haya resuelto el problema crytografivo valdra True.
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest() #esta varaible sera un string de 64 caracteres. encode() verifica que el formato es el adecuado.
            if hash_operation[:4]=='0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # Función para dependiendo de un bloque calcular su hash
    def hash (self, block):
         # utilizamos esta variable para guardar el volcado de el diccionario a un objeto json. el parametro sort_keys es para ordenar las claves del diccionario.
        encoded_block = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # Función para validar si la cadena es valida
    def is_chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index] # le asignamos a block el valor que tiene el bloque en la cadena en ese nomento.
           #evaluamos la condición si el previo hash del bloque es diferente al hash del bloque anterior, la cadana no es valida.
            if block['prev_hash'] != self.hash(prev_block): 
                return False
            # El valor de la prueba de trabajo del bloque actual y del previo.
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                 return False
            prev_block = block
            block_index +=1
        return True
    
                
   def add_transaction(self, sender, receiver, amount):
           self.transactions.append({'sender':sender,
                                     'receiver':receiver,
                                     'amount':amount})
           prev_block = self.prev_block()
           return prev_block['index'] + 1
   #Añadir un nuevo nodo    
   def add_node(self, address): 
       # Funcion que procesa direcciones
       parsed_url = urlparse(address)
       # de la url parseada solo me quedo con el campo netloc y lo adiciona con add ya que los nodos son un conjunto y no pedomos ussar append con lo usariamos en una lista.
       self.nodes.add(parsed_url.netloc)
       
#Parte 2 Minado de un bloque de la Cadena

#Crear una aplicación web
app  = Flask(__name__)


#Crear una Blockchain
blockchain = Blockchain() #instanciando la clase Blockchain

#Minar un nuevo bloque clase 31
# paso 1 para minar un bloque es tener la proof of work
@app.route('/mine_block', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash =blockchain.hash(prev_block)
    block= blockchain.create_block(proof,prev_hash)
    response = {'message':'Enhorabuena, has minado un nuevo bloque',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof':block['proof'],
                'prev_hash': block['prev_hash']
                
        }
    return jsonify(response), 200
    
# Obtener la cadena de bloques al completo
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response ={'chain':blockchain.chain,
               'length':len(blockchain.chain)}
    return jsonify(response), 200

# Validar la Blockchain es valida
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'massage':'La Blockcahin es válida'}
    else:
        response ={'massage':'La Blockcahin no es válida'}
    
    return jsonify(response), 200  

# Parte 3 - Descentralizar la cadena de bloques
 

# Ejecutar la app
app.run(host='0.0.0.0', port=5000)
    

    