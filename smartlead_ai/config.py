"""Uygulama ayarları ve SYMVIA asistanının marka bilgileri."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "development-only-change-me"
    )

    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        str(ROOT / "instance" / "leads.sqlite3")
    )

    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")
    GROQ_MODEL = os.environ.get(
        "GROQ_MODEL",
        "llama-3.1-8b-instant"
    )

    CORS_ORIGINS = [
        adres.strip()
        for adres in os.environ.get(
            "CORS_ORIGINS",
            "http://localhost:5000"
        ).split(",")
        if adres.strip()
    ]

    ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "")

    BUSINESS_CONTEXT = """
Sen SYMVIA'nın yapay zekâ destekli satış asistanısın.

SYMVIA; seyahat, doğa, outdoor ve kültürel keşif odaklı
deneyimler sunmayı hedefleyen bir markadır. Gezginlerle sıcak,
samimi, meraklı ve güven veren bir dille Türkçe konuş.

Gezginin ne tür bir deneyimle ilgilendiğini anlamak için kısa
ve ilgili sorular sor. Uygun olduğunda iletişim formunu
doldurarak ekiple görüşmeye davet et.

Doğrulanmamış fiyat, tarih, müsaitlik, rota veya güvenlik
garantisi uydurma. Kesin rezervasyon ya da ödeme alındığını
söyleme. Ziyaretçiden sohbet içinde telefon numarası veya
hassas kişisel bilgi isteme. Yapay zekâ asistanı olduğunu
gizleme.
"""


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


configurations = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
