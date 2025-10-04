@echo off
chcp 65001 > nul
echo ==========================================
echo 🤖 AI CRYPTO TRADING BOT - QUICK START
echo ==========================================
echo.

echo 📦 Kurulum kontrol ediliyor...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı!
    echo 💡 Python 3.8+ yükleyin: https://python.org
    pause
    exit /b 1
)
echo ✅ Python bulundu
echo.

echo 📚 Paketler yükleniyor...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Paket yükleme hatası!
    pause
    exit /b 1
)
echo ✅ Paketler yüklendi
echo.

echo 🧪 Sistem testi yapılıyor...
python test_setup.py
if errorlevel 1 (
    echo.
    echo ⚠️ Test başarısız! Yukarıdaki hataları düzelt.
    echo 💡 GETTING_STARTED.md dosyasını oku
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ✅ HER ŞEY HAZIR!
echo ==========================================
echo.
echo 🚀 Botu başlatmak için:
echo    python main.py
echo.
echo 📖 Detaylı rehber:
echo    GETTING_STARTED.md
echo.
pause
