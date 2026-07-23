FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install shared core package
COPY core /app/core

# Install bot
COPY services/discord-bot /app/services/discord-bot

WORKDIR /app/services/discord-bot

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -e /app/core

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "bot.main"]