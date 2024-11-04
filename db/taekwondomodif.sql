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
    zona_objetivo VARCHAR(50) NOT NULL,  -- Zona a la que el sistema pidió golpear (Ejemplo: 'Cabeza')
    tiempo_reaccion DECIMAL(5,2) NOT NULL,  -- Tiempo en segundos desde la indicación hasta el golpe
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
