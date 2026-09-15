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

MongoDB runs as container `kage` (`mongo:8.0`) on the external Docker
network `naruto-network`. Do not use `mongo:latest`: that tag is currently
MongoDB 8.3, which cannot open data files created by `mongo:7` (container
exit code 62). Upgrade path is 7.0 → 8.0, not 7.0 → 8.3.
Port `27017` is published on the VPS. Access is protected by the Mongo root
password, not by binding to localhost.

There are two env files. Do not commit either `.env`.

| File | Used by | What to set |
|---|---|---|
| `core/mongo/.env` | `kage` | `MONGO_INITDB_ROOT_USERNAME` and `MONGO_INITDB_ROOT_PASSWORD` (first boot only) |
| `services/discord-bot/.env` | the bot | `MONGO_URI` **with** the same user and password |

Copy the examples if those files do not exist yet:

```bash
cp core/mongo/.env.example core/mongo/.env
cp services/discord-bot/.env.example services/discord-bot/.env
```

Generate a password and put the **same** value in both files:

```bash
openssl rand -hex 24
```

`core/mongo/.env`:

```
MONGO_INITDB_ROOT_USERNAME=naruto
MONGO_INITDB_ROOT_PASSWORD=YOUR_PASSWORD
```

`services/discord-bot/.env` (hostname `kage` only works inside Docker):

```
MONGO_URI=mongodb://naruto:YOUR_PASSWORD@kage:27017/narutotcg?authSource=admin
```

If `MONGO_URI` is set, the bot uses it as-is and ignores `MONGO_USERNAME` /
`MONGO_PASSWORD`. A URI without a user (`mongodb://kage:27017`) will fail once
Mongo requires a password.

On the VPS, from the project root:

```bash
docker network create naruto-network
```

If that says the network already exists, continue.

If an old `kage` container is crash-looping after an image change, stop it
and start again on `mongo:8.0` so it can read the existing `kage-data`
volume. Only delete the volume if the database is empty and you want a
fresh 8.0 data directory.

```bash
docker stop kage
docker rm kage
docker compose up -d --build
docker compose ps
docker logs kage --tail 80
docker logs naruto-discord-bot --tail 50
```

### Compass from your PC

`kage` is a Docker hostname. From your laptop use the VPS IP:

```
mongodb://naruto:YOUR_PASSWORD@VPS_IP:27017/narutotcg?authSource=admin
```

## Run Locally

```bash
python -m bot.main
```