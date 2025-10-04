"""AI Engine PRO - Gelişmiş DeepSeek Entegrasyonu"""
import os
import json
import requests
from datetime import datetime

class AIEnginePro:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"
        self.max_tokens = 2000
        self.temperature = 0.2  # Daha tutarlı kararlar
        print("🧠 AI Engine PRO başlatıldı")
    
    def analyze_whale_psychology(self, symbol, technical_data, market_context):
        """
        WHALE PSİKOLOJİSİNİ ANALİZ ET
        - Pump & Dump davranış kalıpları
        - FOMO/FUD döngüleri
        - Manipülasyon sinyalleri
        """
        prompt = self._create_psychology_prompt(symbol, technical_data, market_context)
        response = self._call_deepseek(prompt)
        
        if response:
            return self._parse_response(response)
        else:
            return self._get_fallback_response("API çağrısı başarısız")
    
    def _create_psychology_prompt(self, symbol, data, context):
        """
        GELİŞMİŞ PSİKOLOJİK ANALİZ PROMPTU
        """
        prompt = f"""Sen bir **WHALE PSİKOLOJİSİ UZMANI** ve profesyonel kripto trader'sın.

🎯 GÖREVİN: {symbol} coininde whale manipülasyonunu tespit et ve SHORT fırsatı olup olmadığına karar ver.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 WHALE PUMP VERİLERİ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 **{symbol}**
💵 Fiyat: ${data.get('price', 0):.4f}
📈 7 Günlük Artış: **+{data.get('change_7d', 0):.1f}%** (WHALE PUMP!)
📊 24h Volume: ${data.get('volume_24h', 0):,.0f}

🧪 TEKNİK GÖSTERGELER:
━━━━━━━━━━━━━━━━━━━
📉 Volume Düşüşü: **{data.get('volume_drop', 0)*100:.0f}%** (peak'ten)
⚡ Momentum (15dk): **{data.get('momentum', 0):.1f}%**
🎢 RSI: **{data.get('rsi', 50):.0f}** {"🔴 EXTREME OVERBOUGHT!" if data.get('rsi', 50) > 75 else "⚠️ Overbought" if data.get('rsi', 50) > 70 else ""}
₿ BTC Korelasyon: **{data.get('btc_change', 0):.1f}%**
📊 Teknik Skor: **{data.get('score', 0)}/4**

🌐 PİYASA DURUMU:
━━━━━━━━━━━━━━━━━
💭 Sentiment: **{context.get('sentiment', 'neutral').upper()}**
📈 Market Condition: **{context.get('market_condition', 'neutral').upper()}**
💰 Funding Rate: **{context.get('funding_rate', 0):.4f}%** {"(Çok fazla long var!)" if context.get('funding_rate', 0) > 0.05 else ""}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 PSİKOLOJİK ANALİZ SORUSU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎭 **WHALE DAVRANIŞI:**
Bu +{data.get('change_7d', 0):.0f}% artış bir whale pump mı? Şu soruları analiz et:

1. **PUMP FAZİ**: Whale'ler bu coin'i neden pumplaladı?
   - Düşük market cap'ten mi yararlanıyorlar?
   - Retail yatırımcıları cezbetmek için mi?
   - FOMO yaratmak için mi?

2. **DUMP SİNYALLERİ**: Şimdi dump zamanı mı?
   - Volume düşüşü ({data.get('volume_drop', 0)*100:.0f}%) whale'lerin çıkış yaptığını gösteriyor mu?
   - RSI {data.get('rsi', 50):.0f} - retail'ler tepede mi yakalandı?
   - Momentum yavaşlaması dump başlangıcı mı?

3. **RETAİL PSİKOLOJİSİ**: Küçük yatırımcılar ne yapıyor?
   - FOMO'da mı? (geç alıyorlar mı?)
   - Panik satış başladı mı?
   - Hala "daha da çıkar" umudu mu var?

4. **MARKET MANİPÜLASYONU RİSKİ**:
   - Yapay volume var mı?
   - Wash trading (sahte işlem) belirtisi?
   - Koordineli whale hareketi mi yoksa organik artış mı?

5. **TİMİNG**: Şimdi short açmak için doğru zaman mı?
   - Erken mi? (daha pump olabilir)
   - Geç mi? (dump başladı)
   - TAM ZAMANINDA MI? ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ KRİTİK KURALLAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. **SADECE %80+ GÜVEN İLE TRADE ÖNER**
2. **Whale manipülasyonu kesinse ve dump başladıysa → SHORT**
3. **Belirsizlik varsa → BEKLE**
4. **Risk/Reward minimum 1:3 olmalı**
5. **Psikolojik analiz teknik analizden ÖNEMLİ!**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 CEVAP FORMATINDA SADECE JSON VER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{{
    "should_trade": true/false,
    "confidence": 0.85,
    "whale_psychology": "Whale'ler pump tamamladı, şimdi retail'i trap ediyor. Volume düşüşü açık dump sinyali.",
    "market_manipulation": "Yüksek - Yapay pump belirtileri var, koordineli hareket görülüyor",
    "retail_sentiment": "FOMO - Geç girenler var, panik satış başlamak üzere",
    "timing_analysis": "MÜKEMMEL - Dump tam başladı, momentum kırıldı",
    "risk_reward": 3.5,
    "stop_loss_percent": 2.5,
    "take_profit_levels": [4.0, 8.0, 15.0],
    "key_reason": "Volume çöküşü + RSI extreme + whale çıkış sinyalleri = DUMP BAŞLADI"
}}

SADECE JSON CEVAP VER, BAŞKA HİÇBİR ŞEY YAZMA!"""
        
        return prompt
    
    def _call_deepseek(self, prompt, max_retries=2):
        """DeepSeek API çağrısı"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "Sen bir whale psychology uzmanı ve kripto manipülasyon dedektifisin. Pump & dump şemalarını tespit eder, retail psikolojisini analiz eder ve whale davranışlarını okursun. SADECE JSON formatında cevap verirsin."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=20
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                else:
                    print(f"⚠️ API Hata {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                print(f"⏱️ API timeout (deneme {attempt+1}/{max_retries})")
            except Exception as e:
                print(f"❌ API çağrı hatası: {e}")
        
        return None
    
    def _parse_response(self, response_text):
        """AI cevabını parse et"""
        try:
            response_text = response_text.strip()
            
            # JSON'u bul
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]
            
            # Parse et
            data = json.loads(response_text)
            
            # Validasyon
            required_keys = ['should_trade', 'confidence', 'whale_psychology']
            if not all(key in data for key in required_keys):
                print(f"⚠️ Eksik key'ler: {data}")
                return self._get_fallback_response("Eksik veri")
            
            # Güvenlik kontrolleri
            data['confidence'] = max(0.0, min(1.0, float(data['confidence'])))
            data['should_trade'] = bool(data['should_trade'])
            
            # Varsayılan değerler
            if 'risk_reward' not in data:
                data['risk_reward'] = 2.5
            if 'stop_loss_percent' not in data:
                data['stop_loss_percent'] = 3.0
            if 'take_profit_levels' not in data:
                data['take_profit_levels'] = [4.0, 8.0, 15.0]
            
            return data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse hatası: {e}")
            print(f"Response: {response_text[:300]}")
            return self._get_fallback_response("JSON hatası")
        except Exception as e:
            print(f"❌ Parse hatası: {e}")
            return self._get_fallback_response(str(e))
    
    def _get_fallback_response(self, reason):
        """AI hata verirse güvenli fallback"""
        return {
            'should_trade': False,
            'confidence': 0.0,
            'whale_psychology': f"AI analiz başarısız: {reason}",
            'market_manipulation': 'Unknown',
            'retail_sentiment': 'Unknown',
            'timing_analysis': 'Unknown',
            'risk_reward': 0.0,
            'stop_loss_percent': 5.0,
            'take_profit_levels': [5.0, 10.0, 15.0],
            'key_reason': 'AI error - no analysis'
        }


# Test
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    ai = AIEnginePro()
    
    # Test verisi - Whale pump sonrası
    test_data = {
        'symbol': 'APEUSDT',
        'price': 1.234,
        'change_7d': 52.3,
        'volume_24h': 45_000_000,
        'score': 3,
        'rsi': 76,
        'volume_drop': 0.65,
        'momentum': -3.2,
        'btc_change': 0.8
    }
    
    test_context = {
        'sentiment': 'positive',
        'market_condition': 'bullish',
        'funding_rate': 0.08
    }
    
    print("\n🧪 WHALE PSİKOLOJİ ANALİZİ TEST\n")
    print(f"Coin: {test_data['symbol']}")
    print(f"Pump: +{test_data['change_7d']}%")
    print(f"\n🤖 AI'ya gönderiliyor...\n")
    
    result = ai.analyze_whale_psychology('APEUSDT', test_data, test_context)
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 AI ANALİZ SONUCU")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{'Karar:':<20} {'SHORT AÇ! ✅' if result['should_trade'] else 'ATLA ❌'}")
    print(f"{'Güven:':<20} %{result['confidence']*100:.0f}")
    print(f"{'Risk/Reward:':<20} 1:{result['risk_reward']:.1f}")
    print(f"\n🎭 Whale Psikolojisi:\n{result['whale_psychology']}")
    print(f"\n🎯 Ana Sebep:\n{result.get('key_reason', 'N/A')}")
    print(f"\n📈 Take Profit: {result['take_profit_levels']}")
    print(f"🛑 Stop Loss: %{result['stop_loss_percent']}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
