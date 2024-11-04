# Sistema de Entrenamiento en Taekwondo 🥋

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![MicroPython](https://img.shields.io/badge/MicroPython-Compatible-green.svg)](https://micropython.org/)

Un sistema interactivo de entrenamiento en Taekwondo que utiliza sensores y microcontroladores para detectar golpes, medir tiempos de reacción y realizar seguimiento del progreso del deportista en tiempo real.

## 📝 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Componentes](#componentes)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Modos de Entrenamiento](#modos-de-entrenamiento)
- [Diagrama de Flujo](#diagrama-de-flujo)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## 📖 Descripción

Este innovador sistema de entrenamiento en Taekwondo permite a los practicantes mejorar sus habilidades a través de diferentes modos de entrenamiento interactivo. Mediante sensores estratégicamente ubicados, el sistema detecta golpes en zonas específicas (cabeza, torso, pierna izquierda y derecha), registra tiempos de reacción y envía datos en tiempo real a un servidor para análisis posteriores.

## ✨ Características

### 🎯 Modos de Entrenamiento
- **Modo Normal**: Registro preciso de golpes en zonas específicas
- **Modo de Reacción**: Medición de tiempos de respuesta
- **Modo de Secuencia**: Práctica de combinaciones predefinidas

### 🔧 Características Técnicas
- Conectividad Wi-Fi para transmisión de datos en tiempo real
- Sistema de LED RGB para indicación visual de objetivos
- Almacenamiento y análisis de datos en la nube
- Compatible con ESP32 y Raspberry Pi Pico W

## 🛠 Componentes

El proyecto está compuesto por los siguientes archivos principales:

```
├── tkd_training-enhanced-esp32.py   # Script principal
├── Wifi_lib.py                      # Configuración Wi-Fi
├── secrets.py                       # Credenciales Wi-Fi
└── server/                          # Backend para datos
```

## 📋 Requisitos

### Hardware
- Microcontrolador ESP32
- Sensores de impacto
- LED RGB
- Cables y conectores
- Fuente de alimentación

### Software
- MicroPython
- Python 3.7+
- php para la conexion con el web service y html para el template del dash

## 🚀 Instalación

1. **Preparación del Microcontrolador**
```bash
# Instalar MicroPython en el dispositivo
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 write_flash -z 0x1000 micropython_firmware.bin
```

2. **Configuración Wi-Fi**
```python
# En secrets.py
secrets = {
    'ssid': 'tu_red_wifi',
    'password': 'tu_contraseña_wifi'
}
Copia los archivos tkd_training-enhanced-esp32.py, Wifi_lib.py y secrets.py al microcontrolador.

Configura el servidor backend para recibir y almacenar los datos enviados por el dispositivo.

Uso
Iniciar el dispositivo: Al encender el dispositivo, este se conectará a la red Wi-Fi usando la configuración en Wifi_lib.py.
Comenzar una sesión de entrenamiento:
Presiona el botón de inicio para activar la sesión.
Selecciona el modo de entrenamiento deseado presionando el botón de modo.
Registrar los golpes y tiempos de reacción:
Dependiendo del modo seleccionado, golpea las zonas específicas cuando el LED RGB lo indique.
Finalizar la sesión:
Cuando termines la sesión de entrenamiento, presiona el botón de finalización para que el dispositivo envíe un resumen al servidor.
Modos de Entrenamiento
Modo Normal: Registra los golpes en cada zona y envía la información al servidor.
Modo de Reacción: Mide el tiempo que el usuario tarda en golpear una zona indicada al azar.
Modo de Secuencia: Genera una secuencia de zonas para golpear en el orden correcto.
Flujo de Datos
Inicio del dispositivo:
Configura la conexión Wi-Fi.
Envía una solicitud de inicio de sesión al servidor.
Entrenamiento:
Durante el entrenamiento, registra golpes, tiempos de reacción, y secuencias.
Envía estos datos al servidor en tiempo real.
Fin de la sesión:
Envía un resumen de la sesión al servidor.
Licencia
Este proyecto está bajo la licencia MIT.
