"""AI Engine - DeepSeek Integration"""
import os
import json
import requests
from datetime import datetime

class AIEngine:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"
        self.max_tokens = 1000
        self.temperature = 0.3
        print("🤖 AI Engine başlatıldı")
    
    def analyze_trade(self, symbol, technical_data):
        """Teknik analiz verilerini AI'ya gönder ve karar al"""
        try:
            prompt = self._create_analysis_prompt(symbol, technical_data)
            response = self._call_deepseek(prompt)
            
            if response:
                return self._parse_response(response)
            else:
                return self._get_fallback_response("API çağrısı başarısız")
                
        except Exception as e:
            print(f"❌ AI analiz hatası: {e}")
            return self._get_fallback_response(str(e))
    
    def _create_analysis_prompt(self, symbol, data):
        """AI için optimize edilmiş prompt oluştur"""
        prompt = f"""Sen profesyonel bir kripto trader AI'sısın. Whale pump sonrası SHORT pozisyonu açıp açmayacağıma karar ver.

📊 COIN ANALİZİ:
Sembol: {symbol}
Güncel Fiyat: ${data.get('price', 0):.4f}
7 Günlük Değişim: +{data.get('change_7d', 0):.1f}%

📈 TEKNİK GÖSTERGELER:
- Volume Düşüşü: {data.get('volume_drop', 0)*100:.0f}% (peak'ten)
- Momentum (15m): {data.get('momentum', 0):.1f}%
- RSI: {data.get('rsi', 50):.0f}
- BTC Değişim (1h): {data.get('btc_change', 0):.1f}%
- Teknik Skor: {data.get('score', 0)}/4

CEVAP FORMATINDA SADECE JSON VER:
{{
    "should_trade": true/false,
    "confidence": 0.85,
    "reasoning": "Sebep...",
    "risk_reward": 3.5,
    "stop_loss_percent": 3.0,
    "take_profit_levels": [5.0, 10.0, 15.0]
}}"""
        return prompt
    
    def _call_deepseek(self, prompt, max_retries=2):
        """DeepSeek API çağrısı yap"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Sen bir profesyonel kripto trader AI asistanısın."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(self.api_url, headers=headers, json=payload, timeout=15)
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                else:
                    print(f"⚠️ API Hata {response.status_code}")
            except Exception as e:
                print(f"❌ API çağrı hatası: {e}")
        return None
    
    def _parse_response(self, response_text):
        """AI cevabını parse et"""
        try:
            response_text = response_text.strip()
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]
            
            data = json.loads(response_text)
            data['confidence'] = max(0.0, min(1.0, float(data['confidence'])))
            data['should_trade'] = bool(data['should_trade'])
            
            if 'risk_reward' not in data:
                data['risk_reward'] = 2.0
            if 'stop_loss_percent' not in data:
                data['stop_loss_percent'] = 3.0
            if 'take_profit_levels' not in data:
                data['take_profit_levels'] = [5.0, 10.0, 15.0]
            
            return data
        except Exception as e:
            print(f"❌ Parse hatası: {e}")
            return self._get_fallback_response("JSON hatası")
    
    def _get_fallback_response(self, reason):
        """AI hata verirse güvenli fallback"""
        return {
            'should_trade': False,
            'confidence': 0.0,
            'reasoning': f"AI analiz başarısız: {reason}",
            'risk_reward': 0.0,
            'stop_loss_percent': 5.0,
            'take_profit_levels': [5.0, 10.0, 15.0]
        }


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    ai = AIEngine()
    test_data = {
        'symbol': 'LINKUSDT',
        'price': 10.45,
        'change_7d': 47.5,
        'score': 3,
        'rsi': 78,
        'volume_drop': 0.68,
        'momentum': -2.3,
        'btc_change': 0.5
    }
    
    print("\n🧪 Test başlatılıyor...\n")
    result = ai.analyze_trade('LINKUSDT', test_data)
    print(f"\n📊 Sonuç: {json.dumps(result, indent=2, ensure_ascii=False)}")
