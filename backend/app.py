from flask import Flask, render_template, request, jsonify
import mysql.connector
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Función para conectarse a la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",      
            user="root",           
            password="",           
            database="golpear_topo",  # Asegúrate de que este sea el nombre correcto de tu base de datos
        )
        print("Conexión exitosa a la base de datos")  # Mensaje de éxito en la conexión
        return conexion
    except mysql.connector.Error as err:
        print(f"Error conectándose a la base de datos: {err}")  # Mensaje de error si la conexión falla
        return None

# Ruta raíz para servir el archivo index.html
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para servir la página dashboard.html
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Ruta para obtener datos del jugador para el gráfico de torta
@app.route('/datos_jugador', methods=['POST'])
def datos_jugador():
    data = request.json
    nombre = data['nombre']

    conexion = conectar()
    if conexion is None:
        return jsonify({"status": "error", "message": "No se pudo conectar a la base de datos"})

    cursor = conexion.cursor()

    try:
        # Obtener el ID del jugador por su nombre
        cursor.execute("SELECT id_jugador FROM jugadores WHERE nombre = %s", (nombre,))
        jugador = cursor.fetchone()

        if jugador is None:
            return jsonify({"status": "error", "message": "Jugador no encontrado"})
        
        id_jugador = jugador[0]

        # Obtener la suma de topos golpeados y no golpeados del jugador
        cursor.execute("""
            SELECT SUM(golpes), SUM(no_golpeados)
            FROM resultados
            WHERE id_jugador = %s
        """, (id_jugador,))
        resultado = cursor.fetchone()

        if resultado:
            golpes = resultado[0] or 0
            no_golpeados = resultado[1] or 0
            return jsonify({
                "status": "success",
                "golpes": golpes,
                "no_golpeados": no_golpeados
            })
        else:
            return jsonify({"status": "error", "message": "No se encontraron resultados para este jugador"})

    except mysql.connector.Error as err:
        print(f"Error en la base de datos: {err}")
        return jsonify({"status": "error", "message": str(err)})

    finally:
        cursor.close()
        conexion.close()

# Nueva ruta para obtener datos de todos los jugadores, filtrado por fecha
@app.route('/datos_jugadores_fecha', methods=['POST'])
def datos_jugadores_fecha():
    data = request.json
    fecha = data['fecha']

    conexion = conectar()
    if conexion is None:
        return jsonify({"status": "error", "message": "No se pudo conectar a la base de datos"})

    cursor = conexion.cursor()

    try:
        # Obtener los datos de todos los jugadores filtrados por la fecha
        cursor.execute("""
            SELECT j.nombre, SUM(r.golpes), SUM(r.no_golpeados)
            FROM jugadores j
            JOIN resultados r ON j.id_jugador = r.id_jugador
            JOIN partidas p ON r.id_partida = p.id_partida
            WHERE DATE(p.fecha) = %s
            GROUP BY j.nombre
        """, (fecha,))
        resultados = cursor.fetchall()

        if resultados:
            jugadores = []
            golpes = []
            no_golpeados = []
            for resultado in resultados:
                jugadores.append(resultado[0])
                golpes.append(resultado[1] or 0)
                no_golpeados.append(resultado[2] or 0)

            return jsonify({
                "status": "success",
                "jugadores": jugadores,
                "golpes": golpes,
                "no_golpeados": no_golpeados
            })
        else:
            return jsonify({"status": "error", "message": "No se encontraron resultados para esta fecha"})

    except mysql.connector.Error as err:
        print(f"Error en la base de datos: {err}")
        return jsonify({"status": "error", "message": str(err)})

    finally:
        cursor.close()
        conexion.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
