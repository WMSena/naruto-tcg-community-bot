"""
Reconstructed MongoDB documents for an empty `narutotcg` database.

Evidence:
- `message_store` / `message_template` are the only collections the bot reads.
- leftover debug code in `bot/cogs/ping.py` looks up key `"rules"`.
- Discord snowflake 1529821999977857036 decodes to 2026-07-23 12:06:27 UTC
  (19:06 WIB), matching the published peraturan embed.
- embed color default 0xF39C12 matches the orange accent bar.
"""

from datetime import datetime, timezone

RULES_MESSAGE_ID = "1529821999977857036"
RULES_PUBLISHED_AT = datetime(2026, 7, 23, 12, 6, 27, 513000, tzinfo=timezone.utc)

# 0xF39C12 — discord.Embed default in embed_builder.py and the live accent color.
RULES_EMBED_COLOR = 0xF39C12

RULES_TEMPLATE = {
    "slug": "rules",
    "title": "📜 Peraturan Server - Aliansi Shinobi INAGAKURE",
    "description": (
        "Selamat datang di **Naruto TCG Community Indonesia!**\n\n"
        "Demi menjaga ekosistem komunitas yang sehat, adil, dan menyenangkan, "
        "setiap Shinobi diwajibkan membaca dan mematuhi peraturan di bawah ini."
    ),
    "color": RULES_EMBED_COLOR,
    "fields": [
        {
            "name": "1️⃣ Menghormati Sesama Shinobi (Sopan Santun)",
            "value": (
                "Saling menghargai sesama anggota. Dilarang keras melakukan "
                "harassment, ujaran kebencian (*hate speech*), provokasi, atau "
                "serangan pribadi."
            ),
            "inline": False,
        },
        {
            "name": "2️⃣ Transaksi & Trade Aman",
            "value": (
                "Gunakan channel pasar/jual-beli yang disediakan. Sangat "
                "disarankan menggunakan jasa Rekber (Rekening Bersama) terpercaya. "
                "Penipuan (*scamming*) akan berujung pada **permanent ban**."
            ),
            "inline": False,
        },
        {
            "name": "3️⃣ Kejujuran Kartu & Proxies",
            "value": (
                "Wajib memberikan deskripsi kondisi kartu secara jujur saat "
                "jual-beli/barter.\n"
                "Penggunaan kartu *Proxy* / cetakan sendiri wajib diinfokan "
                "secara transparan saat *casual match* dan dilarang pada "
                "turnamen resmi."
            ),
            "inline": False,
        },
        {
            "name": "4️⃣ Keamanan & Konten Bebas NSFW",
            "value": (
                "Dilarang membagikan konten NSFW, SARA, atau konten ilegal "
                "lainnya. Jaga agar server tetap aman dan nyaman untuk semua umur."
            ),
            "inline": False,
        },
        {
            "name": "5️⃣ Dilarang Spam & Promosi Tanpa Izin",
            "value": (
                "Hindari *spamming*, *mention* berlebihan, atau membagikan tautan "
                "promosi/server lain tanpa izin dari Moderator/Kage."
            ),
            "inline": False,
        },
        {
            "name": "6️⃣ Gunakan Channel Sesuai Diskusi",
            "value": (
                "Gunakan channel yang sesuai untuk topik tertentu seperti "
                "*deck building*, *rules clarification*, transaksi, atau "
                "obrolan santai."
            ),
            "inline": False,
        },
    ],
    "footer": {
        "text": "Aliansi Shinobi INAGAKURE • Terakhir Diperbarui",
        "icon_url": "https://cmsapi-frontend.naruto-official.com/site/api/naruto/Image/get?path=/naruto/en/news/2026/06/18/J1bgbqcDwU7O6QdD/bkX6MlvKX4LLmZAUKYG8GGK8n9lE6cPD.jpeg"
    },
}

DEFAULT_MESSAGE_TEMPLATES = [RULES_TEMPLATE]
