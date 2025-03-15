from scapy.all import *
import logging
import os
from termcolor import colored
from src.utils import generate_log_filename

# Función para configurar el archivo de log
def configurar_log():
    LOG_DIR = 'Logs'
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    nombre_arch = generate_log_filename()
    logging.basicConfig(filename=os.path.join(LOG_DIR, nombre_arch),
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s')
    print(colored(f"El archivo {nombre_arch} donde se guardará la captura se ha generado correctamente", 'green'))

# Función para capturar paquetes con un filtro(Por defecto --> se configura de la siguiente forma)
def capturar_paquetes(iface="Wi-Fi", filtro_prot="tcp", num_pkts=100, tiempo_limite=None, callback = None):
    
    print(colored(f"Comenzando la captura en la interfaz: {iface} con filtro {filtro_prot}", 'yellow'))
    try:
        # Capturar los paquetes con el filtro y número de paquetes especificados
        pkts = sniff(iface=iface, filter=f"{filtro_prot}", count=num_pkts, timeout=tiempo_limite)
        
        # Procesar y mostrar los paquetes capturados
        count = 1
        for pkt in pkts:
            print(colored(f"Paquete {count} --> ", 'cyan'))
            print(pkt.summary())
            # pkt.show()
            # Guardar la información en el log
            logging.info(pkt.summary())
            if callback: #Si callback es distinto a None
                callback(pkt)
            count += 1

    except Exception as e:
        print(colored(f"Error al capturar paquetes: {e}", 'red'))

# Función para captura continua de paquetes
def captura_continua(iface="Wi-Fi", filtro_prot="tcp", callback=None):
    print(colored(f"Iniciando la captura continua en {iface} con filtro {filtro_prot}...", 'magenta'))
    
    capturar_paquetes(iface=iface, filtro_prot=filtro_prot, num_pkts=10000, tiempo_limite=None, callback=callback)

# Función para monitorear la actividad de red
def monitorear_red(iface="Wi-Fi", num_pkts=100, tiempo_limite=60, filtro_prot="tcp"):
    print(colored(f"Monitoreando tráfico en {iface} durante {tiempo_limite} segundos con filtro {filtro_prot}...", 'blue'))
    
    # Generar archivo donde guardamos la captura
    configurar_log()
    
    # Capturar paquetes según los parámetros
    capturar_paquetes(iface=iface, filtro_prot=filtro_prot, num_pkts=num_pkts, tiempo_limite=tiempo_limite)
    print(colored("La captura de tráfico ha finalizado.", 'green'))

# Función para hacer pruebas
if __name__ == "__main__":
    print(colored("Iniciando la captura de tráfico...", 'magenta'))
    
    # Configurar y capturar tráfico
    iface = "Wi-Fi"  # interfaz usada
    num_pkts = 20    # Número de paquetes a capturar
    tiempo_limite = 60  # Tiempo límite en segundos
    filtro_prot = "tcp or udp"  # Filtrar por TCP y UDP
    
    # Monitorear tráfico
    monitorear_red(iface=iface, num_pkts=num_pkts, tiempo_limite=tiempo_limite, filtro_prot=filtro_prot)
    # captura_continua(iface, filtro_prot)