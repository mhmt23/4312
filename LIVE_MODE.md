# ⚠️ CANLI MOD - GERÇEK TRADE REHBERİ

## 🔴 DİKKAT: GERÇEK PARA İLE ÇALIŞIYORSUN!

`DEMO_MODE = False` → Bot **GERÇEK** trade açacak!

---

## 🐳 DAĞITIM SEÇENEKLERİ

Botu iki şekilde dağıtabilirsiniz:

1. **Doğrudan Ubuntu** (Önerilen)
2. **Docker ile** (İzole ortam, kolay yönetim)

Detaylı kurulum adımları aşağıdadır.

## ✅ BAŞLATMADAN ÖNCE KONTROL LİSTESİ

### 1. Binance Ayarları
- [ ] Binance hesabında yeterli bakiye var mı? (min $1000 önerilen)
- [ ] Futures Trading aktif mi?
- [ ] API izinleri doğru mu? (Futures Trading + Read)
- [ ] **IP Restriction** MUTLAKA ekle! (Güvenlik için)
- [ ] 2FA aktif mi?

### 2. Bot Ayarları
- [ ] `config.py` kontrol edildi mi?
  - `TOTAL_CAPITAL` = Gerçek bakiyenle uyumlu
  - `LEVERAGE` = Rahat hissettiğin seviye (10x fazla olabilir, 5x dene)
  - `POSITION_SIZE_PERCENT` = %10 uygun mu? (çok büyük değil)
  - `MAX_OPEN_POSITIONS` = 3 uygun mu?
- [ ] `.env` dosyasında API'ler doğru mu?
- [ ] Test edildi mi? (`python3 test_setup.py`)

### 3. İlk Çalıştırma Stratejisi
- [ ] **Küçük sermaye ile başla** ($100-200)
- [ ] İlk 24 saat sürekli izle
- [ ] İlk trade'i manuel kontrol et (Binance'de gözükecek)
- [ ] Telegram bildirimleri kurulu mu?

---

## 🚀 GÜVENLE BAŞLAT (Adım Adım)

### Seçenek 1: Doğrudan Ubuntu (Önerilen)

### Adım 1: Binance IP Restriction (ZORUNLU!)

```
1. Binance'e giriş yap
2. API Management → Edit API
3. Restrict access to trusted IPs only
4. Sunucu IP'sini ekle

Sunucu IP'ni öğrenmek için:
curl ifconfig.me
```

⚠️ **Bu adımı atlarsan, API'ler çalınırsa hesabın boşaltılabilir!**

---

### Adım 2: Test Çalıştırması (10 Dakika İzle)

```bash
# Sunucuda
cd ~/ai-whale-bot
source venv/bin/activate

# Direkt çalıştır (logları ekranda gör)
python3 main_pro.py
```

İlk 10 dakika:
- ✅ Bot başladı mı?
- ✅ Whale pump taraması çalışıyor mu?
- ✅ Binance'e bağlanıyor mu?
- ✅ Hata var mı?

**Herhangi bir sorun varsa**: `CTRL+C` ile durdur, düzelt, tekrar başlat

---

### Adım 3: Arkaplanda Çalıştır

```bash
# Her şey yolundaysa, arkaplanda başlat
nohup python3 main_pro.py > bot.log 2>&1 &

# Logları izle
tail -f bot.log
```

---

## 📱 TELEGRAM BİLDİRİMLERİ (Şiddetle Tavsiye!)

Bot ne zaman trade açsa/kapatsa sana bildirim gelsin:

### Kurulum:
```bash
# 1. @BotFather'da bot oluştur → Token al
# 2. Botunla konuş
# 3. https://api.telegram.org/botTOKEN/getUpdates → Chat ID bul
# 4. .env dosyasına ekle

nano .env

# Ekle:
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=123456789

# Kaydet: CTRL+X, Y, ENTER

# Test et:
python3 -c "
import requests, os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
url = f'https://api.telegram.org/bot{token}/sendMessage'
r = requests.post(url, json={'chat_id': chat_id, 'text': '🔴 Bot canlı modda başladı!'})
print('✅ Telegram OK!' if r.status_code == 200 else f'❌ Hata: {r.status_code}')
"
```

---

## 🎯 İLK TRADE'İ NASIL TAKİP EDERİM?

### 1. Loglardan İzle
```bash
tail -f ~/ai-whale-bot/bot.log

# Şunları göreceksin:
# 🐋 WHALE PUMP: APEUSDT +%52
# 🧠 AI ONAY: %87
# 🔴 SHORT: APEUSDT @ $1.2340
# ✅ GERÇEK TRADE AÇILDI!
```

### 2. Binance'den Kontrol Et
```
Binance → Futures → Positions
Orada açık pozisyonunu göreceksin
```

### 3. Telegram'dan Bildirim Gelecek
```
🔴 SHORT AÇILDI
APEUSDT @ $1.2340
Değer: $100.00
🧠 AI Psychology
```

---

## ⚠️ ACİL DURUM PROSEDÜRÜ

### Bot Hemen Durdur
```bash
# Process ID bul
ps aux | grep main_pro.py

# Durdur
kill <PID>

# Veya hepsini durdur
pkill -f main_pro.py
```

