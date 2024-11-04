-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS BD_Taekwondo;
USE BD_Taekwondo;

-- Eliminar las tablas si existen para evitar conflictos
DROP TABLE IF EXISTS secuencias;
DROP TABLE IF EXISTS velocidad_reaccion;
DROP TABLE IF EXISTS puntos_registrados;
DROP TABLE IF EXISTS sesiones;
DROP TABLE IF EXISTS usuarios;

-- Tabla de usuarios (atletas)
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de sesiones (entrenamientos o competencias)
CREATE TABLE sesiones (
    id_sesion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    tipo_sesion VARCHAR(50) NOT NULL,  -- 'Entrenamiento' o 'Competencia'
    fecha_sesion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    numero_golpes INT DEFAULT 0,  -- Número total de golpes en la sesión
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Tabla de puntos registrados (dónde y cuándo se golpeó)
CREATE TABLE puntos_registrados (
    id_punto INT AUTO_INCREMENT PRIMARY KEY,
    id_sesion INT,
    lugar_golpe VARCHAR(50) NOT NULL,  -- Ejemplo: 'Cabeza', 'Torso', 'Pierna Izquierda'
    tiempo_registrado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sesion) REFERENCES sesiones(id_sesion)
);

-- Tabla de velocidad de reacción (cuánto tiempo tardó en golpear)
CREATE TABLE velocidad_reaccion (
    id_reaccion INT AUTO_INCREMENT PRIMARY KEY,
    id_sesion INT,
    zona_objetivo VARCHAR(50) NOT NULL,  -- Zona a la que el sistema pidió golpear
    tiempo_reaccion DECIMAL(5,2) NOT NULL,  -- Tiempo en segundos
    FOREIGN KEY (id_sesion) REFERENCES sesiones(id_sesion)
);

-- Tabla de secuencias (entrenamiento de secuencias)
CREATE TABLE secuencias (
    id_secuencia INT AUTO_INCREMENT PRIMARY KEY,
    id_sesion INT,
    secuencia_objetivo VARCHAR(100),  -- Ejemplo: 'Cabeza,Torso,Pierna Izquierda'
    secuencia_real VARCHAR(100),  -- Ejemplo: 'Cabeza,Pierna Izquierda,Torso'
    errores INT NOT NULL,  -- Número de errores cometidos en la secuencia
    FOREIGN KEY (id_sesion) REFERENCES sesiones(id_sesion)
);

-- Insertar algunos usuarios de ejemplo
INSERT INTO usuarios (nombre, apellidos) VALUES 
('Juan', 'Pérez González'),
('María', 'López Martínez'),
('Carlos', 'Rodríguez Silva');

-- Insertar algunas sesiones de ejemplo
INSERT INTO sesiones (id_usuario, tipo_sesion, numero_golpes) VALUES 
(1, 'Entrenamiento', 25),
(2, 'Competencia', 15),
(3, 'Entrenamiento', 30);

-- Insertar algunos puntos registrados de ejemplo
INSERT INTO puntos_registrados (id_sesion, lugar_golpe) VALUES 
(1, 'Cabeza'),
(1, 'Torso'),
(1, 'Pierna Izquierda'),
(2, 'Torso'),
(2, 'Cabeza'),
(3, 'Pierna Derecha');

-- Insertar algunos datos de velocidad de reacción
INSERT INTO velocidad_reaccion (id_sesion, zona_objetivo, tiempo_reaccion) VALUES 
(1, 'Cabeza', 0.75),
(1, 'Torso', 0.68),
(2, 'Pierna Izquierda', 0.82);

-- Insertar algunas secuencias de ejemplo
INSERT INTO secuencias (id_sesion, secuencia_objetivo, secuencia_real, errores) VALUES 
(1, 'Cabeza,Torso,Pierna Izquierda', 'Cabeza,Torso,Pierna Izquierda', 0),
(2, 'Torso,Cabeza,Pierna Derecha', 'Torso,Pierna Derecha,Cabeza', 2),
(3, 'Cabeza,Torso,Torso', 'Cabeza,Torso,Torso', 0);

-- Consultas de verificación
SELECT 'Número de usuarios:' as 'Info', COUNT(*) as 'Cantidad' FROM usuarios
UNION ALL
SELECT 'Número de sesiones:', COUNT(*) FROM sesiones
UNION ALL
SELECT 'Número de puntos registrados:', COUNT(*) FROM puntos_registrados
UNION ALL
SELECT 'Número de registros de velocidad:', COUNT(*) FROM velocidad_reaccion
UNION ALL
SELECT 'Número de secuencias:', COUNT(*) FROM secuencias;
