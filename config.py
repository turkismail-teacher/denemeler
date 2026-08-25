# Telegram Bot Kimliği (BotFather'dan aldığın token'ı buraya yapıştır)
#deneme kanalı
 # //var botToken = "8869455219:AAEO_h33-FMgs79R55QGIHriY8cx7qUieOk";
 # //var chatId = "-1003683404801";
TELEGRAM_TOKEN = "8869455219:AAEO_h33-FMgs79R55QGIHriY8cx7qUieOk"

# Öncelikli Taranacak Hisseler (Hızlı Tarama) - Yahoo formatında (.IS uzantılı)
BIST100 = [
    "THYAO.IS", "ASELS.IS", "GARAN.IS", "AKBNK.IS", "TUPRS.IS", 
    "KCHOL.IS", "SAHOL.IS", "ISCTR.IS", "SISE.IS", "BIMAS.IS"
    # Not: Listeyi uzatmamak için 10 tane yazdım. BIST 100'ün geri kalanını senin buraya eklemen gerekecek.
]

# Arka Planda Yavaş Taranacak Sığ/Yan Tahtalar
BIST_OTHERS = [
    "IZENR.IS", "KLRHO.IS"
    # Not: BIST 500'den geriye kalanları buraya ekleyeceksin.
]

# J Formasyonu Parametreleri (Buradan kolayca müdahale edebilmen için dışarı aldım)
PARAMS = {
    "kavis_min_dusus_orani": 0.03,  # %3 düşüş şartı
    "hacim_carpani": 1.5,           # 1.5 kat hacim şartı
    "sig_tahta_ciro_siniri": 50_000_000 # 50 Milyon TL ciro sınırı
}
