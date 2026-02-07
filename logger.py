import time
import sqlite3
from datetime import datetime

import board
import adafruit_dht


DB_PATH = "data.db"
INTERVAL_OK = 5          # sekúnd medzi úspešnými meraniami
INTERVAL_ERR = 2         # sekúnd po chybe čítania
GPIO_PIN = board.D4      # DATA pin DHT11


def init_db(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        temperature REAL,
        humidity REAL
    )
    """)
    conn.commit()


def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main() -> None:
    print("[LOGGER] IoT Pilár – štartujem logger…")

    # DB
    conn = sqlite3.connect(DB_PATH, timeout=10)
    init_db(conn)
    cur = conn.cursor()

    # DHT11
    dht = adafruit_dht.DHT11(GPIO_PIN, use_pulseio=False)

    ok_count = 0
    err_count = 0

    try:
        while True:
            try:
                t = dht.temperature
                h = dht.humidity

                # DHT11 občas vráti None, to je OK → preskoč
                if t is None or h is None:
                    err_count += 1
                    print(f"[{now_ts()}] WARN: None reading (t={t}, h={h})")
                    time.sleep(INTERVAL_ERR)
                    continue

                cur.execute(
                    "INSERT INTO measurements (timestamp, temperature, humidity) VALUES (?, ?, ?)",
                    (now_ts(), float(t), float(h))
                )
                conn.commit()
                ok_count += 1
                print(f"[{now_ts()}] OK: {t:.1f} °C | {h:.1f} % (ok={ok_count}, err={err_count})")

                time.sleep(INTERVAL_OK)

            except RuntimeError as e:
                # checksum / timing chyby z DHT11 – bežné
                err_count += 1
                print(f"[{now_ts()}] DHT WARN: {e} (ok={ok_count}, err={err_count})")
                time.sleep(INTERVAL_ERR)

            except sqlite3.Error as e:
                # DB problémy musia byť viditeľné
                err_count += 1
                print(f"[{now_ts()}] DB ERROR: {e} (ok={ok_count}, err={err_count})")
                time.sleep(5)

            except Exception as e:
                # Nečakané chyby – nech to nespadne potichu
                err_count += 1
                print(f"[{now_ts()}] FATAL: {type(e).__name__}: {e} (ok={ok_count}, err={err_count})")
                time.sleep(5)

    except KeyboardInterrupt:
        print("\n[LOGGER] Zastavené používateľom (Ctrl+C).")

    finally:
        try:
            conn.close()
        except Exception:
            pass
        print("[LOGGER] Ukončené.")


if __name__ == "__main__":
    main()

