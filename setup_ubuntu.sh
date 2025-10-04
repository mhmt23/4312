#!/bin/bash

# Ubuntu Server için Hızlı Kurulum Scripti

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 AI WHALE KILLER BOT - UBUNTU KURULUM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Sistem güncelleme
echo "📦 Sistem güncelleniyor..."
sudo apt update && sudo apt upgrade -y

# Python ve pip kurulumu
echo "🐍 Python kurulumu..."
sudo apt install python3 python3-pip python3-venv -y

# Virtual environment oluştur
echo "🔧 Virtual environment oluşturuluyor..."
python3 -m venv venv
source venv/bin/activate

# Python paketlerini yükle
echo "📚 Python paketleri yükleniyor..."
pip install --upgrade pip
pip install python-binance pandas requests python-dotenv

# .env dosyası oluştur
echo ""
echo "🔑 API Anahtarlarını gir:"
echo ""

# Binance API
read -p "Binance API KEY: " BINANCE_API
read -p "Binance API SECRET: " BINANCE_SECRET

# DeepSeek API
read -p "DeepSeek API KEY: " DEEPSEEK_API

# Telegram (opsiyonel)
read -p "Telegram Bot Token (opsiyonel, Enter geç): " TELEGRAM_TOKEN
read -p "Telegram Chat ID (opsiyonel, Enter geç): " TELEGRAM_CHAT

# .env dosyası oluştur
cat > .env << EOF
# Binance API
API_KEY=$BINANCE_API
API_SECRET=$BINANCE_SECRET

# DeepSeek API
DEEPSEEK_API_KEY=$DEEPSEEK_API

# Telegram (Opsiyonel)
TELEGRAM_BOT_TOKEN=$TELEGRAM_TOKEN
TELEGRAM_CHAT_ID=$TELEGRAM_CHAT
EOF

echo ""
echo "✅ .env dosyası oluşturuldu"

# Test çalıştır
echo ""
echo "🧪 Sistem testi yapılıyor..."
python3 test_setup.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ KURULUM TAMAMLANDI!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 Botu başlatmak için:"
echo "   source venv/bin/activate"
echo "   python3 main.py"
echo ""
echo "📊 Arkaplanda çalıştırmak için:"
echo "   nohup python3 main.py > bot.log 2>&1 &"
echo ""
echo "📝 Logları görmek için:"
echo "   tail -f bot.log"
echo ""
