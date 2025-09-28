import sqlite3, os, pandas as pd
def ensure_db(path="trades.db"):
    if path and os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    conn=sqlite3.connect(path); c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS trades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT, symbol TEXT, direction TEXT,
        entry REAL, stop REAL, tp REAL, result TEXT, pnl REAL, factors TEXT, live INTEGER DEFAULT 0)""")
    conn.commit(); conn.close()
def insert_trade(path, **k):
    ensure_db(path)
    conn=sqlite3.connect(path); c=conn.cursor()
    c.execute("""INSERT INTO trades (time,symbol,direction,entry,stop,tp,result,pnl,factors,live)
              VALUES (?,?,?,?,?,?,?,?,?,?)""",
              (k.get("time"),k.get("symbol"),k.get("direction"),k.get("entry"),k.get("stop"),
               k.get("tp"),k.get("result"),k.get("pnl"),k.get("factors"), int(k.get("live",0))))
    conn.commit(); conn.close()
def read_trades(path="trades.db"):
    ensure_db(path); conn=sqlite3.connect(path)
    df=pd.read_sql_query("SELECT * FROM trades ORDER BY time DESC", conn); conn.close(); return df
