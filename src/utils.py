import datetime
import random
import string
# Función para generar un nombre único para el archivo de log
def generate_log_filename():
    fecha = datetime.datetime.now().strftime("%d-%m-%Y")
    unique_identifier = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"Log_{fecha}_{unique_identifier}.log"

#Funcion para generar el nombre del archivo para los analisís
def generate_analisy_record():
    fecha = datetime.datetime.now().strftime("%d-%m-%Y")
    unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=4)) #modificar la k --> mayor longitud !!
    return f"Analisys_{fecha}_{unique_id}.txt"