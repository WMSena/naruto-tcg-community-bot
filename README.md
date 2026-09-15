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

`MONGO_INITDB_*` only creates the root user on a **new empty volume**. If
`kage` is **Up** but **unhealthy** and logs say `UserNotFound`, Mongo is
running and the user was never created. Create it from inside the
container (same username and password as `core/mongo/.env` / `MONGO_URI`):

```bash
docker exec -it kage mongosh admin --eval 'db.createUser({user: "YOUR_USERNAME", pwd: "YOUR_PASSWORD", roles: [{role: "root", db: "admin"}]})'
docker compose up -d
```

If `createUser` returns **Command createUser requires authentication**, a user
already exists and the localhost exception is off. Start Mongo once **without**
auth on the same volume, create `hashirama` (or use the existing username in
`MONGO_URI`), then start `kage` again:

```bash
VOLUME=$(docker inspect kage --format '{{range .Mounts}}{{if eq .Destination "/data/db"}}{{.Name}}{{end}}{{end}}')
docker stop kage
docker run --rm -d --name kage-repair -v "${VOLUME}:/data/db" mongo:8.0 --bind_ip_all
sleep 5
docker exec kage-repair mongosh admin --eval 'db.getUsers()'
docker exec -it kage-repair mongosh admin --eval 'db.createUser({user: "YOUR_USERNAME", pwd: "YOUR_PASSWORD", roles: [{role: "root", db: "admin"}]})'
docker stop kage-repair
docker start kage
docker compose up -d
```

If the database is still empty and you would rather start over:

```bash
docker compose down
docker volume ls | grep kage
docker volume rm VOLUME_NAME
docker compose up -d
```

If an old `kage` container is already running **without** a password, remove it
so Compose can recreate it with auth:

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