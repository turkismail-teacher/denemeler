import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import config
from scanner import fetch_and_scan
from keep_alive import keep_alive

# Yahoo Finance parametre eşleştirmeleri (4S yfinance tarafından desteklenmediği için çıkarıldı)
TIMEFRAMES = {
    "5D": {"interval": "5m", "period": "60d"},
    "15D": {"interval": "15m", "period": "60d"},
    "1S": {"interval": "1h", "period": "730d"},
    "Günlük": {"interval": "1d", "period": "2y"},
    "Haftalık": {"interval": "1wk", "period": "5y"}
}

# Kalıcı Klavye Menüsü
REPLY_KEYBOARD = [
    ["5D", "15D", "1S"],
    ["Günlük", "Haftalık"]
]
MARKUP = ReplyKeyboardMarkup(REPLY_KEYBOARD, resize_keyboard=True, is_persistent=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bota /start denildiğinde klavyeyi gösterir."""
    await update.message.reply_text(
        "BIST J Formasyon Tarayıcı Aktif.\nAşağıdaki butonlardan zaman dilimini seç.",
        reply_markup=MARKUP
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Butonlara basıldığında taramayı tetikler."""
    text = update.message.text
    
    if text not in TIMEFRAMES:
        return # Buton dışı yazıları yoksay
        
    interval = TIMEFRAMES[text]["interval"]
    period = TIMEFRAMES[text]["period"]
    
    await update.message.reply_text(f"🚀 {text} taraması BIST 100 için başlatıldı. Bekle...")
    
    # --- 1. AŞAMA: BIST 100 (HIZLI TARAMA) ---
    bist100_results = []
    for ticker in config.BIST100:
        res = await fetch_and_scan(ticker, period=period, interval=interval)
        if res:
            bist100_results.append(res)
            
    if bist100_results:
        response_100 = "\n".join(bist100_results)
        await update.message.reply_text(f"🎯 **BIST 100 SONUÇLARI** 🎯\n\n{response_100}", parse_mode='Markdown')
    else:
        await update.message.reply_text("BIST 100 içinde J formasyonu bulunamadı.")
        
    # --- 2. AŞAMA: YAN TAHTALAR (YAVAŞ TARAMA) ---
    await update.message.reply_text("⏳ BIST 100 tamamlandı. Şimdi yan tahtalar arka planda yavaşça taranıyor. Bu işlem sürecektir...")
    
    bist_others_results = []
    for ticker in config.BIST_OTHERS:
        res = await fetch_and_scan(ticker, period=period, interval=interval)
        if res:
            bist_others_results.append(res)
        # IP Ban yememek için yan tahtalarda her hisse arası 1.5 saniye bekle
        await asyncio.sleep(1.5)
        
    if bist_others_results:
        response_others = "\n".join(bist_others_results)
        await update.message.reply_text(f"⚠️ **YAN TAHTA SONUÇLARI** ⚠️\n\n{response_others}", parse_mode='Markdown')
    else:
        await update.message.reply_text("Yan tahtalarda J formasyonu bulunamadı.")

def main():
    """Botu ayağa kaldıran ana fonksiyon"""
    # Sahte web sunucusunu başlat
    keep_alive() 
    
    # Render üzerindeki 'event loop' çökme hatasını çözen zorunlu ekleme:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    app = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot çalışıyor. Telegram'dan /start yazabilirsin.")
    app.run_polling()

if __name__ == "__main__":
    main()
