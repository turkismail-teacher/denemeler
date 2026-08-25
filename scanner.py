import yfinance as yf
import pandas as pd
import asyncio
from config import PARAMS

def check_j_hook(ticker, df):
    # En az 40 mumluk veri yoksa hesaplama yapamayız
    if len(df) < 40:
        return None

    # Hacim ortalaması hesaplama (Kırılım mumu hariç, son 20 mum)
    df['Vol_SMA_20'] = df['Volume'].rolling(window=20).mean().shift(1)
    
    # Kırılım anı (Son mum)
    current = df.iloc[-1]
    
    # Önceki Tepeyi Bulma (Son mumdan önceki 20 mum)
    past_20 = df.iloc[-21:-1]
    prev_peak = past_20['High'].max()
    peak_idx = past_20['High'].idxmax()
    
    # Tepeden sonraki dip bölgesi
    after_peak = df.loc[peak_idx:df.index[-2]]
    if len(after_peak) < 2:
        return None
        
    local_dip = after_peak['Low'].min()
    
    # Düşüş Yüzdesi (Kavis derinliği)
    dip_drop_pct = (prev_peak - local_dip) / prev_peak
    
    # J Formasyonu Kuralları
    rule_1_drop = dip_drop_pct >= PARAMS["kavis_min_dusus_orani"]
    rule_2_breakout = current['Close'] > prev_peak
    rule_3_volume = current['Volume'] >= (current['Vol_SMA_20'] * PARAMS["hacim_carpani"])
    
    # Ciro Hesaplaması (Sığ tahta kontrolü)
    turnover = current['Close'] * current['Volume']
    is_shallow = turnover < PARAMS["sig_tahta_ciro_siniri"]
    
    if rule_1_drop and rule_2_breakout and rule_3_volume:
        # Momentum oranını hesapla
        vol_ratio = current['Volume'] / current['Vol_SMA_20']
        
        # Ciroyu okunabilir formata çevir (Milyar / Milyon)
        if turnover >= 1_000_000_000:
            turnover_str = f"{turnover/1_000_000_000:.1f}Mlyr"
        else:
            turnover_str = f"{turnover/1_000_000:.0f}M"
            
        # Sığ tahta uyarısı
        warning = " ⚠️" if is_shallow else ""
        
        # Sonucu senin istediğin temiz mobil formata dönüştür
        ticker_clean = ticker.replace('.IS', '')
        result_text = f"🎯 {ticker_clean}{warning} | 📉 Kvs: %{dip_drop_pct*100:.1f} | 🚀 Hcm: {vol_ratio:.1f}x | 💰 Cro: {turnover_str}"
        return result_text
        
    return None

async def fetch_and_scan(ticker, period="3mo", interval="1d"):
    """
    yfinance normalde senkron çalışır ve sistemi kilitler. 
    asyncio.to_thread ile bu işlemi arka plana itiyoruz ki Telegram botumuz donmasın.
    """
    try:
        data = await asyncio.to_thread(yf.download, tickers=ticker, period=period, interval=interval, progress=False)
        
        if data.empty:
            return None
            
        return check_j_hook(ticker, data)
        
    except Exception as e:
        # API kaynaklı geçici bağlantı hatalarını yoksayıyoruz
        return None
