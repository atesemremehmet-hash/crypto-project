import requests

def get_bitcoin_price():
    # Binance'in halka açık anlık fiyat API adresi
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    
    try:
        response = requests.get(url)  # requests ve .get(url) düzeltildi
        data = response.json()
        symbol = data['symbol']
        price = float(data['price'])
        print(f"🚀 Canlı Bağlantı Başarılı!")
        print(f"Anlık {symbol} Fiyatı: ${price:,.2f}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    get_bitcoin_price()
            