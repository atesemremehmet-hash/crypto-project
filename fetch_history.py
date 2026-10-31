# fetch_history.py
import sqlite3
import requests
from datetime import datetime

# 1. Veritabanı bağlantısını oluşturalım (Aynı klasördeki crypto.db dosyası)
DB_NAME = "crypto.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Geçmiş mum (kline) verilerini saklayacağımız tabloyu oluşturuyoruz
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            timestamp TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL
        )
    """)
    conn.commit()
    conn.close()
    print("Veritabanı tablosu hazır.")

def fetch_binance_history(symbol="BTCUSDT", interval="1d", limit=365):
    """
    Binance REST API'den geçmiş verileri (klines) çeker.
    interval='1d' -> Günlük mumlar
    limit=365 -> Son 365 gün (1 yıl)
    """
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"{symbol} için veri çekilirken hata oluştu: {e}")
        return []

def save_to_db(symbol, klines):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    count = 0
    for kline in klines:
        # Binance kline veri formatı:
        # [0: Open time, 1: Open, 2: High, 3: Low, 4: Close, 5: Volume, ...]
        timestamp_ms = kline[0]
        # Milisaniye cinsinden zamanı okunabilir tarih formatına (YYYY-MM-DD HH:MM:SS) çeviriyoruz
        readable_time = datetime.fromtimestamp(timestamp_ms / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
        
        open_price = float(kline[1])
        high_price = float(kline[2])
        low_price = float(kline[3])
        close_price = float(kline[4])
        volume = float(kline[5])
        
        cursor.execute("""
            INSERT INTO historical_prices (symbol, timestamp, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (symbol, readable_time, open_price, high_price, low_price, close_price, volume))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"[{symbol}] için {count} günlük veri veritabanına başarıyla kaydedildi.")

if __name__ == "__main__":
    print("Geçmiş veri toplama süreci başlatılıyor...")
    
    # Veritabanını ve tabloyu hazırla
    init_db()
    
    # Belirlediğimiz ilk 5 büyük coin sepeti
    coins = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
    
    for coin in coins:
        print(f"{coin} verileri çekiliyor...")
        raw_data = fetch_binance_history(symbol=coin, interval="1d", limit=365)
        if raw_data:
            save_to_db(coin, raw_data)
            
    print("Tüm coinlerin 1 yıllık geçmiş verileri başarıyla kaydedildi!")