### Tüm Pozisyonları Manuel Kapat
```bash
# Python ile
python3 << 'EOF'
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

positions = client.futures_position_information()
for pos in positions:
    if float(pos['positionAmt']) != 0:
        symbol = pos['symbol']
        amount = abs(float(pos['positionAmt']))
        side = 'BUY' if float(pos['positionAmt']) < 0 else 'SELL'
        print(f"Kapatılıyor: {symbol} {side} {amount}")
        try:
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=amount
            )
            print(f"✅ {symbol} kapatıldı!")
        except Exception as e:
            print(f"❌ Hata: {e}")
EOF
```

**Veya** Binance web/app'ten manuel kapat

---

## 📊 İLK GÜN TAKİP

### Sürekli İzlenmesi Gerekenler:
```bash
# Her 5 dakikada bir kontrol et:

# 1. Bot çalışıyor mu?
ps aux | grep main_pro.py

# 2. Son loglar
tail -n 50 bot.log

# 3. Binance pozisyonlar
# Web/app'ten kontrol et

# 4. Bakiye değişimi
# Binance'te kontrol et
```

### Beklenen Davranış:
- ✅ Her 2 saatte whale pump taraması
- ✅ Her 5 dakikada izleme listesi kontrolü
- ✅ AI analizi yapıyor
- ✅ Trade açıyor/kapatıyor
- ✅ Telegram bildirimleri geliyor

---

## 💡 PERFORMANS TAKİBİ

### Günlük Kontrol (Sabah)
```bash
# Dün ne oldu?
grep "SHORT:" ~/ai-whale-bot/bot.log | tail -20
grep "KAPANDI" ~/ai-whale-bot/bot.log | tail -20

# AI kararları
cat ~/ai-whale-bot/logs/decisions_$(date +%Y%m%d).json | jq '.'

# Kaç trade açıldı?
grep "GERÇEK TRADE" ~/ai-whale-bot/bot.log | wc -l
```

### Haftalık Analiz
```bash
# Bu haftaki tüm trade'ler
grep -E "SHORT:|KAPANDI" ~/ai-whale-bot/bot.log | tail -100

# Win rate hesapla (kârlı trade'ler / toplam)
# Binance'te "Closed PNL" kontrol et
```

---

## 🔒 GÜVENLİK TAVSİYELERİ

1. **IP Restriction**: MUTLAKA ekle
2. **2FA**: Aktif tut
3. **Withdrawal Whitelist**: Sadece kendi cüzdanını ekle
4. **API İzinleri**: Futures Trading + Read Only (Withdrawal KAPALI)
5. **Düzenli Kontrol**: Günde en az 2 kez kontrol et
6. **Backup**: Config ve .env dosyalarını yedekle

---

## 📈 OPTİMİZASYON (1 Hafta Sonra)

İlk haftadan sonra ayarları optimize et:

```python
# config.py ayarları:

# Daha az whale pump bulmak için:
MIN_PRICE_CHANGE_7D = 40  # %40'a çıkar

# Daha çok whale pump bulmak için:
MIN_PRICE_CHANGE_7D = 25  # %25'e düşür

# Daha dikkatli trade için:
MIN_AI_CONFIDENCE = 0.80  # %80'e çıkar

# Daha agresif trade için:
MIN_AI_CONFIDENCE = 0.65  # %65'e düşür

# Daha küçük pozisyon için:
POSITION_SIZE_PERCENT = 5  # %5'e düşür

# Risk yönetimi:
MAX_OPEN_POSITIONS = 2  # Aynı anda max 2 pozisyon
```

---

## 🎯 SON KONTROL

Başlatmadan hemen önce:

```bash
# 1. Test çalıştır
python3 test_setup.py

# 2. Config kontrol
cat config.py | grep "DEMO_MODE"
# Görmeli: DEMO_MODE = False

# 3. API test
python3 -c "
from binance.client import Client
import os
from dotenv import load_dotenv
load_dotenv()
c = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))
print('✅ Binance OK - Trade:', c.get_account()['canTrade'])
print('💰 Bakiye:', float(c.futures_account()['totalWalletBalance']), 'USDT')
"

# 4. AI test
python3 ai_engine_pro.py

# Her şey OK ise → BAŞLAT!
```

---

## 🚀 BAŞLATMA KOMUTU

```bash
cd ~/ai-whale-bot && \
source venv/bin/activate && \
echo "⚠️ CANLI MOD - 5 saniye içinde başlıyor..." && \
sleep 5 && \
nohup python3 main_pro.py > bot.log 2>&1 & \
echo "✅ Bot başlatıldı! PID: $!" && \
echo "📊 Loglar: tail -f bot.log" && \
sleep 2 && \
tail -f bot.log
```

---

## 🎊 BAŞARDIN!

Bot artık 7/24 çalışacak ve gerçek trade açacak!

**İlk 24 saat sürekli izle!**
**Telegram'ı aç ve bildirimleri takip et!**

**Başarılar! 🚀💰🐋**

---

**Acil Durum**: Herhangi bir sorun olursa `pkill -f main_pro.py` ile hemen durdur!
