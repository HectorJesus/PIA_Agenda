from flask import Flask, render_template
from database import dbConnection
import bcrypt

def validar_usuario(name, password):
    # Obtener la instancia de la base de datos
    database = dbConnection()

    # Obtener la colección de usuarios de la base de datos
    coleccion_usuarios = database['users']

    # Realizar la consulta para encontrar un documento con el nombre de usuario y contraseña
    usuario = coleccion_usuarios.find_one({'name': name})

    # Verificar si se encontró un usuario válido
    if usuario and bcrypt.checkpw(password.encode('utf-8'),usuario['password']):
        return True
    else:
        return False
    
def encriptarContraseña(name, password, email):
    # Obtener la instancia de la base de datos
    database = dbConnection()

    # Obtener la colección de usuarios de la base de datos
    coleccion_usuarios = database['users']

    # Generar un hash de la contraseña
    contrasena_encriptada = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insertar el nuevo usuario en la base de datos
    coleccion_usuarios.insert_one({'name': name, 'password': contrasena_encriptada, 'email': email})
