# 📊 PROJE BİLGİLERİ

## 🎯 Proje Adı
**AI-Powered Crypto Trading Bot v3.0**

## 📝 Açıklama
DeepSeek AI ile güçlendirilmiş kripto futures trading botu. Whale pump'ları tespit eder, teknik analiz yapar ve AI onayı ile short pozisyonları açar.

## 🗂️ Dosya Yapısı

```
📁 123/
│
├── 📄 main.py                    # Ana bot dosyası (700+ satır)
│   └── AITradingBot sınıfı
│       ├── Whale pump tarayıcı
│       ├── Teknik analiz
│       ├── AI entegrasyonu
│       ├── Pozisyon yönetimi
│       └── Risk kontrolü
│
├── 📄 ai_engine.py               # DeepSeek AI motoru (350+ satır)
│   └── AIEngine sınıfı
│       ├── Trade analizi
│       ├── Prompt engineering
│       ├── Response parsing
│       └── Fallback sistemi
│
├── 📄 data_collector.py          # Veri toplama (200+ satır)
│   └── DataCollector sınıfı
│       ├── Sentiment analizi
│       ├── Market durumu
│       ├── Funding rate
│       └── Whale sinyalleri
│
├── 📄 config.py                  # Konfigürasyon
│   ├── Sermaye/kaldıraç
│   ├── Tarama parametreleri
│   ├── Short sinyalleri
│   ├── Çıkış stratejisi
│   └── AI ayarları
│
├── 📄 .env                       # API anahtarları (GİZLİ)
├── 📄 .env.example               # Örnek ENV dosyası
├── 📄 requirements.txt           # Python bağımlılıkları
│
├── 📄 test_setup.py              # Kurulum test scripti
├── 📄 start.bat                  # Windows başlatıcı
│
├── 📄 README.md                  # Ana dokümantasyon
├── 📄 GETTING_STARTED.md         # Başlangıç rehberi
├── 📄 PROJECT_INFO.md            # Bu dosya
│
└── 📁 logs/                      # AI karar logları
    └── decisions_YYYYMMDD.json
```

## 🔧 Teknolojiler

### Backend
- **Python 3.8+**
- **python-binance**: Binance API wrapper
- **pandas**: Veri analizi
- **requests**: HTTP istekleri

### AI
- **DeepSeek API**: GPT benzeri LLM
- **Custom prompt engineering**
- **JSON response parsing**

### Exchange
- **Binance Futures API**
- **WebSocket (gelecek)**

## 🧠 Algoritma

### 1. Whale Pump Tespiti
```
FOR her USDT çifti:
  IF 7_günlük_artış > %30 AND
     BTC_korelasyon > 1.5x AND
     24h_volume > $10M:
    → İzleme listesine ekle
```

### 2. Teknik Analiz Skoru (0-4)
```
score = 0
IF volume_düşüşü > %40: score++
IF momentum < -%1: score++
IF BTC_stabil: score++
IF RSI > 70: score++
```

### 3. AI Kararı
```
IF teknik_skor >= 2:
  ai_analiz = DeepSeek_API(teknik_data + sentiment_data)
  
  IF ai_güven >= %70:
    → SHORT AÇ
  ELSE:
    → ATLA
```

### 4. Çıkış Stratejisi
```
IF kâr >= %12: TAM ÇIKIŞ
ELIF kâr >= %6: %40 ÇIKIŞ (kısmi-2)
ELIF kâr >= %3: %30 ÇIKIŞ (kısmi-1)
ELIF süre > 48h: TAM ÇIKIŞ (zaman aşımı)
```

## 📈 İstatistikler

### Kod
- **Toplam Satır**: ~1500
- **Sınıf Sayısı**: 3
- **Fonksiyon**: ~40
- **Dosya**: 11

### Özellikler
- ✅ Whale pump detector
- ✅ Teknik analiz (RSI, Volume, Momentum)
- ✅ AI analiz (DeepSeek)
- ✅ Sentiment tracking
- ✅ Kısmi çıkış stratejisi
- ✅ Demo mode
- ✅ Telegram bildirimleri
- ✅ Karar loglama
- ✅ Risk yönetimi
- ✅ Fallback sistemi

