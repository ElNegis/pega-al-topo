from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permitir acceso entre dominios (frontend -> backend)

# Función para conectarse a la base de datos
def conectar():
    return mysql.connector.connect(
        host="localhost",      # XAMPP generalmente usa localhost para MySQL
        user="root",           # El usuario por defecto en XAMPP es 'root'
        password="",           # XAMPP por defecto no tiene contraseña para MySQL
        database="topos_game", # Asegúrate de que esta base de datos existe
        port=3306            # Especificar el puerto (3306 es el predeterminado)
    )

# Ruta para recibir los datos del juego y guardarlos en la base de datos
@app.route('/guardar_juego', methods=['POST'])
def guardar_juego():
    data = request.json
    nombre = data['nombre']
    golpes = data['golpes']
    no_golpeados = data['no_golpeados']
    tiempo = data['tiempo']

    conexion = conectar()
    cursor = conexion.cursor()

    # Insertar los datos del jugador en la tabla "jugadores"
    sql = "INSERT INTO jugadores (nombre, golpes, no_golpeados, promedio_respuesta, fecha) VALUES (%s, %s, %s, %s, %s)"
    valores = (nombre, golpes, no_golpeados, tiempo, datetime.now())
    cursor.execute(sql, valores)

    # Confirmar los cambios
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"status": "success", "message": "Datos guardados correctamente"})

if __name__ == '__main__':
    app.run(debug=True)
