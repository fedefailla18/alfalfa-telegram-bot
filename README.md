# 🌱 Monitor de Precios de Alfalfa (`alfalfa-telegram-bot`)

Bot automatizado en Python que extrae periódicamente los valores de referencia de la **Cámara Argentina de la Alfalfa** (publicados en TodoAgro), calcula el valor estimado para rollos de **350 a 400 kg** y envía el reporte directamente a Telegram mediante **GitHub Actions**.

## 🚀 Arquitectura y funcionamiento

El proyecto funciona en dos modos complementarios:
1. **Notificaciones automáticas (Push - Este repositorio):** Un workflow de GitHub Actions ejecuta `scraper.py` de forma programada y envía el resumen diario a un chat de Telegram.
2. **Consultas interactivas (Webhook - Google Apps Script):** El bot `@alfalfa_precios_bot` responde en tiempo real a comandos como `precios`, `primera 380` o `segunda 400`. (VER EN https://script.google.com/home/projects/1GvyOCKTy8LFkFR4z0t5vwXzkPObiIdJU8LnP1KfYWbGN_F1oS5qQGWjj/edit)

## ⏰ Programación (Scheduler)

El workflow `.github/workflows/check_alfalfa.yml` utiliza la siguiente configuración de cron:

* **Horario configurado:** `0 13 * * 1-5`
* **Equivalencia local:** Lunes a viernes a las **10:00 AM (ART / UTC-3)**.
* **Ejecución manual:** Habilitada mediante `workflow_dispatch` desde la pestaña **Actions** de GitHub.

> **Nota sobre GitHub Actions:** GitHub pausa automáticamente los workflows programados si el repositorio no recibe commits durante 60 días seguidos. Si esto ocurre, basta con reactivarlo desde la pestaña *Actions*.

## 🔐 Variables de entorno (Secrets)

Para que el script funcione en GitHub Actions, deben estar configurados los siguientes secretos en **Settings > Secrets and variables > Actions**:

| Secret | Descripción |
| :--- | :--- |
| `TELEGRAM_TOKEN` | Token HTTP API entregado por `@BotFather` para `@alfalfa_precios_bot`. |
| `TELEGRAM_CHAT_ID` | ID numérico del usuario o grupo destino que recibirá los reportes. |

## 📂 Estructura del repositorio

```text
├── .github/
│   └── workflows/
│       └── check_alfalfa.yml   # Definición del cronjob y entorno Python
├── scraper.py                  # Script de extracción (BeautifulSoup) y envío a Telegram
└── README.md                   # Documentación del proyecto
```

## 🛠️ Ejecución local (opcional)

Si deseas correr el script de forma manual en tu máquina:

```bash
pip install requests beautifulsoup4
export TELEGRAM_TOKEN="tu_token"
export TELEGRAM_CHAT_ID="tu_chat_id"
python scraper.py
```
