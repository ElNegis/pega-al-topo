Sistema de Entrenamiento en Taekwondo
Este proyecto está diseñado para proporcionar una experiencia interactiva de entrenamiento en Taekwondo, utilizando sensores y un dispositivo de microcontrolador (como ESP32 o Raspberry Pi Pico W) que detecta golpes en diferentes zonas y mide el tiempo de reacción del usuario. Además, el dispositivo se conecta a una red Wi-Fi para enviar datos al servidor, permitiendo el seguimiento y análisis de los entrenamientos.

Tabla de Contenidos
Descripción del Proyecto
Características
Componentes del Proyecto
Requisitos
Configuración
Uso
Flujo de Datos
Licencia
Descripción del Proyecto
Este sistema de entrenamiento en Taekwondo permite que los usuarios practiquen golpes en diferentes zonas (cabeza, torso, pierna izquierda y pierna derecha) a través de tres modos de entrenamiento: Modo Normal, Modo de Reacción y Modo de Secuencia. Al detectar golpes, el dispositivo registra y envía los datos a un servidor para un análisis más profundo y seguimiento del progreso del usuario.

Características
Modos de Entrenamiento:
Modo Normal: Registra golpes en zonas específicas.
Modo de Reacción: Mide el tiempo de reacción al golpear una zona objetivo.
Modo de Secuencia: Genera secuencias de zonas para ser golpeadas en un orden específico.
Conectividad Wi-Fi: Envía datos a un servidor para su almacenamiento y análisis.
Indicador Visual: Utiliza un LED RGB para señalar la zona objetivo en algunos modos.
Componentes del Proyecto
tkd_training-enhanced-esp32.py: Script principal que gestiona los modos de entrenamiento, registra golpes, tiempos y secuencias, y envía los datos al servidor.
Wifi_lib.py: Biblioteca de configuración de Wi-Fi, que conecta el dispositivo a la red.
secrets.py: Archivo que contiene las credenciales Wi-Fi.
Servidor: Backend configurado para recibir y almacenar los datos enviados por el dispositivo.
Requisitos
Hardware:
Microcontrolador ESP32 o Raspberry Pi Pico W.
Sensores para detectar golpes en distintas zonas.
LED RGB (opcional, para indicar zonas de golpeo).
Software:
Python MicroPython (firmware para ESP32 o Raspberry Pi Pico W).
Archivo secrets.py con las credenciales Wi-Fi.
Servidor backend para almacenar y analizar los datos.
Configuración
Instala MicroPython en tu dispositivo de microcontrolador (ESP32 o Raspberry Pi Pico W).

Configura el Wi-Fi:

En secrets.py, define el SSID y la password de la red Wi-Fi:

python
Copiar código
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