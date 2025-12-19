const API_URL = ""; // Ruta relativa para evitar problemas de CORS/Red
let alumnosCache = []; // Para guardar los datos localmente

// 1. Cargar alumnos al iniciar
document.addEventListener('DOMContentLoaded', cargarAlumnos);

async function cargarAlumnos() {
    const tabla = document.getElementById('tablaAlumnos');

    try {
        const response = await fetch(`${API_URL}/escuela/alumnos/`);
        const alumnos = await response.json();
        alumnosCache = alumnos; // Guardamos copia

        tabla.innerHTML = ''; // Limpiar tabla

        alumnos.forEach(alumno => {
            // Lógica de Estado (Vencido vs Activo)
            const hoy = new Date();
            // Truco: Convertir fecha string "2023-12-01" a objeto Date
            const vencimiento = alumno.vencimiento_mensualidad ? new Date(alumno.vencimiento_mensualidad) : null;

            let estadoHTML = '<span class="badge bg-secondary">Nuevo</span>';
            let esMoroso = true;

            if (vencimiento) {
                // Ajustar zona horaria simple
                vencimiento.setDate(vencimiento.getDate() + 1);

                if (vencimiento >= hoy) {
                    estadoHTML = '<span class="badge bg-success">Activo</span>';
                    esMoroso = false;
                } else {
                    estadoHTML = '<span class="badge bg-danger">Vencido</span>';
                }
            }

            // Insertar fila
            const row = `
                <tr>
                    <td>${alumno.id}</td>
                    <td><strong>${alumno.nombre}</strong></td>
                    <td>${alumno.nivel}</td>
                    <td>${alumno.vencimiento_mensualidad || 'Sin pagos'}</td>
                    <td>${estadoHTML}</td>
                    <td>
                        <button onclick="abrirModalPago(${alumno.id})" class="btn btn-sm btn-outline-success">
                            <i class="bi bi-cash-coin"></i> Pagar
                        </button>
                    </td>
                </tr>
            `;
            tabla.innerHTML += row;
        });

    } catch (error) {
        console.error(error);
        tabla.innerHTML = '<tr><td colspan="6" class="text-danger">Error cargando datos. Revisa la consola.</td></tr>';
    }
}

// 2. Crear Nuevo Alumno
document.getElementById('formNuevoAlumno').addEventListener('submit', async (e) => {
    e.preventDefault();

    const datos = {
        nombre: document.getElementById('nombreAlumno').value,
        telefono_contacto: document.getElementById('telAlumno').value,
        nivel: document.getElementById('nivelAlumno').value
    };

    try {
        const res = await fetch(`${API_URL}/escuela/alumnos/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        if (res.ok) {
            alert("Alumno inscrito correctamente");
            location.reload(); // Recargar página para ver cambios
        } else {
            alert("Error al guardar");
        }
    } catch (error) {
        alert("Error de conexión");
    }
});

// 3. Abrir Modal de Pago (Prepara los datos)
let alumnoIdParaPagar = null;

function abrirModalPago(id) {
    const alumno = alumnosCache.find(a => a.id === id);
    if (!alumno) return;

    alumnoIdParaPagar = id;
    document.getElementById('pagoAlumnoId').innerText = id;
    document.getElementById('pagoAlumnoNombre').innerText = alumno.nombre;

    // Abrir modal usando Bootstrap (desde JS)
    const modal = new bootstrap.Modal(document.getElementById('modalPago'));
    modal.show();
}

// 4. Enviar Pago al Backend
async function enviarPago() {
    if (!alumnoIdParaPagar) return;

    const datos = {
        alumno_id: alumnoIdParaPagar,
        monto: parseFloat(document.getElementById('montoPago').value),
        concepto: document.getElementById('conceptoPago').value,
        dias_vigencia: 30
    };

    try {
        const res = await fetch(`${API_URL}/escuela/pagos/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        if (res.ok) {
            alert("¡Pago registrado! La fecha de vencimiento se ha actualizado.");
            location.reload();
        } else {
            alert("Error registrando el pago");
        }
    } catch (error) {
        alert("Error de conexión");
    }
}
