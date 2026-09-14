# Wutherer Architecture & Modular Extensions Reference

This document provides a comprehensive technical breakdown of all 26 extension modules, background daemons, data access models, and service integrations comprising the **Wutherer Discord Platform**.

---

## 1. Core Architecture

```
Wutherer Platform
├── bot/
│   ├── core/                  # Bot framework, context, permissions, error dispatch
│   ├── database/              # SQLite WAL connection pool & 24 DAO models
│   ├── services/              # Gemini AI, YouTube, Minecraft, CAPTCHA, Welcome Card, AntiPhishing
│   ├── extensions/            # 26 modular command extensions
│   ├── workers/               # 5 background daemons
│   └── api/                   # FastAPI REST control daemon
└── dashboard/                 # Next.js 14 Web Control Panel (Tailwind CSS, Glassmorphic UI)
```

---

## 2. Command Extensions Directory

### 1. Moderation (`bot/extensions/moderation/`)
- Disciplinary actions: `ban`, `unban`, `kick`, `softban`, `warn`, `timeout`, `purge`, `lock`, `unlock`, `slowmode`, `nuke`.
- Persistent infractions: Stores cases in `mod_cases` and `warnings` tables.
- DM notifications: Automatically sends DM explanations to moderated users.

### 2. Automod (`bot/extensions/automod/`)
- Content inspection engine filtering chat messages in real time.
- Heuristics: Anti-spam velocity, anti-invite link scanner, emoji flooding, mass mentions, and all-caps filtering.

### 3. Antinuke (`bot/extensions/antinuke/`)
- Sub-second anti-raid defense monitoring 14 Discord audit events.
- Intercepts unauthorized mass channel deletion, mass role deletion, bot additions, and mass bans.
- Automatically quarantines offenders, strips roles, and restores state.

### 4. Server (`bot/extensions/server/`)
- Prefix customization, autoroles (human/bot), reaction roles, and welcome/leave alerts.
- Includes `s!welcome testcard` for generating dynamic Pillow-based glassmorphic welcome cards.

### 5. Tickets (`bot/extensions/tickets/`)
- Discord persistent button UI panels for user support.
- Creates private ticket channels under dedicated categories with staff claiming and transcript generation.

### 6. Verification (`bot/extensions/verification/`)
- Anti-raid gatekeeper utilizing PIL-rendered distorted visual CAPTCHAs and mathematical challenges.
- Assigns verified role upon successful modal submission.

### 7. Leveling (`bot/extensions/leveling/`)
- Text and voice XP progression with configurable multipliers and cooldown buckets.
- Dynamic rank card image generation, server leaderboards, and automated level rewards.

### 8. Logging (`bot/extensions/logging/`)
- Comprehensive audit trails: Message edits, message deletions, member joins/leaves, role modifications, and voice activity.

### 9. AI (`bot/extensions/ai/`)
- Google Gemini multi-turn conversational AI chat.
- Text summarization, code explanation, translation, rewriting, and configurable guild system personas.

### 10. YouTube (`bot/extensions/youtube/`)
- YouTube Data API v3 integration for channel subscriber metrics, latest upload notifications, and video searches.

### 11. Gaming (`bot/extensions/gaming/`)
- Minecraft server status inspection (online player counts, MOTD, latency), Mojang UUID lookups, and 3D player skin renders.

### 12. Economy (`bot/extensions/economy/`)
- Virtual currency system (`wallet`, `bank`), daily rewards (`s!daily`), work shifts (`s!work`), coinflips, and bank transfers.

### 13. Economy Shop (`bot/extensions/shop/`)
- Server store enabling buyable Discord roles, custom perks, and inventory items (`s!shop`, `s!buy`, `s!inventory`, `s!gift`).

### 14. Community (`bot/extensions/community/`)
- Timed giveaways with automatic reaction tracking, voting polls, suggestions with staff review, and starboard.

### 15. Server Backups (`bot/extensions/backup/`)
- Encrypted JSON snapshots of server topology (roles, channels, categories, permission overwrites, emojis).
- Commands: `s!backup create`, `s!backup restore`, `s!backup download`, `s!backup list`.

### 16. Server Analytics (`bot/extensions/analytics/`)
- Chat velocity telemetry, 24-hour ASCII engagement heatmaps, top channel rankings, and demographic health audits.

### 17. Auto-Responder (`bot/extensions/autoresponder/`)
- Automated keyword and regex triggers with wildcard matching, embed responses, cooldowns, and variable substitutions.

### 18. Anti-Phishing (`bot/extensions/antiphishing/`)
- Heuristic scam link defense detecting typosquatting lookalikes, token loggers, and malicious promo campaigns.

### 19. Fun (`bot/extensions/fun/`)
- Interactive Discord mini-games: Wordle, 2048, TicTacToe, Connect Four, Rock Paper Scissors, Chess, Typeracer.

### 20. Music (`bot/extensions/music/`)
- Voice channel streaming, audio queue management, track skipping, and volume equalization.

### 21. Productivity (`bot/extensions/productivity/`)
- Timed reminders, countdown alerts, mathematical expression evaluator, and unit converter.

### 22. Social (`bot/extensions/social/`)
- AFK statuses with auto-reply mentions, user profiles, reputation karma, and custom biographies.

### 23. Developer (`bot/extensions/developer/`)
- JSON formatting, regex testing, Base64 encoder/decoder, cryptographic hashing (SHA256, MD5), and Discord timestamps.

### 24. Utility (`bot/extensions/utility/`)
- Server info, user info, avatar/banner inspect, bot latency ping, and platform system statistics.

### 25. Admin (`bot/extensions/admin/`)
- Dynamic extension reload/unload, slash command synchronization, safe eval, and cross-server announcements.

### 26. Events (`bot/extensions/events/`)
- Centralized Discord gateway event listener handling error dispatch, guild join handshakes, and command completion hooks.

---

## 3. Background Daemons (`bot/workers/`)

1. **`YouTubeMonitorWorker`**: Periodically polls YouTube channels and dispatches video announcement alerts.
2. **`GiveawayCheckerWorker`**: Checks giveaway end timestamps and randomly draws verified winners.
3. **`ReminderDispatcherWorker`**: Dispatches due reminders to users via DM or channel alerts.
4. **`MinecraftStatusUpdaterWorker`**: Keeps live server status display embeds updated.
5. **`AnalyticsAggregatorWorker`**: Aggregates active voice minutes and engagement telemetry into hourly rollups.

---

## 4. Database Storage Engine

All data is managed through an asynchronous SQLite engine using **Write-Ahead Logging (WAL)**:
- Connection pool with query timeouts and concurrent read scalability.
- Self-healing migration system (`bot/database/migrations.py`) running automatically on startup.
- Indexed relational tables for sub-millisecond lookups across all guild operations.
