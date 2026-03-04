# AI Logistics Agent

Agente inteligente en Python para monitoreo automatizado de guías de paquetería, detección de incidencias y generación de reportes operativos estructurados.

Este proyecto combina automatización, reglas de negocio y modelos de IA para transformar estatus técnicos de paqueterías en información accionable para equipos internos.

---

## 🚀 ¿Qué problema resuelve?

En entornos logísticos, los estatus de paquetería suelen ser técnicos, inconsistentes y difíciles de interpretar rápidamente.

Este agente:

* Normaliza estatus de múltiples paqueterías.
* Detecta posibles retrasos mediante reglas de negocio.
* Clasifica niveles de alerta (Verde / Amarillo / Rojo).
* Sugiere acciones internas.
* Genera un reporte diario estructurado en JSON.
* Permite envío opcional de alertas internas por correo (SMTP).

El enfoque no es solo informar al cliente, sino habilitar acción operativa preventiva.

---

## 🧠 Enfoque Técnico

El flujo combina:

1. Interpretación inteligente de estatus técnicos mediante OpenAI API.
2. Reglas de negocio determinísticas para detección de riesgo.
3. Generación de salida estructurada lista para integrarse en dashboards o sistemas backend.
4. Automatización del reporte diario.

---

## 🛠 Stack Tecnológico

* Python 3
* OpenAI API (`openai`)
* `python-dotenv` para manejo seguro de variables de entorno
* JSON como formato de entrada y salida
* SMTP opcional para alertas internas

---

## 📂 Estructura del Proyecto

* `agent.py` → Lógica principal del agente.
* `guias.json` → Datos de ejemplo para simulación.
* `reporte_diario.json` → Reporte generado automáticamente.
* `.env.example` → Plantilla de configuración.
* `.gitignore` → Protección de credenciales y archivos locales.

---

## ⚙️ Configuración

### 1️⃣ Crear entorno virtual

```powershell
python -m venv venv
```

### 2️⃣ Activar entorno

```powershell
.\venv\Scripts\Activate.ps1
```

### 3️⃣ Instalar dependencias

```powershell
pip install openai python-dotenv
```

### 4️⃣ Configurar variables de entorno

Crear archivo `.env` basado en `.env.example` y definir como mínimo:

```env
OPENAI_API_KEY=tu_api_key
```

### Variables opcionales para alertas internas:

* SMTP_HOST
* SMTP_PORT
* SMTP_USER
* SMTP_PASSWORD
* ALERT_FROM
* ALERT_TO

Si SMTP no está configurado, el sistema continúa sin enviar correo.

---

## 🧩 Lógica de Detección de Retraso (MVP)

Una guía se marca como retrasada cuando:

* El estatus contiene palabras clave como:

  * `EXCEPTION`
  * `FAILED`
  * `NOT FOUND`
* O cuando:

  * `horas_sin_movimiento >= 48`

Esto permite una combinación de:

* Heurística determinística
* Interpretación contextual asistida por IA

---

## 📊 Salida Generada

Se crea automáticamente `reporte_diario.json` con:

### `resumen`

* total_guias
* retrasadas
* alertas_rojas
* fecha_reporte

### `guias`

Por cada guía:

* `retrasado`
* `motivo_retraso`
* `nivel_alerta`
* `accion_interna`
* `explicacion_cliente`
* `explicacion_interna`

Este formato está diseñado para:

* Integrarse con APIs backend
* Alimentar dashboards
* Generar notificaciones automáticas

---

## 🧪 Demo Recomendada para Portafolio

1. Ejecutar `python agent.py` en PowerShell.
2. Mostrar salida en terminal.
3. Abrir `reporte_diario.json`.
4. Explicar en una frase:

> Agente automatizado que combina IA + reglas de negocio para generar acción operativa en logística.

---

## 🔐 Seguridad

* Nunca subir el archivo `.env` al repositorio.
* Si una API key se expone, debe revocarse y regenerarse.
* Las credenciales SMTP deben manejarse únicamente mediante variables de entorno.

---
## 👩‍💻 Sobre el Proyecto
Desarrollado por **Miriam G.** como proyecto enfocado en automatización logistica. 

🔗 LinkedIn:
https://www.linkedin.com/in/miriam-garc%C3%ADa100625/
📩 Contacto:
miriam100625@gmail.com


