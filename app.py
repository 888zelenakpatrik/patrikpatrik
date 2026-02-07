from flask import Flask
import sqlite3

DB_PATH = "data.db"
app = Flask(__name__)

def fetch_one(q, params=()):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(q, params)
    row = cur.fetchone()
    conn.close()
    return row

def fetch_all(q, params=()):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(q, params)
    rows = cur.fetchall()
    conn.close()
    return rows

@app.get("/")
def index():
    latest = fetch_one(
        "SELECT timestamp, temperature, humidity FROM measurements ORDER BY id DESC LIMIT 1"
    )
    rows = fetch_all(
        "SELECT timestamp, temperature, humidity FROM measurements ORDER BY id DESC LIMIT 20"
    )

    if latest:
        ts, t, h = latest
        latest_html = f"""
        <h2>Aktuálne meranie</h2>
        <ul>
          <li><b>Čas:</b> {ts}</li>
          <li><b>Teplota:</b> {t:.1f} °C</li>
          <li><b>Vlhkosť:</b> {h:.1f} %</li>
        </ul>
        """
    else:
        latest_html = "<p><b>Žiadne dáta v databáze.</b></p>"

    table_rows = ""
    for ts, t, h in rows:
        table_rows += f"<tr><td>{ts}</td><td>{t:.1f}</td><td>{h:.1f}</td></tr>"

    return f"""
    <html lang="sk">
    <head>
      <meta charset="utf-8">
      <title>IoT Pilár – Meteostanica</title>
    </head>
    <body>
      <h1>IoT Pilár – Meteostanica</h1>
      {latest_html}
      <h2>Posledných 20 meraní</h2>
      <table border="1" cellpadding="6" cellspacing="0">
        <tr><th>Čas</th><th>Teplota (°C)</th><th>Vlhkosť (%)</th></tr>
        {table_rows}
      </table>
      <p><i>Zdroj dát: SQLite databáza na Raspberry Pi</i></p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

