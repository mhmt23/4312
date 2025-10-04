#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  WHALE KILLER BOT - CANLI MOD BAŞLATMA ⚠️"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔴 DİKKAT: Bu bot GERÇEK TRADE AÇACAK!"
echo ""

# Bot klasörüne git
cd ~/ai-whale-bot || { echo "❌ Bot klasörü bulunamadı!"; exit 1; }

# Virtual env kontrol
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment bulunamadı!"
    echo "💡 Önce kurulum yap: ./setup_ubuntu.sh"
    exit 1
fi

# Virtual env aktif et
source venv/bin/activate

# Config kontrol
echo "📋 Config kontrolü..."
if grep -q "DEMO_MODE = True" config.py; then
    echo ""
    echo "⚠️⚠️⚠️ UYARI! ⚠️⚠️⚠️"
    echo "config.py'de DEMO_MODE = True"
    echo "Canlı mod için DEMO_MODE = False olmalı!"
    echo ""
    read -p "Devam etmek istiyor musun? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "İptal edildi."
        exit 0
    fi
elif grep -q "DEMO_MODE = False" config.py; then
    echo "✅ CANLI MOD aktif"
else
    echo "❌ DEMO_MODE ayarı bulunamadı!"
    exit 1
fi

# API test
echo ""
echo "🔑 Binance API testi..."
python3 << 'PYEOF'
from binance.client import Client
import os, sys
from dotenv import load_dotenv

load_dotenv()
try:
    client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))
    acc = client.get_account()
    balance = float(client.futures_account()['totalWalletBalance'])
    print(f"✅ Binance bağlantısı OK")
    print(f"✅ Trading: {acc['canTrade']}")
    print(f"💰 Futures Bakiye: {balance:.2f} USDT")
    
    if balance < 100:
        print(f"⚠️  UYARI: Bakiye çok düşük! (${balance:.2f})")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Binance API hatası: {e}")
    sys.exit(1)
PYEOF

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ API testi başarısız!"
    echo "💡 .env dosyasını kontrol et"
    exit 1
fi

# DeepSeek API test
echo ""
echo "🧠 DeepSeek API testi..."
python3 << 'PYEOF'
import os, requests, sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('DEEPSEEK_API_KEY')

if not api_key:
    print("❌ DeepSeek API anahtarı bulunamadı!")
    sys.exit(1)

try:
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 10
        },
        timeout=10
    )
    if response.status_code == 200:
        print("✅ DeepSeek API OK")
    else:
        print(f"⚠️ DeepSeek API yanıt: {response.status_code}")
except Exception as e:
    print(f"⚠️ DeepSeek API testi başarısız: {e}")
    print("💡 İnternet bağlantısını kontrol et")
PYEOF

# Son onay
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  SON ONAY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Bot şunları yapacak:"
echo "  ✅ Whale pump'ları tespit edecek"
echo "  ✅ AI ile analiz edecek"
echo "  ✅ GERÇEK SHORT TRADE AÇACAK 🔴"
echo "  ✅ Otomatik pozisyon yönetimi"
echo ""
echo "Risklerin farkında mısın?"
echo "  - Kripto trading risklidir"
echo "  - Bütün sermayeni kaybedebilirsin"
echo "  - Bot %100 başarılı değildir"
echo ""
read -p "Başlatmak istediğinden EMİN MİSİN? (yes yazarak onayla): " final_confirm

if [ "$final_confirm" != "yes" ]; then
    echo ""
    echo "İptal edildi. Güvenli bir seçim! ✅"
    exit 0
fi

# Başlat
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 BOT BAŞLATILIYOR..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Eski process'i durdur
pkill -f main_pro.py 2>/dev/null
sleep 2

# Başlat
nohup python3 main_pro.py > bot.log 2>&1 &
BOT_PID=$!

echo "✅ Bot başlatıldı!"
echo "📊 Process ID: $BOT_PID"
echo "📝 Log dosyası: ~/ai-whale-bot/bot.log"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📱 TAKİP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Logları izlemek için:"
echo "  tail -f ~/ai-whale-bot/bot.log"
echo ""
echo "Botu durdurmak için:"
echo "  kill $BOT_PID"
echo "  # veya: pkill -f main_pro.py"
echo ""
echo "Durum kontrolü:"
echo "  ps aux | grep main_pro.py"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⏳ 3 saniye sonra loglar gösterilecek..."
sleep 3
echo ""
echo "📊 CANLI LOGLAR (CTRL+C ile çıkış):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
tail -f bot.log
