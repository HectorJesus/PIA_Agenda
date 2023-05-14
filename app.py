from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from  user import User
from actividades import Actividad
from datetime import datetime
from validacion import validar_usuario
from validacion import encriptarContraseña
from datos import data


db = dbase.dbConnection()

app = Flask(__name__)

#Rutas de la aplicacion
@app.route('/')
def home():
    users = db['users']
    usersRecieved = users.find()
    return render_template('index.html')

@app.route('/SingUp')
def SingUp():
    users = db['users']
    usersRecieved = users.find()
    return render_template('singUp.html')

#Valida usuario en BD e Inisiar sesion
@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    password = request.form['password']

    if validar_usuario(name, password):
        # Usuario válido, realizar las acciones correspondientes (redirigir, establecer una sesión, etc.)
        return render_template('menu.html')
    else:
        # Usuario inválido, mostrar un mensaje de error
        return render_template('index.html')

@app.route('/formAdd')
def formAdd():
    users = db['users']
    usersRecieved = users.find()
    return render_template('formAdd.html')

@app.route('/formEdith')
def formEdith():
    users = db['users']
    usersRecieved = users.find()
    return render_template('formEdith.html')

@app.route('/menu')
def menu():
    return render_template('menu.html', data=data)

#Metodo POST para crear usuarios
@app.route('/crearUsuarios', methods=['POST'])
def addUser():
    users = db['users']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    
    if name and email and password:
        encriptarContraseña(name, password, email)
        return redirect(url_for('home'))
    else:
        return notFound()
    

#Metodo POST para crear actividad
@app.route('/crearActividad', methods=['POST'])
def addActividad():
    addAct = db['actividades']
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    hora = request.form['hora']
    prioridad = request.form['prioridad']
    
    if titulo and descripcion and hora and prioridad:
        actividades = Actividad(titulo, descripcion, hora, prioridad)
        addAct.insert_one(actividades.toDBCollection())
        response = jsonify({
            'titulo' : titulo,
            'descripcion' : descripcion,
            'hora' : hora,
            'prioridad' : prioridad
        })
        return redirect(url_for('home'))
    else:
        return notFound()

#Metodo Delete
@app.route('/delete/<string:user_name>')
def delete(user_name):
    users = db['users']
    users.delete_one({'name' : user_name})
    return redirect(url_for('home'))

#Metodo Put
@app.route('/edit/<string:user_name>', methods=['POST'])
def edit(user_name):
    users = db['users']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    
    if name and email and password:
        users.update_one({'name' : user_name}, {'set' : {'name' : name, 'email' : email, 'password' : password}})
        response = jsonify({'message' : 'User' + user_name + ' actualizado correctamente'})
        return redirect(url_for('home'))
    else:
        return notFound()

@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message' : 'No encontrado' + request.url,
        'status' : '404 Not Found'
    }
    
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__' :
    app.run(debug=True, port=4000)