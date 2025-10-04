# 🚀 BAŞLANGIÇ REHBERİ

## 1. İlk Kurulum (5 dakika)

### Adım 1: Paketleri Yükle
```bash
cd C:\Users\ESME\claude\botcrypt\123
pip install -r requirements.txt
```

### Adım 2: API Anahtarlarını Gir
`.env` dosyasını aç ve düzenle:
```
DEEPSEEK_API_KEY=sk-9bc10973f79e41109a8dfd6b9d1392a1
API_KEY=your_binance_api_key_here  # Şimdilik opsiyonel
API_SECRET=your_binance_secret_here  # Şimdilik opsiyonel
```

### Adım 3: Test Et
```bash
python test_setup.py
```

Tüm testler ✅ olmalı!

---

## 2. İlk Test (AI Engine)

AI'nın nasıl çalıştığını görmek için:

```bash
python ai_engine.py
```

**Örnek Çıktı:**
```
🤖 AI Engine başlatıldı

🧪 Test başlatılıyor...

📊 AI ANALİZ SONUCU:
Trade Aç: True
Güven: %85
Sebep: Strong volume drop + extreme RSI + BTC stable
Risk/Reward: 1:3.5
Stop Loss: %3.0
Take Profit: [5.0, 10.0, 15.0]
```

---

## 3. Data Collector Testi

Binance verilerini test et:

```bash
python data_collector.py
```

**Örnek Çıktı:**
```
📡 Data Collector başlatıldı

🧪 Test başlatılıyor...

📊 BTCUSDT Analizi:
Sentiment: positive
Piyasa: bullish
Funding Rate: 0.0012%
Whale Signals: {'has_whale_activity': False, 'avg_trade_size': 45231}
```

---

## 4. Config Ayarları

`config.py` dosyasını aç ve ayarları kontrol et:

### Önemli Ayarlar:
```python
DEMO_MODE = True  # ⚠️ İlk başta True KALMALI!
ENABLE_AI = True  # AI'yı aktif et
TOTAL_CAPITAL = 1000  # Test sermayesi
LEVERAGE = 10  # Kaldıraç
```

### AI Ayarları:
```python
MIN_AI_CONFIDENCE = 0.70  # AI %70+ güvende olmalı
AI_MIN_TECHNICAL_SCORE = 2  # Teknik skor en az 2/4
```

---

## 5. Botu Başlat (Demo Mode)

```bash
python main.py
```

**İlk Ekran:**
```
======================================================================
🤖 AI-POWERED CRYPTO TRADING BOT v3.0
======================================================================
💰 Sermaye: $1000
⚡ Kaldıraç: 10x
🧠 AI: AKTIF
🎮 Mod: DEMO (Güvenli)
======================================================================

🎯 BOT BAŞLATILDI!

🔍 [14:30:00] Whale pump taraması...
```

---

## 6. Ne Olacak?

