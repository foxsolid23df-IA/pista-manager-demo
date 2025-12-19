const API_URL = ""; // Ruta relativa

document.addEventListener('DOMContentLoaded', function () {
    cargarProfesores();
    inicializarCalendario();
});

let calendarInstance = null; // Guardar referencia global

// --- 1. CONFIGURACIÓN DEL CALENDARIO ---
function inicializarCalendario() {
    var calendarEl = document.getElementById('calendar');

    calendarInstance = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek', // Vista semanal por horas
        locale: 'es', // Español
        headerToolbar: {
            left: '',
            center: 'title',
            right: 'timeGridWeek,timeGridDay'
        },
        slotMinTime: '08:00:00', // La pista abre a las 8am
        slotMaxTime: '22:00:00', // Cierra a las 10pm
        allDaySlot: false,
        height: 'auto',

        // Aquí conectamos con Python para obtener los eventos
        events: {
            url: `${API_URL}/escuela/calendario/`,
            method: 'GET',
            failure: function () {
                console.error("Error cargando calendario");
            }
        },

        // Al hacer click en un evento
        eventClick: function (info) {
            alert('Clase: ' + info.event.title);
        }
    });

    calendarInstance.render();
}

// --- 2. GESTIÓN DE PROFESORES ---
async function cargarProfesores() {
    const lista = document.getElementById('listaProfesores');
    const select = document.getElementById('instructorClase'); // Nuevo select para formulario de clases

    try {
        const res = await fetch(`${API_URL}/escuela/instructores/`);
        const profesores = await res.json();

        lista.innerHTML = '';
        select.innerHTML = '<option selected disabled>Seleccionar...</option>';

        profesores.forEach(profe => {
            // Lista lateral
            lista.innerHTML += `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    ${profe.nombre}
                    <span class="badge bg-secondary rounded-pill">${profe.especialidad}</span>
                </li>
            `;

            // Select del formulario de clases
            let option = document.createElement("option");
            option.value = profe.id;
            option.text = profe.nombre;
            select.add(option);
        });
    } catch (e) {
        lista.innerHTML = '<li class="list-group-item text-danger">Error conexión</li>';
    }
}

// --- 3. CREAR NUEVO PROFESOR ---
document.getElementById('formInstructor').addEventListener('submit', async (e) => {
    e.preventDefault();
    const datos = {
        nombre: document.getElementById('nombreProfe').value,
        especialidad: document.getElementById('especialidadProfe').value
    };

    try {
        const res = await fetch(`${API_URL}/escuela/instructores/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        if (res.ok) {
            alert('Profesor registrado');
            document.getElementById('formInstructor').reset();
            cargarProfesores(); // Recargar lista y selects
        }
    } catch (e) {
        alert('Error guardando profesor');
    }
});

// --- 4. CREAR NUEVA CLASE ---
document.getElementById('formClase').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Validar Instructor
    const instructorId = document.getElementById('instructorClase').value;
    if (!instructorId || instructorId === "Seleccionar...") {
        return alert("Por favor selecciona un instructor");
    }

    const datos = {
        nombre: document.getElementById('nombreClase').value,
        instructor_id: parseInt(instructorId),
        dia_semana: document.getElementById('diaClase').value,
        hora_inicio: document.getElementById('horaClase').value,
        duracion_minutos: 60 // Por ahora fijo
    };

    try {
        const res = await fetch(`${API_URL}/escuela/clases/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        if (res.ok) {
            alert('Clase programada exitosamente');
            document.getElementById('formClase').reset();
            calendarInstance.refetchEvents(); // Recargar calendario automáticamente
        } else {
            alert("Error al programar clase");
        }
    } catch (e) {
        alert('Error de conexión');
    }
});
