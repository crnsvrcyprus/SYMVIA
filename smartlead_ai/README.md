# SYMVIA SmartLead AI

SYMVIA için yapay zekâ destekli sohbet ve iletişim talebi toplama projesi.

## Nasıl çalışır?

- Wix Studio, ziyaretçiye Support sohbetini ve iletişim formunu gösterir.
- Flask API, sohbet mesajını Groq yapay zekâ servisine iletir.
- Ziyaretçinin formda bıraktığı ad, telefon ve mesaj SQLite veritabanına kaydedilir.
- Kayıt listesi yalnızca yönetici anahtarıyla alınabilir.

## Backend dosyaları

- `config.py`: Ayarlar ve SYMVIA asistanının konuşma talimatları.
- `app/database.py`: Veritabanı işlemleri.
- `app/services/ai_service.py`: Yapay zekâ servisi.
- `app/routes.py`: Sayfa ve API adresleri.
- `app/__init__.py`: Flask uygulama fabrikası.
- `run.py`: Uygulama başlangıcı.

## API adresleri

- `GET /health`: Sunucu çalışıyor mu?
- `POST /api/sohbet`: Mesaja yanıt üretir.
- `POST /api/leads`: İletişim talebi kaydeder.
- `GET /api/leads`: Yetkili yöneticiye kayıtları listeler.

## Render ayarları

Root Directory: `smartlead_ai`  
Build Command: `pip install -r requirements.txt`  
Start Command: `gunicorn run:app`

Gerçek API anahtarları GitHub'a eklenmez; Render ortam değişkenlerinde saklanır.
Groq anahtarı yoksa sohbet yalnızca demo yanıtı verir.
