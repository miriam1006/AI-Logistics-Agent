# AI Logistics Agent

Agente en Python para monitorear guias de paqueteria, detectar retrasos y generar un reporte operativo interno.

Este proyecto combina:
- IA para interpretar estatus tecnicos de distintas paqueterias.
- Reglas de negocio simples para detectar riesgo/retraso.
- Salida estructurada en JSON para seguimiento diario.
- Alerta interna opcional por email (SMTP).

## Que resuelve

En lugar de solo avisar al cliente, este agente ayuda al equipo interno a actuar antes:
- identifica guias retrasadas,
- clasifica nivel de alerta,
- sugiere accion interna,
- y genera un resumen diario.

## Stack

- Python 3
- OpenAI API (`openai`)
- Variables de entorno (`python-dotenv`)
- JSON como entrada/salida
- SMTP opcional para alertas internas

## Estructura del proyecto

- `agent.py`: logica principal del agente.
- `guias.json`: datos de ejemplo de guias.
- `reporte_diario.json`: salida generada por ejecucion.
- `.env.example`: plantilla de configuracion.
- `.gitignore`: proteccion de secretos y archivos locales.

## Configuracion

1) Crea tu entorno virtual:

```powershell
python -m venv venv
```

2) Activa el entorno:

```powershell
.\venv\Scripts\Activate.ps1
```

3) Instala dependencias:

```powershell
pip install openai python-dotenv
```

4) Crea tu `.env` a partir de `.env.example` y completa al menos:

```env
OPENAI_API_KEY=tu_api_key
```

Opcional (alertas internas por email):
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `ALERT_FROM`
- `ALERT_TO`

## Ejecucion

```powershell
python agent.py
```

Si no tienes configurado SMTP, el flujo continua y solo omite el envio de correo.

## Logica de retraso (MVP)

Una guia se marca como retrasada si:
- el estatus contiene `EXCEPTION`, `FAILED` o `NOT FOUND`, o
- `horas_sin_movimiento >= 48`.

## Salida esperada

Se genera `reporte_diario.json` con:
- `resumen`: total de guias, retrasadas y alertas rojas.
- `guias`: detalle por guia con:
  - `retrasado`
  - `motivo_retraso`
  - `nivel_alerta`
  - `accion_interna`
  - `explicacion_cliente`
  - `explicacion_interna`

## Demo recomendada para portafolio

1) Mostrar ejecucion en terminal (PowerShell).
2) Mostrar el `reporte_diario.json` con una guia retrasada.
3) Explicar en 1 frase: IA + reglas de negocio para accion operativa.

## Nota de seguridad

- No subir `.env` al repositorio.
- Si una API key se expone, rotarla (revocar y generar una nueva).

