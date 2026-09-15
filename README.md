# Naruto TCG Discord Bot

Discord bot for the **Naruto TCG Community Indonesia**.

## Features

- Managed Discord embeds
- MongoDB-backed message templates
- Slash commands
- Role-based permissions
- Modular architecture for future expansion

## Tech Stack

- Python 3.13
- discord.py
- MongoDB
- Docker
- Docker Compose

## Run with Docker

MongoDB runs as container `kage` on the external Docker network `naruto-network`.
Port `27017` is published only on `127.0.0.1` so Compass can use an SSH tunnel.
Do not expose `27017` on the public VPS IP.

On the VPS, from the project root:

```bash
docker network create naruto-network
```

If that says the network already exists, continue.

If an old `kage` container is already running **without** a password, remove it
so Compose can recreate it with auth. This is safe when the database is already
empty. `MONGO_INITDB_*` only applies to a **new empty volume**.

```bash
docker stop kage
docker rm kage
```

Copy `services/discord-bot/.env.example` to `services/discord-bot/.env` if needed,
then set a password:

```bash
openssl rand -hex 24
```

Put that value in `MONGO_INITDB_ROOT_PASSWORD`. Username defaults to `naruto`.

```bash
docker compose up -d --build
docker compose ps
docker logs naruto-discord-bot --tail 50
```

### Compass from your PC

Do not connect to `mongodb://kage:27017` from your laptop. `kage` only exists
inside Docker.

1. SSH tunnel: `ssh -L 27017:127.0.0.1:27017 YOUR_USER@VPS_IP`
2. Compass URI: `mongodb://naruto:YOUR_PASSWORD@127.0.0.1:27017/narutotcg?authSource=admin`

Or in Compass use **Advanced → SSH / Tunnel** with MongoDB host `127.0.0.1`
and your VPS SSH login.

## Run Locally

```bash
python -m bot.main
```