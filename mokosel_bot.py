from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes
from telegram import Update
import requests
import asyncio

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else str(user.id)
    text = update.message.text.strip()

    try:
        trx_number, sku_code, pin = text.split(".")
    except ValueError:
        await update.message.reply_text("Format salah. Gunakan: trx_number.sku_code.pin")
        return

    payload = {
        "username": username,
        "trx_number": trx_number,
        "sku_code": sku_code,
        "pin": pin
    }

    # Kirim POST request ke API pakai thread executor supaya gak nge-freeze
    def send_request():
        try:
            return requests.post("https://api.mokosel.com/api/Telegram/inquiryproduct", json=payload)
        except Exception as e:
            return e

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, send_request)

    # Cek hasilnya
    if isinstance(result, Exception):
        await update.message.reply_text(f"Terjadi error: {result}")
    elif result.ok:
        await update.message.reply_text("Permintaan berhasil dikirim.")
    else:
        await update.message.reply_text(f"Gagal kirim ke API. Status code: {result.status_code}")

# Jalankan bot
app = ApplicationBuilder().token("7742109602:AAFbhpFMEVURFRmRowQ3-UcrPuhH5F0ZbkI").build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
