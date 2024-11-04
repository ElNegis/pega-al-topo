from flask import Flask, render_template, jsonify, request
import mysql.connector
import plotly.graph_objs as go
import plotly.io as pio
import plotly.express as px
from datetime import datetime, timedelta

# Inicializar la aplicación Flask
app = Flask(__name__)

def conectar():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="BD_Taekwondo"
    )
    return conexion

def obtener_usuarios():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuario, CONCAT(nombre, ' ', apellidos) as nombre_completo FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [{"id": u[0], "nombre": u[1]} for u in usuarios]

def obtener_datos_sesiones_por_usuario(atleta=None, fecha_inicio=None, fecha_fin=None):
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT 
        u.nombre, 
        u.apellidos, 
        COUNT(s.id_sesion) AS num_sesiones,
        s.tipo_sesion,
        DATE_FORMAT(s.fecha_sesion, '%Y-%m') as mes
    FROM usuarios u
    LEFT JOIN sesiones s ON u.id_usuario = s.id_usuario
    WHERE 1=1
    """
    
    params = []
    if atleta:
        sql += " AND u.id_usuario = %s"
        params.append(atleta)
    if fecha_inicio and fecha_fin:
        sql += " AND s.fecha_sesion BETWEEN %s AND %s"
        params.extend([fecha_inicio, fecha_fin])
    
    sql += " GROUP BY u.id_usuario, s.tipo_sesion, mes"
    
    cursor.execute(sql, params)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    return resultados

def obtener_datos_velocidad_reaccion(atleta=None, fecha_inicio=None, fecha_fin=None):
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT 
        s.id_sesion,
        u.nombre,
        u.apellidos,
        DATE_FORMAT(s.fecha_sesion, '%Y-%m-%d') as fecha,
        AVG(vr.tiempo_reaccion) AS avg_reaccion,
        MIN(vr.tiempo_reaccion) AS min_reaccion,
        MAX(vr.tiempo_reaccion) AS max_reaccion,
        COUNT(vr.id_reaccion) AS total_intentos
    FROM sesiones s
    JOIN usuarios u ON s.id_usuario = u.id_usuario
    LEFT JOIN velocidad_reaccion vr ON s.id_sesion = vr.id_sesion
    WHERE vr.tiempo_reaccion IS NOT NULL
    """
    
    params = []
    if atleta:
        sql += " AND u.id_usuario = %s"
        params.append(atleta)
    if fecha_inicio and fecha_fin:
        sql += " AND s.fecha_sesion BETWEEN %s AND %s"
        params.extend([fecha_inicio, fecha_fin])
    
    sql += " GROUP BY s.id_sesion ORDER BY s.fecha_sesion"
    
    cursor.execute(sql, params)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    return resultados

def obtener_datos_golpes(atleta=None, fecha_inicio=None, fecha_fin=None):
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT 
        pr.lugar_golpe,
        COUNT(pr.id_punto) AS num_golpes,
        u.nombre,
        u.apellidos,
        DATE_FORMAT(s.fecha_sesion, '%Y-%m-%d') as fecha
    FROM puntos_registrados pr
    JOIN sesiones s ON pr.id_sesion = s.id_sesion
    JOIN usuarios u ON s.id_usuario = u.id_usuario
    WHERE 1=1
    """
    
    params = []
    if atleta:
        sql += " AND u.id_usuario = %s"
        params.append(atleta)
    if fecha_inicio and fecha_fin:
        sql += " AND s.fecha_sesion BETWEEN %s AND %s"
        params.extend([fecha_inicio, fecha_fin])
    
    sql += " GROUP BY pr.lugar_golpe, u.id_usuario, DATE_FORMAT(s.fecha_sesion, '%Y-%m-%d')"
    
    cursor.execute(sql, params)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    return resultados

def obtener_progreso_atleta(atleta=None, fecha_inicio=None, fecha_fin=None):
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    SELECT 
        u.nombre,
        u.apellidos,
        DATE_FORMAT(s.fecha_sesion, '%Y-%m-%d') as fecha,
        COUNT(DISTINCT s.id_sesion) as num_sesiones,
        AVG(vr.tiempo_reaccion) as avg_velocidad,
        SUM(seq.errores) as total_errores,
        COUNT(pr.id_punto) as total_golpes
    FROM usuarios u
    LEFT JOIN sesiones s ON u.id_usuario = s.id_usuario
    LEFT JOIN velocidad_reaccion vr ON s.id_sesion = vr.id_sesion
    LEFT JOIN secuencias seq ON s.id_sesion = seq.id_sesion
    LEFT JOIN puntos_registrados pr ON s.id_sesion = pr.id_sesion
    WHERE 1=1
    """
    
    params = []
    if atleta:
        sql += " AND u.id_usuario = %s"
        params.append(atleta)
    if fecha_inicio and fecha_fin:
        sql += " AND s.fecha_sesion BETWEEN %s AND %s"
        params.extend([fecha_inicio, fecha_fin])
    
    sql += " GROUP BY u.id_usuario, DATE_FORMAT(s.fecha_sesion, '%Y-%m-%d')"
    
    cursor.execute(sql, params)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    return resultados

