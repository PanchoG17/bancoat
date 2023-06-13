from zeep import Client
from zeep.transports import Transport
from requests import Session
import urllib3
import requests

session = Session()
session.verify = False
transport = Transport(session=session)
cliente = Client('https://####', transport=transport)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def ADWSLogin(username, password):
    # verificacion del usuario con AD
    try:
        is_user = cliente.service.Login(username, password)

        if is_user:
            return is_user
    except:
        return

def ADWSGetDni(username):
    # obtencion del documento del usuario
    try:
        dni = cliente.service.GetDni(username)

        return dni

    except:
        return

def ADWSGetUser(dni_usuario):
    try:
        usuario = cliente.service.GetUser(dni_usuario)

        return usuario

    except:
        return 'No hay datos para el dni ' + dni_usuario

def ADWSGetUsuarioYPass(username):
    try:
        datos = cliente.service.GetUsuarioYPass(username)
        return datos
    except:
        return 'No se han encontrado datos del usuario ' + username