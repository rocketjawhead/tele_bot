from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder

async def handle_message(update, context):
    user = update.effective_user
    username = f"@{user.username}" if user.username else str(user.id)
    text = update.message.text.strip()

    try:
        trx_number, sku_code, pin = text.split(".")
    except ValueError:
        await update.message.reply_text("Format salah. Gunakan: trx_number.sku_code.pin")
        return

    # Kirim ke API mokosel
    payload = {
        "username": username,
        "trx_number": trx_number,
        "sku_code": sku_code,
        "pin": pin
    }

    # Contoh kirim ke API pakai requests
    import requests
    response = requests.post("https://api.mokosel.com/api/Telegram/inquiryproduct", json=payload)

    if response.ok:
        await update.message.reply_text("Permintaan berhasil dikirim.")
    else:
        await update.message.reply_text("Gagal kirim ke API.")

app = ApplicationBuilder().token("7742109602:AAFbhpFMEVURFRmRowQ3-UcrPuhH5F0ZbkI").build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
