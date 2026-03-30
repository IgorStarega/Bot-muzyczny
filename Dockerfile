FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser \
    && useradd -r -m -d /app -g appuser appuser \
    && mkdir -p /app/.cache \
    && chown appuser:appuser /app /app/.cache

COPY --chown=appuser:appuser requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser bot.py ./

ENV HOME=/app \
    XDG_CACHE_HOME=/app/.cache

USER appuser

CMD ["python", "bot.py"]
