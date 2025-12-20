# ⛸️ Pista Manager - Sistema de Gestión de Pista de Hielo

**Versión 1.0.0 - Edición Profesional**

Sistema integral de clase empresarial para la administración operativa, financiera y de control de acceso para centros de patinaje sobre hielo y centros deportivos.

![Badge Status](https://img.shields.io/badge/Status-Stable-green) ![Badge Python](https://img.shields.io/badge/Backend-FastAPI-blue) ![Badge Docker](https://img.shields.io/badge/Deploy-Docker-2496ED)

## 📋 Descripción Ejecutiva

**Pista Manager** es una solución tecnológica "todo en uno" diseñada para modernizar y asegurar la operación de una pista de hielo. La plataforma centraliza los procesos críticos del negocio: desde la venta de entradas en taquilla con impresoras térmicas (POS), hasta la validación física de torniquetes mediante códigos de barras y la administración académica de alumnos.

El sistema prioriza la **seguridad financiera** y la **integridad operativa**, eliminando fugas de dinero por errores humanos o evasión de tiempos.

---

## 🚀 Módulos Principales

### 1. 🎫 Taquilla Inteligente (POS)
* **Interfaz de Alto Rendimiento**: Diseño limpio optimizado para pantallas táctiles y operación rápida.
* **Emisión de Tickets Seguros**: Generación automática de códigos de barra (CODE128) únicos por sesión.
* **Soporte de Hardware**: Formato de impresión nativo para impresoras térmicas **Epson TM (80mm)**.
* **Flexibilidad Comercial**: Gestión de tarifas variables, rentas de equipo auxiliar (andaderas) y venta cruzada de clases.
* **Múltiples Métodos de Pago**: Registro diferenciado de Efectivo vs Tarjetas Bancarias.

### 2. 🚧 Control de Acceso y Seguridad (Torniquetes)
* **Lógica "Anti-Passback"**: Bloqueo automático si un ticket intenta ser reutilizado para ingresar (evita traspaso de tickets).
* **Validación de Ciclo Completo**: Regla de negocio estricta que impide registrar una salida si no existe una entrada previa validada.
* **Cálculo de Tiempo Real**: El cronómetro de cobro inicia estrictamente al cruzar el torniquete, no al comprar el ticket.
* **Cobro de Excedentes**: Algoritmo automático que calcula minutos extra al momento de la salida y bloquea el torniquete si hay saldo pendiente.

### 3. 💰 Auditoría y Finanzas
* **Corte de Caja Automatizado**: Dashboard en tiempo real con arqueo de caja (Efectivo vs Banco).
* **Cálculo de Utilidad Neta**: Deducción automática de honorarios pagados a instructores del flujo de efectivo diario.
* **Reportes Duales**: 
    * **Formato A4**: Para archivo contable y firmas.
    * **Formato Tira POS**: Para cierre rápido en caja.

### 4. 🎓 Gestión Académica (Escuela)
* **Base de Datos de Alumnos**: Expedientes digitales para disciplinas (Hockey / Artístico).
* **Control de Pagos**: Seguimiento de mensualidades, inscripciones y vigencias.
* **Nómina de Instructores**: Cálculo de comisiones por clases particulares impartidas.

---

## 🛠️ Arquitectura Técnica

El sistema sigue una arquitectura monolítica modular contenerizada, garantizando facilidad de despliegue y escalabilidad vertical.

| Capa | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Backend** | Python 3.10 + **FastAPI** | API RESTful de alto rendimiento asíncrono. |
| **Base de Datos** | **PostgreSQL** 15 | Persistencia de datos relacional robusta. |
| **ORM** | SQLAlchemy | Abstracción de datos y manejo seguro de transacciones. |
| **Frontend** | HTML5 / JS / Bootstrap 5 | Interfaz responsiva servida estáticamente. |
| **Infraestructura** | **Docker & Compose** | Orquestación de servicios y aislamiento de entorno. |

---

## ⚙️ Guía de Despliegue (Instalación)

Este proyecto está diseñado para ser desplegado en menos de 5 minutos utilizando Docker.

### Prerrequisitos
* Docker Desktop (Windows/Mac) o Docker Engine (Linux).
* Git instalado.

### Pasos de Instalación

1.  **Clonar el Repositorio**
    ```bash
    git clone https://github.com/TU_USUARIO/pista-manager-demo.git
    cd pista-manager-demo
    ```

2.  **Configuración de Variables de Entorno**
    Crea un archivo `.env` en la raíz del proyecto para definir las credenciales seguras de la base de datos (NO subir este archivo al control de versiones).
    
    ```env
    POSTGRES_USER=admin_pista
    POSTGRES_PASSWORD=tu_password_seguro_aqui
    POSTGRES_DB=pista_produccion
    ```

3.  **Construcción y Ejecución**
    ```bash
    docker-compose up -d --build
    ```

4.  **Acceso al Sistema**
    *   **Panel Principal UI**: `http://localhost:8000/ui/index.html`
    *   **Documentación API (Swagger)**: `http://localhost:8000/docs`

---

## 📖 Estructura de Base de Datos (Resumen)

El modelo de datos garantiza la integridad mediante llaves foráneas y constraints.

*   `sesiones_patinaje`: Núcleo operativo. Vincula tickets, tarifas y tiempos.
*   `alumnos` & `pagos_escuela`: Módulo académico.
*   `instructores` & `rentas_instructores`: Gestión de nómina y servicios adicionales.
*   `tarifas`: Configuración de precios del sistema.

---

## 🛡️ Seguridad y Buenas Prácticas Implementadas

1.  **Sanitización de Datos**: Uso de Pydantic para validación estricta de payloads en la API.
2.  **Manejo de Errores**: Respuestas HTTP estandarizadas para evitar exponer stack traces al cliente.
3.  **Seguridad Lógica**:
    *   Verificación de estado de tickets en cada punto de control.
    *   Bloqueo de operaciones financieras en tickets cerrados.

---

## 📞 Soporte y Contacto

Para soporte técnico, despliegue en producción o personalizaciones, contactar al equipo de desarrollo.

---
© 2025 Pista Manager. Todos los derechos reservados.
