from core.database import get_connection

def get_balance():
    conn = get_connection()
    if not conn: return 0
    
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) - 
            COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0)
        FROM transactions
    """)
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result

def get_monthly_stats(month_year):
    conn = get_connection() # Diperbaiki: dari db.get_connection()
    if not conn: return {}
    
    cursor = conn.cursor()
    # PostgreSQL menggunakan %s sebagai placeholder, bukan ?
    cursor.execute("""
        SELECT type, SUM(amount) FROM transactions 
        WHERE month_year = %s GROUP BY type
    """, (month_year,))
    
    stats = dict(cursor.fetchall())
    cursor.close()
    conn.close()
    return stats 

def get_comparison(current_month_year, last_month_year):
    conn = get_connection() # Diperbaiki: dari db.get_connection()
    if not conn: return 0, 0
    
    cursor = conn.cursor()
    
    def get_total(my):
        # PostgreSQL menggunakan %s sebagai placeholder
        cursor.execute("""
            SELECT SUM(amount) FROM transactions 
            WHERE month_year = %s AND type = 'expense'
        """, (my,))
        res = cursor.fetchone()[0]
        return res if res else 0

    curr_total = get_total(current_month_year)
    last_total = get_total(last_month_year)
    
    cursor.close()
    conn.close()
    return curr_total, last_total