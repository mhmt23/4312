# ⚡ HIZLI KOMUT REFERANSI

## 🚀 Hızlı Başlangıç

```bash
# Windows Başlatıcı (Otomatik kurulum + test)
start.bat

# Manuel Kurulum
pip install -r requirements.txt

# Sistem Testi
python test_setup.py

# Botu Başlat
python main.py

# Docker ile Başlat (Alternatif)
docker-compose up -d

# Docker loglarını izle
docker-compose logs -f
```

---

## 🐳 Docker Komutları

### Docker Kurulumu
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose -y

# CentOS/RHEL
sudo yum install docker docker-compose -y

# Docker servisini başlat
sudo systemctl start docker
sudo systemctl enable docker

# Kullanıcıyı docker grubuna ekle
sudo usermod -aG docker $USER
```

### Docker ile Derleme ve Çalıştırma
```bash
# Docker imajı oluştur
docker build -t whale-bot .

# Container çalıştır
docker run -d --name whale-bot \
  --env-file .env \
  -v ./logs:/app/logs \
  whale-bot python main_pro.py

# Logları izle
docker logs -f whale-bot
```

### Docker Compose ile Dağıtım
```bash
# Servisleri başlat (arkaplanda)
docker-compose up -d

# Logları izle
docker-compose logs -f

# Servis durumunu kontrol et
docker-compose ps

# Servisleri durdur
docker-compose down

# Tekrar başlat
docker-compose restart
```

### Docker Yönetim Komutları
```bash
# Çalışan container'ları listele
docker ps

# Tüm container'ları listele
docker ps -a

# Container detaylarını gör
docker inspect whale-bot

# Container'a shell erişimi
docker exec -it whale-bot /bin/bash

# Container'ı durdur
docker stop whale-bot

# Container'ı sil
docker rm whale-bot

# İmajı sil
docker rmi whale-bot
```

---

## 🧪 Test Komutları

### Tüm Sistemi Test Et
```bash
python test_setup.py
```

### AI Engine'i Test Et
```bash
python ai_engine.py
```

### Data Collector'ı Test Et
```bash
python data_collector.py
```

---

## 🔧 Geliştirme Komutları

### Paket Yükleme
```bash
# Temel paketler
pip install python-binance pandas requests python-dotenv

# Requirements'tan
pip install -r requirements.txt

# Güncelleme
pip install --upgrade python-binance
```

### Log İnceleme
```bash
# Windows
notepad logs\decisions_20251004.json
type logs\decisions_20251004.json

# Python ile analiz
python -c "import json; print(json.load(open('logs/decisions_20251004.json', 'r')))"
```

---

## 📊 Analiz Komutları

### Log Analizi (Python)
```python
import json
from datetime import datetime

# Bugünün loglarını oku
date_str = datetime.now().strftime('%Y%m%d')
with open(f'logs/decisions_{date_str}.json', 'r', encoding='utf-8') as f:
    logs = json.load(f)

# İstatistikler
total = len(logs)
ai_approved = sum(1 for log in logs if log['action_taken'] == 'opened_short')
avg_confidence = sum(log['ai_decision']['confidence'] for log in logs) / total if total > 0 else 0

print(f"Toplam Karar: {total}")
print(f"AI Onaylı: {ai_approved} (%{ai_approved/total*100:.1f})")
print(f"Ortalama Güven: %{avg_confidence*100:.0f}")
```

### Başarı Oranı Hesaplama
```python
import json

with open('logs/decisions_20251004.json', 'r') as f:
    logs = json.load(f)

# AI onaylı tradeler
approved_trades = [log for log in logs if log['action_taken'] == 'opened_short']

print(f"AI Onaylı Trade: {len(approved_trades)}")

# Güven dağılımı
for log in approved_trades:
    symbol = log['symbol']
    confidence = log['ai_decision']['confidence']
    print(f"{symbol}: %{confidence*100:.0f} güven")
```

---

## 🔐 Güvenlik Komutları

### ENV Dosyasını Kontrol Et
```bash
# Windows
type .env

# Linux/Mac
cat .env
```

### API Test
```python
from dotenv import load_dotenv
import os

load_dotenv()

# DeepSeek API kontrolü
deepseek_key = os.getenv('DEEPSEEK_API_KEY')
print(f"DeepSeek API: {'✅ Var' if deepseek_key else '❌ Yok'}")

