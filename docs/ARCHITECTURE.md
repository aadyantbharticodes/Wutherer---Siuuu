# Wutherer Architecture & Engineering Specification

## 1. System Overview

Wutherer is an enterprise-grade Discord bot platform and web control panel engineered for high-scale communities, gaming networks, and creator servers. The architecture combines an asynchronous Python bot core (`discord.py` 2.3+ `AutoShardedBot`) with a **FastAPI** REST daemon and a **Next.js 14** web application.

```
┌─────────────────────────────────────────────────────────────┐
│                       Discord Gateway                       │
└──────────────────────────────┬──────────────────────────────┘
                               │ WebSocket Events & Sharding
┌──────────────────────────────▼──────────────────────────────┐
│                    Wutherer Core (Python)                   │
│                                                             │
│  ┌────────────────────────┐    ┌─────────────────────────┐  │
│  │   21 Extension Modules │    │     Services Layer      │  │
│  │  ────────────────────  │    │  ─────────────────────  │  │
│  │  • Moderation & Automod│◄───┤  • AIService (Gemini)   │  │
│  │  • Antinuke Security   │    │  • YouTubeService (v3)  │  │
│  │  • Server & Automation │    │  • MinecraftService     │  │
│  │  • Tickets & Verify    │    │  • Image & CAPTCHA      │  │
│  │  • Leveling & XP       │    │  • EmbedBuilder         │  │
│  │  • Economy & Casino    │    │  • PermissionManager    │  │
│  │  • Music & Fun         │    │  • CooldownBuckets      │  │
│  │  • Utility & Dev       │    │  • AsyncScheduler       │  │
│  │  • Gaming & YouTube    │    │  • TTLCache             │  │
│  └───────────┬────────────┘    └─────────────────────────┘  │
│              │                                              │
│  ┌───────────▼────────────┐    ┌─────────────────────────┐  │
│  │   Unified DB Pool      │    │    FastAPI Daemon       │  │
│  │   (SQLite WAL Pool)    │◄───┤    (Port 8080)          │  │
│  └───────────┬────────────┘    └────────────▲────────────┘  │
│              │                              │               │
│  ┌───────────▼────────────┐                 │               │
│  │   Background Workers   │                 │               │
│  │  • YouTube Monitor     │                 │               │
│  │  • Giveaway Checker    │                 │               │
│  │  • Reminder Dispatcher │                 │               │
│  │  • Minecraft Tracker   │                 │               │
│  └────────────────────────┘                 │               │
└─────────────────────────────────────────────┼───────────────┘
                                              │ REST + API Key / Bearer
┌─────────────────────────────────────────────┴───────────────┐
│              Next.js 14 Dashboard (Port 3000)               │
│  • Modern Tailwind + Radix UI + Wutherer Purple Aesthetics  │
│  • Real-time Guild Module Configuration Controls            │
│  • Gemini AI Persona & Sandbox Controls                     │
│  • YouTube Creator Hub & Notification Manager               │
│  • Minecraft Live Server Ping & Skin Preview Utility        │
│  • Antinuke Shield & Automod Threshold Configuration        │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Core Components

### 2.1 Bot Core (`bot/launcher.py` & `bot/core/bot.py`)
- **Single Unified Entrypoint**: `launcher.py` initializes structured logging, starts the FastAPI daemon thread, and launches `WuthererBot`.
- **Auto-Sharding**: Automatically manages Discord gateway shards as server scale expands.
- **Dynamic Prefix Resolution**: Database-driven prefix caching with instant in-memory lookups falling back to `DEFAULT_PREFIX` (`s!`).
- **Dynamic Presence**: Status rotation displaying active server and user counts.

### 2.2 Database Layer (`bot/database/`)
- **Consolidated Architecture**: Consolidated 38 legacy DB files into a single unified SQLite database with WAL journaling mode (`bot/data/wutherer.db`).
- **Async Connection Pool (`pool.py`)**: Executes concurrent asynchronous queries using `aiosqlite` with `PRAGMA journal_mode=WAL` and `PRAGMA busy_timeout=5000` to prevent lock contention between the bot and API threads.
- **Automated Schema Migrations (`migrations.py`)**: Self-healing migrations create and update 40+ tables and indexes on startup.
- **Modular Data Access Objects (`models/`)**: Strongly typed DAO models for guilds, users, moderation, leveling, tickets, verification, economy, giveaways, and logging.

### 2.3 Command Extensions (`bot/extensions/`)
Categorized under 21 distinct extension modules:
1. `moderation`: Complete moderation toolkit with case logging, hierarchy verification, and DM notifications.
2. `automod`: Real-time filtering against spam, invites, links, caps, and mass mentions.
3. `antinuke`: Anti-raid shield tracking 14 unauthorized server mutation event types.
4. `server`: Prefix configuration, welcome/goodbye greetings, autoroles, and reaction roles.
5. `tickets`: Interactive support ticket panel with button triggers and staff claiming.
6. `verification`: Distorted visual CAPTCHA and button challenges for server entry.
7. `leveling`: Message XP calculation, Pillow graphical rank cards, and role rewards.
8. `logging`: Audit logging for deleted/edited messages, role updates, and channel changes.
9. `ai`: Google Gemini conversational intelligence, coding assistance, and language tools.
10. `youtube`: Channel search, video search, and upload notifications.
11. `gaming`: Minecraft server queries, skin rendering, UUID lookups, and Hypixel stats.
12. `economy`: Virtual currency, daily rewards, work shifts, banking, transfers, and casino games.
13. `community`: Giveaways, interactive polls, suggestions, and starboard.
14. `fun`: Mini-games (Wordle, 2048, Rock Paper Scissors, trivia, 8-ball, dice).
15. `music`: Audio playback, queue management, volume, and playback controls.
16. `productivity`: Reminders, countdown timers, calculator, and unit converters.
17. `social`: AFK notifications, user profiles, reputation points, and bios.
18. `developer`: JSON formatting, regex testing, base64, hashing, and timestamp generator.
19. `utility`: Serverinfo, userinfo, avatar, banner, ping, and botinfo.
20. `admin`: Owner-only controls, extension reloading, eval, and tree syncing.
21. `events`: Central ready and command error event handling.

### 2.4 Background Workers (`bot/workers/`)
- `YouTubeMonitorWorker`: Regularly polls subscribed YouTube channels for new video releases.
- `GiveawayCheckerWorker`: Checks active giveaways and resolves winners when timers conclude.
- `ReminderDispatcherWorker`: Dispatches database-backed reminders at scheduled timestamps.
- `MinecraftStatusUpdaterWorker`: Periodically pings tracked Minecraft servers and edits Discord embeds.

### 2.5 REST API & Dashboard (`bot/api/` & `dashboard/`)
- **FastAPI Backend**: Provides modular endpoints for guild metadata, settings, moderation logs, leveling leaderboards, tickets, verification, and AI settings.
- **Next.js 14 Frontend**: Built with React 18, Tailwind CSS, Lucide icons, and Radix UI primitives. Features a dark Wutherer purple palette, responsive mobile design, and server management pages.
