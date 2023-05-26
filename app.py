from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from  user import User
from actividades import Actividad
from datetime import datetime, timedelta
from validacion import validar_usuario
from validacion import encriptarContraseña
from datos import data
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


db = dbase.dbConnection()

app = Flask(__name__)

def enviar_correo(destinatario, asunto, mensaje):
    # Configurar los detalles del servidor SMTP de Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Puerto para STARTTLS

    # Credenciales de inicio de sesión
    remitente = 'condedooku115@gmail.com'
    contraseña = 'awxyycvmtfxulhiu'


    # Crear el mensaje de correo electrónico
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        # Iniciar una conexión SMTP segura con el servidor de Gmail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remitente, contraseña)

        # Enviar el correo electrónico
        server.sendmail(remitente, destinatario, msg.as_string())

        # Cerrar la conexión SMTP
        server.quit()

        print(f"Correo electrónico enviado a {destinatario}")
    except Exception as e:
        print(f"No se pudo enviar el correo electrónico a {destinatario}. Error: {str(e)}")

    # Crear el objeto MIMEText para el mensaje
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    # Enviar el correo electrónico utilizando SMTP
    try:
        smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_obj.starttls()
        smtp_obj.login(remitente, contraseña)
        smtp_obj.sendmail(remitente, destinatario, msg.as_string())
        smtp_obj.quit()
        print('Correo electrónico enviado correctamente a', destinatario)
    except Exception as e:
        print('Error al enviar el correo electrónico:', str(e))

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
    user_name = request.form['user_name']

    if titulo and descripcion and hora and prioridad and user_name:
        actividades = Actividad(titulo, descripcion, hora, prioridad)
        addAct.insert_one(actividades.toDBCollection())

        # Obtener la fecha actual y calcular la fecha límite de la actividad
        fecha_actual = datetime.now()
        fecha_limite = fecha_actual + timedelta(hours=int(hora))

        # Consultar el correo electrónico del usuario desde la base de datos
        users = db['users']
        usuario = users.find_one({'name': user_name})  # Se busca el correo del usuario en base a su nombre
        destinatario = usuario['email']

        # Enviar un correo electrónico al usuario
        asunto = 'Actividad por vencer'
        mensaje = f"Hola, tu actividad '{titulo}' está por vencer. Fecha límite: {fecha_limite}. ¡No olvides completarla a tiempo!"

        enviar_correo(destinatario, asunto, mensaje)

        response = jsonify({
            'titulo': titulo,
            'descripcion': descripcion,
            'hora': hora,
            'prioridad': prioridad
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