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
        self.chain = [] #creando el objeto chain en una lista vacia
        self.create_block(proof = 1, prev_hash = '0')# Invocando la función crear bloque dentro del constructor, se le pasan los parametros del primer bloque.
    # Creación da la función crear bloque.    
    def create_block(self, proof, prev_hash):  # la proof en la preuba de trabajo, demostrando que el bloque fue minado. LLamando asi a la funcion despues de haber minado el bloque.
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()), # esto me devuelve la fecha en la que fue minado el bloque. (llamamos a la libreira datatime, con la funcion datetime y el metodo now()), le hago un casting a string ya que lo voy aguardar en formato json.
                 'proof':proof, # la prueba de trabajo que se creo el bloque.
                 'prev_hash':prev_hash      
            }
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
    
# Ejecutar la app
app.run(host='0.0.0.0', port=5000)
    
    
    
    
    
    
    
    
    
    
    