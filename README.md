# 🛠️ Herramienta de Análisis de Tráfico de Red 🚦

**Herramienta de Análisis de Tráfico de Red** es una solución potente y flexible para capturar paquetes de red, analizar tráfico y detectar patrones en logs de red. Diseñada para ser fácil de usar, permite tanto la captura en tiempo real como el análisis de logs previamente capturados.

---

## 🚀 Instalación

Sigue estos pasos para configurar el proyecto en tu entorno local:

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```

2. **Instala las dependencias**:

   Asegúrate de tener `Python 3.x` instalado y luego ejecuta:

   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Uso

La herramienta se ejecuta desde la línea de comandos y ofrece tres modos principales:

### 1. **Captura de tráfico de red** 🌐

Captura paquetes de red en tiempo real según los parámetros especificados.

```bash
python main.py captura --iface "Wi-Fi" --filtro "tcp" --num_pkts 100 --tiempo 60
```

#### Opciones:
- `--iface`: Interfaz de red a usar (por defecto: `Wi-Fi`).
- `--filtro`: Filtro de protocolo (por defecto: `tcp`).
- `--num_pkts`: Número de paquetes a capturar (por defecto: `100`).
- `--tiempo`: Tiempo límite de captura en segundos (por defecto: `60`).

---

### 2. **Análisis de archivo de log** 📊

Analiza logs de tráfico previamente capturados.

```bash
python main.py analizar Logs/Log_13-03-2025_PmCQRd.log
```

#### Parámetros:
- `log_file`: nombre del archivo de log a analizar.

---

### 3. **Captura continua en tiempo real** ⏱️

Inicia una captura continua de tráfico en tiempo real.

```bash
python main.py continua --iface "Wi-Fi" --filtro "tcp"
```

#### Opciones:
- `--iface`: Interfaz de red a usar (por defecto: `Wi-Fi`).
- `--filtro`: Filtro de protocolo (por defecto: `tcp`).

---

## 📋 Requisitos

- **Python 3.x**
- Bibliotecas requeridas (instaladas automáticamente con `requirements.txt`):
  - `scapy`
  - `termcolor`
  - `argparse`
  - `os` 

---
