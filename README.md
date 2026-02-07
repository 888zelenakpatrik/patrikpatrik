# IoT Pilár – Meteostanica (Raspberry Pi)

## Cieľ projektu
Domáca IoT meteostanica postavená na Raspberry Pi, ktorá:
- meria teplotu a vlhkosť pomocou DHT11,
- ukladá merania do SQLite databázy,
- zobrazuje aktuálne meranie a posledných 20 meraní cez web rozhranie (Flask),
- po reštarte sa automaticky spúšťa (systemd service).

UI je v slovenskom jazyku.

---

## Použitý hardvér
- Raspberry Pi 4 Model B
- DHT11 (modul) – teplota / vlhkosť
- Prepojovacie vodiče
- Napájanie 5V 3A (stabilné napájanie je kritické)

### Zapojenie DHT11
DHT11 modul (3 piny) -> Raspberry Pi:
- VCC -> 3.3V (Pin 1)
- GND -> GND (Pin 6)
- DATA -> GPIO4 (BCM4) (Pin 7)

Poznámka: DHT11 je lacný senzor, občas vráti chybu „Checksum did not validate“. Logger tieto chyby ošetruje a číta znova.

---

## Softvér a architektúra
- OS: Debian/Raspberry Pi OS (aarch64)
- Python virtual env: `~/iot`
- Zber dát: `logger.py` (DHT11 -> SQLite)
- Web UI: `app.py` (SQLite -> Flask HTML)

Tok dát: **Senzor → Python logger → SQLite → Flask web UI**

---

## Inštalácia a spustenie (stručne)
### Projekt
```bash
cd ~
git clone <URL_GITHUB_REPO>
cd iot-pilar

