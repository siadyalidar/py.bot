import requests
import numpy as np
import talib
import time

API_KEY = "Dd3Tj4IsX4kbRSdyA9hs7XoBzFPoBKwn8pCblecEydya45FjJSxXBRBoPT1aWNmP"
API_SECRET = "0rODIxKWQPPJb06Ly8airNZKM8rkYriEoUKXPmRBEw6v9PS3N6EhNHXnFaLa3Kse"

def get_historical_candlesticks(symbol, interval, limit):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    return data

def calculate_rsi(prices, period=14):
    rsi = talib.RSI(prices, timeperiod=period)
    return rsi[-1]

def calculate_macd(prices, fast_period=12, slow_period=26, signal_period=9):
    macd, signal, _ = talib.MACD(prices, fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period)
    return macd[-1], signal[-1]

def get_realtime_prices(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    headers = {
        "X-MBX-APIKEY": API_KEY
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return float(data['price'])

def main():
    btc_symbol = "BTCUSDT"  # Bitcoin sembolü
    eth_symbol = "ETHUSDT"  # Ethereum sembolü
    interval = "1h"  # 1 saatlik mumlar
    limit = 100  # Son 100 mum

    while True:
        try:
            # Gerçek zamanlı BTC fiyatı
            btc_price = get_realtime_prices(btc_symbol)

            # Geçmiş BTC kapanış fiyatları
            btc_candlesticks = get_historical_candlesticks(btc_symbol, interval, limit)
            btc_prices = np.array([float(candlestick[4]) for candlestick in btc_candlesticks])  # Kapanış fiyatlarını al

            # Gerçek zamanlı ETH fiyatı
            eth_price = get_realtime_prices(eth_symbol)

            # Geçmiş ETH kapanış fiyatları
            eth_candlesticks = get_historical_candlesticks(eth_symbol, interval, limit)
            eth_prices = np.array([float(candlestick[4]) for candlestick in eth_candlesticks])  # Kapanış fiyatlarını al

            # BTC RSI hesaplama
            btc_rsi = calculate_rsi(btc_prices)

            # BTC MACD hesaplama
            btc_macd, btc_signal = calculate_macd(btc_prices)

            # ETH RSI hesaplama
            eth_rsi = calculate_rsi(eth_prices)

            # ETH MACD hesaplama
            eth_macd, eth_signal = calculate_macd(eth_prices)

            # Bollinger Bantları
            btc_upper_band, btc_middle_band, btc_lower_band = talib.BBANDS(btc_prices, timeperiod=20)
            eth_upper_band, eth_middle_band, eth_lower_band = talib.BBANDS(eth_prices, timeperiod=20)

            print("------- S1dar v0.1.1 Bot Verileri --------")
            print(f"Anlık BTC fiyatı: {btc_price:.2f}")
            print(f"BTC RSI: {btc_rsi:.2f}")
            if btc_rsi <= 30:
                print("RSI için Long işlem ve alım uygun bölge 🚀📈")
            elif btc_rsi <= 40:
                print("RSI için Satış baskını, kademeli alım yapılabilir 📈🔄")
            elif btc_rsi <= 50:
                print("RSI için Alım için riskli bölge ⚠️")
            elif btc_rsi <= 80:
                print("RSI için Alım için uygun değil ❌")
            else:
                print("RSI için Kademeli short işlem açılabilir 📉🔄")

            print(f"BTC MACD: {btc_macd:.2f}")
            print(f"BTC Signal: {btc_signal:.2f}")
            if btc_macd > btc_signal:
                print("MACD sinyal çizgisini yukarı yönde keserek alım sinyali 📈")
            elif btc_macd < btc_signal:
                print("MACD sinyal çizgisini aşağı yönde keserek satım sinyali 📉")
            else:
                print("MACD sinyal çizgisi ile kesişme yok, bekleyin ⏳")

            print("/" * 45)  # Değiştirilen sembol

            print(f"Anlık ETH fiyatı: {eth_price:.2f}")
            print(f"ETH RSI: {eth_rsi:.2f}")
            if eth_rsi <= 30:
                print("RSI için Long işlem ve alım uygun bölge 🚀📈")
            elif eth_rsi <= 40:
                print("RSI için Satış baskını, kademeli alım yapılabilir 📈🔄")
            elif eth_rsi <= 50:
                print("RSI için Alım için riskli bölge ⚠️")
            elif eth_rsi <= 80:
                print("RSI için Alım için uygun değil ❌")
            else:
                print("RSI için Kademeli short işlem açılabilir 📉🔄")

            print(f"ETH MACD: {eth_macd:.2f}")
            print(f"ETH Signal: {eth_signal:.2f}")
            if eth_macd > eth_signal:
                print("MACD sinyal çizgisini yukarı yönde keserek alım sinyali 📈")
            elif eth_macd < eth_signal:
                print("MACD sinyal çizgisini aşağı yönde keserek satım sinyali 📉")
            else:
                print("MACD sinyal çizgisi ile kesişme yok, bekleyin ⏳")

            print("*" * 45)  # Değiştirilen sembol

            time.sleep(5)  # 5 saniye bekle

        except Exception as e:
            print(f"Hata oluştu: {e}")
            print("*" * 45)

if __name__ == "__main__":
    main()
