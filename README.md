# Fincord AI 🚀

Fincord AI adalah asisten finansial pribadi berbasis Artificial Intelligence yang terintegrasi langsung dengan Telegram. Bot ini dirancang untuk memudahkan pengguna dalam mencatat keuangan, memvisualisasikan data, dan memberikan saran finansial cerdas secara *real-time*.

## 🌟 Fitur Utama
* **Pencatatan Transaksi Natural Language (NLP):** Tidak perlu format kaku. Cukup ketik seperti *"Beli nasi padang 25rb"* dan bot akan otomatis mencatat.
* **Analisis AI:** Konsultasi finansial langsung dengan Google Gemini untuk mendapatkan saran penghematan atau analisis pengeluaran.
* **Visualisasi Data:** Generate grafik batang (arus kas) dan pie chart (distribusi pengeluaran) secara otomatis.
* **Reminder Rutin:** Pengingat otomatis untuk tagihan bulanan agar Anda tidak pernah terlambat membayar.
* **Alarm Saldo Kritis:** Peringatan otomatis jika saldo Anda mendekati batas aman yang ditentukan.
* **Cloud-Native:** Menggunakan PostgreSQL (Supabase) untuk penyimpanan data yang aman dan persisten.

## 🛠️ Tech Stack
* **Language:** Python 3.11+
* **Bot Framework:** `python-telegram-bot`
* **AI Engine:** Google Gemini API (`google-generativeai`)
* **Database:** Supabase (PostgreSQL)
* **Visualization:** Pandas & Matplotlib
* **Deployment:** Render.com

## 📂 Struktur Proyek
```text
fincord-ai/
├── core/            # Logika koneksi DB & helper bisnis
├── models/          # Engine AI, NLP, & Forecaster
├── utils/           # Generator chart & pemrosesan gambar
├── main.py          # Entry point aplikasi
└── requirements.txt # Daftar dependencies
