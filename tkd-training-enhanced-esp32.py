import sys
import os
import network
import ubinascii
import machine
from machine import Pin, PWM
import urequests as requests
import ujson
import time
import utime
from secrets import secrets
from Wifi_lib import wifi_init

# Inicializar la conexión Wi-Fi
wifi_init()

# Configuración específica para ESP32
# Pulsadores para diferentes zonas
pulsador_cabeza = Pin(32, Pin.IN, Pin.PULL_UP)
pulsador_torso = Pin(33, Pin.IN, Pin.PULL_UP)
pulsador_pierna_izq = Pin(25, Pin.IN, Pin.PULL_UP)
pulsador_pierna_der = Pin(26, Pin.IN, Pin.PULL_UP)

# Botones de control
button_inicio = Pin(27, Pin.IN, Pin.PULL_UP)
button_fin = Pin(14, Pin.IN, Pin.PULL_UP)
button_modo = Pin(13, Pin.IN, Pin.PULL_UP)  # Nuevo botón para cambiar modo

# LED RGB - Ajustar estos pines según tu conexión
led_r = PWM(Pin(4), freq=5000)  # Canal rojo
led_g = PWM(Pin(16), freq=5000) # Canal verde
led_b = PWM(Pin(17), freq=5000) # Canal azul

# Variables de configuración
url = "http://192.168.86.25/registrar_golpe.php"
ID_USUARIO = 1

# Constantes para colores RGB (0-1023 para ESP32)
COLORS = {
    'red': (1023, 0, 0),
    'green': (0, 1023, 0),
    'blue': (0, 0, 1023),
    'yellow': (1023, 1023, 0),
    'off': (0, 0, 0)
}

# Mapeo de zonas a colores
ZONE_COLORS = {
    'Cabeza': 'red',
    'Torso': 'blue',
    'Pierna Izquierda': 'green',
    'Pierna Derecha': 'yellow'
}

def set_rgb_color(color_name):
    """Establece el color del LED RGB"""
    r, g, b = COLORS[color_name]
    led_r.duty(r)
    led_g.duty(g)
    led_b.duty(b)

class TrainingMode:
    NORMAL = 0
    REACTION = 1
    SEQUENCE = 2

# Variables de estado
current_mode = TrainingMode.NORMAL
sesion_activa = False
id_sesion_actual = None
tiempo_inicio_sesion = 0
contador_golpes = 0
ultima_lectura = {}
DEBOUNCE_TIME = 300

# Variables para modos de entrenamiento
target_zone = None
reaction_start_time = 0
current_sequence = []
target_sequence = []
sequence_index = 0

def iniciar_sesion():
    """Inicia una nueva sesión de entrenamiento"""
    datos = {
        "tipo": "nueva_sesion",
        "id_usuario": ID_USUARIO,
        "tipo_sesion": "Entrenamiento"
    }
    try:
        response = requests.post(url, json=datos)
        resultado = response.json()
        response.close()
        return resultado.get("id_sesion")
    except Exception as e:
        print("Error al iniciar sesión:", e)
        return None

def registrar_golpe(zona):
    """Registra un golpe en la base de datos"""
    global contador_golpes
    datos = {
        "tipo": "punto_registrado",
        "id_sesion": id_sesion_actual,
        "lugar_golpe": zona
    }
    try:
        response = requests.post(url, json=datos)
        response.close()
        contador_golpes += 1
        print(f"Golpe registrado en {zona}")
    except Exception as e:
        print("Error al registrar golpe:", e)

def registrar_tiempo_reaccion(zona, tiempo):
    """Registra el tiempo de reacción en la base de datos"""
    datos = {
        "tipo": "tiempo_reaccion",
        "id_sesion": id_sesion_actual,
        "zona_objetivo": zona,
        "tiempo_reaccion": tiempo
    }
    try:
        response = requests.post(url, json=datos)
        response.close()
    except Exception as e:
        print("Error al registrar tiempo de reacción:", e)

def registrar_secuencia(seq_objetivo, seq_real, errores):
    """Registra una secuencia completada en la base de datos"""
    datos = {
        "tipo": "secuencia",
        "id_sesion": id_sesion_actual,
        "secuencia_objetivo": ",".join(seq_objetivo),
        "secuencia_real": ",".join(seq_real),
        "errores": errores
    }
    try:
        response = requests.post(url, json=datos)
        response.close()
    except Exception as e:
        print("Error al registrar secuencia:", e)

def finalizar_sesion():
    """Finaliza la sesión actual"""
    datos = {
        "tipo": "actualizar_sesion",
        "id_sesion": id_sesion_actual,
        "numero_golpes": contador_golpes
    }
    try:
        response = requests.post(url, json=datos)
        response.close()
    except Exception as e:
        print("Error al finalizar sesión:", e)

def generate_random_sequence(length=3):
    """Genera una secuencia aleatoria de zonas"""
    zonas = list(ZONE_COLORS.keys())
    return [zonas[utime.ticks_ms() % len(zonas)] for _ in range(length)]

