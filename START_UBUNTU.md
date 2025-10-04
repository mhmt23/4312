# 🚀 UBUNTU SUNUCUDA BAŞLATMA KOMUTU

## ⚡ TEK KOMUTLA BAŞLAT

```bash
cd ~/ai-whale-bot && source venv/bin/activate && python3 main_pro.py
```

## 🔥 ARKAPLANDA ÇALIŞTIR

```bash
cd ~/ai-whale-bot && source venv/bin/activate && nohup python3 main_pro.py > bot.log 2>&1 & echo "Bot başlatıldı! PID: $!" && tail -f bot.log
```

Bu komut:
✅ Bot klasörüne gider
✅ Virtual env aktif eder  
✅ Botu arkaplanda başlatır
✅ Process ID gösterir
✅ Logları ekrana basar

## 📊 LOGLAR

```bash
# Canlı log izle
tail -f ~/ai-whale-bot/bot.log

# AI kararları
cat ~/ai-whale-bot/logs/decisions_$(date +%Y%m%d).json | jq

# Son 50 satır
tail -n 50 ~/ai-whale-bot/bot.log
```

## 🛑 DURDUR

```bash
# Process ID bul
ps aux | grep main_pro.py

# Durdur
kill <PID>

# Hepsini durdur
pkill -f main_pro.py
```

## 📱 DURUM KONTROL

```bash
# Bot çalışıyor mu?
ps aux | grep main_pro.py | grep -v grep

# Loglar
tail -f ~/ai-whale-bot/bot.log

# Son trade'ler
tail ~/ai-whale-bot/bot.log | grep "SHORT"

# AI kararları
tail ~/ai-whale-bot/bot.log | grep "AI"
```

## 🔄 RESTART

```bash
# Durdur ve başlat
pkill -f main_pro.py && sleep 2 && cd ~/ai-whale-bot && source venv/bin/activate && nohup python3 main_pro.py > bot.log 2>&1 &
```

## 🎯 HIZLI ERİŞİM ALIASları

`.bashrc` dosyasına ekle:

```bash
nano ~/.bashrc
```

Ekle:
```bash
# Whale Bot
alias bot-start="cd ~/ai-whale-bot && source venv/bin/activate && nohup python3 main_pro.py > bot.log 2>&1 & tail -f bot.log"
alias bot-stop="pkill -f main_pro.py"
alias bot-status="ps aux | grep main_pro.py | grep -v grep"
alias bot-logs="tail -f ~/ai-whale-bot/bot.log"
alias bot-restart="pkill -f main_pro.py && sleep 2 && cd ~/ai-whale-bot && source venv/bin/activate && nohup python3 main_pro.py > bot.log 2>&1 &"
```

Kaydet ve yükle:
```bash
source ~/.bashrc
```

Artık kullan:
```bash
bot-start    # Botu başlat
bot-stop     # Botu durdur
bot-status   # Durum
bot-logs     # Logları izle
bot-restart  # Restart
```

---

**🎉 HAZIR! Sunucuda botu başlatmak için yukarıdaki komutları kullan!**
