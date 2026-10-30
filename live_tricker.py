import asyncio
import websockets
import json

async def watch_binance_price():
    # Binance WebSocket halka açık BTC/USDT anlık işlem akışı adresi
    uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    
    print("🔄 Binance canlı veri akışına bağlanılıyor... (Durdurmak için Ctrl+C basabilirsin)\n")
    
    async with websockets.connect(uri) as websocket:
        while True:
            # Borsadan gelen her yeni anlık veriyi dinle
            message = await websocket.recv()
            data = json.loads(message)
            
            price = float(data['p'])
            quantity = float(data['q'])
            
            print(f"Anlık İşlem -> Fiyat: ${price:,.2f} | Miktar: {quantity} BTC")

if __name__ == "__main__":
    try:
        asyncio.run(watch_binance_price())
    except KeyboardInterrupt:
        print("\n🛑 Bağlantı güvenli bir şekilde kapatıldı.")