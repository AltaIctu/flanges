import sqlite3

def sql_request(request):
    conn = sqlite3.connect(f'PNEN10216_2.db')
    c = conn.cursor()
    respond = c.execute(request)
    return respond.fetchall()

def columns(table_name):
    return [i[1] for i in sql_request(f"PRAGMA table_info({table_name})")]