def modo_reaccion():
    """Maneja el modo de entrenamiento de tiempo de reacción"""
    global target_zone, reaction_start_time
    
    if target_zone is None:
        # Seleccionar nueva zona objetivo
        zonas = list(ZONE_COLORS.keys())
        target_zone = zonas[utime.ticks_ms() % len(zonas)]
        set_rgb_color(ZONE_COLORS[target_zone])
        reaction_start_time = utime.ticks_ms()
        print(f"¡Golpea {target_zone}!")
        return
    
    # Verificar si se golpeó la zona correcta
    tiempo_actual = utime.ticks_ms()
    if check_hit(target_zone, tiempo_actual):
        tiempo_reaccion = (tiempo_actual - reaction_start_time) / 1000.0
        print(f"¡Bien! Tiempo: {tiempo_reaccion:.2f} segundos")
        registrar_tiempo_reaccion(target_zone, tiempo_reaccion)
        target_zone = None
        set_rgb_color('off')
        utime.sleep_ms(500)

def modo_secuencia():
    """Maneja el modo de entrenamiento de secuencias"""
    global target_sequence, current_sequence, sequence_index
    
    if not target_sequence:
        # Iniciar nueva secuencia
        target_sequence = generate_random_sequence()
        current_sequence = []
        sequence_index = 0
        print("Nueva secuencia:", " → ".join(target_sequence))
        # Mostrar primer objetivo
        set_rgb_color(ZONE_COLORS[target_sequence[0]])
        return
    
    # Verificar golpes
    tiempo_actual = utime.ticks_ms()
    for zona in ZONE_COLORS.keys():
        if check_hit(zona, tiempo_actual):
            current_sequence.append(zona)
            if zona == target_sequence[sequence_index]:
                sequence_index += 1
                if sequence_index < len(target_sequence):
                    # Mostrar siguiente objetivo
                    set_rgb_color(ZONE_COLORS[target_sequence[sequence_index]])
                else:
                    # Secuencia completada
                    errores = sum(1 for a, b in zip(target_sequence, current_sequence) if a != b)
                    print(f"Secuencia completada. Errores: {errores}")
                    registrar_secuencia(target_sequence, current_sequence, errores)
                    target_sequence = []
                    set_rgb_color('off')
                    utime.sleep_ms(1000)

def check_hit(zona, tiempo_actual):
    """Verifica si se ha golpeado una zona específica"""
    pulsador = None
    if zona == "Cabeza":
        pulsador = pulsador_cabeza
    elif zona == "Torso":
        pulsador = pulsador_torso
    elif zona == "Pierna Izquierda":
        pulsador = pulsador_pierna_izq
    elif zona == "Pierna Derecha":
        pulsador = pulsador_pierna_der
    
    if pulsador and not pulsador.value():
        if zona not in ultima_lectura or \
           (tiempo_actual - ultima_lectura[zona]) > DEBOUNCE_TIME:
            ultima_lectura[zona] = tiempo_actual
            return True
    return False

# Bucle principal
print("Iniciando sistema de entrenamiento...")
print("Presione el botón de inicio para comenzar una sesión")
print("Use el botón de modo para cambiar entre modos de entrenamiento")

while True:
    if not button_inicio.value() and not sesion_activa:
        # Iniciar nueva sesión
        id_sesion_actual = iniciar_sesion()
        if id_sesion_actual:
            sesion_activa = True
            tiempo_inicio_sesion = time.time()
            contador_golpes = 0
            print("Sesión iniciada:", id_sesion_actual)
            print("Modo actual: Normal")
    
    if sesion_activa:
        # Cambiar modo con button_modo
        if not button_modo.value():
            current_mode = (current_mode + 1) % 3
            modes = ['Normal', 'Reacción', 'Secuencia']
            print(f"Modo cambiado a: {modes[current_mode]}")
            target_zone = None
            target_sequence = []
            set_rgb_color('off')
            utime.sleep_ms(500)
        
        if current_mode == TrainingMode.NORMAL:
            # Modo normal
            tiempo_actual = utime.ticks_ms()
            for zona, pulsador in [
                ("Cabeza", pulsador_cabeza),
                ("Torso", pulsador_torso),
                ("Pierna Izquierda", pulsador_pierna_izq),
                ("Pierna Derecha", pulsador_pierna_der)
            ]:
                if check_hit(zona, tiempo_actual):
                    registrar_golpe(zona)
        
        elif current_mode == TrainingMode.REACTION:
            modo_reaccion()
        
        elif current_mode == TrainingMode.SEQUENCE:
            modo_secuencia()
        
        # Verificar fin de sesión
        if not button_fin.value():
            finalizar_sesion()
            sesion_activa = False
            set_rgb_color('off')
            print("Sesión finalizada. Total golpes:", contador_golpes)
            utime.sleep(1)
    
    utime.sleep_ms(20)
