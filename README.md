# Bot-muzyczny

Discordowy bot muzyczny napisany w Pythonie, gotowy do uruchomienia w Dockerze.

## Wymagania

- Token bota Discord (`DISCORD_TOKEN`)
- Włączony przywilejowy **Message Content Intent** w [Discord Developer Portal](https://discord.com/developers/applications)  
  (Ustawienia aplikacji → zakładka **Bot** → sekcja **Privileged Gateway Intents** → zaznacz **Message Content Intent**)
- Uprawnienia bota do **Connect** i **Speak** na kanałach głosowych na serwerze, na którym ma działać

## Uruchomienie lokalnie (Docker Compose)

1. Skopiuj i uzupełnij zmienne środowiskowe:

   ```bash
   cp .env.example .env
   ```

2. Uruchom:

   ```bash
   docker compose up --build
   ```

## Komendy bota

- `!join` – bot dołącza do Twojego kanału głosowego
- `!play <url>` – odtwarza audio z podanego URL
- `!pause` – pauzuje odtwarzanie
- `!resume` – wznawia odtwarzanie
- `!stop` – zatrzymuje odtwarzanie
- `!leave` – bot opuszcza kanał

Prefiks komend można zmienić przez zmienną `PREFIX` (domyślnie `!`).
