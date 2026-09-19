"""Sayfa ve API adresleri: istekleri doğrular, ilgili katmana yönlendirir."""

import hmac
import sqlite3

from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
)

from .database import lead_ekle, tum_leadler
from .services.ai_service import AIServiceError, ai_service


pages_bp = Blueprint("pages", __name__)
api_bp = Blueprint("api", __name__)


@pages_bp.get("/")
def index():
    return render_template("index.html")


@pages_bp.get("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api_bp.post("/sohbet")
def sohbet():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            basari=False,
            hata="Geçerli bir JSON gönderin."
        ), 400

    mesaj = data.get("mesaj")
    gecmis = data.get("gecmis", [])

    if (
        not isinstance(mesaj, str)
        or not 0 < len(mesaj.strip()) <= 1000
    ):
        return jsonify(
            basari=False,
            hata="Mesaj 1-1000 karakter olmalı."
        ), 400

    if (
        not isinstance(gecmis, list)
        or len(gecmis) > 10
        or any(
            not isinstance(item, dict)
            or item.get("role") not in ("user", "assistant")
            or not isinstance(item.get("content"), str)
            or len(item["content"]) > 1000
            for item in gecmis
        )
    ):
        return jsonify(
            basari=False,
            hata="Konuşma geçmişinin biçimi geçersiz."
        ), 400

    try:
        cevap = ai_service.yanit_uret(mesaj.strip(), gecmis)
        return jsonify(basari=True, cevap=cevap)

    except AIServiceError:
        current_app.logger.exception("AI response failed")
        return jsonify(basari=False, hata='Asistan şu anda yanıt veremiyor; lütfen daha sonra deneyin.'), 503


@api_bp.post("/leads")
def create_lead():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(
            basari=False,
            hata="Geçerli bir JSON gönderin."
        ), 400

    isim = data.get("isim")
    telefon = data.get("telefon")
    mesaj = data.get("mesaj", "")

    if (
        not isinstance(isim, str)
        or not 1 <= len(isim.strip()) <= 100
        or not isinstance(telefon, str)
        or not 7 <= len(telefon.strip()) <= 25
        or not isinstance(mesaj, str)
        or len(mesaj) > 1000
    ):
        return jsonify(
            basari=False,
            hata="İsim, telefon veya mesaj geçersiz."
        ), 400

    try:
        lead_id = lead_ekle(
            isim.strip(),
            telefon.strip(),
            mesaj.strip()
        )

        return jsonify(basari=True, id=lead_id), 201

    except sqlite3.Error:
        return jsonify(
            basari=False,
            hata="Kayıt oluşturulamadı."
        ), 503


@api_bp.get("/leads")
def list_leads():
    """Özel kayıtları yalnızca doğru yönetici anahtarıyla gösterir."""
    key = current_app.config["ADMIN_API_KEY"]
    candidate = request.headers.get(
        "Authorization", ""
    ).removeprefix("Bearer ").strip()

    if not key or not hmac.compare_digest(candidate, key):
        return jsonify(
            basari=False,
            hata="Yetkisiz erişim."
        ), 401

    try:
        return jsonify(
            basari=True,
            leadler=tum_leadler()
        )

    except sqlite3.Error:
        return jsonify(
            basari=False,
            hata="Kayıtlar getirilemedi."
        ), 503
