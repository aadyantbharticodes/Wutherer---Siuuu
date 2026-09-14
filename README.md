<div align="center">

```
███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗     
██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║     
███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║     
╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║     
███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗
╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
```

<h3>Wutherer • Server Intelligence, Automated • Next-Gen Discord Bot Platform</h3>

<p>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/></a>
  <a href="https://nextjs.org"><img src="https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=nextdotjs&logoColor=white"/></a>
  <a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/FastAPI-REST_API-009688?style=for-the-badge&logo=fastapi&logoColor=white"/></a>
  <a href="https://discordpy.readthedocs.io"><img src="https://img.shields.io/badge/Discord.py-v2.3+-5865F2?style=for-the-badge&logo=discord&logoColor=white"/></a>
  <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/Google_Gemini-AI_Engine-8E75C2?style=for-the-badge&logo=google&logoColor=white"/></a>
</p>
<p>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge"/></a>
  <a href="docs/ARCHITECTURE.md"><img src="https://img.shields.io/badge/Docs-Architecture-indigo?style=for-the-badge"/></a>
  <a href="docs/COMMANDS.md"><img src="https://img.shields.io/badge/Docs-Commands-success?style=for-the-badge"/></a>
  <a href="docs/SETUP.md"><img src="https://img.shields.io/badge/Docs-Setup_Guide-orange?style=for-the-badge"/></a>
</p>

</div>

---

## ✦ Overview

**Wutherer** is an enterprise-grade, all-in-one Discord bot platform and web dashboard re-architected from the ground up for high-scale communities, gaming servers, and creators.

Combining asynchronous Python architecture with a **FastAPI** daemon, a unified **SQLite WAL connection pool**, and a sleek **Next.js 14** web control panel, Wutherer provides modular server intelligence, sub-second antinuke defense, Google Gemini AI chat, and comprehensive automation.

```
Wutherer/
├── 🤖  bot/                   Python Discord bot + FastAPI REST API
│   ├── launcher.py            Single unified entrypoint (starts API daemon & WuthererBot)
│   ├── config.py              Environment variables and brand color tokens (0x6C5CE7)
│   ├── core/                  WuthererBot client, context, cog base, permissions, checks, cooldowns
│   ├── database/              SQLite async WAL pool with self-healing migrations & models
│   ├── services/              Gemini AI, YouTube v3, Minecraft status, CAPTCHA, image cards, scheduler
│   ├── extensions/            21 Modular categories (moderation, automod, antinuke, ai, tickets, etc.)
│   ├── workers/               YouTube monitor, giveaway checker, reminder dispatcher, Minecraft tracker
│   ├── api/                   FastAPI REST API routes powering the web dashboard
│   └── tests/                 Comprehensive unit test suite
│
├── 🌐  dashboard/             Next.js 14 Web Application
│   ├── app/                   App Router (landing page, server selector, guild modules)
│   ├── components/            Tailwind CSS & Radix UI dashboard components
│   ├── lib/                   Authenticated REST API client
│   └── types/                 TypeScript schemas
│
└── 📚  docs/                  Documentation
    ├── ARCHITECTURE.md        Technical architecture and subsystem design
    ├── COMMANDS.md            Command catalog and usage directory
    └── SETUP.md               End-to-end setup and deployment guide
```

---

## ✦ Core Subsystems

### 🛡️ Enterprise Security & Moderation
- **Disciplinary Actions**: Ban, tempban, kick, softban, timeout, warn, purge, lock, and nuke.
- **Automod Engine**: 7 content filters (spam, caps, links, invites, mentions, emojis, bad words).
- **Anti-Raid Antinuke**: 14 automated event protections (mass bans, channel deletions, rogue bots).
- **Image CAPTCHA**: Distorted visual and math verification challenges with Pillow.

### 🧠 Google Gemini AI Engine
- **Conversational Chat**: Multi-turn dialogue with per-user persistent memory buffer.
- **Custom System Personas**: Configure server-tailored personality and tone from the dashboard.
- **Tools & Assistants**: Code generation, text summaries, translation, and grammar fixes.

### 🎮 Gaming & Minecraft Hub
- **Live Server Monitoring**: Auto-refreshing status embeds for Java and Bedrock servers.
- **Player Skin Viewer**: 3D body skin renders and UUID lookups via Mojang/Crafatar.
- **Hypixel Analytics**: Player level and statistics.

### 📺 YouTube Upload Engine
- **Search**: Video and channel search with subscriber and view metrics.
- **Live Notifications**: Automated upload alerts dispatched to designated server channels.

### 🎫 Support & Community Automation
- **Tickets**: Dynamic buttons, private support channels, and staff claiming.
- **Leveling**: Message XP, custom Pillow rank cards, and role rewards.
- **Community**: Giveaways, interactive polls, suggestions, and starboard.

---

## ✦ Quick Start

### 1. Bot Setup
```bash
cd bot
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your DISCORD_TOKEN, GEMINI_API_KEY, and YOUTUBE_API_KEY
python launcher.py
```

### 2. Dashboard Setup
```bash
cd dashboard
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to access the Wutherer Control Panel.

---

## ✦ License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
