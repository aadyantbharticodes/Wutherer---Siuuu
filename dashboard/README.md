# Wutherer Web Console — Next.js 14 Dashboard

### Modern Next.js 14 web console with dark-mode glassmorphism, Discord OAuth2 authentication, real-time Gemini AI sandbox, YouTube creator alerts, and Minecraft server monitors.

---

## ✦ Features

- **Discord NextAuth Integration**: Single-sign-on using Discord OAuth2 with permission validation (`MANAGE_GUILD` or `ADMINISTRATOR`).
- **Google Gemini AI Hub**: Real-time prompt sandbox, custom persona prompt editor, memory depth adjustment, and user memory wipe tool.
- **YouTube Creator Center**: Live creator search via YouTube Data API v3, custom `{channel}`, `{title}`, `{url}` message templates, and target role pings.
- **Minecraft Server Tracking**: Java & Bedrock auto-refreshing Discord status embeds, live server query ping utility, and 3D player skin renders.
- **Disciplinary Audit Console**: Real-time cases browser with action filters (BAN, KICK, TIMEOUT, WARN), search, and warning pardon actions.
- **16 Server Management Modules**: Full controls for Welcome, Antinuke, Automod, Tickets, Leveling, Verification, Reaction Roles, and more.

---

## ✦ Directory Structure

```
dashboard/
├── app/                       Next.js 14 App Router
│   ├── api/auth/              NextAuth Discord provider endpoints
│   ├── dashboard/             Authenticated console
│   │   ├── admin/             Global bot administration & node status
│   │   ├── guilds/            Server selection grid
│   │   └── guild/[guildId]/   Guild management modules
│   │       ├── ai/            Google Gemini AI persona & testing sandbox
│   │       ├── youtube/       YouTube channel alerts manager
│   │       ├── minecraft/     Minecraft server status & player lookup
│   │       ├── moderation/    Disciplinary cases & warning registry
│   │       ├── antinuke/      Anti-raid and server lockdown rules
│   │       ├── automod/       Spam, links, and caps filter controls
│   │       ├── tickets/       Persistent button ticket panels
│   │       ├── verification/  Image CAPTCHA & button gate configuration
│   │       ├── leveling/      XP curves and rank card settings
│   │       ├── welcome/       Cinematic join/leave cards & embeds
│   │       └── settings/      Custom command prefix
│   ├── layout.tsx             Root layout with Inter & Outfit fonts
│   └── page.tsx               Cinematic landing page with feature matrix
│
├── components/                Component Library
│   ├── dashboard/             Module forms (ai-form, youtube-form, minecraft-form, moderation-logs...)
│   └── ui/                    Radix UI primitives & styled controls
│
├── lib/                       Client Logic
│   ├── api.ts                 REST client with Bearer authentication
│   ├── auth.ts                NextAuth session & callbacks
│   └── utils.ts               Tailwind styling & admin checkers
│
└── types/                     TypeScript Definitions
    └── api.ts                 Strongly typed schemas matching bot FastAPI models
```

---

## ✦ Development Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_DASHBOARD_API_KEY=nexus_dashboard_api_secret_key_8492049182
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=nexus_nextauth_secure_random_key_9938210482_2026
DISCORD_CLIENT_ID=1547928923130830850
DISCORD_CLIENT_SECRET=your_discord_client_secret
NEXT_PUBLIC_BRAND_NAME="Wutherer"
NEXT_PUBLIC_BRAND_NAME_WORD="Wutherer"
```

### 3. Run Development Server
```bash
npm run dev
```
Navigate to [http://localhost:3000](http://localhost:3000) to inspect the application.
