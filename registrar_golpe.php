<?php
// Configuración de la base de datos
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "BD_Taekwondo";

try {
    // Crear conexión
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Leer datos JSON
    $json = file_get_contents('php://input');
    $data = json_decode($json, true);

    $response = array();

    if (isset($data['tipo'])) {
        switch ($data['tipo']) {
            case 'nueva_sesion':
                // Crear nueva sesión
                $stmt = $conn->prepare("INSERT INTO sesiones (id_usuario, tipo_sesion) 
                                      VALUES (:id_usuario, :tipo_sesion)");
                $stmt->execute([
                    ':id_usuario' => $data['id_usuario'],
                    ':tipo_sesion' => $data['tipo_sesion']
                ]);
                $response['id_sesion'] = $conn->lastInsertId();
                $response['status'] = 'success';
                break;

            case 'punto_registrado':
                // Registrar un golpe
                $stmt = $conn->prepare("INSERT INTO puntos_registrados (id_sesion, lugar_golpe) 
                                      VALUES (:id_sesion, :lugar_golpe)");
                $stmt->execute([
                    ':id_sesion' => $data['id_sesion'],
                    ':lugar_golpe' => $data['lugar_golpe']
                ]);
                $response['status'] = 'success';
                break;

            case 'actualizar_sesion':
                // Actualizar el contador de golpes de la sesión
                $stmt = $conn->prepare("UPDATE sesiones SET numero_golpes = :numero_golpes 
                                      WHERE id_sesion = :id_sesion");
                $stmt->execute([
                    ':numero_golpes' => $data['numero_golpes'],
                    ':id_sesion' => $data['id_sesion']
                ]);
                $response['status'] = 'success';
                break;

            case 'tiempo_reaccion':
                // Registrar tiempo de reacción
                $stmt = $conn->prepare("INSERT INTO velocidad_reaccion (id_sesion, zona_objetivo, tiempo_reaccion) 
                                      VALUES (:id_sesion, :zona_objetivo, :tiempo_reaccion)");
                $stmt->execute([
                    ':id_sesion' => $data['id_sesion'],
                    ':zona_objetivo' => $data['zona_objetivo'],
                    ':tiempo_reaccion' => $data['tiempo_reaccion']
                ]);
                $response['status'] = 'success';
                break;

            case 'secuencia':
                // Registrar secuencia
                $stmt = $conn->prepare("INSERT INTO secuencias (id_sesion, secuencia_objetivo, secuencia_real, errores) 
                                      VALUES (:id_sesion, :secuencia_objetivo, :secuencia_real, :errores)");
                $stmt->execute([
                    ':id_sesion' => $data['id_sesion'],
                    ':secuencia_objetivo' => $data['secuencia_objetivo'],
                    ':secuencia_real' => $data['secuencia_real'],
                    ':errores' => $data['errores']
                ]);
                $response['status'] = 'success';
                break;

            default:
                $response['status'] = 'error';
                $response['message'] = 'Tipo de operación no válido';
        }
    } else {
        $response['status'] = 'error';
        $response['message'] = 'Datos incompletos';
    }

    echo json_encode($response);

} catch(PDOException $e) {
    echo json_encode([
        'status' => 'error',
        'message' => 'Error de conexión: ' . $e->getMessage()
    ]);
}

$conn = null;
?>
