"""AI-Powered Crypto Trading Bot v3.0"""
import time
import os
import json
from datetime import datetime, timedelta
from binance.client import Client
from binance.enums import *
import pandas as pd
import requests
from config import *
from ai_engine import AIEngine
from data_collector import DataCollector

class AITradingBot:
    def __init__(self):
        self.client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))
        self.ai_engine = AIEngine() if ENABLE_AI else None
        self.data_collector = DataCollector()
        
        self.watchlist = {}
        self.positions = {}
        self.total_trades = 0
        self.winning_trades = 0
        self.ai_calls_today = 0
        self.last_ai_reset = datetime.now()
        
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        print("="*70)
        print("🤖 AI-POWERED CRYPTO TRADING BOT v3.0")
        print("="*70)
        print(f"💰 Sermaye: ${TOTAL_CAPITAL}")
        print(f"⚡ Kaldıraç: {LEVERAGE}x")
        print(f"🧠 AI: {'AKTIF' if ENABLE_AI else 'KAPALI'}")
        print(f"🎮 Mod: {'DEMO (Güvenli)' if DEMO_MODE else 'CANLI (Gerçek Trade)'}")
        print("="*70)
    
    def scan_parabolic_coins(self):
        """Whale pump olan coinleri tara"""
        print(f"\n🔍 [{datetime.now().strftime('%H:%M:%S')}] Whale pump taraması...")
        try:
            tickers = self.client.get_ticker()
            btc_data = self.get_btc_data()
            found = 0
            
            for ticker in tickers:
                symbol = ticker['symbol']
                if not symbol.endswith('USDT'):
                    continue
                
                try:
                    price = float(ticker['lastPrice'])
                    volume = float(ticker['quoteVolume'])
                    
                    if price < MIN_PRICE or price > MAX_PRICE or volume < MIN_VOLUME_24H:
                        continue
                    
                    klines = self.client.futures_klines(
                        symbol=symbol, 
                        interval=KLINE_INTERVAL_1DAY, 
                        limit=8
                    )
                    
                    if len(klines) < 7:
                        continue
                    
                    price_7d = float(klines[0][4])
                    change_7d = ((price - price_7d) / price_7d) * 100
                    
                    if change_7d < MIN_PRICE_CHANGE_7D:
                        continue
                    
                    correlation = change_7d / btc_data['change_7d'] if btc_data['change_7d'] > 0 else change_7d
                    
                    if correlation < BTC_CORRELATION_RATIO:
                        continue
                    
                    if symbol not in self.watchlist:
                        self.watchlist[symbol] = {
                            'symbol': symbol,
                            'price': price,
                            'change_7d': change_7d,
                            'added_at': datetime.now()
                        }
                        found += 1
                        print(f"🐋 WHALE PUMP BULUNDU: {symbol} +%{change_7d:.0f}")
                        self.send_telegram(f"🐋 WHALE PUMP!\n{symbol}\n+%{change_7d:.0f}")
                
                except Exception as e:
                    continue
            
            print(f"✅ Tarama tamamlandı: {found} yeni whale pump")
            
        except Exception as e:
            print(f"❌ Tarama hatası: {e}")
    
    def check_short_conditions(self, symbol):
        """Teknik analiz + AI analizi ile short kararı ver"""
        try:
            # Teknik analiz yap
            result = self.client.futures_symbol_ticker(symbol=symbol)
            ticker = result[0] if isinstance(result, list) else result
            price = float(ticker['price'])
            
            # Volume analizi
            klines_24h = self.client.futures_klines(
                symbol=symbol, 
                interval=KLINE_INTERVAL_1HOUR, 
                limit=25
            )
            volumes = [float(k[7]) for k in klines_24h]
            peak_vol = max(volumes)
            current_vol = volumes[-1]
            vol_drop = (peak_vol - current_vol) / peak_vol
            
            # Momentum
            klines_15m = self.client.futures_klines(
                symbol=symbol,
                interval=KLINE_INTERVAL_15MINUTE,
                limit=2
            )
            price_15m = float(klines_15m[0][4])
            momentum = ((price - price_15m) / price_15m) * 100
            
            # BTC durumu
            btc = self.get_btc_data()
            
            # RSI
            closes = [float(k[4]) for k in klines_24h]
            rsi = self.calc_rsi(closes)
            
            # Teknik skor hesapla
            tech_score = 0
            if vol_drop > VOLUME_DROP_THRESHOLD:
                tech_score += 1
            if momentum < MOMENTUM_DROP_THRESHOLD:
                tech_score += 1
            if abs(btc['change_1h']) < BTC_MAX_CHANGE_1H:
                tech_score += 1
            if rsi > RSI_OVERBOUGHT:
                tech_score += 1
            
            print(f"   📊 {symbol}: Vol↓{vol_drop*100:.0f}% | Mom{momentum:.1f}% | BTC{btc['change_1h']:.1f}% | RSI{rsi:.0f} = Skor:{tech_score}/4")
            
            # AI devreye girsin mi?
            if ENABLE_AI and tech_score >= AI_MIN_TECHNICAL_SCORE:
                return self._ai_enhanced_decision(
                    symbol, price, tech_score, rsi, vol_drop, momentum, btc
                )
            else:
                # Sadece teknik analiz (eski yöntem)
                should_trade = tech_score >= 3
                return should_trade, price, tech_score, None
        
        except Exception as e:
            print(f"   ❌ {symbol} analiz hatası: {e}")
            return False, 0, 0, None
    
    def _ai_enhanced_decision(self, symbol, price, tech_score, rsi, vol_drop, momentum, btc):
        """AI ile geliştirilmiş karar verme"""
        try:
            # AI çağrı limiti kontrolü
            if not self._check_ai_quota():
                print("   ⚠️ AI günlük limit aşıldı, teknik analize dönülüyor")
                should_trade = tech_score >= 3
                return should_trade, price, tech_score, None
            
            # Ek veri topla
            enriched_data = self.data_collector.get_enriched_data(symbol)
            
            # AI'ya gönderilecek veri paketi
            ai_data = {
                'price': price,
                'change_7d': self.watchlist.get(symbol, {}).get('change_7d', 0),
                'score': tech_score,
                'rsi': rsi,
                'volume_drop': vol_drop,
                'momentum': momentum,
                'btc_change': btc['change_1h'],
                'sentiment': enriched_data['sentiment'],
                'market_condition': enriched_data['market_condition'],
                'funding_rate': enriched_data['funding_rate']
            }
            
            # AI analizi
            print(f"   🤖 AI analiz ediliyor...")
            ai_result = self.ai_engine.analyze_trade(symbol, ai_data)
            
            self.ai_calls_today += 1
            
            # AI güven seviyesi yeterli mi?
            if ai_result['confidence'] >= MIN_AI_CONFIDENCE:
                print(f"   ✅ AI ONAY: %{ai_result['confidence']*100:.0f} güven")
                print(f"   💭 Sebep: {ai_result['reasoning']}")
                
                # Telegram bildirimi
                if TELEGRAM_ALERT_ON_AI_DECISION:
                    self.send_telegram(
                        f"🤖 AI KARAR\n{symbol}\n"
                        f"Güven: %{ai_result['confidence']*100:.0f}\n"
                        f"{ai_result['reasoning']}"
                    )
                
                # Kararı logla
                self._log_decision(symbol, ai_data, ai_result, True)
                
                return ai_result['should_trade'], price, tech_score, ai_result
            else:
                print(f"   ❌ AI RED: %{ai_result['confidence']*100:.0f} güven (min %{MIN_AI_CONFIDENCE*100:.0f})")
                print(f"   💭 Sebep: {ai_result['reasoning']}")
                
                # Kararı logla
                self._log_decision(symbol, ai_data, ai_result, False)
                
                return False, price, tech_score, ai_result
        
        except Exception as e:
            print(f"   ❌ AI analiz hatası: {e}")
            # AI hata verirse teknik analize geri dön
            should_trade = tech_score >= 3
            return should_trade, price, tech_score, None
    
    def open_short(self, symbol, price, ai_result=None):
        """Short pozisyon aç"""
        try:
            balance = self.get_balance()
            pos_value = balance * (POSITION_SIZE_PERCENT / 100)
            quantity = (pos_value * LEVERAGE) / price
            quantity = round(quantity, 3)
            
            print(f"\n🔴 SHORT POZİSYON AÇILIYOR:")
            print(f"   Coin: {symbol}")
            print(f"   Fiyat: ${price:.4f}")
            print(f"   Miktar: {quantity}")
            print(f"   Değer: ${pos_value:.2f}")
            
            if ai_result:
                print(f"   🤖 AI Güven: %{ai_result['confidence']*100:.0f}")
                print(f"   🎯 Risk/Reward: 1:{ai_result['risk_reward']:.1f}")
            
            if not DEMO_MODE:
                # Gerçek trade aç
                self.client.futures_change_leverage(symbol=symbol, leverage=LEVERAGE)
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
                print("   ✅ GERÇEK TRADE AÇILDI!")
            else:
                print("   ✅ DEMO TRADE AÇILDI (Gerçek değil)")
            
            # Pozisyonu kaydet
            self.positions[symbol] = {
                'entry_price': price,
                'quantity': quantity,
                'entry_time': datetime.now(),
                'partial_exits': [],
                'ai_result': ai_result,
                'position_value': pos_value
            }
            
            # Watchlist'ten çıkar
            if symbol in self.watchlist:
                del self.watchlist[symbol]
            
            # Telegram bildirimi
            self.send_telegram(
                f"🔴 SHORT AÇILDI\n{symbol} @ ${price:.4f}\n"
                f"Değer: ${pos_value:.2f}\n"
                f"{'🤖 AI Onaylı' if ai_result else '📊 Teknik'}"
            )
        
        except Exception as e:
            print(f"   ❌ Short açma hatası: {e}")
    
    def manage_positions(self):
        """Açık pozisyonları yönet"""
        for symbol in list(self.positions.keys()):
            try:
                pos = self.positions[symbol]
                
                # Güncel fiyat
                result = self.client.futures_symbol_ticker(symbol=symbol)
                ticker = result[0] if isinstance(result, list) else result
                price = float(ticker['price'])
                
                # Kâr/Zarar hesapla
                profit_pct = ((pos['entry_price'] - price) / pos['entry_price']) * 100
                hours = (datetime.now() - pos['entry_time']).total_seconds() / 3600
                
                print(f"💼 {symbol}: %{profit_pct:.1f} kâr | {hours:.1f} saat")
                
                # Kalan miktar
                remaining = pos['quantity']
                for exit in pos['partial_exits']:
                    remaining -= exit['qty']
                
                # Çıkış kararı
                exit_qty = 0
                reason = ""
                
                if profit_pct >= EXIT_LEVEL_3:
                    exit_qty = remaining
                    reason = f"TAM ÇIKIŞ +%{profit_pct:.1f}"
                elif profit_pct >= EXIT_LEVEL_2 and not any(e['level']==2 for e in pos['partial_exits']):
                    exit_qty = pos['quantity'] * (EXIT_PERCENT_2/100)
                    reason = f"KISMİ-2 +%{profit_pct:.1f}"
                elif profit_pct >= EXIT_LEVEL_1 and not any(e['level']==1 for e in pos['partial_exits']):
                    exit_qty = pos['quantity'] * (EXIT_PERCENT_1/100)
                    reason = f"KISMİ-1 +%{profit_pct:.1f}"
                elif hours > MAX_HOLD_HOURS:
                    exit_qty = remaining
                    reason = f"MAX SÜRE {hours:.0f}h"
                
                if exit_qty > 0:
                    self.close_position(symbol, exit_qty, price, reason, profit_pct)
                    
                    if exit_qty >= remaining * 0.9:
                        del self.positions[symbol]
                    else:
                        level = 1 if profit_pct < EXIT_LEVEL_2 else 2
                        pos['partial_exits'].append({'level': level, 'qty': exit_qty})
            
            except Exception as e:
                print(f"❌ {symbol} yönetim hatası: {e}")
    
    def close_position(self, symbol, qty, price, reason, profit):
        """Pozisyon kapat"""
        try:
            print(f"\n💰 POZİSYON KAPATILIYOR: {symbol}")
            print(f"   Sebep: {reason}")
            print(f"   Miktar: {qty}")
            print(f"   Kâr: %{profit:.1f}")
            
            if not DEMO_MODE:
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=SIDE_BUY,
                    type=ORDER_TYPE_MARKET,
                    quantity=round(qty, 3)
                )
                print("   ✅ GERÇEK TRADE KAPATILDI!")
            else:
                print("   ✅ DEMO TRADE KAPATILDI")
            
            self.total_trades += 1
            if profit > 0:
                self.winning_trades += 1
            
            self.send_telegram(f"💰 POZİSYON KAPANDI\n{symbol}\n{reason}")
        
        except Exception as e:
            print(f"   ❌ Kapatma hatası: {e}")
    
    def get_btc_data(self):
        """BTC verisini al"""
        try:
            result = self.client.futures_symbol_ticker(symbol='BTCUSDT')
            ticker = result[0] if isinstance(result, list) else result
            price = float(ticker['price'])
            
            k7d = self.client.futures_klines(symbol='BTCUSDT', interval=KLINE_INTERVAL_1DAY, limit=8)
            p7d = float(k7d[0][4])
            c7d = ((price - p7d) / p7d) * 100
            
            k1h = self.client.futures_klines(symbol='BTCUSDT', interval=KLINE_INTERVAL_1HOUR, limit=2)
            p1h = float(k1h[0][4])
            c1h = ((price - p1h) / p1h) * 100
            
            return {'price': price, 'change_7d': c7d, 'change_1h': c1h}
        except:
            return {'price': 0, 'change_7d': 0, 'change_1h': 0}
    
    def get_balance(self):
        """Bakiye al"""
        try:
            if not DEMO_MODE:
                acc = self.client.futures_account()
                return float(acc['totalWalletBalance'])
            else:
                return TOTAL_CAPITAL
        except:
            return TOTAL_CAPITAL
    
    def calc_rsi(self, prices, period=14):
        """RSI hesapla"""
        df = pd.DataFrame({'close': prices})
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else 50
    
    def send_telegram(self, msg):
        """Telegram bildirimi gönder"""
        try:
            if ENABLE_TELEGRAM and self.telegram_token and self.telegram_chat_id:
                url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
                requests.post(url, json={"chat_id": self.telegram_chat_id, "text": msg})
        except:
            pass
    
    def _check_ai_quota(self):
        """AI günlük kullanım limitini kontrol et"""
        now = datetime.now()
        if (now - self.last_ai_reset).days >= 1:
            self.ai_calls_today = 0
            self.last_ai_reset = now
        
        return self.ai_calls_today < MAX_AI_CALLS_PER_DAY
    
    def _log_decision(self, symbol, technical_data, ai_result, action_taken):
        """AI kararlarını logla (öğrenme için)"""
        if not LOG_ALL_DECISIONS:
            return
        
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'symbol': symbol,
                'technical_data': technical_data,
                'ai_decision': {
                    'should_trade': ai_result['should_trade'],
                    'confidence': ai_result['confidence'],
                    'reasoning': ai_result['reasoning'],
                    'risk_reward': ai_result.get('risk_reward', 0)
                },
                'action_taken': 'opened_short' if action_taken else 'skipped',
                'entry_price': technical_data['price'] if action_taken else None
            }
            
            log_file = f"logs/decisions_{datetime.now().strftime('%Y%m%d')}.json"
            
            # Dosyayı aç ve ekle
            logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            print(f"⚠️ Log hatası: {e}")
    
    def print_stats(self):
        """İstatistikleri göster"""
        balance = self.get_balance()
        roi = ((balance - TOTAL_CAPITAL) / TOTAL_CAPITAL) * 100
        win_rate = (self.winning_trades / self.total_trades * 100) if self.total_trades > 0 else 0
        
        print(f"\n{'='*70}")
        print(f"📊 İSTATİSTİKLER")
        print(f"{'='*70}")
        print(f"💰 Bakiye: ${balance:.2f} (ROI: %{roi:.1f})")
        print(f"📈 Trade: {self.total_trades} | Kazanan: {self.winning_trades} (%{win_rate:.0f})")
        print(f"👀 İzleme Listesi: {len(self.watchlist)}")
        print(f"💼 Açık Pozisyon: {len(self.positions)}")
        if ENABLE_AI:
            print(f"🤖 AI Çağrıları: {self.ai_calls_today}/{MAX_AI_CALLS_PER_DAY}")
        print(f"{'='*70}")
    
    def run(self):
        """Ana döngü"""
        print("\n🎯 BOT BAŞLATILDI!\n")
        last_scan = datetime.now() - timedelta(hours=999)
        
        while True:
            try:
                now = datetime.now()
                
                # Periyodik tarama
                if (now - last_scan).total_seconds() / 3600 >= SCAN_INTERVAL_HOURS:
                    self.scan_parabolic_coins()
                    last_scan = now
                
                print(f"\n{'='*70}")
                print(f"⏰ {now.strftime('%H:%M:%S')}")
                self.print_stats()
                
                # İzleme listesindeki coinleri kontrol et
                for symbol in list(self.watchlist.keys()):
                    if len(self.positions) >= MAX_OPEN_POSITIONS:
                        print(f"⚠️ Max pozisyon limitine ulaşıldı ({MAX_OPEN_POSITIONS})")
                        break
                    
                    should_short, price, tech_score, ai_result = self.check_short_conditions(symbol)
                    
                    if should_short:
                        self.open_short(symbol, price, ai_result)
                
                # Açık pozisyonları yönet
                if self.positions:
                    print(f"\n💼 POZİSYON YÖNETİMİ:")
                    self.manage_positions()
                
                print(f"\n⏳ {CHECK_INTERVAL_MINUTES} dakika bekleniyor...\n")
                time.sleep(CHECK_INTERVAL_MINUTES * 60)
            
            except KeyboardInterrupt:
                print("\n🛑 Bot durduruldu")
                break
            except Exception as e:
                print(f"\n❌ Hata: {e}")
                time.sleep(60)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    bot = AITradingBot()
    bot.run()
