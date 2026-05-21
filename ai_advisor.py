# models/ai_advisor.py
import os
import sqlite3
import pandas as pd
from google import genai  # Menggunakan SDK baru sesuai standar 2026
from dotenv import load_dotenv
from core.database import get_connection

load_dotenv()

# Inisialisasi Client baru (otomatis membaca GEMINI_API_KEY dari .env)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY tidak ditemukan di file .env!")
    client = None
else:
    client = genai.Client()  # Struktur Client baru

def get_financial_context():
    conn = get_connection()
    if not conn:
        return "Gagal terhubung ke database."
    
    try:
        # Gunakan query PostgreSQL untuk mengambil 30 transaksi terakhir
        query = """
            SELECT amount, category, description, type, timestamp 
            FROM transactions 
            ORDER BY timestamp DESC LIMIT 30
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Format konteks untuk AI
        from core.logic import get_balance
        current_balance = get_balance()
        
        context = f"Saldo Saat Ini: Rp{current_balance:,.0f}\n"
        context += "Histori Transaksi Terakhir:\n"
        if df.empty:
            context += "(Belum ada riwayat transaksi)"
        else:
            context += df.to_string(index=False)
        return context
        
    except Exception as e:
        print(f"❌ Error saat mengambil konteks Supabase: {e}")
        return "Saldo saat ini: Rp0."

async def ask_fincord_ai(user_question):
    if not client:
        return "Maaf, konfigurasi AI belum siap karena API Key hilang."
        
    try:
        context = get_financial_context()
        
        prompt = f"""
        Anda adalah Fincord, asisten keuangan pribadi yang cerdas, analitis, dan suportif.
        Berikut adalah data keuangan riil pengguna saat ini:
        {context}
        
        Pertanyaan Pengguna: "{user_question}"
        
        Tugas Anda:
        1. Berikan analisis finansial yang tajam namun ringkas INGKAT, PADAT, dan LANGSUNG PADA INTINYA (Maksimal 3-4 kalimat atau gunakan poin-poin pendek) berdasarkan data di atas.
        2. Jika user bertanya tentang rencana membeli barang, langsung jawab: BISA/TIDAK, berikan alasannya secara matematis berdasarkan saldo saat ini, lalu berikan 1 saran konkret.
        3. Berikan rekomendasi tindakan (saran konkret).
        4. Jawab dengan gaya bahasa Indonesia yang santai, edukatif, dan profesional.
        5. Jangan bertele-tele atau memberikan pembukaan/penutup yang panjang.
        """
        
        # Panggilan method generate_content versi SDK 2026
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        raise e