## 🚀 Gelecek Geliştirmeler

### Faz 2 (Yakında)
- [ ] Twitter/Reddit sentiment scraping
- [ ] Order book depth analizi
- [ ] Chart pattern recognition
- [ ] Backtesting engine
- [ ] Performance dashboard

### Faz 3 (Gelecek)
- [ ] On-chain whale tracking
- [ ] Multi-AI comparison (DeepSeek vs Claude vs GPT)
- [ ] Auto-learning system
- [ ] WebSocket real-time data
- [ ] Web UI dashboard

### Faz 4 (Uzun Vade)
- [ ] Multi-exchange support
- [ ] Long + Short kombinasyonu
- [ ] Portfolio management
- [ ] Mobile app
- [ ] Cloud deployment

## 💡 Tasarım Kararları

### Neden DeepSeek?
1. ✅ Uygun fiyat
2. ✅ Hızlı yanıt
3. ✅ Finansal analiz yeteneği
4. ✅ API kolaylığı

### Neden Demo Mode?
1. 🔒 Güvenlik öncelik
2. 📊 Strateji test
3. 💡 Öğrenme fırsatı
4. 💰 Risk yönetimi

### Neden Sadece Short?
1. 🐋 Whale pump sonrası düşüş olasılığı yüksek
2. 📉 Momentum stratejisi için uygun
3. 🎯 Basit ve fokuslu strateji
4. 📊 Backtesting'de başarılı

### Neden Kısmi Çıkış?
1. 💰 Kârı güvenceye al
2. 📈 Daha fazla kazanç şansı
3. 🎯 Risk/Reward optimizasyonu
4. 🧠 Profesyonel trader yaklaşımı

## 📊 Performans Metrikleri

### Hedef Metrikler (1 Ay)
- Win Rate: >%55
- Avg. Profit per Trade: >%5
- Max Drawdown: <%15
- Sharpe Ratio: >1.5
- AI Onay Başarısı: >%70

### Takip Edilenler
```python
{
  "total_trades": 0,
  "winning_trades": 0,
  "total_profit": 0.0,
  "ai_calls": 0,
  "ai_approved": 0,
  "avg_confidence": 0.0,
  "avg_hold_time": 0.0
}
```

## 🔐 Güvenlik

### API Güvenliği
- ✅ ENV dosyasında saklanır
- ✅ Git'e commit edilmez (.gitignore)
- ✅ IP restriction önerilir
- ✅ Minimum izinler

### Risk Kontrolü
- ✅ Max pozisyon limiti (3)
- ✅ Position size kontrolü (%10)
- ✅ Demo mode
- ✅ AI güven threshold (%70)
- ✅ Günlük AI limit (500)
- ✅ Timeout kontrolü (15s)

### Fallback Sistemleri
- ✅ AI hata verirse → Teknik analiz
- ✅ API timeout → Güvenli red
- ✅ Binance API hata → Log ve devam
- ✅ Data collector hata → Neutral değer

## 📚 Öğrenme Kaynakları

### Kripto Trading
- Investopedia Crypto Trading
- Binance Academy
- TradingView Ideas

### AI & Machine Learning
- DeepSeek Documentation
- Prompt Engineering Guide
- LangChain Tutorials

### Python
- python-binance docs
- Pandas documentation
- Async programming

## 🤝 Katkı

### Kod Standartları
- PEP 8 uyumlu
- Türkçe yorumlar
- Docstring'ler
- Type hints (gelecek)

### Git Workflow
```bash
git checkout -b feature/yeni-ozellik
# Değişiklikler yap
git commit -m "feat: Yeni özellik eklendi"
git push origin feature/yeni-ozellik
# Pull request oluştur
```

## 📧 İletişim

- **Geliştirici**: [İsim]
- **Email**: [Email]
- **GitHub**: [Repo Link]
- **Discord**: [Discord]

## 📜 Lisans

MIT License - Özgürce kullan, değiştir, dağıt!

## 🙏 Teşekkürler

- Binance API Team
- DeepSeek AI Team
- Python Community
- Crypto Trading Community

---

**Son Güncelleme**: 4 Ekim 2025
**Versiyon**: 3.0
**Durum**: 🟢 Aktif Geliştirme
