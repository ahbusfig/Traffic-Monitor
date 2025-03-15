from src.analysis import *
from src.capture import *
from termcolor import colored
import argparse
import os

def main():
    #Parser principal del programa
    parser = argparse.ArgumentParser(description="Analizador de trafico capturado")

    #Creamos los subparser para cada funcion que queremos (capturar,analizar, captura y analizar in real time)
    subparsers = parser.add_subparsers(dest="accion", help="Selecciona una accion (captura,analizar,continua)") 
    # Subcomando para capturar tráfico de red
    parser_capture = subparsers.add_parser('captura', help="Captura tráfico de red y guarda log")
    parser_capture.add_argument('--iface', type=str, default="Wi-Fi", help="Interfaz de red a usar (por defecto: 'Wi-Fi')")
    parser_capture.add_argument('--filtro', type=str, default="tcp", help="Filtro de protocolo (por defecto: 'tcp')")
    parser_capture.add_argument('--num_pkts', type=int, default=20, help="Número de paquetes a capturar (por defecto: 100)")
    parser_capture.add_argument('--tiempo', type=int, default=60, help="Tiempo límite de captura en segundos (por defecto: 60)")

    # Subcomando para analizar los logs guardados
    parser_analysis = subparsers.add_parser('analizar', help="Analiza los logs capturados previamente")
    parser_analysis.add_argument('log_file', type=str, help="Ruta del archivo de log a analizar")

    # Subcomando para captura continua en tiempo real
    parser_continua = subparsers.add_parser('continua', help="analiza tráfico en tiempo real")
    parser_continua.add_argument('--iface', type=str, default="Wi-Fi", help="Interfaz de red a usar (por defecto: 'Wi-Fi')")
    parser_continua.add_argument('--filtro', type=str, default="tcp", help="Filtro de protocolo (por defecto: 'tcp')")

    args = parser.parse_args()

    # Acción según el subcomando elegido
    if args.accion == 'captura':
        print(colored(f"Capturando tráfico en la interfaz {args.iface} con filtro {args.filtro}...", 'blue'))
        monitorear_red(iface=args.iface, filtro_prot=args.filtro, num_pkts=args.num_pkts, tiempo_limite=args.tiempo)

    elif args.accion == 'analizar':
        log_file_path = os.path.join(os.path.dirname(__file__), 'logs', args.log_file)
        print(colored(f"Analizando archivo de log: {log_file_path}...", 'green'))
        analizar_archivo_log(log_file_path)

    elif args.accion == 'continua':
        print(colored(f"\nPara parar la captura y analisis in real time --> ctrl + c\n","red"))
        analizar_continua(iface=args.iface, filtro_prot=args.filtro)

    else:
        print(colored("Opción no válida. Usa 'captura', 'analizar' o 'continua'.", 'red'))

if __name__ == "__main__":
    main()