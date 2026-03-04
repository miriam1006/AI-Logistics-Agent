# 🤖 AI Logistics Agent

Agente inteligente en **Python** diseñado para el monitoreo automatizado de guías de paquetería, detección proactiva de incidencias y generación de reportes operativos estructurados.

Este proyecto combina automatización tradicional, reglas de negocio y modelos de lenguaje de última generación (**GPT-4o**) para transformar estatus técnicos crudos en información accionable para equipos de soporte y clientes finales.

---

## 🚀 ¿Qué problema resuelve?

En entornos logísticos y de e-commerce, los estatus proporcionados por las transportistas suelen ser técnicos, inconsistentes y difíciles de interpretar a gran escala.

**Este agente permite:**

* **Normalizar estatus** de múltiples paqueterías (FedEx, DHL, Estafeta, etc.).
* **Detectar retrasos** mediante una combinación de reglas fijas e interpretación contextual.
* **Clasificar niveles de alerta** (Verde / Amarillo / Rojo) según la gravedad operativa.
* **Sugerir acciones inmediatas** (Contactar cliente, llamar a paquetería, etc.).
* **Generar reportes estructurados** en formato JSON listos para integrarse con dashboards o bases de datos como **Supabase**.

---

## 🧠 Enfoque Técnico

El flujo de trabajo del agente integra dos metodologías para maximizar la precisión:

1. **Interpretación Contextual (IA):** Utiliza la API de OpenAI para entender el "sentimiento" y significado de errores complejos en el rastreo.
2. **Heurística Determinística (Reglas de Negocio):** Aplica validaciones lógicas para detectar anomalías de tiempo (ej. más de 48 horas sin movimiento).
3. **Salida Estructurada:** Garantiza que la respuesta sea siempre un objeto JSON válido, facilitando la automatización de procesos posteriores.

---

## 🛠 Stack Tecnológico

* **Lenguaje:** Python 3.10+.
* **IA:** OpenAI API (`openai` SDK).
* **Gestión de Entorno:** `python-dotenv` para el manejo seguro de credenciales.
* **Persistencia:** JSON (entrada/salida) y compatibilidad con SQL (Supabase/PostgreSQL).
* **Infraestructura:** Preparado para despliegue en entornos como Render.

---

## 📂 Estructura del Proyecto

* `agent.py` → Lógica principal del agente y conexión con la IA.
* `guias.json` → Dataset de ejemplo con casos de prueba reales.
* `reporte_diario.json` → Output generado con el análisis consolidado.
* `.env.example` → Plantilla de configuración de variables de entorno.
* `.gitignore` → Protección de llaves de API y archivos temporales.

---

## ⚙️ Configuración e Instalación

### 1️⃣ Preparar el Entorno (Windows/PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

```

### 2️⃣ Instalar Dependencias

```powershell
pip install openai python-dotenv

```

### 3️⃣ Configurar Variables de Env

Crear un archivo `.env` basado en `.env.example`:

```env
OPENAI_API_KEY=tu_api_key_aqui

```

---

## 📊 Salida de Ejemplo (JSON)

El sistema genera automáticamente un `reporte_diario.json` con la siguiente estructura, ideal para alimentar un backend o sistema de notificaciones:

```json
{
  "guia": "CF-102",
  "retrasado": true,
  "nivel_alerta": "Amarillo",
  "explicacion_cliente": "No hemos podido localizar tu domicilio, por favor verifica tus datos.",
  "accion_interna": "Contactar cliente para confirmar dirección"
}

```

---

## 🔐 Seguridad y Buenas Prácticas

* **Aislamiento de Credenciales:** Uso estricto de `.env` para evitar la exposición de saldos o llaves de API.
* **Manejo de Errores:** Estructura preparada para gestionar fallos de conexión o cuotas excedidas en la API sin interrumpir el flujo logístico.

---

## 👩‍💻 Sobre el Proyecto

Desarrollado por **Miriam G.**, enfocado en la optimización operativa de flujos de e-commerce y logística inteligente. Inspirado en la automatización de procesos reales.


