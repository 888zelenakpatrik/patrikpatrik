# Runbook – IoT Pilár (skúška)

Tento dokument je rýchly postup, ako projekt spustiť a odkontrolovať funkčnosť počas skúšky.

## 1) IP adresa Raspberry Pi
```bash
hostname -I
```

## 2) Overenie, že logger beží po boote (systemd)
```bash
systemctl status iot-pilar-logger --no-pager
```
Očakávanie: `Active: active (running)`

## 3) Logy služby (posledných 50 riadkov)
```bash
journalctl -u iot-pilar-logger -n 50 --no-pager
```

## 4) Overenie, že sa ukladajú dáta do databázy
```bash
sqlite3 ~/iot-pilar/data.db "SELECT * FROM measurements ORDER BY id DESC LIMIT 5;"
```
Očakávanie: pribúdajú nové riadky (ID rastie).

## 5) Spustenie web rozhrania (manuálne)
```bash
source ~/iot/bin/activate
cd ~/iot-pilar
python app.py
```
Web v prehliadači:
```
http://<IP_RPI>:5000
```

## 6) Zastavenie webu
V okne, kde beží Flask:
```
Ctrl + C
```

## 7) Reštart logger služby
```bash
sudo systemctl restart iot-pilar-logger
systemctl status iot-pilar-logger --no-pager
```

## 8) Najčastejšie problémy a riešenia

### DHT11 – checksum chyby
- Hlásenie `Checksum did not validate` je bežné.
- DHT11 je lacný senzor, logger chyby ignoruje a pokračuje.

### Raspberry Pi zmizne zo siete
Najčastejšia príčina:
- slabé alebo nestabilné napájanie

Riešenie:
- použiť stabilné 5V / 3A napájanie
- skontrolovať USB-C kábel

### Databáza sa neplní
```bash
systemctl status iot-pilar-logger --no-pager
journalctl -u iot-pilar-logger -n 50 --no-pager
```

### Web neukazuje nové dáta
- Web iba číta z databázy
- Dáta zapisuje logger (systemd služba)
- Obnov stránku (F5) alebo reštartuj logger

