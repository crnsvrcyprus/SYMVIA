"""SQLite bağlantısı ve lead kayıt işlemleri yalnızca bu dosyada bulunur."""

import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    """Veritabanı bağlantısını açar."""
    if "db" not in g:
        location = current_app.config["DATABASE_URL"]

        if location.startswith("sqlite:///"):
            location = location.removeprefix("sqlite:///")

        path = Path(location).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        g.db = sqlite3.connect(path, timeout=15)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(_error=None):
    """İstek bitince veritabanı bağlantısını kapatır."""
    connection = g.pop("db", None)

    if connection is not None:
        connection.close()


def init_db(app):
    """Leads tablosunu, henüz yoksa oluşturur."""
    app.teardown_appcontext(close_db)

    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            tarih TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()


def lead_ekle(isim, telefon, mesaj):
    """Yeni iletişim talebini kaydeder."""
    db = get_db()

    cursor = db.execute(
        "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
        (isim, telefon, mesaj)
    )

    db.commit()
    return cursor.lastrowid


def tum_leadler():
    """Kayıtları en yeniden en eskiye sıralar."""
    rows = get_db().execute(
        "SELECT id, isim, telefon, mesaj, tarih "
        "FROM leads ORDER BY id DESC"
    ).fetchall()

    return [dict(row) for row in rows]
