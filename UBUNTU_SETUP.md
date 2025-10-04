# 🖥️ UBUNTU SUNUCU KURULUM REHBERİ

## 📋 Ön Hazırlık

### 1. Dosyaları Sunucuya Yükle

```bash
# Windows'tan Ubuntu'ya dosya kopyalama (3 seçenek)

# SEÇENEK 1: SCP ile (tavsiye edilen)
scp -r C:\Users\ESME\claude\botcrypt\123\* root@your-server-ip:~/ai-whale-bot/

# SEÇENEK 2: FileZilla ile
# - FileZilla aç
# - Host: your-server-ip
# - Username: root
# - Port: 22
# - Dosyaları sürükle-bırak

# SEÇENEK 3: GitHub ile
cd C:\Users\ESME\claude\botcrypt\123
git init
git add .
git commit -m "AI Whale Bot"
git remote add origin https://github.com/USERNAME/ai-whale-bot.git
git push -u origin main

# Sunucuda:
cd ~
git clone https://github.com/USERNAME/ai-whale-bot.git
```

---

## 🚀 Hızlı Kurulum (Otomatik)

```bash
# Sunucuya bağlan
ssh root@your-server-ip

# Bot klasörüne git
cd ~/ai-whale-bot

# Kurulum scriptini çalıştırılabilir yap
chmod +x setup_ubuntu.sh

# Kurulumu başlat
./setup_ubuntu.sh
```

---

## 🔧 Manuel Kurulum (Adım Adım)

### 1. Sistem Güncelleme
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Python Kurulumu
```bash
sudo apt install python3 python3-pip python3-venv -y
```

### 3. Virtual Environment
```bash
cd ~/ai-whale-bot
python3 -m venv venv
source venv/bin/activate
```

### 4. Python Paketleri
```bash
pip install --upgrade pip
pip install python-binance pandas requests python-dotenv
```

### 5. .env Dosyası Oluştur
```bash
nano .env
```

İçeriği yapıştır:
```
# Binance API
API_KEY=lQXr4g9BcInXIT2eoRiQdjgJwfxPCPaStTTfGf2AwEjTypdAt7i9FIrRNhy2UjLn
API_SECRET=wS3PZXqYhzVsb0pIAYc2YvKRggv0udYn1WDk5xs6v9UACzFMt9y3ByeBk6YfXrOH

# DeepSeek API
DEEPSEEK_API_KEY=sk-9bc10973f79e41109a8dfd6b9d1392a1

# Telegram (Opsiyonel)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Kaydet: `CTRL + X`, `Y`, `ENTER`

### 6. Test Et
```bash
python3 test_setup.py
```

---

## 🎯 Botu Çalıştırma

### Normal Mod
```bash
source venv/bin/activate
python3 main.py
```

### Arkaplanda Çalıştırma (Tavsiye)
```bash
source venv/bin/activate
nohup python3 main.py > bot.log 2>&1 &
```

### Logları İzle
```bash
tail -f bot.log
```

### Botu Durdur
```bash
ps aux | grep main.py
kill <process_id>
```

---

## 📊 Systemd Service (Otomatik Başlatma)

### 1. Service Dosyası Oluştur
```bash
sudo nano /etc/systemd/system/whale-bot.service
```

İçerik:
```ini
[Unit]
Description=AI Whale Killer Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/ai-whale-bot
Environment="PATH=/root/ai-whale-bot/venv/bin"
ExecStart=/root/ai-whale-bot/venv/bin/python3 /root/ai-whale-bot/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Service'i Aktif Et
```bash
sudo systemctl daemon-reload
sudo systemctl enable whale-bot
sudo systemctl start whale-bot
sudo systemctl status whale-bot
```

### 3. Service Komutları
```bash
sudo systemctl start whale-bot      # Başlat
sudo systemctl stop whale-bot       # Durdur
sudo systemctl restart whale-bot    # Restart
sudo systemctl status whale-bot     # Durum
sudo journalctl -u whale-bot -f     # Loglar
```

---

## 🔒 Güvenlik

```bash
# Firewall
sudo ufw enable
sudo ufw allow 22/tcp

# .env izinleri
chmod 600 .env

# Düzenli güncelleme
sudo apt update && sudo apt upgrade -y
```

---

## 📈 Monitoring

```bash
# Bot durumu
ps aux | grep main.py

# Loglar
tail -f bot.log

# Sistem kaynakları
htop

# Disk kullanımı
df -h
```

---

## 🚨 Sorun Giderme

```bash
# Python versiyonu
python3 --version

# Paketler
pip list

# API test
python3 -c "from binance.client import Client; import os; from dotenv import load_dotenv; load_dotenv(); c = Client(os.getenv('API_KEY'), os.getenv('API_SECRET')); print(c.get_account()['canTrade'])"

# Detaylı log
python3 main.py 2>&1 | tee debug.log
```

---

## 📱 Telegram Kurulum

```bash
# 1. @BotFather'da bot oluştur
# 2. Chat ID bul: https://api.telegram.org/botTOKEN/getUpdates
# 3. .env dosyasına ekle

nano .env
# TELEGRAM_BOT_TOKEN=your_token
# TELEGRAM_CHAT_ID=your_chat_id

# Test et
python3 -c "
import requests, os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
url = f'https://api.telegram.org/bot{token}/sendMessage'
requests.post(url, json={'chat_id': chat_id, 'text': '🤖 Bot test OK!'})
"
```

---

## ⚡ HIZLI BAŞLATMA KOMUTU

Ubuntu sunucunda tek komutla başlat:

```bash
cd ~/ai-whale-bot && source venv/bin/activate && nohup python3 main.py > bot.log 2>&1 & tail -f bot.log
```

Bu komut:
1. Klasöre gider
2. Virtual env aktif eder
3. Botu arkaplanda başlatır
4. Logları ekrana basar

---

## 📊 Performans Optimizasyonu

```bash
# Swap ekle (düşük RAM için)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Log rotasyonu
sudo nano /etc/logrotate.d/whale-bot
```

Ekle:
```
/root/ai-whale-bot/bot.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## 🎯 Başarıyla Çalıştırma Checklist

- [ ] Dosyalar sunucuya yüklendi
- [ ] Python ve paketler kuruldu
- [ ] .env dosyası oluşturuldu
- [ ] API anahtarları doğru
- [ ] test_setup.py başarılı
- [ ] Bot başladı (nohup ile)
- [ ] Loglar akıyor
- [ ] Telegram çalışıyor (opsiyonel)
- [ ] Systemd service kuruldu (opsiyonel)

---

**🚀 HAZIRSIN! Bot artık 7/24 çalışacak!**
