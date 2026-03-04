import os
import json
import smtplib
from datetime import datetime
from email.message import EmailMessage
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Eres un analista logistico de Casa Ferro. Recibiras un estatus tecnico y devolveras un JSON con:
1. 'explicacion_cliente': Mensaje amable en espanol para cliente.
2. 'explicacion_interna': Resumen operativo para equipo logistico.
3. 'nivel_alerta': Verde, Amarillo o Rojo.
4. 'accion_interna': Ninguna, Monitorear, Llamar paqueteria, Escalar incidencia.
Solo responde con el objeto JSON.
"""

def interpretar_tracking_pro(estatus_tecnico):
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Estatus técnico: {estatus_tecnico}"}
        ],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

def evaluar_retraso_regla(item):
    estatus = item.get("estatus_raw", "").upper()
    horas_sin_movimiento = item.get("horas_sin_movimiento", 0)

    if "EXCEPTION" in estatus or "FAILED" in estatus or "NOT FOUND" in estatus:
        return True, "Incidencia reportada por paqueteria"

    if horas_sin_movimiento >= 48:
        return True, f"Sin movimiento por {horas_sin_movimiento} horas"

    return False, "Sin retraso por regla"

def enviar_alerta_interna(resumen, guias_retrasadas):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    alert_from = os.getenv("ALERT_FROM")
    alert_to = os.getenv("ALERT_TO")

    if not all([smtp_host, smtp_user, smtp_password, alert_from, alert_to]):
        print("Alerta interna omitida: faltan variables SMTP/ALERT en .env")
        return

    destinatarios = [mail.strip() for mail in alert_to.split(",") if mail.strip()]
    if not destinatarios:
        print("Alerta interna omitida: ALERT_TO no tiene destinatarios validos")
        return

    detalle = "\n".join(
        [
            f"- {g['id_guia']} | {g['paqueteria']} | {g['motivo_retraso']}"
            for g in guias_retrasadas
        ]
    )

    body = (
        "Reporte automatico de tracking\n\n"
        f"Total guias: {resumen['total_guias']}\n"
        f"Retrasadas: {resumen['retrasadas']}\n"
        f"Alertas rojas: {resumen['alertas_rojas']}\n\n"
        "Guias retrasadas:\n"
        f"{detalle}"
    )

    msg = EmailMessage()
    msg["Subject"] = "[Tracking] Alertas internas de paqueteria"
    msg["From"] = alert_from
    msg["To"] = ", ".join(destinatarios)
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

    print("Alerta interna enviada por email.")

def nivel_alerta_final(nivel_ia, retrasado):
    if nivel_ia == "Rojo":
        return "Rojo"
    if retrasado and nivel_ia == "Verde":
        return "Amarillo"
    return nivel_ia

print("Iniciando reporte diario de tracking...\n")

base_dir = os.path.dirname(__file__)
guias_path = os.path.join(base_dir, "guias.json")
reporte_path = os.path.join(base_dir, "reporte_diario.json")

with open(guias_path, "r", encoding="utf-8") as f:
    guias = json.load(f)

resultados = []
for item in guias:
    print(f"Procesando guia: {item['id_guia']} ({item['paqueteria']})")

    retrasado, motivo_retraso = evaluar_retraso_regla(item)

    try:
        analisis = interpretar_tracking_pro(item["estatus_raw"])
    except Exception as error:
        analisis = {
            "explicacion_cliente": "Estamos validando tu envio con la paqueteria.",
            "explicacion_interna": f"Fallo al consultar IA: {error}",
            "nivel_alerta": "Amarillo",
            "accion_interna": "Monitorear",
        }

    alerta_final = nivel_alerta_final(analisis.get("nivel_alerta", "Amarillo"), retrasado)

    resultado = {
        "id_guia": item["id_guia"],
        "paqueteria": item["paqueteria"],
        "estatus_raw": item["estatus_raw"],
        "retrasado": retrasado,
        "motivo_retraso": motivo_retraso,
        "nivel_alerta": alerta_final,
        "accion_interna": analisis.get("accion_interna", "Monitorear"),
        "explicacion_cliente": analisis.get("explicacion_cliente", ""),
        "explicacion_interna": analisis.get("explicacion_interna", ""),
    }
    resultados.append(resultado)
    print(f"  Alerta: {resultado['nivel_alerta']} | Retrasado: {resultado['retrasado']}")

retrasadas = [r for r in resultados if r["retrasado"]]
alertas_rojas = [r for r in resultados if r["nivel_alerta"] == "Rojo"]

resumen = {
    "fecha_reporte": datetime.now().isoformat(timespec="seconds"),
    "total_guias": len(resultados),
    "retrasadas": len(retrasadas),
    "alertas_rojas": len(alertas_rojas),
}

reporte = {
    "resumen": resumen,
    "guias": resultados,
}

with open(reporte_path, "w", encoding="utf-8") as f:
    json.dump(reporte, f, ensure_ascii=False, indent=2)

print("\nResumen:")
print(f"Total guias: {resumen['total_guias']}")
print(f"Retrasadas: {resumen['retrasadas']}")
print(f"Alertas rojas: {resumen['alertas_rojas']}")
print(f"Reporte guardado en: {reporte_path}")

if retrasadas:
    try:
        enviar_alerta_interna(resumen, retrasadas)
    except Exception as error:
        print(f"No se pudo enviar alerta interna: {error}")

print("\nReporte finalizado.")