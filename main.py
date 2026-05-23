import os
import datetime
import logging
from datetime import time
from dotenv import load_dotenv

from telegram import Update, constants
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, 
    MessageHandler, filters
)
from telegram.request import HTTPXRequest

# Modul Internal
from models.ai_advisor import ask_fincord_ai
from models.nlp_engine import parse_natural_language, predict_category
from utils.visualizer import generate_monthly_report_img, generate_cashflow_chart
from core.database import add_transaction
from core import logic

# 1. Konfigurasi Awal
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
SAFE_LIMIT = float(os.getenv('SAFE_LIMIT', 1500000))
MY_CHAT_ID = os.getenv('MY_CHAT_ID')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- FUNGSI REMINDER ---
async def tagihan_reminder_callback(context: ContextTypes.DEFAULT_TYPE):
    if datetime.datetime.now().day == 25:
        reminder_msg = (
            "🔔 <b>[REMINDER OTOMATIS FINCORD]</b>\n\n"
            "Halo! Hari ini tanggal 25, waktunya membayar tagihan rutin:\n"
            "🏠 Kost: Rp1.500.000 | 🏋️ Gym: Rp350.000"
        )
        await context.bot.send_message(chat_id=MY_CHAT_ID, text=reminder_msg, parse_mode=constants.ParseMode.HTML)

# --- HANDLER START & STATUS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Fincord aktif! Kirimkan transaksi atau tanya saya apapun seputar keuangan.", parse_mode=constants.ParseMode.HTML)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    balance = logic.get_balance()
    await update.message.reply_text(f"💳 <b>Saldo Anda:</b> Rp{balance:,.0f}", parse_mode=constants.ParseMode.HTML)

# --- HANDLER REPORT (VISUAL) ---
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    loading = await update.message.reply_text("🔄 Menyiapkan laporan...")
    try:
        month_year = datetime.datetime.now().strftime("%m-%Y")
        path_dist = generate_monthly_report_img(month_year)
        path_cash = generate_cashflow_chart(month_year)
        
        await update.message.reply_photo(photo=open(path_dist, 'rb'), caption="📊 Distribusi Pengeluaran")
        await update.message.reply_photo(photo=open(path_cash, 'rb'), caption="📈 Arus Kas")
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=loading.message_id)
    except Exception as e:
        await loading.edit_text("❌ Gagal membuat laporan. Pastikan sudah ada data transaksi.")

# --- HANDLER UTAMA (NLP & AI) ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    parsed = parse_natural_language(text)
    
    # KONSULTASI AI
    if parsed["intent"] == "ai_consult":
        msg = await update.message.reply_text("🤔 Fincord sedang menganalisis...")
        response = await ask_fincord_ai(text)
        await msg.edit_text(response)
            
    # REPORT
    elif parsed["intent"] == "report":
        await report(update, context)
        
    # TRANSAKSI OTOMATIS
    elif parsed["intent"] == "transaction":
        amount, t_type, desc = parsed["amount"], parsed["type"], parsed["description"]
        category = parsed["category"] or predict_category(desc)
        
        add_transaction(amount, category, desc, t_type, datetime.datetime.now().strftime("%m-%Y"))
        balance = logic.get_balance()
        
        reply = f"✅ <b>Tercatat!</b>\nJumlah: Rp{amount:,.0f}\nSisa Saldo: Rp{balance:,.0f}"
        if t_type == "expense" and balance < SAFE_LIMIT:
            reply += "\n\n⚠️ <b>ALARM: Saldo di bawah batas aman!</b>"
        await update.message.reply_text(reply, parse_mode=constants.ParseMode.HTML)

# --- MAIN RUNNER ---
if __name__ == '__main__':
    # Jika ada variabel 'PYTHONANYWHERE_SITE', berarti kita di server
    if 'PYTHONANYWHERE_SITE' in os.environ:
        app.run_webhook(
            listen="0.0.0.0",
            port=8443,
            url_path=TOKEN,
            webhook_url=f"https://username_anda.pythonanywhere.com/{TOKEN}"
        )
    else:
        # Jika di laptop (lokal), pakai polling biasa
        print("🚀 Fincord AI running in Local Mode...")
        app.run_polling()
