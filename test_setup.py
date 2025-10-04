"""Quick Start Test - Tüm sistemleri test et"""
import os
import sys
from datetime import datetime

def test_imports():
    """Gerekli paketlerin yüklü olduğunu kontrol et"""
    print("📦 Paket kontrolü...")
    required = {
        'binance': 'python-binance',
        'pandas': 'pandas',
        'requests': 'requests',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} eksik!")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Eksik paketler: {', '.join(missing)}")
        print(f"Yüklemek için: pip install {' '.join(missing)}")
        return False
    
    print("✅ Tüm paketler yüklü\n")
    return True

def test_env():
    """ENV dosyasını kontrol et"""
    print("🔑 API anahtarları kontrolü...")
    
    if not os.path.exists('.env'):
        print("❌ .env dosyası bulunamadı!")
        print("💡 .env.example dosyasını .env olarak kopyala ve düzenle")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    keys = {
        'DEEPSEEK_API_KEY': 'DeepSeek API',
        'API_KEY': 'Binance API Key (opsiyonel)',
        'API_SECRET': 'Binance API Secret (opsiyonel)'
    }
    
    missing = []
    for key, name in keys.items():
        value = os.getenv(key)
        if value and value != f'your_{key.lower()}_here':
            print(f"   ✅ {name}")
        else:
            if key == 'DEEPSEEK_API_KEY':
                print(f"   ❌ {name} eksik!")
                missing.append(key)
            else:
                print(f"   ⚠️ {name} (test için opsiyonel)")
    
    if missing:
        print(f"\n❌ Gerekli anahtarlar eksik: {', '.join(missing)}")
        return False
    
    print("✅ API anahtarları tamam\n")
    return True

def test_ai_engine():
    """AI Engine'i test et"""
    print("🤖 AI Engine testi...")
    try:
        from ai_engine import AIEngine
        from dotenv import load_dotenv
        load_dotenv()
        
        ai = AIEngine()
        
        # Test verisi
        test_data = {
            'price': 10.45,
            'change_7d': 47.5,
            'score': 3,
            'rsi': 78,
            'volume_drop': 0.68,
            'momentum': -2.3,
            'btc_change': 0.5
        }
        
        print("   📡 DeepSeek API'ye bağlanılıyor...")
        result = ai.analyze_trade('TESTUSDT', test_data)
        
        if result['confidence'] >= 0:
            print(f"   ✅ AI yanıt verdi!")
            print(f"   📊 Karar: {'AÇILSIN' if result['should_trade'] else 'AÇILMASIN'}")
            print(f"   📈 Güven: %{result['confidence']*100:.0f}")
            print(f"   💭 Sebep: {result['reasoning'][:80]}...")
            print("✅ AI Engine çalışıyor\n")
            return True
        else:
            print("   ⚠️ AI yanıt verdi ama karar yok")
            return True
            
    except Exception as e:
        print(f"   ❌ AI Engine hatası: {e}")
        print("   💡 DeepSeek API anahtarını kontrol et\n")
        return False

def test_data_collector():
    """Data Collector'ı test et"""
    print("📡 Data Collector testi...")
    try:
        from data_collector import DataCollector
        
        collector = DataCollector()
        
        print("   🌐 Binance API'ye bağlanılıyor...")
        sentiment = collector.get_coin_sentiment('BTCUSDT')
        market = collector.get_market_condition()
        
        print(f"   ✅ Sentiment: {sentiment}")
        print(f"   ✅ Market: {market}")
        print("✅ Data Collector çalışıyor\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Data Collector hatası: {e}")
        print("   💡 İnternet bağlantısını kontrol et\n")
        return False

def test_config():
    """Config dosyasını kontrol et"""
    print("⚙️ Config kontrolü...")
    try:
        from config import *
        
        print(f"   💰 Sermaye: ${TOTAL_CAPITAL}")
        print(f"   ⚡ Kaldıraç: {LEVERAGE}x")
        print(f"   🤖 AI: {'AKTIF' if ENABLE_AI else 'KAPALI'}")
        print(f"   🎮 Mod: {'DEMO (Güvenli)' if DEMO_MODE else 'CANLI'}")
        
        if not DEMO_MODE:
            print("\n   ⚠️ UYARI: DEMO_MODE kapalı!")
            print("   💡 İlk test için DEMO_MODE = True önerilir")
        
        print("✅ Config yüklendi\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Config hatası: {e}\n")
        return False

def main():
    """Tüm testleri çalıştır"""
    print("="*70)
    print("🚀 AI TRADING BOT - QUICK START TEST")
    print("="*70)
    print()
    
    results = []
    
    # Testleri çalıştır
    results.append(("Paketler", test_imports()))
    results.append(("API Anahtarları", test_env()))
    results.append(("Config", test_config()))
    results.append(("Data Collector", test_data_collector()))
    results.append(("AI Engine", test_ai_engine()))
    
    # Sonuçlar
    print("="*70)
    print("📊 TEST SONUÇLARI")
    print("="*70)
    
    all_passed = True
    for name, passed in results:
        status = "✅ BAŞARILI" if passed else "❌ BAŞARISIZ"
        print(f"{status:20} - {name}")
        if not passed:
            all_passed = False
    
    print("="*70)
    
    if all_passed:
        print("\n🎉 TÜM TESTLER BAŞARILI!")
        print("\n📝 Şimdi ne yapmalısın?")
        print("   1. config.py'de DEMO_MODE = True olduğundan emin ol")
        print("   2. Botu başlat: python main.py")
        print("   3. Logları takip et: logs/decisions_*.json")
        print("   4. Demo'da başarılı olursan DEMO_MODE = False yap")
    else:
        print("\n⚠️ BAZI TESTLER BAŞARISIZ!")
        print("   Yukarıdaki hata mesajlarını kontrol et ve düzelt")
    
    print()

if __name__ == "__main__":
    main()
