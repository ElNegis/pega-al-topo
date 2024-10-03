let golpes = 0;
let noGolpeados = 0;
let tiempoRestante = 50; // 15 minutos en segundos
let jugador = prompt("Introduce tu nombre:");
document.getElementById("nombre-jugador").textContent = jugador;

let topoPosicion = null;
let golpeado = false;

// Actualizar el temporizador cada segundo
setInterval(() => {
    tiempoRestante--;
    let minutos = Math.floor(tiempoRestante / 60);
    let segundos = tiempoRestante % 60;
    document.getElementById("tiempo").textContent = `${minutos}:${segundos.toString().padStart(2, '0')}`;
    
    if (tiempoRestante <= 0) {
        finalizarJuego();
    }
}, 1000);

// Mostrar el topo en una posición aleatoria
function mostrarTopo() {
    if (!golpeado && topoPosicion !== null) {
        noGolpeados++;
        document.getElementById("no-golpeados").textContent = noGolpeados;
    }

    // Resetear estado
    golpeado = false;

    // Escoger nueva posición aleatoria
    topoPosicion = Math.floor(Math.random() * 9);
    const botones = document.querySelectorAll('.grid button');
    botones.forEach((btn, index) => {
        if (index === topoPosicion) {
            btn.textContent = "Topo!";
        } else {
            btn.textContent = "Golpear";
        }
    });

    // Hacer aparecer el topo cada 2 segundos
    setTimeout(mostrarTopo, 2000);
}

mostrarTopo();

// Función para golpear al topo
function golpear(posicion) {
    if (posicion === topoPosicion) {
        golpes++;
        golpeado = true;
        document.getElementById("golpes").textContent = golpes;
    }
}

// Finalizar el juego
function finalizarJuego() {
    alert("Juego terminado");
    fetch('http://localhost:5000/guardar_juego', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre: jugador,
            golpes: golpes,
            no_golpeados: noGolpeados,
            tiempo: 50 - tiempoRestante
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Datos guardados:", data);
        window.location.reload();
    })
    .catch(error => console.error('Error:', error));
}
