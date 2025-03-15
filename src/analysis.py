from collections import defaultdict
import re
from src.capture import captura_continua
from src.utils import generate_analisy_record
import os
from termcolor import colored

# Diccionarios para contar las IPs, protocolos y pares de IPs
ip_count = defaultdict(int)
protocol_count = defaultdict(int)
ip_pairs_count = defaultdict(int)

# Función para leer un archivo de log
def leer_logs(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_archivo}")
        return []

# Función para procesar una línea de log y extraer las IPs y el protocolo
def procesar_log_linea(linea):
    # Regex para IPs, tanto IPv4 como IPv6
    ip_origen = re.search(r'\d{1,3}(\.\d{1,3}){3}|\[([a-fA-F0-9:]+)\]', linea)
    ip_destino = None
    if '>' in linea:
        ip_destino = re.search(r'\d{1,3}(\.\d{1,3}){3}|\[([a-fA-F0-9:]+)\]', linea.split('>')[1])

    # Definimos el protocolo, si está presente
    protocolo = None
    if 'TCP' in linea:
        protocolo = 'TCP'
    elif 'UDP' in linea:
        protocolo = 'UDP'
    elif 'ICMP' in linea:
        protocolo = 'ICMP'

    # Verificamos si las IPs y el protocolo fueron encontrados
    if ip_origen and ip_destino:
        return ip_origen, ip_destino, protocolo
    return None, None, None

# Función para procesar las líneas de log
def procesar_log(lineas_log):
    for linea in lineas_log:
        ip_origen, ip_destino, protocolo = procesar_log_linea(linea)

        if ip_origen and ip_destino:
            # Contamos la frecuencia de las IPs
            ip_count[ip_origen.group()] += 1
            ip_count[ip_destino.group()] += 1

        if protocolo:
            protocol_count[protocolo] += 1

        # Contabilizamos las IPs de origen y destino como pares
        if ip_origen and ip_destino:
            ip_pairs_count[(ip_origen.group(), ip_destino.group())] += 1

# Función para mostrar las frecuencias
def mostrar_frecuencia():
    # Mostramos la frecuencia de IPs
    print("\nFrecuencia de paquetes por IP:")
    for ip, count in ip_count.items():
        print(f"IP: {ip} --> {count} paquetes")

    # Mostramos la frecuencia de protocolos
    print("\nFrecuencia de paquetes por Protocolo:")
    for protocolo, count in protocol_count.items():
        print(f"Protocolo: {protocolo} --> {count} paquetes")

    # Mostramos la frecuencia de las combinaciones de IPs origen y destino
    print("\nFrecuencia de pares IPs (Origen > Destino):")
    for (ip_origen, ip_destino), count in ip_pairs_count.items():
        print(f"De {ip_origen} a {ip_destino} --> {count} paquetes")

    generador_reporte(ip_count, protocol_count, ip_pairs_count)

# Función para analizar un archivo de log
def analizar_archivo_log(ruta_archivo):
    print(f"\nAnalizando el archivo de log: {ruta_archivo}")
    
    lineas_log = leer_logs(ruta_archivo)
    if lineas_log:
        procesar_log(lineas_log)
        mostrar_frecuencia()
    else:
        print("No se encontraron datos para analizar.")

# Función para procesar un paquete de red individual (en caso de análisis continuo)
def procesar_paquete(pkt):
    ip_origen, ip_destino, protocolo = procesar_log_linea(str(pkt))

    if ip_origen and ip_destino:
        # Contamos la frecuencia de las IPs
        ip_count[ip_origen.group()] += 1
        ip_count[ip_destino.group()] += 1

    if protocolo:
        protocol_count[protocolo] += 1

    # Contabilizamos las IPs de origen y destino como pares
    if ip_origen and ip_destino:
        ip_pairs_count[(ip_origen.group(), ip_destino.group())] += 1

# Función para analizar tráfico de red continuamente
def analizar_continua(iface, filtro_prot):
    captura_continua(iface=iface, filtro_prot=filtro_prot, callback=procesar_paquete)
    mostrar_frecuencia()

# Función para generar informe de las estadísticas dadas
def generador_reporte(ip_count, protocol_count, ip_pairs_count, carpeta_destino="reportes"):
    # Verifica si la carpeta existe, si no la crea
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Generar el nombre del archivo
    name = generate_analisy_record()

    # Ruta completa para el archivo en la carpeta destino
    ruta_archivo = os.path.join(carpeta_destino, f'{name}.txt')

    # Generar el reporte
    with open(ruta_archivo, 'w') as file:
        file.write("Frecuencia de paquetes por IP:\n")
        for ip, count in ip_count.items():
            file.write(f"IP: {ip} --> {count} paquetes\n")

        file.write("\nFrecuencia de paquetes por Protocolo:\n")
        for protocolo, count in protocol_count.items():
            file.write(f"Protocolo: {protocolo} --> {count} paquetes\n")

        file.write("\nFrecuencia de pares IPs (Origen > Destino):\n")
        for (ip_origen, ip_destino), count in ip_pairs_count.items():
            file.write(f"De {ip_origen} a {ip_destino} --> {count} paquetes\n")

    print(colored(f"Reporte generado en: {ruta_archivo}", "green"))


# Función principal para ejecutar análisis de logs o monitoreo continuo
if __name__ == "__main__":
    # Analizar archivo de log
    ruta_archivo = 'logs\\Log_13-03-2025_PmCQRd.log'  # Ajusta este nombre según el archivo generado
    analizar_archivo_log(ruta_archivo)

    # O iniciar análisis continuo (descomenta esta línea cuando quieras monitorear tráfico en vivo)
    # analizar_continua()
