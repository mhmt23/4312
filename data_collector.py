"""Data Collector - Basit Veri Toplama"""
import requests
from datetime import datetime

class DataCollector:
    def __init__(self):
        print("📡 Data Collector başlatıldı")
    
    def get_coin_sentiment(self, symbol):
        """
        Coin hakkında basit sentiment analizi
        (İlk versiyonda basit, sonra Twitter/Reddit ekleriz)
        """
        try:
            # Şimdilik Binance haberlerinden veya fiyat momentumundan basit sentiment
            sentiment_score = self._analyze_price_sentiment(symbol)
            
            if sentiment_score > 0.3:
                return "positive"
            elif sentiment_score < -0.3:
                return "negative"
            else:
                return "neutral"
                
        except Exception as e:
            print(f"⚠️ Sentiment hatası: {e}")
            return "neutral"
    
    def _analyze_price_sentiment(self, symbol):
        """
        Basit fiyat bazlı sentiment
        (Gelecekte social media verileri eklenecek)
        """
        try:
            # Binance API'den son 24 saat verisi
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                price_change_pct = float(data['priceChangePercent'])
                
                # Basit skor: -1 (çok negatif) ile +1 (çok pozitif)
                sentiment_score = price_change_pct / 100
                return max(-1.0, min(1.0, sentiment_score))
            
            return 0.0
            
        except Exception as e:
            print(f"⚠️ Price sentiment hatası: {e}")
            return 0.0
    
    def get_market_condition(self):
        """
        Genel piyasa durumu (BTC + alt dominance)
        """
        try:
            # BTC durumu
            btc_url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
            response = requests.get(btc_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                btc_change = float(data['priceChangePercent'])
                
                if btc_change > 2:
                    return "bullish"
                elif btc_change < -2:
                    return "bearish"
                else:
                    return "sideways"
            
            return "neutral"
            
        except Exception as e:
            print(f"⚠️ Market condition hatası: {e}")
            return "neutral"
    
    def get_funding_rate(self, symbol):
        """
        Funding rate'i al (long/short dengesini gösterir)
        Pozitif = Çok long var (short fırsatı olabilir)
        """
        try:
            url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                funding_rate = float(data['lastFundingRate']) * 100
                return funding_rate
            
            return 0.0
            
        except Exception as e:
            print(f"⚠️ Funding rate hatası: {e}")
            return 0.0
    
    def get_whale_signals(self, symbol):
        """
        Whale sinyalleri (basit versiyon)
        İleride order book depth, whale wallet movements eklenecek
        """
        try:
            # Şimdilik büyük volume hareketlerini kontrol et
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                volume_24h = float(data['quoteVolume'])
                trades_count = int(data['count'])
                
                # Ortalama trade size
                avg_trade_size = volume_24h / trades_count if trades_count > 0 else 0
                
                # Büyük trade'ler varsa whale aktivitesi olabilir
                if avg_trade_size > 50000:  # $50k+ ortalama
                    return {"has_whale_activity": True, "avg_trade_size": avg_trade_size}
                
                return {"has_whale_activity": False, "avg_trade_size": avg_trade_size}
            
            return {"has_whale_activity": False, "avg_trade_size": 0}
            
        except Exception as e:
            print(f"⚠️ Whale signals hatası: {e}")
            return {"has_whale_activity": False, "avg_trade_size": 0}
    
    def get_enriched_data(self, symbol):
        """
        Tüm ek verileri topla (AI'ya göndermek için)
        """
        return {
            'sentiment': self.get_coin_sentiment(symbol),
            'market_condition': self.get_market_condition(),
            'funding_rate': self.get_funding_rate(symbol),
            'whale_signals': self.get_whale_signals(symbol),
            'timestamp': datetime.now().isoformat()
        }


# Test
if __name__ == "__main__":
    collector = DataCollector()
    
    print("\n🧪 Test başlatılıyor...\n")
    
    symbol = "BTCUSDT"
    
    print(f"📊 {symbol} Analizi:")
    print(f"Sentiment: {collector.get_coin_sentiment(symbol)}")
    print(f"Piyasa: {collector.get_market_condition()}")
    print(f"Funding Rate: {collector.get_funding_rate(symbol):.4f}%")
    print(f"Whale Signals: {collector.get_whale_signals(symbol)}")
    
    print("\n📦 Zenginleştirilmiş Veri:")
    enriched = collector.get_enriched_data(symbol)
    import json
    print(json.dumps(enriched, indent=2, ensure_ascii=False))
