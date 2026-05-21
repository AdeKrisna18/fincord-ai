import pandas as pd
import matplotlib.pyplot as plt
import os
from core.database import get_connection

def generate_monthly_report_img(month_year):
    conn = get_connection()
    # Gunakan query PostgreSQL dengan parameter %s
    query = """
        SELECT category, amount FROM transactions 
        WHERE month_year = %s AND type = 'expense'
    """
    df = pd.read_sql_query(query, conn, params=(month_year,))
    conn.close()

    if df.empty:
        raise ValueError("No data found for this month")

    summary = df.groupby('category')['amount'].sum()

    plt.figure(figsize=(8, 6))
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0', '#ffb3e6']
    summary.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=colors[:len(summary)], explode=[0.05]*len(summary))
    plt.title(f"Distribusi Pengeluaran - {month_year}", fontsize=14)
    plt.ylabel('')
    
    # Simpan di folder sementara (sesuaikan dengan path cloud Anda)
    output_path = f'report_{month_year}.png'
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    return output_path

def generate_cashflow_chart(month_year):
    conn = get_connection()
    query = """
        SELECT type, SUM(amount) as total 
        FROM transactions 
        WHERE month_year = %s 
        GROUP BY type
    """
    df = pd.read_sql_query(query, conn, params=(month_year,))
    conn.close()

    if df.empty:
        raise ValueError("Data kosong")

    plt.figure(figsize=(8, 5))
    # Pastikan income hijau, expense merah
    colors = ['#4CAF50' if t == 'income' else '#F44336' for t in df['type']]
    
    bars = plt.bar(df['type'], df['total'], color=colors)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'Rp{yval:,.0f}', 
                 va='bottom', ha='center', fontweight='bold')

    plt.title(f"Arus Kas (Income vs Expense) - {month_year}", fontsize=14)
    plt.ylabel("Jumlah (Rupiah)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    output_path = f'cashflow_{month_year}.png'
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    return output_path