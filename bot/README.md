# Wutherer Core — Discord Bot & FastAPI Backend

### High-performance Discord platform built with discord.py, Google Gemini AI, mcstatus, YouTube Data API v3, and an embedded FastAPI REST server.

---

## ✦ Directory Structure

```
bot/
├── launcher.py                Single unified entrypoint (starts API daemon & WuthererBot)
├── config.py                  Central configuration & Wutherer color tokens (0x6C5CE7)
│
├── core/                      Internal Framework
│   ├── bot.py                 WuthererBot (AutoShardedBot, prefix resolver, dynamic status)
│   ├── context.py             Context subclass with success/error/warn/info/confirm embeds
│   ├── cog.py                 WuthererCog base class
│   ├── permissions.py         PermissionManager role hierarchy & discord permissions
│   ├── cooldowns.py           Sliding window cooldown buckets and tiered cooldown checks
│   ├── checks.py              Command permission predicates
│   └── errors.py              Custom framework exceptions
│
├── database/                  Unified SQLite Database
│   ├── pool.py                Async connection pool with WAL mode
│   ├── migrations.py          Schema definitions & migration runner
│   └── models/                Guild, moderation, leveling, tickets, verification, ai, economy...
│
├── services/                  Business Logic Layer
│   ├── ai.py                  Google Gemini AI engine (chat, summarize, code, translate)
│   ├── youtube.py             YouTube Data API v3 integration
│   ├── minecraft.py           Server status queries, skin rendering, Hypixel lookups
│   ├── captcha.py             Pillow-based distorted visual and math CAPTCHAs
│   ├── image.py               Avatar cropping, filters, and custom rank card renderer
│   ├── embed.py               EmbedBuilder standardizer
│   ├── pagination.py          Paginators with button navigation
│   ├── cache.py               In-memory TTL cache
│   ├── moderation.py          Moderation execution, DM notices, and mod case logging
│   └── scheduler.py           Async background task scheduler
│
├── extensions/                21 Modular Command Categories
│   ├── moderation/            Ban, unban, kick, warn, timeout, softban, purge, lock...
│   ├── automod/               Spam, caps, links, invites, mentions, emojis, bad words
│   ├── antinuke/              Anti-raid defense against channel, role, bot, and guild attacks
│   ├── server/                Prefix, welcome, goodbye, autoroles, reaction roles
│   ├── tickets/               Interactive panels, private channels, and staff claiming
│   ├── verification/          CAPTCHA and button entry verification
│   ├── leveling/              Message XP, rank cards, and role rewards
│   ├── logging/               Audit logging for message edits, deletes, and server changes
│   ├── ai/                    Gemini chat, ask, summarize, rewrite, translate, code
│   ├── youtube/               Video and channel searches, live upload notifications
│   ├── gaming/                Minecraft server status, player skins, and profiles
│   ├── economy/               Credits, daily, work, deposit, withdraw, coinflip, slots
│   ├── community/             Giveaways, polls, suggestions, starboard
│   ├── fun/                   Mini-games (RPS, 8ball, roll, flip, choose, trivia)
│   ├── music/                 Voice playback, queue, volume, skip, pause
│   ├── productivity/          Reminders, timers, calculator, unit converter
│   ├── social/                AFK notifications, user profiles, reputation
│   ├── developer/             JSON validator, regex tester, base64, hash, timestamps
│   ├── utility/               Userinfo, serverinfo, avatar, banner, ping, botinfo
│   ├── admin/                 Owner commands, extension reload, eval, sync, broadcast
│   └── events/                Ready, member join/leave, command errors
│
├── workers/                   Background Daemons
│   ├── youtube_monitor.py     Periodic YouTube upload monitor
│   ├── giveaway_checker.py    Giveaway timer and winner picker
│   ├── reminder_dispatcher.py Database reminder scheduler
│   └── mc_status_updater.py   Minecraft server status embed updater
│
├── api/                       FastAPI Dashboard Backend
│   ├── app.py                 FastAPI application factory with CORS & middleware
│   ├── auth.py                API key & Bearer token authentication
│   ├── middleware.py          Request logging & latency tracker
│   └── routes/                Health, bot, guilds, moderation, leveling, tickets...
│
└── tests/                     Unit Test Suite
    ├── test_permissions.py    Role hierarchy & ownership tests
    ├── test_database.py       Leveling XP calculation and schema models
    ├── test_ai_service.py     AI service initialization & prompt validation
    ├── test_moderation.py     Moderation permission checks
    ├── test_verification.py   CAPTCHA generation tests
    ├── test_api.py            FastAPI route mounts & app factory
    └── test_cache.py          TTL cache expiry & invalidation
```

---

## ✦ Getting Started

### 1. Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate   # On Windows (or 'source venv/bin/activate' on Linux/macOS)
pip install -r requirements.txt
```

### 2. Configure Environment Variables (`.env`)
Copy `.env.example` to `.env`:
```env
TOKEN=your_discord_bot_token
GEMINI_API_KEY=your_gemini_api_key
YOUTUBE_API_KEY=your_youtube_api_key
DASHBOARD_SECRET=your_dashboard_api_key
API_ENABLED=true
API_PORT=8080
```

### 3. Start Wutherer
```bash
python launcher.py
```

### 4. Run Unit Tests
```bash
python -m unittest discover -s tests -p "test_*.py"
```
