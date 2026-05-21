import re

def predict_category(description):
    desc = description.lower()
    mapping = {
        "makanan": ["nasi", "makan", "minum", "kopi", "warteg", "restoran", "bakso", "snack"],
        "transport": ["bensin", "grab", "gojek", "parkir", "ojek", "mrt", "bus"],
        "hiburan": ["nonton", "bioskop", "netflix", "game", "topup", "spotify"],
        "kesehatan": ["obat", "apotek", "dokter", "vitamin", "gym"],
        "tagihan": ["kost", "listrik", "wifi", "pulsa", "asuransi"]
    }
    for category, keywords in mapping.items():
        if any(kw in desc for kw in keywords):
            return category.capitalize()
    return "Lain-lain"

def parse_natural_language(text):
    text = text.lower()
    
    # 1. Jika ada kata tanya, prioritaskan ke AI (bukan transaksi)
    tanya_keywords = ["apa", "bagaimana", "kenapa", "aman", "bisakah", "bolehkah", "saran", "hitung"]
    if any(kw in text for kw in tanya_keywords) or "?" in text:
        return {"intent": "ai_consult"}

    # 2. Deteksi Intent Report
    if "report" in text or "laporan" in text or "grafik" in text:
        return {"intent": "report"}

    # 3. Ambil Angka (Nominal)
    numbers = re.findall(r'\d+', text.replace('.', '').replace(',', ''))
    if not numbers:
        return {"intent": "ai_consult"} # Jika tidak ada angka, tanya AI saja
    
    amount = float(numbers[0])
    
    # 4. Deteksi Tipe (Pemasukan vs Pengeluaran)
    income_keywords = ["dapat", "masuk", "gaji", "bonus", "terima", "pemasukan", "tabungan"]
    t_type = "income" if any(kw in text for kw in income_keywords) else "expense"
    
    # Filter: Jika nominal terlalu besar (misal > 1 Milyar) dan ada kata "beli/mau", 
    # kemungkinan besar itu diskusi, bukan catatan nyata.
    if amount > 1000000000: 
        return {"intent": "ai_consult"}

    clean_desc = re.sub(r'\d+', '', text).replace('rp', '').strip()
    
    return {
        "intent": "transaction",
        "amount": amount,
        "type": t_type,
        "description": clean_desc if clean_desc else "Transaksi Tanpa Judul",
        "category": "Pemasukan" if t_type == "income" else None
    }