// Variables iniciales
let golpes = 0;
let noGolpeados = 0;
let tiempoRestante = 10; // Ajustado a 10 segundos para la prueba
let jugador = "";
let topoPosicion = null;
let golpeado = false;
let intervalId = null;
let topoIntervalId = null;
let chart = null; // Variable para almacenar el gráfico

// Función para pedir el nombre del jugador
function pedirNombre() {
    jugador = prompt("Introduce tu nombre:");
    if (!jugador) {
        pedirNombre();  // Asegurarse de que el jugador ingrese un nombre
    }
    document.getElementById("nombre-jugador").textContent = jugador;
}

// Llamar a pedirNombre al iniciar
pedirNombre();

// Actualizar el temporizador cada segundo
function iniciarTemporizador() {
    intervalId = setInterval(() => {
        tiempoRestante--;
        let minutos = Math.floor(tiempoRestante / 60);
        let segundos = tiempoRestante % 60;
        document.getElementById("tiempo").textContent = `${minutos}:${segundos.toString().padStart(2, '0')}`;

        if (tiempoRestante <= 0) {
            finalizarJuego();
        }
    }, 1000);
}

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
}

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
    alert(`Juego terminado para ${jugador}`);

    // Detener el ciclo de topo y temporizador
    clearInterval(intervalId);
    clearInterval(topoIntervalId);

    // Log para verificar los datos que se envían al servidor
    console.log({
        nombre: jugador,
        golpes: golpes,
        no_golpeados: noGolpeados,
        rondas: 10  // Cambia este valor según tu lógica de rondas
    });

    // Enviar los datos del jugador actual al servidor
    fetch('http://localhost:5000/guardar_juego', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre: jugador,
            golpes: golpes,
            no_golpeados: noGolpeados,
            rondas: 10
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Datos guardados:", data);
    })
    .catch(error => console.error('Error:', error));
}


// Función para reiniciar el juego
function reiniciarJuego() {
    // Pedir un nuevo nombre para el siguiente jugador
    pedirNombre();

    // Reiniciar las variables del juego
    golpes = 0;
    noGolpeados = 0;
    tiempoRestante = 10; // Reiniciar el tiempo a 10 segundos para la prueba.

    // Reiniciar los textos en pantalla
    document.getElementById("golpes").textContent = 0;
    document.getElementById("no-golpeados").textContent = 0;
    document.getElementById("tiempo").textContent = "0:10";

    // Iniciar de nuevo el ciclo de temporizador y aparición del topo
    iniciarTemporizador();
    iniciarTopo();
}

// Función para iniciar el ciclo de aparición del topo
function iniciarTopo() {
    topoIntervalId = setInterval(mostrarTopo, 2000);  // Aparece un nuevo topo cada 2 segundos
}

// Iniciar el temporizador y la aparición del topo al principio
iniciarTemporizador();
iniciarTopo();

// Función para mostrar el dashboard
function mostrarDashboard() {
    // Si ya existe un gráfico, destruirlo antes de crear uno nuevo
    if (chart) {
        chart.destroy();
    }

    // Crear el gráfico usando Chart.js
    const ctx = document.getElementById('myChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'bar',  // Tipo de gráfico
        data: {
            labels: ['Golpes', 'No golpeados'],  // Etiquetas de los datos
            datasets: [{
                label: 'Estadísticas del juego',
                data: [golpes, noGolpeados],  // Datos de golpes y no golpeados
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',  // Color para los golpes
                    'rgba(255, 99, 132, 0.2)'   // Color para los no golpeados
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
