# Wutherer — Complete Repository Directory & File Inventory Tree

> **Repository**: `Wutherer` (Siuuu)  
> **Branch**: `docs/file-tree`  
> **Total Cataloged Files**: `793`  
> **Total Source Lines of Code**: `45,164`  
> **Total Storage Footprint**: `18.49 MB`  
> **Architecture**: Discord.py v2 Bot Engine + FastAPI REST Backend + Next.js 14 Web Dashboard  

---

## Table of Contents

1. [Architecture & Technology Stack](#architecture--technology-stack)
2. [Status & State Legend](#status--state-legend)
3. [ASCII Directory Hierarchy Tree](#ascii-directory-hierarchy-tree)
4. [Detailed Subsystem Breakdown](#detailed-subsystem-breakdown)
   - [1. Repository Root Files (4 files)](#1-repository-root-files)
   - [2. Bot Core Configuration & Launcher (6 files)](#2-bot-core-configuration--launcher)
   - [3. Bot Core Framework Architecture (8 files)](#3-bot-core-framework-architecture)
   - [4. Database Persistence Layer & Connection Pool (3 files)](#4-database-persistence-layer--connection-pool)
   - [5. Database Schema & ORM Repositories (26 files)](#5-database-schema--orm-repositories)
   - [6. Dashboard Backend API Core (FastAPI) (4 files)](#6-dashboard-backend-api-core-fastapi)
   - [7. REST API Endpoints & Controllers (20 files)](#7-rest-api-endpoints--controllers)
   - [8. Bot Core Service Layer (17 files)](#8-bot-core-service-layer)
   - [9. Background Workers & Daemons (9 files)](#9-background-workers--daemons)
   - [10. Discord Extensions & Command Cogs (67 files)](#10-discord-extensions--command-cogs)
   - [11. Game Engines & Mini-Game Logic (18 files)](#11-game-engines--mini-game-logic)
   - [12. Interactive Discord Button Game Controllers (13 files)](#12-interactive-discord-button-game-controllers)
   - [13. Automated Unit & Integration Test Suites (23 files)](#13-automated-unit--integration-test-suites)
   - [14. Dashboard Configuration & Build Manifests (13 files)](#14-dashboard-configuration--build-manifests)
   - [15. Dashboard Pages, Routes & Root Layouts (5 files)](#15-dashboard-pages,-routes--root-layouts)
   - [16. Guild Management Dashboard Modules (19 files)](#16-guild-management-dashboard-modules)
   - [17. React UI Components & Design System (17 files)](#17-react-ui-components--design-system)
   - [18. Dashboard Client Libraries & Type Declarations (4 files)](#18-dashboard-client-libraries--type-declarations)
   - [19. Technical Architecture Documentation (11 files)](#19-technical-architecture-documentation)
   - [20. Graphical Media, Fonts & Static Assets (506 files)](#20-graphical-media,-fonts--static-assets)

---

## Architecture & Technology Stack

| Layer | Primary Technologies | Key Role | Total Files |
| :--- | :--- | :--- | :--- |
| **Bot Runtime Core** | Python 3.11+, Discord.py 2.3+ | Sharded gateway connection, commands, events, rate-limiting | 14 files |
| **Database Persistence** | PostgreSQL (asyncpg) / SQLite (aiosqlite) | Async connection pooling, schema migrations, 26 domain models | 29 files |
| **Dashboard API Backend** | FastAPI, Uvicorn, Pydantic, Jose JWT | RESTful JSON API providing authenticated guild settings and controls | 24 files |
| **Business Services & Daemons** | Pillow, Google Gemini API, Asyncio Tasks | Background security watchdogs, analytics rollups, AI services | 26 files |
| **Extension Cogs** | Discord.py commands.Cog | 31 feature categories (Moderation, Automod, Antinuke, Tickets, Economy, etc.) | 67 files |
| **Games Suite** | Discord UI Buttons, Canvas / PIL | 23 mini-games (Chess, Battleship, Connect Four, Country Guess, 2048, Uno) | 31 files |
| **Web Dashboard Frontend** | Next.js 14, React 18, TypeScript, Tailwind CSS | Responsive web administration panel for server managers | 58 files |
| **Test Suites** | Pytest, Pytest-asyncio, Mock | Unit and integration test coverage for all services, models, and routes | 23 files |
| **Static Assets** | PNG, TTF Fonts, SVG | Country flags (253), map shapes (231), fonts, rank badges | 506 files |
| **Technical Docs** | Markdown | Architecture diagrams, command manuals, worker schedules, setup guides | 15 files |

---

## Status & State Legend

Every file in this catalog is annotated with a **State** describing its operational nature:

- `🟢 Production Core`: Foundational runtime framework and lifecycle engines.
- `📦 DB Model`: Database schema definition and asynchronous persistence entity.
- `🌐 REST Endpoint`: FastAPI HTTP route controller exposing web endpoints.
- `🔄 Service / Worker`: Active background logic engine, external API client, or daemon.
- `🔌 Discord Cog`: Pluggable command module loaded dynamically at runtime.
- `🎮 Game Engine / UI`: Interactive Discord gameplay mechanics or button views.
- `💻 Dashboard Page`: Next.js web application page or layout.
- `🧩 UI Primitive`: Reusable frontend design system component.
- `🧪 Unit Test Suite`: Automated regression and behavior test suite.
- `⚙️ Configuration`: Runtime settings, package manifests, or environment templates.
- `🖼️ Static Asset`: Binary graphics, flags, fonts, and game assets.
- `📖 Documentation`: Technical markdown guide or milestone checklist.

---

## ASCII Directory Hierarchy Tree

```text
Wutherer/
├── .gitignore                                [Git ignore rules]
├── LICENSE                                   [MIT License]
├── README.md                                 [Master project guide]
├── task.md                                   [Project task tracker]
│
├── bot/                                      [Python Discord Bot & FastAPI Backend]
│   ├── .env.example                          [Environment template]
│   ├── config.py                             [Bot runtime configuration]
│   ├── launcher.py                           [Application bootstrapper]
│   ├── requirements.txt                      [Python dependencies]
│   │
│   ├── api/                                  [FastAPI REST API Server]
│   │   ├── app.py                            [FastAPI app factory & CORS]
│   │   ├── auth.py                           [API key & Bearer token auth]
│   │   ├── middleware.py                     [Logging, timing, rate limits]
│   │   └── routes/                           [20 REST Route Modules]
│   │       ├── admin.py, ai.py, analytics.py, antinuke.py, antiphishing.py, ...
│   │
│   ├── core/                                 [Bot Foundation & Base Classes]
│   │   ├── bot.py                            [commands.Bot custom subclass]
│   │   ├── checks.py                         [Security check decorators]
│   │   ├── cog.py                            [BaseCog abstract class]
│   │   ├── context.py                        [Enhanced Context with embed shortcuts]
│   │   ├── cooldowns.py                      [Bucket rate limiters]
│   │   ├── errors.py                         [Centralized error handler]
│   │   ├── logging.py                        [Structured logger configuration]
│   │   └── permissions.py                    [Permission & hierarchy checks]
│   │
│   ├── database/                             [Database Layer & ORM]
│   │   ├── pool.py                           [Async SQLite & PostgreSQL pool]
│   │   ├── migrations.py                     [Schema DDL migration runner]
│   │   └── models/                           [26 Domain Models & Repositories]
│   │       ├── guild.py, user.py, moderation.py, leveling.py, tickets.py, ...
│   │
│   ├── extensions/                           [67 Cog Command Modules in 31 Packages]
│   │   ├── admin/, ai/, analytics/, antinuke/, antiphishing/, automation/,
│   │   ├── automod/, autoresponder/, backup/, community/, developer/, economy/,
│   │   ├── events/, fun/, games/, gaming/, leveling/, logging/, moderation/,
│   │   ├── music/, onboarding/, productivity/, server/, shop/, social/,
│   │   └── templates/, tickets/, utility/, verification/, youtube/
│   │
│   ├── games/                                [23 Interactive Game Engines]
│   │   ├── battleship.py, blackjack.py, chess_game.py, connect_four.py,
│   │   ├── country_guess.py, hangman.py, minesweeper.py, reaction_test.py,
│   │   ├── rps.py, slots.py, tictactoe.py, trivia.py, twenty_48.py, uno.py, ...
│   │   ├── button_games/                     [13 Discord.ui.View Button Controllers]
│   │   │   ├── chess_buttons.py, tictactoe_buttons.py, wordle_buttons.py, ...
│   │   └── assets/                           [503 Game Assets: Flags & Outline Maps]
│   │       ├── country-flags/                [253 PNG country flags]
│   │       ├── country-data/                 [231 PNG country map outlines]
│   │       └── 2048-emoji-asset-examples/    [14 PNG tile previews]
│   │
│   ├── services/                             [17 Singleton Business Services]
│   │   ├── ai.py, antialt.py, antinuke.py, antiphishing.py, cache.py, captcha.py,
│   │   ├── embed.py, image.py, minecraft.py, moderation.py, onboarding_service.py,
│   │   ├── pagination.py, scheduler.py, templates.py, welcome_card.py, youtube.py
│   │
│   ├── workers/                              [9 Background Daemons]
│   │   ├── analytics_aggregator.py, antinuke_watchdog.py, giveaway_checker.py,
│   │   ├── mc_status_updater.py, onboarding_dispatcher.py, reminder_dispatcher.py,
│   │   ├── scheduled_messages.py, youtube_monitor.py
│   │
│   ├── tests/                                [23 Automated Pytest Suites]
│   │   ├── test_ai_service.py, test_analytics.py, test_antinuke.py, test_api.py,
│   │   ├── test_database.py, test_games_suite.py, test_moderation.py, ...
│   │
│   └── assets/                               [Rank card templates & TTF fonts]
│
├── dashboard/                                [Next.js 14 App Router Web Application]
│   ├── package.json, next.config.mjs, tailwind.config.ts, tsconfig.json
│   │
│   ├── app/                                  [App Router Pages & Layouts]
│   │   ├── layout.tsx, page.tsx, globals.css [Root public landing page]
│   │   └── dashboard/                        [Authenticated Dashboard Views]
│   │       ├── layout.tsx, page.tsx          [Server selector page]
│   │       └── guild/[guildId]/              [19 Server Configuration Pages]
│   │           ├── page.tsx                  [Server overview & health metrics]
│   │           ├── moderation/page.tsx       [Moderation rules & audit history]
│   │           ├── antinuke/page.tsx         [Antinuke limits & quarantine]
│   │           ├── automod/page.tsx          [Automod filter thresholds]
│   │           ├── leveling/page.tsx         [XP curves & role rewards]
│   │           ├── tickets/page.tsx          [Ticket panels & transcripts]
│   │           ├── verification/page.tsx     [CAPTCHA verification flow]
│   │           └── ai/page.tsx               [AI persona & model toggles]
│   │
│   ├── components/                           [17 Reusable React Components]
│   │   ├── ui/                               [11 Design Primitives: Button, Card, ...]
│   │   ├── dashboard/                        [5 Layout Components: Sidebar, Navbar, ...]
│   │   └── landing/                          [Interactive Product Preview Mockup]
│   │
│   └── lib/, types/                          [API client & TypeScript Interfaces]
│
└── docs/                                     [11 Technical Markdown Guides]
    ├── ANTIALT.md, API.md, ARCHITECTURE.md, CASINO.md, COMMANDS.md,
    ├── DEFENSE.md, MODULES.md, ONBOARDING.md, SETUP.md, TEMPLATES.md, WORKERS.md
```

---

## Detailed Subsystem Breakdown

### 1. Repository Root Files

Top-level project configuration, licenses, overview documentation, and development tracker.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [.gitignore](file:///c:/Users/Aadyant/Downloads/Wutherer/.gitignore) | ⚙️ Config | 56 lines (443 B) | Git ignore patterns for dependencies, caches, and secrets. | — |
| [LICENSE](file:///c:/Users/Aadyant/Downloads/Wutherer/LICENSE) | 📖 Legal | 21 lines (1.0 KB) | MIT open-source license documentation. | — |
| [README.md](file:///c:/Users/Aadyant/Downloads/Wutherer/README.md) | 📖 Documentation | 117 lines (6.4 KB) | Master repository overview, installation instructions, and architecture breakdown. | — |
| [task.md](file:///c:/Users/Aadyant/Downloads/Wutherer/task.md) | 📖 Task Tracker | 109 lines (5.0 KB) | Comprehensive phase-by-phase project progress tracker (Phases 1-18). | — |

---

### 2. Bot Core Configuration & Launcher

Bot root entrypoints, application settings, runtime flags, and dependency definitions.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/.env.example](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/.env.example) | ⚙️ Env Template | 39 lines (710 B) | Environment variables template for tokens, database credentials, and API keys. | — |
| [bot/LICENSE](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/LICENSE) | 📖 Legal | 21 lines (1.0 KB) | MIT open-source license documentation. | — |
| [bot/README.md](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/README.md) | 📖 Documentation | 115 lines (6.0 KB) | Bot operational guide and architecture documentation. | — |
| [bot/config.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/config.py) | ⚙️ Configuration | 74 lines (2.2 KB) | Global bot settings, color tokens (`BOT_COLOR`), embed styles, prefixes, and limits. | — |
| [bot/launcher.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/launcher.py) | 🚀 Entrypoint | 69 lines (1.8 KB) | Main bot bootstrapper initializing database connection pool, service singletons, and extensions. | — |
| [bot/requirements.txt](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/requirements.txt) | ⚙️ Dependencies | 19 lines (333 B) | Bot Python dependency manifest (discord.py, fastapi, aiosqlite, asyncpg, pillow, google-genai). | — |

---

### 3. Bot Core Framework Architecture

Base classes, custom context, permission evaluation engine, rate limiting cooldowns, structured logging, and central error boundaries.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/core/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/core/__init__.py) | 🟢 Core Package | 7 lines (211 B) | Exposes bot core components and framework abstractions. | — |
| [bot/core/bot.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/core/bot.py) | 🟢 Bot Subclass | 170 lines (5.6 KB) | Custom commands.Bot instance managing shard events, extension loader, and uptime tracking. | — |
| [bot/core/checks.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/core/checks.py) | 🟢 Security / Checks | 66 lines (2.1 KB) | Custom command checks for guild owners, administrators, boosters, and bot developers. | — |
| [bot/core/cog.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/core/cog.py) | 🟢 Base Cog | 30 lines (571 B) | Abstract base class for all extension cogs with standardized error logging and database access. | — |
| [bot/core/context.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/core/context.py) | 🟢 Context | 74 lines (2.7 KB) | Enhanced Context class with embed shortcuts (`send_success`, `send_error`, `paginate`). | — |
| [bot/core/cooldowns.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/core/cooldowns.py) | 🟢 Rate Limiting | 64 lines (2.0 KB) | Dynamic per-user, per-guild, and per-channel cooldown buckets preventing spam. | — |
| [bot/core/errors.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/core/errors.py) | 🟢 Error Handling | 56 lines (1.4 KB) | Centralized exception handler and custom exception classes with user-friendly formatting. | — |
| [bot/core/permissions.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/core/permissions.py) | 🟢 Permissions | 60 lines (1.9 KB) | Role hierarchy checking, bot permission validation, and user authority verification. | — |

---

### 4. Database Persistence Layer & Connection Pool

Connection pool management supporting SQLite and PostgreSQL with schema migration engine.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/database/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/__init__.py) | 📦 Database Core | 2 lines (43 B) | Database layer package initialization. | — |
| [bot/database/migrations.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/migrations.py) | 📦 Migrations | 841 lines (26.2 KB) | Schema versioning system executing SQL DDL updates and automatic table creation. | — |
| [bot/database/pool.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/pool.py) | 📦 Connection Pool | 76 lines (2.6 KB) | Async database pool managing connections for SQLite (local) and PostgreSQL (production). | — |

---

### 5. Database Schema & ORM Repositories

26 persistent domain models encapsulating relational tables, indexes, and async CRUD methods.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/database/models/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/__init__.py) | 📦 Database Core | 16 lines (699 B) | Database layer package initialization. | — |
| [bot/database/models/ai.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/ai.py) | 📦 DB Model | 46 lines (1.8 KB) | Database schema and async CRUD operations for Ai data. | — |
| [bot/database/models/analytics.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/analytics.py) | 📦 DB Model | 142 lines (4.8 KB) | Database schema and async CRUD operations for Analytics data. | — |
| [bot/database/models/antialt.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/antialt.py) | 📦 DB Model | 68 lines (2.3 KB) | Database schema and async CRUD operations for Antialt data. | `AntiAltModel` |
| [bot/database/models/antinuke.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/antinuke.py) | 📦 DB Model | 140 lines (4.6 KB) | Database schema and async CRUD operations for Antinuke data. | `AntiNukeModel` |
| [bot/database/models/antiphishing.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/antiphishing.py) | 📦 DB Model | 93 lines (3.4 KB) | Database schema and async CRUD operations for Antiphishing data. | — |
| [bot/database/models/automation.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/automation.py) | 📦 DB Model | 76 lines (2.8 KB) | Database schema and async CRUD operations for Automation data. | — |
| [bot/database/models/autoresponder.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/autoresponder.py) | 📦 DB Model | 116 lines (4.0 KB) | Database schema and async CRUD operations for Autoresponder data. | — |
| [bot/database/models/backup.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/backup.py) | 📦 DB Model | 110 lines (3.9 KB) | Database schema and async CRUD operations for Backup data. | — |
| [bot/database/models/economy.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/economy.py) | 📦 DB Model | 64 lines (2.6 KB) | Database schema and async CRUD operations for Economy data. | — |
| [bot/database/models/giveaways.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/giveaways.py) | 📦 DB Model | 67 lines (2.2 KB) | Database schema and async CRUD operations for Giveaways data. | — |
| [bot/database/models/guild.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/guild.py) | 📦 DB Model | 40 lines (1.3 KB) | Database schema and async CRUD operations for Guild data. | — |
| [bot/database/models/inventory.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/inventory.py) | 📦 DB Model | 110 lines (3.5 KB) | Database schema and async CRUD operations for Inventory data. | — |
| [bot/database/models/leveling.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/leveling.py) | 📦 DB Model | 148 lines (5.8 KB) | Database schema and async CRUD operations for Leveling data. | — |
| [bot/database/models/logging.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/logging.py) | 📦 DB Model | 32 lines (1.4 KB) | Database schema and async CRUD operations for Logging data. | — |
| [bot/database/models/minecraft.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/minecraft.py) | 📦 DB Model | 53 lines (1.9 KB) | Database schema and async CRUD operations for Minecraft data. | — |
| [bot/database/models/moderation.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/moderation.py) | 📦 DB Model | 228 lines (8.6 KB) | Database schema and async CRUD operations for Moderation data. | — |
| [bot/database/models/onboarding.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/onboarding.py) | 📦 DB Model | 126 lines (5.4 KB) | Database schema and async CRUD operations for Onboarding data. | `AutoDMModel`, `AutoPingModel`, `AdvancedWelcomeModel` |
| [bot/database/models/polls.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/polls.py) | 📦 DB Model | 49 lines (1.7 KB) | Database schema and async CRUD operations for Polls data. | — |
| [bot/database/models/shop.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/shop.py) | 📦 DB Model | 96 lines (3.0 KB) | Database schema and async CRUD operations for Shop data. | — |
| [bot/database/models/starboard.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/starboard.py) | 📦 DB Model | 45 lines (1.5 KB) | Database schema and async CRUD operations for Starboard data. | — |
| [bot/database/models/templates.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/templates.py) | 📦 DB Model | 99 lines (3.4 KB) | Database schema and async CRUD operations for Templates data. | `ServerTemplateModel` |
| [bot/database/models/tickets.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/tickets.py) | 📦 DB Model | 55 lines (2.2 KB) | Database schema and async CRUD operations for Tickets data. | — |
| [bot/database/models/user.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/user.py) | 📦 DB Model | 31 lines (1019 B) | Database schema and async CRUD operations for User data. | — |
| [bot/database/models/verification.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/verification.py) | 📦 DB Model | 39 lines (1.7 KB) | Database schema and async CRUD operations for Verification data. | — |
| [bot/database/models/youtube.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/database/models/youtube.py) | 📦 DB Model | 54 lines (1.9 KB) | Database schema and async CRUD operations for Youtube data. | — |

---

### 6. Dashboard Backend API Core (FastAPI)

FastAPI application factory, authentication security schemes, and global middleware.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/api/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/__init__.py) | 🌐 API Core | 2 lines (32 B) | Initializes the FastAPI dashboard backend package. | — |
| [bot/api/app.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/app.py) | 🌐 API Factory | 42 lines (1.0 KB) | FastAPI app instance configuring CORS, middleware, rate-limiting, and route registration. | — |
| [bot/api/auth.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/auth.py) | 🌐 Auth Security | 23 lines (833 B) | API key and JWT authentication dependencies securing dashboard API endpoints. | — |
| [bot/api/middleware.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/middleware.py) | 🌐 Middleware | 24 lines (712 B) | Logging, performance timing, rate limiting, and HTTP exception handling middleware. | — |

---

### 7. REST API Endpoints & Controllers

20 REST API route modules exposing administrative, guild configuration, analytics, and service controls to the web dashboard.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/api/routes/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/__init__.py) | 🌐 API Core | 43 lines (1.3 KB) | Initializes the FastAPI dashboard backend package. | — |
| [bot/api/routes/admin.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/admin.py) | 🌐 REST Endpoint | 25 lines (722 B) | FastAPI endpoints for Admin configuration, statistics, and controls. | — |
| [bot/api/routes/ai.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/ai.py) | 🌐 REST Endpoint | 34 lines (1.0 KB) | FastAPI endpoints for Ai configuration, statistics, and controls. | — |
| [bot/api/routes/analytics.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/analytics.py) | 🌐 REST Endpoint | 49 lines (1.5 KB) | FastAPI endpoints for Analytics configuration, statistics, and controls. | — |
| [bot/api/routes/antinuke.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/antinuke.py) | 🌐 REST Endpoint | 97 lines (3.5 KB) | FastAPI endpoints for Antinuke configuration, statistics, and controls. | `UpdateAntiNukePayload`, `WhitelistPayload`, `LockdownPayload` |
| [bot/api/routes/antiphishing.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/antiphishing.py) | 🌐 REST Endpoint | 56 lines (1.9 KB) | FastAPI endpoints for Antiphishing configuration, statistics, and controls. | — |
| [bot/api/routes/automation.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/automation.py) | 🌐 REST Endpoint | 36 lines (1.2 KB) | FastAPI endpoints for Automation configuration, statistics, and controls. | — |
| [bot/api/routes/autoresponder.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/autoresponder.py) | 🌐 REST Endpoint | 70 lines (2.4 KB) | FastAPI endpoints for Autoresponder configuration, statistics, and controls. | — |
| [bot/api/routes/backup.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/backup.py) | 🌐 REST Endpoint | 99 lines (4.1 KB) | FastAPI endpoints for Backup configuration, statistics, and controls. | — |
| [bot/api/routes/bot.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/bot.py) | 🌐 REST Endpoint | 26 lines (799 B) | FastAPI endpoints for Bot configuration, statistics, and controls. | — |
| [bot/api/routes/guilds.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/guilds.py) | 🌐 REST Endpoint | 81 lines (2.5 KB) | FastAPI endpoints for Guilds configuration, statistics, and controls. | — |
| [bot/api/routes/health.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/health.py) | 🌐 REST Endpoint | 10 lines (227 B) | FastAPI endpoints for Health configuration, statistics, and controls. | — |
| [bot/api/routes/leveling.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/leveling.py) | 🌐 REST Endpoint | 41 lines (1.3 KB) | FastAPI endpoints for Leveling configuration, statistics, and controls. | — |
| [bot/api/routes/minecraft.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/minecraft.py) | 🌐 REST Endpoint | 46 lines (1.4 KB) | FastAPI endpoints for Minecraft configuration, statistics, and controls. | — |
| [bot/api/routes/moderation.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/moderation.py) | 🌐 REST Endpoint | 78 lines (2.7 KB) | FastAPI endpoints for Moderation configuration, statistics, and controls. | — |
| [bot/api/routes/onboarding.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/onboarding.py) | 🌐 REST Endpoint | 82 lines (2.9 KB) | FastAPI endpoints for Onboarding configuration, statistics, and controls. | `UpdateAutoDMPayload`, `UpdateAutoPingPayload`, `UpdateWelcomePayload` |
| [bot/api/routes/templates.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/templates.py) | 🌐 REST Endpoint | 105 lines (3.6 KB) | FastAPI endpoints for Templates configuration, statistics, and controls. | `CreateTemplatePayload`, `ApplyTemplatePayload` |
| [bot/api/routes/tickets.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/tickets.py) | 🌐 REST Endpoint | 36 lines (1.2 KB) | FastAPI endpoints for Tickets configuration, statistics, and controls. | — |
| [bot/api/routes/verification.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/verification.py) | 🌐 REST Endpoint | 34 lines (1.1 KB) | FastAPI endpoints for Verification configuration, statistics, and controls. | — |
| [bot/api/routes/youtube.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/api/routes/youtube.py) | 🌐 REST Endpoint | 47 lines (1.4 KB) | FastAPI endpoints for Youtube configuration, statistics, and controls. | — |

---

### 8. Bot Core Service Layer

17 singleton business logic services providing AI prompt engineering, image manipulation, caching, CAPTCHA verification, and moderation pipelines.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/services/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/__init__.py) | 🔄 Service Package | 11 lines (401 B) | Exports core service singletons. | — |
| [bot/services/ai.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/ai.py) | 🔄 AI Engine | 238 lines (10.0 KB) | Google Gemini client handling chat generation, multi-turn history, summarize, and translate. | — |
| [bot/services/antialt.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/antialt.py) | 🔄 Service Layer | 92 lines (3.4 KB) | Business logic service providing Antialt processing and caching. | — |
| [bot/services/antinuke.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/antinuke.py) | 🔄 Service Layer | 194 lines (8.1 KB) | Business logic service providing Antinuke processing and caching. | — |
| [bot/services/antiphishing.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/antiphishing.py) | 🔄 Service Layer | 138 lines (4.2 KB) | Business logic service providing Antiphishing processing and caching. | — |
| [bot/services/cache.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/cache.py) | 🔄 In-Memory Cache | 53 lines (1.4 KB) | Async TTL cache store reducing database queries for frequently read guild configs. | — |
| [bot/services/captcha.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/captcha.py) | 🔄 Verification | 98 lines (3.4 KB) | Pillow-based CAPTCHA image generator and mathematical challenge verification engine. | — |
| [bot/services/embed.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/embed.py) | 🔄 Embed Builder | 66 lines (2.4 KB) | Standardized Discord embed builder enforcing brand styling and consistent design. | — |
| [bot/services/image.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/image.py) | 🔄 Image Processing | 107 lines (3.6 KB) | Avatar cropping, card backgrounds, and Pillow-based composite image rendering. | — |
| [bot/services/minecraft.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/minecraft.py) | 🔄 Service Layer | 125 lines (4.8 KB) | Business logic service providing Minecraft processing and caching. | — |
| [bot/services/moderation.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/moderation.py) | 🔄 Service Layer | 74 lines (2.9 KB) | Business logic service providing Moderation processing and caching. | — |
| [bot/services/onboarding_service.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/onboarding_service.py) | 🔄 Service Layer | 144 lines (5.3 KB) | Business logic service providing Onboarding Service processing and caching. | — |
| [bot/services/pagination.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/pagination.py) | 🔄 UI Paginator | 133 lines (5.0 KB) | Interactive Discord button paginator view for multi-page embeds with timeout handlers. | — |
| [bot/services/scheduler.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/scheduler.py) | 🔄 Task Scheduler | 53 lines (1.3 KB) | Asynchronous priority task queue for delayed actions, reminders, and unbans. | — |
| [bot/services/templates.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/templates.py) | 🔄 Service Layer | 406 lines (19.9 KB) | Business logic service providing Templates processing and caching. | — |
| [bot/services/welcome_card.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/welcome_card.py) | 🔄 Welcome Cards | 106 lines (3.7 KB) | Personalized welcome and rank image generator with user avatars and dynamic text. | — |
| [bot/services/youtube.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/youtube.py) | 🔄 Service Layer | 117 lines (4.9 KB) | Business logic service providing Youtube processing and caching. | — |

---

### 9. Background Workers & Daemons

9 asynchronous scheduled tasks executing periodic security checks, analytics rollups, reminder alerts, and YouTube monitors.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/workers/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/workers/__init__.py) | 🔄 Workers Package | 10 lines (454 B) | Initializes background worker daemon tasks. | — |
| [bot/workers/analytics_aggregator.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/workers/analytics_aggregator.py) | 🔄 Background Task | 69 lines (2.3 KB) | Continuous background task handling Analytics Aggregator checks on automated intervals. | — |
| [bot/workers/antinuke_watchdog.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/workers/antinuke_watchdog.py) | 🔄 Background Task | 74 lines (2.8 KB) | Continuous background task handling Antinuke Watchdog checks on automated intervals. | — |
| [bot/workers/giveaway_checker.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/workers/giveaway_checker.py) | 🔄 Background Task | 70 lines (2.8 KB) | Continuous background task handling Giveaway Checker checks on automated intervals. | — |
| [bot/workers/mc_status_updater.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/workers/mc_status_updater.py) | 🔄 Background Task | 79 lines (3.2 KB) | Continuous background task handling Mc Status Updater checks on automated intervals. | — |
| [bot/workers/onboarding_dispatcher.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/workers/onboarding_dispatcher.py) | 🔄 Background Task | 80 lines (2.7 KB) | Continuous background task handling Onboarding Dispatcher checks on automated intervals. | — |
| [bot/workers/reminder_dispatcher.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/workers/reminder_dispatcher.py) | 🔄 Background Task | 59 lines (2.1 KB) | Continuous background task handling Reminder Dispatcher checks on automated intervals. | — |
| [bot/workers/scheduled_messages.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/workers/scheduled_messages.py) | 🔄 Background Task | 26 lines (531 B) | Continuous background task handling Scheduled Messages checks on automated intervals. | — |
| [bot/workers/youtube_monitor.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/workers/youtube_monitor.py) | 🔄 Background Task | 63 lines (2.6 KB) | Continuous background task handling Youtube Monitor checks on automated intervals. | — |

---

### 10. Discord Extensions & Command Cogs

67 command modules organized across 31 feature categories providing user commands, slash commands, and event listeners.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/extensions/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/__init__.py) | 🔌 Extension Root | 1 lines (4 B) | Initializes the dynamic extension cog loader. | — |
| [bot/extensions/admin/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/admin/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Admin extension module. | — |
| [bot/extensions/admin/admin.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/admin/admin.py) | 🔌 Discord Cog | 172 lines (6.4 KB) | Discord commands and event listeners for Admin — Admin. | — |
| [bot/extensions/ai/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/ai/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Ai extension module. | — |
| [bot/extensions/ai/ai.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/ai/ai.py) | 🔌 Discord Cog | 122 lines (5.3 KB) | Discord commands and event listeners for Ai — Ai. | — |
| [bot/extensions/analytics/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/analytics/__init__.py) | 🔌 Cog Package | 4 lines (54 B) | Package initializer for the Analytics extension module. | — |
| [bot/extensions/analytics/analytics.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/analytics/analytics.py) | 🔌 Discord Cog | 204 lines (7.4 KB) | Discord commands and event listeners for Analytics — Analytics. | — |
| [bot/extensions/antinuke/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/antinuke/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Antinuke extension module. | — |
| [bot/extensions/antinuke/antinuke.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/antinuke/antinuke.py) | 🔌 Discord Cog | 266 lines (12.7 KB) | Discord commands and event listeners for Antinuke — Antinuke. | — |
| [bot/extensions/antiphishing/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/antiphishing/__init__.py) | 🔌 Cog Package | 4 lines (57 B) | Package initializer for the Antiphishing extension module. | — |
| [bot/extensions/antiphishing/antiphishing.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/antiphishing/antiphishing.py) | 🔌 Discord Cog | 190 lines (7.2 KB) | Discord commands and event listeners for Antiphishing — Antiphishing. | — |
| [bot/extensions/automation/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/automation/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Automation extension module. | — |
| [bot/extensions/automation/automation.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/automation/automation.py) | 🔌 Discord Cog | 111 lines (4.4 KB) | Discord commands and event listeners for Automation — Automation. | — |
| [bot/extensions/automod/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/automod/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Automod extension module. | — |
| [bot/extensions/automod/automod.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/automod/automod.py) | 🔌 Discord Cog | 312 lines (13.6 KB) | Discord commands and event listeners for Automod — Automod. | — |
| [bot/extensions/autoresponder/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/autoresponder/__init__.py) | 🔌 Cog Package | 4 lines (58 B) | Package initializer for the Autoresponder extension module. | — |
| [bot/extensions/autoresponder/autoresponder.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/autoresponder/autoresponder.py) | 🔌 Discord Cog | 221 lines (8.0 KB) | Discord commands and event listeners for Autoresponder — Autoresponder. | — |
| [bot/extensions/backup/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/backup/__init__.py) | 🔌 Cog Package | 4 lines (51 B) | Package initializer for the Backup extension module. | — |
| [bot/extensions/backup/backup.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/backup/backup.py) | 🔌 Discord Cog | 295 lines (11.7 KB) | Discord commands and event listeners for Backup — Backup. | — |
| [bot/extensions/community/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/community/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Community extension module. | — |
| [bot/extensions/community/community.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/community/community.py) | 🔌 Discord Cog | 213 lines (8.4 KB) | Discord commands and event listeners for Community — Community. | — |
| [bot/extensions/developer/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/developer/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Developer extension module. | — |
| [bot/extensions/developer/developer.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/developer/developer.py) | 🔌 Discord Cog | 122 lines (4.8 KB) | Discord commands and event listeners for Developer — Developer. | — |
| [bot/extensions/economy/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/economy/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Economy extension module. | — |
| [bot/extensions/economy/economy.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/economy/economy.py) | 🔌 Discord Cog | 188 lines (8.5 KB) | Discord commands and event listeners for Economy — Economy. | — |
| [bot/extensions/events/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/events/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Events extension module. | — |
| [bot/extensions/events/events.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/events/events.py) | 🔌 Discord Cog | 142 lines (5.9 KB) | Discord commands and event listeners for Events — Events. | — |
| [bot/extensions/fun/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/fun/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Fun extension module. | — |
| [bot/extensions/fun/fun.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/fun/fun.py) | 🔌 Discord Cog | 139 lines (5.8 KB) | Discord commands and event listeners for Fun — Fun. | — |
| [bot/extensions/games/blackjack_cog.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/games/blackjack_cog.py) | 🔌 Discord Cog | 47 lines (1.8 KB) | Discord commands and event listeners for Games — Blackjack Cog. | `BlackjackCog`, `__init__()` |
| [bot/extensions/games/hangman_cog.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/games/hangman_cog.py) | 🔌 Discord Cog | 59 lines (2.1 KB) | Discord commands and event listeners for Games — Hangman Cog. | `HangmanCog`, `__init__()`, `check()` |
| [bot/extensions/games/minesweeper_cog.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/games/minesweeper_cog.py) | 🔌 Discord Cog | 28 lines (923 B) | Discord commands and event listeners for Games — Minesweeper Cog. | `MinesweeperCog`, `__init__()` |
| [bot/extensions/games/slots_cog.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/games/slots_cog.py) | 🔌 Discord Cog | 66 lines (2.4 KB) | Discord commands and event listeners for Games — Slots Cog. | — |
| [bot/extensions/games/trivia_cog.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/games/trivia_cog.py) | 🔌 Discord Cog | 28 lines (958 B) | Discord commands and event listeners for Games — Trivia Cog. | `TriviaCog`, `__init__()` |
| [bot/extensions/games/uno_cog.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/games/uno_cog.py) | 🔌 Discord Cog | 29 lines (989 B) | Discord commands and event listeners for Games — Uno Cog. | `UnoCog`, `__init__()` |
| [bot/extensions/gaming/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/gaming/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Gaming extension module. | — |
| [bot/extensions/gaming/gaming.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/gaming/gaming.py) | 🔌 Discord Cog | 103 lines (3.9 KB) | Discord commands and event listeners for Gaming — Gaming. | — |
| [bot/extensions/leveling/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/leveling/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Leveling extension module. | — |
| [bot/extensions/leveling/leveling.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/leveling/leveling.py) | 🔌 Discord Cog | 136 lines (5.2 KB) | Discord commands and event listeners for Leveling — Leveling. | — |
| [bot/extensions/logging/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/logging/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Logging extension module. | — |
| [bot/extensions/logging/logging.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/logging/logging.py) | 🔌 Discord Cog | 152 lines (6.4 KB) | Discord commands and event listeners for Logging — Logging. | — |
| [bot/extensions/moderation/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/moderation/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Moderation extension module. | — |
| [bot/extensions/moderation/antialt.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/moderation/antialt.py) | 🔌 Discord Cog | 91 lines (4.4 KB) | Discord commands and event listeners for Moderation — Antialt. | `AntiAltCog`, `__init__()` |
| [bot/extensions/moderation/moderation.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/moderation/moderation.py) | 🔌 Discord Cog | 422 lines (20.2 KB) | Discord commands and event listeners for Moderation — Moderation. | — |
| [bot/extensions/moderation/nuke.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/moderation/nuke.py) | 🔌 Discord Cog | 298 lines (13.7 KB) | Discord commands and event listeners for Moderation — Nuke. | — |
| [bot/extensions/music/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/music/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Music extension module. | — |
| [bot/extensions/music/music.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/music/music.py) | 🔌 Discord Cog | 159 lines (5.7 KB) | Discord commands and event listeners for Music — Music. | — |
| [bot/extensions/onboarding/autodm.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/onboarding/autodm.py) | 🔌 Discord Cog | 100 lines (4.8 KB) | Discord commands and event listeners for Onboarding — Autodm. | `AutoDMCog`, `__init__()` |
| [bot/extensions/onboarding/autoping.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/onboarding/autoping.py) | 🔌 Discord Cog | 113 lines (5.7 KB) | Discord commands and event listeners for Onboarding — Autoping. | `AutoPingCog`, `__init__()` |
| [bot/extensions/onboarding/welcome_advanced.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/onboarding/welcome_advanced.py) | 🔌 Discord Cog | 186 lines (8.6 KB) | Discord commands and event listeners for Onboarding — Welcome Advanced. | — |
| [bot/extensions/productivity/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/productivity/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Productivity extension module. | — |
| [bot/extensions/productivity/productivity.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/productivity/productivity.py) | 🔌 Discord Cog | 118 lines (4.5 KB) | Discord commands and event listeners for Productivity — Productivity. | — |
| [bot/extensions/server/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/server/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Server extension module. | — |
| [bot/extensions/server/server.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/server/server.py) | 🔌 Discord Cog | 179 lines (7.4 KB) | Discord commands and event listeners for Server — Server. | — |
| [bot/extensions/shop/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/shop/__init__.py) | 🔌 Cog Package | 4 lines (49 B) | Package initializer for the Shop extension module. | — |
| [bot/extensions/shop/shop.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/shop/shop.py) | 🔌 Discord Cog | 244 lines (9.1 KB) | Discord commands and event listeners for Shop — Shop. | — |
| [bot/extensions/social/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/social/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Social extension module. | — |
| [bot/extensions/social/social.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/social/social.py) | 🔌 Discord Cog | 89 lines (3.5 KB) | Discord commands and event listeners for Social — Social. | — |
| [bot/extensions/templates/templates.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/templates/templates.py) | 🔌 Discord Cog | 250 lines (11.3 KB) | Discord commands and event listeners for Templates — Templates. | — |
| [bot/extensions/tickets/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/tickets/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Tickets extension module. | — |
| [bot/extensions/tickets/tickets.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/tickets/tickets.py) | 🔌 Discord Cog | 137 lines (5.8 KB) | Discord commands and event listeners for Tickets — Tickets. | — |
| [bot/extensions/utility/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/utility/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Utility extension module. | — |
| [bot/extensions/utility/utility.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/utility/utility.py) | 🔌 Discord Cog | 138 lines (6.6 KB) | Discord commands and event listeners for Utility — Utility. | — |
| [bot/extensions/verification/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/verification/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Verification extension module. | — |
| [bot/extensions/verification/verification.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/verification/verification.py) | 🔌 Discord Cog | 111 lines (5.0 KB) | Discord commands and event listeners for Verification — Verification. | — |
| [bot/extensions/youtube/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/youtube/__init__.py) | 🔌 Cog Package | 1 lines (4 B) | Package initializer for the Youtube extension module. | — |
| [bot/extensions/youtube/youtube.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/extensions/youtube/youtube.py) | 🔌 Discord Cog | 119 lines (4.5 KB) | Discord commands and event listeners for Youtube — Youtube. | — |

---

### 11. Game Engines & Mini-Game Logic

18 standalone turn-based and arcade game engines with state machines and rules enforcement.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/games/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/__init__.py) | 🎮 Game Core | 52 lines (1023 B) | Exports mini-game logic and scoring engines. | — |
| [bot/games/battleship.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/battleship.py) | 🎮 Game Engine | 420 lines (13.8 KB) | Core game engine, state machine, and rules validation for Battleship. | — |
| [bot/games/blackjack.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/blackjack.py) | 🎮 Game Engine | 208 lines (7.9 KB) | Core game engine, state machine, and rules validation for Blackjack. | `Card`, `BlackjackDeck`, `BlackjackGame` (+1 more) |
| [bot/games/chess_game.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/chess_game.py) | 🎮 Game Engine | 120 lines (4.1 KB) | Core game engine, state machine, and rules validation for Chess Game. | — |
| [bot/games/connect_four.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/connect_four.py) | 🎮 Game Engine | 184 lines (5.8 KB) | Core game engine, state machine, and rules validation for Connect Four. | — |
| [bot/games/country_guess.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/country_guess.py) | 🎮 Game Engine | 215 lines (6.8 KB) | Core game engine, state machine, and rules validation for Country Guess. | — |
| [bot/games/hangman.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/hangman.py) | 🎮 Game Engine | 182 lines (5.2 KB) | Core game engine, state machine, and rules validation for Hangman. | — |
| [bot/games/minesweeper.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/minesweeper.py) | 🎮 Game Engine | 195 lines (7.3 KB) | Core game engine, state machine, and rules validation for Minesweeper. | — |
| [bot/games/reaction_test.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/reaction_test.py) | 🎮 Game Engine | 65 lines (1.8 KB) | Core game engine, state machine, and rules validation for Reaction Test. | — |
| [bot/games/rps.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/rps.py) | 🎮 Game Engine | 78 lines (2.4 KB) | Core game engine, state machine, and rules validation for Rps. | — |
| [bot/games/slots.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/slots.py) | 🎮 Game Engine | 43 lines (1.4 KB) | Core game engine, state machine, and rules validation for Slots. | `SpinResult`, `SlotMachine`, `spin()` |
| [bot/games/tictactoe.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/tictactoe.py) | 🎮 Game Engine | 165 lines (5.0 KB) | Core game engine, state machine, and rules validation for Tictactoe. | — |
| [bot/games/trivia.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/trivia.py) | 🎮 Game Engine | 112 lines (8.1 KB) | Core game engine, state machine, and rules validation for Trivia. | — |
| [bot/games/twenty_48.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/twenty_48.py) | 🎮 Game Engine | 325 lines (10.1 KB) | Core game engine, state machine, and rules validation for Twenty 48. | — |
| [bot/games/typeracer.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/typeracer.py) | 🎮 Game Engine | 193 lines (6.0 KB) | Core game engine, state machine, and rules validation for Typeracer. | — |
| [bot/games/uno.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/uno.py) | 🎮 Game Engine | 252 lines (8.8 KB) | Core game engine, state machine, and rules validation for Uno. | — |
| [bot/games/utils.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/utils.py) | 🎮 Game Utilities | 125 lines (3.0 KB) | Shared game utilities, board formatting, dice rolls, and deck generation. | — |
| [bot/games/wordle.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/wordle.py) | 🎮 Game Engine | 163 lines (5.1 KB) | Core game engine, state machine, and rules validation for Wordle. | — |

---

### 12. Interactive Discord Button Game Controllers

13 interactive Discord.ui.View button interfaces for multiplayer and singleplayer Discord games.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/games/button_games/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/__init__.py) | 🎮 UI View Package | 34 lines (856 B) | Exports Discord interactive button game views. | — |
| [bot/games/button_games/battleship_buttons.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/battleship_buttons.py) | 🎮 Button Game View | 482 lines (15.1 KB) | Interactive Discord.ui.View button controller for Battleship. | — |
| [bot/games/button_games/chess_buttons.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/chess_buttons.py) | 🎮 Button Game View | 121 lines (3.6 KB) | Interactive Discord.ui.View button controller for Chess. | — |
| [bot/games/button_games/connect_four_buttons.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/connect_four_buttons.py) | 🎮 Button Game View | 92 lines (2.5 KB) | Interactive Discord.ui.View button controller for Connect Four. | — |
| [bot/games/button_games/country_guess_buttons.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/country_guess_buttons.py) | 🎮 Button Game View | 145 lines (4.8 KB) | Interactive Discord.ui.View button controller for Country Guess. | — |
| [bot/games/button_games/lights_out.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/lights_out.py) | 🎮 Button Game View | 147 lines (4.1 KB) | Interactive Discord.ui.View button controller for Lights Out. | — |
| [bot/games/button_games/memory_game.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/memory_game.py) | 🎮 Button Game View | 156 lines (4.2 KB) | Interactive Discord.ui.View button controller for Memory Game. | — |
| [bot/games/button_games/number_slider.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/number_slider.py) | 🎮 Button Game View | 173 lines (4.9 KB) | Interactive Discord.ui.View button controller for Number Slider. | — |
| [bot/games/button_games/reaction_test_buttons.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/reaction_test_buttons.py) | 🎮 Button Game View | 105 lines (3.1 KB) | Interactive Discord.ui.View button controller for Reaction Test. | — |
| [bot/games/button_games/rps_buttons.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/rps_buttons.py) | 🎮 Button Game View | 153 lines (5.4 KB) | Interactive Discord.ui.View button controller for Rps. | — |
| [bot/games/button_games/tictactoe_buttons.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/tictactoe_buttons.py) | 🎮 Button Game View | 105 lines (3.1 KB) | Interactive Discord.ui.View button controller for Tictactoe. | — |
| [bot/games/button_games/twenty_48_buttons.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/twenty_48_buttons.py) | 🎮 Button Game View | 114 lines (3.2 KB) | Interactive Discord.ui.View button controller for Twenty 48. | — |
| [bot/games/button_games/wordle_buttons.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/button_games/wordle_buttons.py) | 🎮 Button Game View | 120 lines (3.7 KB) | Interactive Discord.ui.View button controller for Wordle. | — |

---

### 13. Automated Unit & Integration Test Suites

23 Pytest test suites ensuring code correctness, permission integrity, database consistency, and API security.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [bot/tests/__init__.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/__init__.py) | 🧪 Test Suite Root | 1 lines (4 B) | Initializes the pytest test directory. | — |
| [bot/tests/test_ai_service.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_ai_service.py) | 🧪 Unit Test Suite | 24 lines (564 B) | Comprehensive unit test suite for Ai Service. | — |
| [bot/tests/test_analytics.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_analytics.py) | 🧪 Unit Test Suite | 32 lines (939 B) | Comprehensive unit test suite for Analytics. | — |
| [bot/tests/test_antialt.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_antialt.py) | 🧪 Unit Test Suite | 18 lines (538 B) | Comprehensive unit test suite for Antialt. | `TestSlotsAndAntiAlt`, `test_slots_spin()` |
| [bot/tests/test_antinuke.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_antinuke.py) | 🧪 Unit Test Suite | 52 lines (1.5 KB) | Comprehensive unit test suite for Antinuke. | `DummyDB`, `DummyBot`, `TestAntiNuke` |
| [bot/tests/test_antiphishing.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_antiphishing.py) | 🧪 Unit Test Suite | 39 lines (1.4 KB) | Comprehensive unit test suite for Antiphishing. | — |
| [bot/tests/test_api.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_api.py) | 🧪 Unit Test Suite | 24 lines (582 B) | Comprehensive unit test suite for Api. | — |
| [bot/tests/test_autoresponder.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_autoresponder.py) | 🧪 Unit Test Suite | 38 lines (1.1 KB) | Comprehensive unit test suite for Autoresponder. | — |
| [bot/tests/test_backup.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_backup.py) | 🧪 Unit Test Suite | 42 lines (1.6 KB) | Comprehensive unit test suite for Backup. | — |
| [bot/tests/test_cache.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_cache.py) | 🧪 Unit Test Suite | 34 lines (849 B) | Comprehensive unit test suite for Cache. | — |
| [bot/tests/test_config.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_config.py) | 🧪 Unit Test Suite | 25 lines (774 B) | Comprehensive unit test suite for Config. | — |
| [bot/tests/test_database.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_database.py) | 🧪 Unit Test Suite | 29 lines (719 B) | Comprehensive unit test suite for Database. | — |
| [bot/tests/test_games_suite.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_games_suite.py) | 🧪 Unit Test Suite | 74 lines (2.6 KB) | Comprehensive unit test suite for Games Suite. | `TestGamesSuite`, `test_minesweeper_init()`, `test_minesweeper_flag_toggle()` (+4 more) |
| [bot/tests/test_moderation.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_moderation.py) | 🧪 Unit Test Suite | 36 lines (771 B) | Comprehensive unit test suite for Moderation. | — |
| [bot/tests/test_new_workers.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_new_workers.py) | 🧪 Unit Test Suite | 24 lines (706 B) | Comprehensive unit test suite for New Workers. | `DummyBot`, `TestNewWorkers`, `test_onboarding_dispatcher_queue()` |
| [bot/tests/test_onboarding.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_onboarding.py) | 🧪 Unit Test Suite | 48 lines (1.5 KB) | Comprehensive unit test suite for Onboarding. | — |
| [bot/tests/test_permissions.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_permissions.py) | 🧪 Unit Test Suite | 50 lines (1.2 KB) | Comprehensive unit test suite for Permissions. | — |
| [bot/tests/test_shop.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_shop.py) | 🧪 Unit Test Suite | 37 lines (1012 B) | Comprehensive unit test suite for Shop. | — |
| [bot/tests/test_templates.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_templates.py) | 🧪 Unit Test Suite | 43 lines (1.6 KB) | Comprehensive unit test suite for Templates. | `TestTemplates`, `test_public_templates_exist()`, `test_public_template_structure()` (+1 more) |
| [bot/tests/test_uno.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_uno.py) | 🧪 Unit Test Suite | 42 lines (1.2 KB) | Comprehensive unit test suite for Uno. | `DummyUser`, `TestUno`, `__init__()` (+3 more) |
| [bot/tests/test_verification.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_verification.py) | 🧪 Unit Test Suite | 26 lines (824 B) | Comprehensive unit test suite for Verification. | — |
| [bot/tests/test_welcome_card.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_welcome_card.py) | 🧪 Unit Test Suite | 22 lines (608 B) | Comprehensive unit test suite for Welcome Card. | — |
| [bot/tests/test_workers.py](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/tests/test_workers.py) | 🧪 Unit Test Suite | 40 lines (1.3 KB) | Comprehensive unit test suite for Workers. | — |

---

### 14. Dashboard Configuration & Build Manifests

Next.js 14, Tailwind CSS, TypeScript, and PostCSS configuration files and package manifests.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [dashboard/.env.example](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/.env.example) | ⚙️ Env Template | 14 lines (461 B) | Environment variables template for Next.js dashboard client and API base URL. | — |
| [dashboard/.env.local](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/.env.local) | ⚙️ Local Env | 15 lines (384 B) | Local development environment variables for dashboard development. | — |
| [dashboard/.eslintrc.json](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/.eslintrc.json) | 🟢 Active | 3 lines (40 B) | Source module. | — |
| [dashboard/LICENSE](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/LICENSE) | 📖 Legal | 21 lines (1.0 KB) | MIT open-source license documentation. | — |
| [dashboard/README.md](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/README.md) | 📖 Documentation | 80 lines (3.8 KB) | Frontend documentation covering development commands and component hierarchy. | — |
| [dashboard/next-env.d.ts](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/next-env.d.ts) | 🟢 Active | 5 lines (201 B) | <reference types="next" /> | — |
| [dashboard/next.config.mjs](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/next.config.mjs) | ⚙️ Next.js Config | 14 lines (208 B) | Next.js compiler settings, image domain whitelists, and environment proxies. | — |
| [dashboard/package-lock.json](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/package-lock.json) | 🟢 Active | 6494 lines (222.0 KB) | Source module. | — |
| [dashboard/package.json](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/package.json) | ⚙️ NPM Manifest | 34 lines (797 B) | Dashboard Node.js dependencies, build scripts (dev, build, lint), and metadata. | — |
| [dashboard/postcss.config.mjs](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/postcss.config.mjs) | 🟢 Active | 8 lines (84 B) | Source module. | — |
| [dashboard/tailwind.config.ts](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/tailwind.config.ts) | ⚙️ Tailwind Config | 49 lines (1.1 KB) | Tailwind CSS theme extensions, brand purple palette, animations, and container styles. | — |
| [dashboard/tsconfig.json](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/tsconfig.json) | ⚙️ TypeScript Config | 43 lines (740 B) | TypeScript compiler options, strict type checking, and path aliases. | — |
| [dashboard/tsconfig.tsbuildinfo](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/tsconfig.tsbuildinfo) | 🟢 Active | 88.5 KB | Source module. | — |

---

### 15. Dashboard Pages, Routes & Root Layouts

Next.js App Router root layout, landing page, and top-level server selector pages.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [dashboard/app/dashboard/layout.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/layout.tsx) | 💻 Dashboard Layout | 15 lines (354 B) | Main authenticated dashboard layout with persistent sidebar and navbar. | — |
| [dashboard/app/dashboard/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/page.tsx) | 💻 Dashboard Page | 72 lines (5.0 KB) | Server selector page listing user guilds where the bot is installed. | — |
| [dashboard/app/globals.css](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/globals.css) | 🎨 Stylesheet | 75 lines (1.5 KB) | Tailwind CSS imports, custom scrollbar styling, and color variable tokens. | — |
| [dashboard/app/layout.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/layout.tsx) | 💻 Root Layout | 22 lines (567 B) | Next.js root HTML layout wrapping font definitions, theme providers, and metadata. | — |
| [dashboard/app/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/page.tsx) | 💻 Landing Page | 57 lines (3.8 KB) | Public landing page showcasing Wutherer features, statistics, and invite button. | — |

---

### 16. Guild Management Dashboard Modules

19 guild-level configuration pages for server moderation, antinuke, automod, leveling, tickets, AI, and verification.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [dashboard/app/dashboard/guild/[guildId]/ai/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/ai/page.tsx) | 💻 Module Config Page | 116 lines (3.8 KB) | Interactive configuration UI for Ai module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/analytics/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/analytics/page.tsx) | 💻 Module Config Page | 127 lines (5.2 KB) | Interactive configuration UI for Analytics module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/antinuke/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/antinuke/page.tsx) | 💻 Module Config Page | 293 lines (10.6 KB) | Interactive configuration UI for Antinuke module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/automation/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/automation/page.tsx) | 💻 Module Config Page | 156 lines (5.5 KB) | Interactive configuration UI for Automation module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/automod/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/automod/page.tsx) | 💻 Module Config Page | 127 lines (4.7 KB) | Interactive configuration UI for Automod module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/autoresponder/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/autoresponder/page.tsx) | 💻 Module Config Page | 150 lines (5.8 KB) | Interactive configuration UI for Autoresponder module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/backup/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/backup/page.tsx) | 💻 Module Config Page | 132 lines (4.9 KB) | Interactive configuration UI for Backup module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/economy/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/economy/page.tsx) | 💻 Module Config Page | 175 lines (5.6 KB) | Interactive configuration UI for Economy module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/layout.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/layout.tsx) | 💻 Dashboard Layout | 22 lines (568 B) | Guild-specific dashboard layout with guild context provider and sub-navigation. | — |
| [dashboard/app/dashboard/guild/[guildId]/leveling/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/leveling/page.tsx) | 💻 Module Config Page | 112 lines (3.8 KB) | Interactive configuration UI for Leveling module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/minecraft/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/minecraft/page.tsx) | 💻 Module Config Page | 177 lines (6.5 KB) | Interactive configuration UI for Minecraft module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/moderation/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/moderation/page.tsx) | 💻 Module Config Page | 95 lines (3.5 KB) | Interactive configuration UI for Moderation module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/onboarding/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/onboarding/page.tsx) | 💻 Module Config Page | 273 lines (11.2 KB) | Interactive configuration UI for Onboarding module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/page.tsx) | 💻 Dashboard Page | 7 lines (166 B) | Guild management overview page with quick metrics, server health, and module toggles. | — |
| [dashboard/app/dashboard/guild/[guildId]/settings/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/settings/page.tsx) | 💻 Module Config Page | 88 lines (2.8 KB) | Interactive configuration UI for Settings module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/templates/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/templates/page.tsx) | 💻 Module Config Page | 213 lines (8.1 KB) | Interactive configuration UI for Templates module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/tickets/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/tickets/page.tsx) | 💻 Module Config Page | 116 lines (3.8 KB) | Interactive configuration UI for Tickets module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/verification/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/verification/page.tsx) | 💻 Module Config Page | 100 lines (3.4 KB) | Interactive configuration UI for Verification module settings. | — |
| [dashboard/app/dashboard/guild/[guildId]/youtube/page.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/app/dashboard/guild/[guildId]/youtube/page.tsx) | 💻 Module Config Page | 180 lines (6.5 KB) | Interactive configuration UI for Youtube module settings. | — |

---

### 17. React UI Components & Design System

17 reusable UI primitives and dashboard layout elements built with Radix and Tailwind CSS.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [dashboard/components/dashboard/antinuke-control.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/dashboard/antinuke-control.tsx) | 🧩 Feature Component | 101 lines (9.6 KB) | Dashboard interface component: Antinuke Control. | — |
| [dashboard/components/dashboard/dashboard-header.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/dashboard/dashboard-header.tsx) | 🧩 Feature Component | 50 lines (2.2 KB) | Dashboard interface component: Dashboard Header. | — |
| [dashboard/components/dashboard/navbar.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/dashboard/navbar.tsx) | 🧩 Feature Component | 43 lines (1.9 KB) | Dashboard interface component: Navbar. | — |
| [dashboard/components/dashboard/server-overview.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/dashboard/server-overview.tsx) | 🧩 Feature Component | 101 lines (8.1 KB) | Dashboard interface component: Server Overview. | — |
| [dashboard/components/dashboard/sidebar.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/dashboard/sidebar.tsx) | 🧩 Feature Component | 149 lines (5.4 KB) | Dashboard interface component: Sidebar. | — |
| [dashboard/components/landing/product-preview.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/landing/product-preview.tsx) | 🧩 Landing Component | 90 lines (3.8 KB) | Landing page interactive product preview and live demonstration mockup. | — |
| [dashboard/components/ui/alert.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/ui/alert.tsx) | 🧩 UI Primitive | 58 lines (1.4 KB) | Reusable shadcn/Radix-inspired UI component for `alert`. | — |
| [dashboard/components/ui/badge.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/ui/badge.tsx) | 🧩 UI Primitive | 31 lines (845 B) | Reusable shadcn/Radix-inspired UI component for `badge`. | — |
| [dashboard/components/ui/button.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/ui/button.tsx) | 🧩 UI Primitive | 37 lines (1.4 KB) | Reusable shadcn/Radix-inspired UI component for `button`. | — |
| [dashboard/components/ui/card.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/ui/card.tsx) | 🧩 UI Primitive | 52 lines (1.1 KB) | Reusable shadcn/Radix-inspired UI component for `card`. | — |
| [dashboard/components/ui/empty-state.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/ui/empty-state.tsx) | 🧩 UI Primitive | 38 lines (1002 B) | Reusable shadcn/Radix-inspired UI component for `empty-state`. | — |
| [dashboard/components/ui/input.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/ui/input.tsx) | 🧩 UI Primitive | 21 lines (689 B) | Reusable shadcn/Radix-inspired UI component for `input`. | — |
| [dashboard/components/ui/label.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/ui/label.tsx) | 🧩 UI Primitive | 21 lines (477 B) | Reusable shadcn/Radix-inspired UI component for `label`. | — |
| [dashboard/components/ui/section-header.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/ui/section-header.tsx) | 🧩 UI Primitive | 31 lines (777 B) | Reusable shadcn/Radix-inspired UI component for `section-header`. | — |
| [dashboard/components/ui/select.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/ui/select.tsx) | 🧩 UI Primitive | 23 lines (702 B) | Reusable shadcn/Radix-inspired UI component for `select`. | — |
| [dashboard/components/ui/switch.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/ui/switch.tsx) | 🧩 UI Primitive | 36 lines (1.2 KB) | Reusable shadcn/Radix-inspired UI component for `switch`. | — |
| [dashboard/components/ui/textarea.tsx](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/components/ui/textarea.tsx) | 🧩 UI Primitive | 21 lines (703 B) | Reusable shadcn/Radix-inspired UI component for `textarea`. | — |

---

### 18. Dashboard Client Libraries & Type Declarations

Typed REST API client, utility functions, and TypeScript interface declarations.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [dashboard/lib/api.ts](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/lib/api.ts) | 💻 API Client | 128 lines (6.5 KB) | Typed fetch client making authenticated requests to the FastAPI bot backend. | — |
| [dashboard/lib/utils.ts](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/lib/utils.ts) | 💻 UI Utilities | 7 lines (170 B) | Class name merging utility (`cn` with clsx and tailwind-merge). | — |
| [dashboard/types/ambient.d.ts](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/types/ambient.d.ts) | 💻 Type Definitions | 264 lines (7.0 KB) | TypeScript interface definitions for API responses, guilds, user state, and configs. | — |
| [dashboard/types/index.ts](file:///c:/Users/Aadyant/Downloads/Wutherer/dashboard/types/index.ts) | 💻 Type Definitions | 120 lines (2.2 KB) | TypeScript interface definitions for API responses, guilds, user state, and configs. | — |

---

### 19. Technical Architecture Documentation

11 comprehensive Markdown specifications covering bot defense, worker schedules, REST API specs, and onboarding flows.

| File Path | State | Lines / Size | Purpose & Role | Key Symbols / Exports |
| :--- | :--- | :--- | :--- | :--- |
| [docs/ANTIALT.md](file:///c:/Users/Aadyant/Downloads/Wutherer/docs/ANTIALT.md) | 📖 Technical Guide | 33 lines (1.6 KB) | Technical documentation and architectural specification for Antialt. | — |
| [docs/API.md](file:///c:/Users/Aadyant/Downloads/Wutherer/docs/API.md) | 📖 Technical Guide | 179 lines (4.4 KB) | Technical documentation and architectural specification for Api. | — |
| [docs/ARCHITECTURE.md](file:///c:/Users/Aadyant/Downloads/Wutherer/docs/ARCHITECTURE.md) | 📖 Technical Guide | 102 lines (8.7 KB) | Technical documentation and architectural specification for Architecture. | — |
| [docs/CASINO.md](file:///c:/Users/Aadyant/Downloads/Wutherer/docs/CASINO.md) | 📖 Technical Guide | 52 lines (2.3 KB) | Technical documentation and architectural specification for Casino. | — |
| [docs/COMMANDS.md](file:///c:/Users/Aadyant/Downloads/Wutherer/docs/COMMANDS.md) | 📖 Technical Guide | 174 lines (10.2 KB) | Technical documentation and architectural specification for Commands. | — |
| [docs/DEFENSE.md](file:///c:/Users/Aadyant/Downloads/Wutherer/docs/DEFENSE.md) | 📖 Technical Guide | 48 lines (2.9 KB) | Technical documentation and architectural specification for Defense. | — |
| [docs/MODULES.md](file:///c:/Users/Aadyant/Downloads/Wutherer/docs/MODULES.md) | 📖 Technical Guide | 131 lines (6.6 KB) | Technical documentation and architectural specification for Modules. | — |
| [docs/ONBOARDING.md](file:///c:/Users/Aadyant/Downloads/Wutherer/docs/ONBOARDING.md) | 📖 Technical Guide | 60 lines (3.6 KB) | Technical documentation and architectural specification for Onboarding. | — |
| [docs/SETUP.md](file:///c:/Users/Aadyant/Downloads/Wutherer/docs/SETUP.md) | 📖 Technical Guide | 135 lines (3.5 KB) | Technical documentation and architectural specification for Setup. | — |
| [docs/TEMPLATES.md](file:///c:/Users/Aadyant/Downloads/Wutherer/docs/TEMPLATES.md) | 📖 Technical Guide | 72 lines (3.1 KB) | Technical documentation and architectural specification for Templates. | — |
| [docs/WORKERS.md](file:///c:/Users/Aadyant/Downloads/Wutherer/docs/WORKERS.md) | 📖 Technical Guide | 43 lines (2.0 KB) | Technical documentation and architectural specification for Workers. | — |

---

### 20. Graphical Media, Fonts & Static Assets

506 static assets including country flags, outline maps, game sprites, fonts, and card templates.

This asset directory contains **506 total binary and data files** supporting Discord games, welcome cards, and canvas graphics:

- **Country Flags Directory** (`bot/games/assets/country-flags/`): `253 PNG flags` indexed by country name, rendered by [`bot/games/country_guess.py`](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/country_guess.py).
- **Country Map Silhouettes** (`bot/games/assets/country-data/`): `231 PNG map outlines` used in geography and trivia challenge games.
- **2048 Emoji Preview Sprites** (`bot/games/assets/2048-emoji-asset-examples/`): `14 PNG previews` for the 2048 puzzle tile theme options.
- **Typography Fonts & Dictionaries**: Segoe UI Semilight font (`.ttf`) and English dictionary (`words.txt`) for Wordle and Hangman.
- **Welcome Card Templates**: Custom card backgrounds in `bot/assets/` rendered by [`bot/services/welcome_card.py`](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/services/welcome_card.py).

| Primary Asset Directory / File | Type | Count / Size | Usage Context |
| :--- | :--- | :--- | :--- |
| [`bot/games/assets/country-flags/`](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/assets/country-flags) | PNG Images | 253 files (3.31 MB) | Displayed in Flag Guessing Discord mini-game |
| [`bot/games/assets/country-data/`](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/assets/country-data) | PNG Maps | 231 files (5.09 MB) | Country silhouette quiz games |
| [`bot/games/assets/2048-emoji-asset-examples/`](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/assets/2048-emoji-asset-examples) | PNG Sprites | 14 files (260.7 KB) | 2048 button game emoji tile themes |
| [`bot/games/assets/words.txt`](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/assets/words.txt) | Wordlist | 75.9 KB | Wordle and Hangman secret word dictionary |
| [`bot/games/assets/segoe-ui-semilight-411.ttf`](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/games/assets/segoe-ui-semilight-411.ttf) | TTF Font | 783.9 KB | TrueType font rendering for Pillow canvas games |
| [`bot/assets/welcome_card.png`](file:///c:/Users/Aadyant/Downloads/Wutherer/bot/assets/welcome_card.png) | PNG Canvas | 0 B | Welcome banner background template |

---

## Summary Statistics

- **Total Files**: `793`
- **Total Python Code**: `210 files` (`33,400+ lines`)
- **Total Dashboard React/TSX Code**: `40 files` (`5,400+ lines`)
- **Total Documentation**: `15 markdown files` (`4,500+ lines`)
- **Total Interactive Mini-Games**: `23 full games`
- **Total Database Models**: `26 schema repositories`
- **Total API Route Controllers**: `20 REST modules`
- **Total Pytest Unit Tests**: `23 test suites`
- **Total Media Assets**: `506 static assets`

---
*Generated automatically for repository branch `docs/file-tree`.*