### Bot Döngüsü:
1. **Her 2 saatte**: Whale pump taraması (30%+ artışlar)
2. **Her 5 dakikada**: İzleme listesindeki coinleri kontrol
3. **AI Analizi**: Teknik skor yeterli ise AI'ya sorar
4. **Karar**: AI %70+ güven verirse trade açar (DEMO'da)
5. **Yönetim**: Açık pozisyonları takip eder

### Loglar:
```
🐋 WHALE PUMP BULUNDU: LINKUSDT +%45
   📊 LINKUSDT: Vol↓68% | Mom-2.3% | BTC+0.5% | RSI78 = Skor:3/4
   🤖 AI analiz ediliyor...
   ✅ AI ONAY: %85 güven
   💭 Sebep: Strong volume drop and extreme RSI...
   
🔴 SHORT POZİSYON AÇILIYOR:
   Coin: LINKUSDT
   Fiyat: $10.4500
   Miktar: 0.956
   Değer: $100.00
   🤖 AI Güven: %85
   🎯 Risk/Reward: 1:3.5
   ✅ DEMO TRADE AÇILDI (Gerçek değil)
```

---

## 7. Logları İncele

Botu 1-2 saat çalıştır, sonra logları kontrol et:

```bash
# Windows
notepad logs\decisions_20251004.json

# Python ile analiz
python -c "
import json
with open('logs/decisions_20251004.json') as f:
    logs = json.load(f)
    print(f'Toplam Karar: {len(logs)}')
    print(f'AI Onaylı: {sum(1 for l in logs if l[\"action_taken\"] == \"opened_short\")}')
"
```

---

## 8. Canlıya Geçiş (Dikkat!)

### Demo'da başarılıysan:

1. **Binance API Oluştur**
   - https://www.binance.com/en/my/settings/api-management
   - Futures Trading iznini aç
   - IP kısıtlaması ekle (güvenlik)

2. **Config'i Güncelle**
   ```python
   DEMO_MODE = False  # ⚠️ Artık gerçek trade!
   TOTAL_CAPITAL = 100  # KÜÇÜK BAŞLA!
   LEVERAGE = 5  # Düşük kaldıraç
   ```

3. **ENV'i Güncelle**
   ```
   API_KEY=binance_api_key
   API_SECRET=binance_api_secret
   ```

4. **Test Trade**
   - İlk trade'i manuel kontrol et
   - Binance'te gerçekten açıldı mı?
   - Stop-loss var mı?

---

## 9. Telegram Bildirimleri (Opsiyonel)

### Telegram Bot Oluştur:
1. @BotFather'a git
2. `/newbot` yaz
3. Token'ı kopyala

### Chat ID Bul:
1. Botunla konuşmaya başla
2. https://api.telegram.org/botYOUR_TOKEN/getUpdates
3. `chat.id` değerini kopyala

### ENV'e Ekle:
```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=123456789
```

---

## 10. Sorun Giderme

### AI yanıt vermiyor
```
❌ AI analiz hatası: 401 Unauthorized
```
**Çözüm**: DeepSeek API anahtarını kontrol et

### Binance API hatası
```
❌ APIError: Signature for this request is not valid
```
**Çözüm**: API Secret'ı doğru girdiğinden emin ol

### Hiç whale pump bulamıyor
```
✅ Tarama tamamlandı: 0 yeni whale pump
```
**Normal**: Whale pump her gün olmaz. Sabırlı ol veya `MIN_PRICE_CHANGE_7D` değerini düşür (örn: 20)

### AI sürekli red ediyor
```
❌ AI RED: %45 güven (min %70)
```
**Normal**: AI dikkatli, düşük güvende trade açmaz. Bu iyi!

---

## 11. Gelecek Adımlar

### 1 Hafta Sonra:
- [ ] Demo loglarını analiz et
- [ ] AI başarı oranını hesapla
- [ ] Parametreleri optimize et

### 2 Hafta Sonra:
- [ ] Küçük sermaye ile canlıya geç
- [ ] İlk gerçek trade'i yap
- [ ] Sonuçları değerlendir

### 1 Ay Sonra:
- [ ] Twitter sentiment ekle (Faz 2)
- [ ] Backtesting sistemi kur
- [ ] Strateji geliştir

---

## 📞 Yardım

Sorun mu yaşıyorsun?

1. **Önce test et**: `python test_setup.py`
2. **Logları kontrol et**: `logs/` klasörü
3. **Config'i gözden geçir**: `config.py`
4. **README oku**: Detaylı bilgi var

---

## ⚠️ ÖNEMLİ HATIRLATMALAR

1. ✅ **İlk testleri DEMO modda yap**
2. ✅ **Küçük sermaye ile başla**
3. ✅ **Stop-loss kullan**
4. ✅ **Kaybedeceğin parayı yatır**
5. ✅ **Piyasayı öğren**

**Başarılar! 🚀**
