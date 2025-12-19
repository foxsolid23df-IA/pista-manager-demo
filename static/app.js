const API_URL = ""; // Usar ruta relativa (mismo dominio/puerto)

// 1. Cargar Datos al abrir la página
document.addEventListener('DOMContentLoaded', async () => {
    cargarTarifas();
    cargarInstructoresVenta();
});

async function cargarTarifas() {
    try {
        const response = await fetch(`${API_URL}/tarifas/`);
        const tarifas = await response.json();

        const select = document.getElementById('selectTarifa');
        select.innerHTML = ''; // Limpiar

        tarifas.forEach(tarifa => {
            const option = document.createElement('option');
            option.value = tarifa.id;
            option.textContent = `${tarifa.nombre} - $${tarifa.costo_base}`;
            select.appendChild(option);
        });
    } catch (error) {
        alert("Error conectando con el servidor. ¿Está prendido Docker?");
    }
}

// NUEVA FUNCIÓN: Llenar el dropdown de instructores en la taquilla
async function cargarInstructoresVenta() {
    try {
        const res = await fetch(`${API_URL}/escuela/instructores/`);
        const profes = await res.json();
        const select = document.getElementById('selectInstructorVenta');

        profes.forEach(profe => {
            const option = document.createElement('option');
            option.value = profe.id;
            option.textContent = `${profe.nombre} (${profe.especialidad})`;
            select.appendChild(option);
        });
    } catch (e) { console.error("Error cargando profes"); }
}

// 2. Función para ENTRADA
async function registrarEntrada() {
    const tarifaId = document.getElementById('selectTarifa').value;
    // Capturar los nuevos campos
    const quiereAndadera = document.getElementById('checkAndadera').checked;
    const instructorSeleccionado = document.getElementById('selectInstructorVenta').value; // String vacío si no selecciona nada

    // Capturar método de pago
    const metodo = document.querySelector('input[name="metodoPago"]:checked').value;

    const datos = {
        tarifa_id: parseInt(tarifaId),
        renta_andadera: quiereAndadera,
        instructor_id: instructorSeleccionado ? parseInt(instructorSeleccionado) : null,
        metodo_pago: metodo
    };

    try {
        const response = await fetch(`${API_URL}/check-in/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.detail || "Error en check-in");

        // Mostrar resultado
        document.getElementById('ticketGenerado').textContent = data.ticket_id;
        document.getElementById('mensajeTicket').textContent = data.mensaje;

        // Mostrar Total
        const totalFmt = new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(data.total_pagado);
        document.getElementById('totalTicket').textContent = totalFmt;

        // Generar Código de Barras (Validar que la librería exista)
        if (typeof JsBarcode !== 'undefined') {
            try {
                JsBarcode("#barcode", data.ticket_id, {
                    format: "CODE128",
                    lineColor: "#000",
                    width: 2,
                    height: 50,
                    displayValue: false
                });

                // --- NUEVO: IMPRIMIR AUTOMÁTICAMENTE EN FORMATO TICKET ---
                setTimeout(() => imprimirTicketTermico(data), 500);

            } catch (e) {
                console.error("Error generando barcode:", e);
                document.getElementById('mensajeTicket').textContent += " (Error Barcode)";
            }
        } else {
            console.error("Librería JsBarcode no cargada.");
            document.getElementById('mensajeTicket').textContent += " (⚠️ Librería Barcode faltante)";
        }

        document.getElementById('resultadoEntrada').classList.remove('d-none');

        // Limpiar formulario para el siguiente cliente
        document.getElementById('checkAndadera').checked = false;
        document.getElementById('selectInstructorVenta').value = "";

    } catch (error) {
        alert("No se pudo generar el ticket: " + error.message);
    }
}

// 4. Función Auxiliar: Imprimir Ticket TÉRMICO (POS)
function imprimirTicketTermico(data) {
    const barcodeImg = document.getElementById('barcode');
    const barcodeSrc = barcodeImg.src;

    // Formatear dinero
    const totalFmt = new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(data.total_pagado);

    // Abrir ventana popup
    const popup = window.open('', '_blank', 'width=400,height=600');

    if (!popup) {
        alert("⚠️ El navegador bloqueó la ventana emergente. Por favor permite pop-ups para imprimir.");
        return;
    }

    const htmlContent = `
    <html>
    <head>
        <title>Ticket ${data.ticket_id}</title>
        <style>
            @page {
                margin: 0;
                size: auto; /* auto is better for roll paper */
            }
            body {
                font-family: 'Courier New', Courier, monospace;
                width: 72mm; /* Standard printable area for 80mm paper */
                margin: 5px auto;
                text-align: center;
                color: #000;
                font-size: 14px;
            }
            .header { margin-bottom: 5px; }
            .title { font-size: 20px; font-weight: bold; }
            .subtitle { font-size: 14px; }
            .divider { border-top: 2px dashed #000; margin: 10px 0; }
            .info { font-size: 12px; text-align: left; margin-bottom: 5px; }
            .product { font-size: 16px; font-weight: bold; margin: 10px 0; }
            .total { font-size: 26px; font-weight: bold; margin: 5px 0; }
            .footer { font-size: 12px; margin-top: 20px; padding-bottom: 20px;}
            img { width: 100%; max-width: 60mm; height: auto; margin-top: 5px; }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">PCTronicMex</div>
            <div class="subtitle">Pista de Hielo</div>
        </div>
        
        <div class="divider"></div>

        <div class="info">
            <strong>Fecha:</strong> ${new Date().toLocaleString()}<br>
            <strong>Ticket ID:</strong> ${data.ticket_id}
        </div>

        <div class="divider"></div>

        <div class="product">
            ${data.mensaje.replace("Entrada: ", "")}
        </div>

        <div class="total">
            TOTAL: ${totalFmt}
        </div>

        <div>
            <img src="${barcodeSrc}" />
            <br>
            <small>${data.ticket_id}</small>
        </div>

        <div class="divider"></div>

        <div class="footer">
            ¡Conserva este ticket para tu salida!<br>
            Si excedes tu tiempo se cobrará extra.<br>
            <br>
            *** GRACIAS POR TU VISITA ***
        </div>

        <script>
            window.onload = function() {
                window.print();
                // window.close(); // Opcional
            }
        </script>
    </body>
    </html>
    `;

    popup.document.write(htmlContent);
    popup.document.close(); // Necesario para terminar carga
}

// 3. Función para SALIDA
async function registrarSalida() {
    const ticketId = document.getElementById('inputTicketSalida').value;
    if (!ticketId) return alert("Escribe un ID de ticket");

    try {
        const response = await fetch(`${API_URL}/check-out/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticket_id: ticketId })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Error al cobrar");
            return;
        }

        // Mostrar cobro
        document.getElementById('precioFinal').textContent = `$${data.total_pagar}`;
        document.getElementById('detalleTiempo').textContent =
            `Tiempo: ${data.tiempo_total_min} min (${data.minutos_extra} extra)`;

        document.getElementById('resultadoSalida').classList.remove('d-none');

        // Limpiar input para el siguiente
        document.getElementById('inputTicketSalida').value = "";

    } catch (error) {
        alert("Error de conexión o ticket inválido");
    }
}

// Extra: Permitir dar ENTER en el input de salida (como un scanner real)
document.getElementById('inputTicketSalida').addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        registrarSalida();
    }
});
