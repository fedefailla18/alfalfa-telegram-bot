import os
import requests
from bs4 import BeautifulSoup

URL = "https://todoagro.com.ar"
TOKEN = os.environ["TELEGRAM_TOKEN"].strip()
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"].strip()


def obtener_precios():
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(URL, headers=headers, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    tabla_alfalfa = None
    for tabla in soup.find_all("table"):
        if "Mercado de Alfalfa" in tabla.get_text():
            tabla_alfalfa = tabla
            break

    if not tabla_alfalfa:
        return "⚠️ No se encontró la tabla de alfalfa en TodoAgro."

    lineas = ["🌱 *Mercado de Alfalfa (Ref. Cámara)*\n"]
    precio_rollo_1 = None

    for fila in tabla_alfalfa.find_all("tr"):
        celdas = [c.get_text(strip=True) for c in fila.find_all(["td", "th"])]
        celdas = [c for c in celdas if c]
        if not celdas:
            continue

        texto_fila = " | ".join(celdas)
        if "actualización" in texto_fila.lower():
            lineas.append(f"📅 _{texto_fila}_\n")
        elif len(celdas) == 2 and celdas[1] != "Precio":
            lineas.append(f"• *{celdas[0]}:* {celdas[1]}")
            if "Rollo de 1°" in celdas[0]:
                num = "".join(filter(str.isdigit, celdas[1]))
                if num:
                    precio_rollo_1 = int(num)

    if precio_rollo_1:
        min_ref = precio_rollo_1 * 350
        max_ref = precio_rollo_1 * 400
        lineas.append(
            f"\n🚜 *Referencia para tus rollos (350-400 kg):*\n"
            f"1° calidad (${precio_rollo_1}/kg): *${min_ref:,.0f} - ${max_ref:,.0f}*".replace(",", ".")
        )

    lineas.append(f"\n🔗 [Ver fuente en TodoAgro]({URL})")
    return "\n".join(lineas)

def enviar_telegram(mensaje):
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    r = requests.post(api_url, json=payload, timeout=15)
    r.raise_for_status()

if __name__ == "__main__":
    reporte = obtener_precios()
    enviar_telegram(reporte)
