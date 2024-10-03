from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite la comunicación entre frontend y backend

# Función para conectar a la base de datos en XAMPP
def conectar():
    conexion = mysql.connector.connect(
        host="localhost",          # Cambia según la configuración de tu XAMPP
        user="root",               # Usuario de MySQL (root es el predeterminado en XAMPP)
        password="",               # Contraseña de MySQL (vacía por defecto en XAMPP)
        database="topos_game"      # Base de datos que creaste
    )
    return conexion

# Ruta para guardar el juego en la base de datos
@app.route('/guardar_juego', methods=['POST'])
def guardar_juego():
    datos = request.json
    nombre = datos.get('nombre')
    golpes = datos.get('golpes')
    no_golpeados = datos.get('no_golpeados')
    tiempo = datos.get('tiempo')

    # Guardar en la base de datos
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Calcular promedio de tiempo de respuesta (aquí lo asumimos como el tiempo total dividido entre golpes)
    if golpes > 0:
        promedio_respuesta = tiempo / golpes
    else:
        promedio_respuesta = 0

    # Insertar los datos en la tabla jugadores
    sql = "INSERT INTO jugadores (nombre, golpes, no_golpeados, promedio_respuesta, fecha) VALUES (%s, %s, %s, %s, %s)"
    valores = (nombre, golpes, no_golpeados, promedio_respuesta, datetime.now())
    cursor.execute(sql, valores)
    
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"status": "Datos guardados correctamente"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=3306)
