"""Groq yapay zekâ servisiyle iletişim yalnızca bu dosyada yapılır."""

import requests

from config import Config


class AIServiceError(Exception):
    """Yapay zekâ servisinde oluşan hata."""


class AIService:
    def _system(self):
        """Asistanın marka talimatlarını getirir."""
        return Config.BUSINESS_CONTEXT

    def _groq_request(self, messages):
        """Mesajları Groq'a gönderir ve yanıtı alır."""
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {Config.GROQ_API_KEY}"
                },
                json={
                    "model": Config.GROQ_MODEL,
                    "messages": messages,
                    "temperature": 0.5,
                    "max_tokens": 300,
                },
                timeout=20,
            )

            if response.status_code >= 400: print("Groq error:", response.status_code, response.json().get("error", {}).get("message", "")[:300])
            response.raise_for_status()
            data = response.json()

            return data["choices"][0]["message"]["content"].strip()

        except (
            requests.RequestException,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ) as exc:
            raise AIServiceError(
                "Yapay zekâ servisine şu anda ulaşılamıyor."
            ) from exc

    def yanit_uret(self, mesaj, gecmis):
        """Yeni mesajı ve önceki konuşmayı değerlendirir."""
        if not Config.GROQ_API_KEY:
            return (
                "Merhaba! SYMVIA asistanının demo sürümündesiniz. "
                "Deneyimlerimiz hakkında bilgi almak için iletişim "
                "formunu doldurabilirsiniz."
            )

        if Config.AI_PROVIDER != "groq":
            raise AIServiceError(
                "Seçili yapay zekâ sağlayıcısı yapılandırılmamış."
            )

        history = [
            {
                "role": item["role"],
                "content": item["content"],
            }
            for item in gecmis[-10:]
        ]

        messages = [
            {
                "role": "system",
                "content": self._system(),
            },
            *history,
            {
                "role": "user",
                "content": mesaj,
            },
        ]

        return self._groq_request(messages)


ai_service = AIService()