# Binance API kontrolü
binance_key = os.getenv('API_KEY')
print(f"Binance API: {'✅ Var' if binance_key else '❌ Yok'}")
```

---

## 🎮 Bot Kontrolü

### Botu Başlat
```bash
python main.py
```

### Botu Durdur
```
CTRL + C
```

### Arkaplanda Çalıştır (Linux/Mac)
```bash
nohup python main.py > bot.log 2>&1 &

# Log takibi
tail -f bot.log
```

### Windows Service (İleri Seviye)
```bash
# NSSM kullanarak (https://nssm.cc/)
nssm install AITradingBot "C:\Python\python.exe" "C:\path\to\main.py"
nssm start AITradingBot
```

---

## 📝 Config Değişiklikleri

### Demo Mode Aç/Kapa
```python
# config.py
DEMO_MODE = True   # Test modu
DEMO_MODE = False  # Canlı mod (DİKKAT!)
```

### AI'yı Aktif/Pasif Yap
```python
# config.py
ENABLE_AI = True   # AI analizi aktif
ENABLE_AI = False  # Sadece teknik analiz
```

### Sermaye Değiştir
```python
# config.py
TOTAL_CAPITAL = 1000  # Test için
TOTAL_CAPITAL = 100   # Canlı için küçük başla
```

---

## 🐛 Debug Komutları

### Python Versiyonu
```bash
python --version
python -m pip --version
```

### Paket Listesi
```bash
pip list
pip show python-binance
```

### Import Testi
```python
import binance
import pandas
import requests
from dotenv import load_dotenv

print("✅ Tüm paketler yüklü!")
```

### Binance Bağlantı Testi
```python
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

try:
    info = client.get_account()
    print("✅ Binance'e bağlandı!")
except Exception as e:
    print(f"❌ Hata: {e}")
```

---

## 📱 Telegram Komutları

### Bot Test
```bash
curl -X POST "https://api.telegram.org/botYOUR_TOKEN/sendMessage" \
  -d "chat_id=YOUR_CHAT_ID" \
  -d "text=Test mesajı"
```

### Python ile Test
```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

url = f"https://api.telegram.org/bot{token}/sendMessage"
requests.post(url, json={"chat_id": chat_id, "text": "Bot test! 🤖"})
```

---

## 🔄 Güncelleme Komutları

### Git ile Güncelleme
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Manuel Yedekleme
```bash
# Windows
xcopy /E /I 123 123_backup_%date%

# Linux/Mac
cp -r 123 123_backup_$(date +%Y%m%d)
```

---

## 📊 Performans Monitoring

### CPU/Memory Kullanımı
```python
import psutil
import os

process = psutil.Process(os.getpid())
print(f"CPU: %{process.cpu_percent()}")
print(f"Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")
```

### Bot İstatistikleri
```python
# main.py içinde çalışırken
# CTRL+C ile durdur, istatistikleri göreceksin
```

---

## 🚨 Acil Durum Komutları

### Tüm Pozisyonları Kapat (Manuel)
```python
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

# Açık pozisyonları listele
positions = client.futures_position_information()
open_positions = [p for p in positions if float(p['positionAmt']) != 0]

for pos in open_positions:
    symbol = pos['symbol']
    amount = abs(float(pos['positionAmt']))
    side = 'BUY' if float(pos['positionAmt']) < 0 else 'SELL'
    
    print(f"Kapatılıyor: {symbol} {side} {amount}")
    # client.futures_create_order(symbol=symbol, side=side, type='MARKET', quantity=amount)
```

### Botu Hemen Durdur
```bash
# Windows
CTRL + C
taskkill /F /IM python.exe

# Linux/Mac
killall python
pkill -f main.py
```

---

## 📖 Dokümantasyon

### Hızlı Erişim
```bash
# Windows
start README.md
start GETTING_STARTED.md
start PROJECT_INFO.md

# Linux/Mac
open README.md
xdg-open README.md
```

---

**💡 İpucu:** Bu komutları sık kullanacaksan bir alias oluştur!

```bash
# .bashrc veya .zshrc dosyasına ekle
alias bot-start="cd /path/to/123 && python main.py"
alias bot-test="cd /path/to/123 && python test_setup.py"
alias bot-logs="cd /path/to/123/logs && ls -lh"
```