@app.route('/')
def index():
    usuarios = obtener_usuarios()
    return render_template('index.html', usuarios=usuarios)

@app.route('/datos_grafico', methods=['GET'])
def datos_grafico():
    atleta = request.args.get('atleta')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    atleta = int(atleta) if atleta else None

    # Obtener datos para todos los gráficos
    datos_sesiones = obtener_datos_sesiones_por_usuario(atleta, fecha_inicio, fecha_fin)
    datos_velocidad = obtener_datos_velocidad_reaccion(atleta, fecha_inicio, fecha_fin)
    datos_golpes = obtener_datos_golpes(atleta, fecha_inicio, fecha_fin)
    datos_progreso = obtener_progreso_atleta(atleta, fecha_inicio, fecha_fin)

    # 1. Gráfico de sesiones mejorado (ahora con tipos de sesión)
    sesiones_data = []
    for tipo in ['Entrenamiento', 'Competencia']:
        sesiones_data.append(
            go.Bar(
                name=tipo,
                x=[f"{r[0]} {r[1]}" for r in datos_sesiones if r[3] == tipo],
                y=[r[2] for r in datos_sesiones if r[3] == tipo]
            )
        )
    
    fig_sesiones = go.Figure(data=sesiones_data)
    fig_sesiones.update_layout(
        title='Sesiones por Usuario y Tipo',
        barmode='group',
        xaxis_title='Atleta',
        yaxis_title='Número de Sesiones'
    )

    # 2. Gráfico de velocidad de reacción mejorado
    fig_velocidad = go.Figure()
    
    for resultado in datos_velocidad:
        nombre = f"{resultado[1]} {resultado[2]}"
        fig_velocidad.add_trace(go.Scatter(
            x=[resultado[3]],
            y=[resultado[4]],
            name=nombre,
            mode='lines+markers',
            error_y=dict(
                type='data',
                symmetric=False,
                array=[resultado[6] - resultado[4]],  # max - avg
                arrayminus=[resultado[4] - resultado[5]],  # avg - min
            )
        ))
    
    fig_velocidad.update_layout(
        title='Velocidad de Reacción por Sesión',
        xaxis_title='Fecha',
        yaxis_title='Tiempo de Reacción (s)',
        showlegend=True
    )

    # 3. Distribución de golpes mejorada
    golpes_por_zona = {}
    for g in datos_golpes:
        if g[0] not in golpes_por_zona:
            golpes_por_zona[g[0]] = 0
        golpes_por_zona[g[0]] += g[1]

    fig_golpes = go.Figure(data=[
        go.Pie(
            labels=list(golpes_por_zona.keys()),
            values=list(golpes_por_zona.values()),
            hole=.3
        )
    ])
    fig_golpes.update_layout(
        title='Distribución de Golpes por Zona',
        annotations=[dict(text='Total', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )

    # 4. Nuevo gráfico: Progreso del atleta
    fig_progreso = go.Figure()
    
    if datos_progreso:
        fechas = [r[2] for r in datos_progreso]
        fig_progreso.add_trace(go.Scatter(
            x=fechas,
            y=[r[4] for r in datos_progreso],
            name='Velocidad Promedio',
            yaxis='y1'
        ))
        fig_progreso.add_trace(go.Bar(
            x=fechas,
            y=[r[6] for r in datos_progreso],
            name='Total Golpes',
            yaxis='y2'
        ))
        
        fig_progreso.update_layout(
            title='Progreso del Atleta',
            xaxis_title='Fecha',
            yaxis=dict(
                title='Velocidad (s)',
                titlefont=dict(color="#1f77b4"),
                tickfont=dict(color="#1f77b4")
            ),
            yaxis2=dict(
                title='Número de Golpes',
                titlefont=dict(color="#ff7f0e"),
                tickfont=dict(color="#ff7f0e"),
                anchor="x",
                overlaying="y",
                side="right"
            )
        )

    # Convertir las gráficas a JSON
    graph_json = {
        "sesiones_por_usuario": pio.to_json(fig_sesiones),
        "velocidad_reaccion": pio.to_json(fig_velocidad),
        "distribucion_golpes": pio.to_json(fig_golpes),
        "progreso_atleta": pio.to_json(fig_progreso)
    }

    return jsonify(graph_json)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5003)