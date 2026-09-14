# Wutherer Setup & Deployment Guide

This document guides you through configuring, hosting, and deploying the complete **Wutherer** platform, including the Python bot core, FastAPI control API, and the Next.js 14 web dashboard.

---

## 1. Prerequisites

- **Python**: Version 3.10 or higher
- **Node.js**: Version 18.17 or higher (`npm` or `pnpm`)
- **Discord Bot Token**: Created in the [Discord Developer Portal](https://discord.com/developers/applications)
- **Google Gemini API Key**: Acquired from [Google AI Studio](https://aistudio.google.com/)
- **YouTube Data API v3 Key**: Acquired from [Google Cloud Console](https://console.cloud.google.com/)

---

## 2. Discord Developer Portal Configuration

1. Visit [Discord Developer Applications](https://discord.com/developers/applications) and create or select your application.
2. Navigate to the **Bot** tab:
   - Under **Privileged Gateway Intents**, enable:
     - ✅ **Presence Intent**
     - ✅ **Server Members Intent**
     - ✅ **Message Content Intent**
   - Click **Reset Token** and copy your token securely into `bot/.env`.
3. Navigate to the **OAuth2** tab:
   - Copy your **Client ID** and **Client Secret**.
   - Under **Redirects**, add:
     - `http://localhost:3000/api/auth/callback/discord` (Local Development)
     - `https://your-domain.com/api/auth/callback/discord` (Production)
4. Bot Invite Link:
   - Go to **OAuth2 ➔ URL Generator**.
   - Select scopes: `bot`, `applications.commands`.
   - Select permissions: `Administrator` (or appropriate moderation permission flags).

---

## 3. Bot Core Setup (`bot/`)

### 3.1 Install Dependencies
```bash
cd bot
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 3.2 Environment Variables (`bot/.env`)
Copy `.env.example` to `.env` and fill in your credentials:
```env
# Discord Configuration
TOKEN=your_bot_token_here
DEFAULT_PREFIX=s!
OWNER_IDS=123456789012345678

# AI & API Integrations
GEMINI_API_KEY=your_gemini_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here

# Control Panel API
API_ENABLED=true
API_PORT=8080
DASHBOARD_SECRET=your_dashboard_api_secret_key_here
```

### 3.3 Launching Wutherer
```bash
python launcher.py
```
Wutherer will initialize its SQLite database with WAL journaling, mount all 21 extension modules, start background workers, and launch the FastAPI dashboard daemon on port 8080.

---

## 4. Web Dashboard Setup (`dashboard/`)

### 4.1 Install Node Dependencies
```bash
cd dashboard
npm install
```

### 4.2 Configure Environment (`dashboard/.env.local`)
Create `.env.local` based on `.env.example`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8080/api
NEXT_PUBLIC_API_KEY=your_dashboard_api_secret_key_here

DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_CLIENT_SECRET=your_discord_client_secret
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_random_secret_string
```

### 4.3 Run the Development Server
```bash
npm run dev
```
Access the dashboard at `http://localhost:3000`.

---

## 5. Production Deployment

### Process Management with PM2 or Systemd
Use `systemd` or `pm2` to ensure continuous uptime in production.

Example `pm2` ecosystem file:
```javascript
module.exports = {
  apps: [
    {
      name: "Wutherer-bot",
      cwd: "./bot",
      script: "venv/bin/python",
      args: "launcher.py",
      autorestart: true,
      watch: false
    },
    {
      name: "Wutherer-dashboard",
      cwd: "./dashboard",
      script: "npm",
      args: "start",
      autorestart: true
    }
  ]
};
```
