"""Configuration - AI Trading Bot"""

# ============================================
# SERMAYE VE KALDIRAÇ
# ============================================
TOTAL_CAPITAL = 1000  # USDT
LEVERAGE = 10  # x kaldıraç
POSITION_SIZE_PERCENT = 10  # Her trade için sermayenin %10'u
MAX_OPEN_POSITIONS = 3  # Aynı anda max kaç pozisyon

# ============================================
# TARAMA PARAMETRELERİ
# ============================================
MIN_PRICE = 0.01  # Minimum coin fiyatı ($)
MAX_PRICE = 1000  # Maximum coin fiyatı ($)
MIN_VOLUME_24H = 10_000_000  # Minimum 24h volume ($10M)
MIN_PRICE_CHANGE_7D = 30  # Minimum 7 günlük artış (%)
BTC_CORRELATION_RATIO = 1.5  # BTC'den en az 1.5x fazla artmalı
SCAN_INTERVAL_HOURS = 2  # Her X saatte bir tarama yap

# ============================================
# SHORT SİNYALİ PARAMETRELERİ
# ============================================
VOLUME_DROP_THRESHOLD = 0.4  # Peak'ten %40 volume düşüşü
MOMENTUM_DROP_THRESHOLD = -1.0  # 15 dakikada -%1 momentum
BTC_MAX_CHANGE_1H = 1.5  # BTC 1 saatte max %1.5 değişsin
RSI_OVERBOUGHT = 70  # RSI > 70 overbought
CHECK_INTERVAL_MINUTES = 5  # Her 5 dakikada kontrol

# ============================================
# ÇIKIŞ STRATEJİSİ
# ============================================
# Kısmi çıkış 1
EXIT_LEVEL_1 = 3.0  # %3 kârda
EXIT_PERCENT_1 = 30  # Pozisyonun %30'unu kapat

# Kısmi çıkış 2
EXIT_LEVEL_2 = 6.0  # %6 kârda
EXIT_PERCENT_2 = 40  # Pozisyonun %40'ını kapat

# Tam çıkış
EXIT_LEVEL_3 = 12.0  # %12 kârda tamamını kapat
MAX_HOLD_HOURS = 48  # Max 48 saat tut

# ============================================
# AI AYARLARI
# ============================================
ENABLE_AI = True  # AI'yı aktif et
MIN_AI_CONFIDENCE = 0.70  # AI %70+ güvende olmalı
AI_TIMEOUT = 15  # AI cevap için max süre (saniye)
MAX_AI_CALLS_PER_DAY = 500  # Günlük max AI çağrısı (maliyet kontrolü)

# AI hangi durumlarda devreye girsin?
AI_MIN_TECHNICAL_SCORE = 2  # Teknik skor en az 2/4 olmalı
AI_DECISION_WEIGHT = 0.6  # AI kararının ağırlığı (%60)
TECHNICAL_DECISION_WEIGHT = 0.4  # Teknik analizin ağırlığı (%40)

# ============================================
# CANLI MOD - GERÇEK TRADE! ⚠️
# ============================================
DEMO_MODE = False  # ⚠️ GERÇEK TRADE AÇILACAK!
LOG_ALL_DECISIONS = True  # Tüm AI kararlarını logla

# ============================================
# BINANCE INTERVALS
# ============================================
KLINE_INTERVAL_15MINUTE = "15m"
KLINE_INTERVAL_1HOUR = "1h"
KLINE_INTERVAL_1DAY = "1d"

# ============================================
# TELEGRAM AYARLARI (Opsiyonel)
# ============================================
ENABLE_TELEGRAM = True  # Telegram bildirimleri
TELEGRAM_ALERT_ON_AI_DECISION = True  # AI kararlarında bildir

print("✅ Config yüklendi")
print("⚠️⚠️⚠️ CANLI MOD - GERÇEK TRADE AÇILACAK! ⚠️⚠️⚠️")
