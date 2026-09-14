# Wutherer REST API Specification

The Wutherer platform includes a built-in, high-performance REST API powered by **FastAPI**. It allows web control panels, external automation scripts, and mobile clients to query and configure bot states, moderation cases, antinuke protections, leveling, tickets, backups, and analytics.

---

## 1. Authentication & Headers

All management endpoints require authentication via either an API key header or a Bearer token:

```http
X-API-Key: your_secure_Wutherer_api_key
```
or
```http
Authorization: Bearer your_secure_Wutherer_api_key
```

### Standard Response Format
Successful requests return JSON with `200 OK` or `201 Created`:
```json
{
  "status": "success",
  "data": { ... }
}
```

Error responses return standard RFC HTTP error schemas:
```json
{
  "detail": "Descriptive error message"
}
```

---

## 2. API Endpoints Reference

### System & Health

#### `GET /api/v1/health`
Returns the status of the bot, latency, and database pool connection state.
- **Response**:
  ```json
  {
    "status": "healthy",
    "version": "2.5.0",
    "timestamp": 1710000000,
    "database": "connected"
  }
  ```

#### `GET /api/v1/bot/stats`
Returns live shard counts, memory footprint, connected guild count, and total cached users.
- **Response**:
  ```json
  {
    "bot_name": "Wutherer",
    "shards": 1,
    "guilds": 48,
    "users": 84200,
    "uptime_seconds": 384210
  }
  ```

---

### Guild Administration

#### `GET /api/v1/guilds`
Lists all Discord servers where Wutherer is currently installed and active.

#### `GET /api/v1/guilds/{guild_id}`
Returns guild metadata, icon URL, member count, and owner ID.

#### `GET /api/v1/guilds/{guild_id}/settings`
Fetches general server settings (custom prefix, primary log channels, starboard settings).

#### `PUT /api/v1/guilds/{guild_id}/settings`
Updates guild configuration.
- **Body**:
  ```json
  {
    "prefix": "s!",
    "log_channel_id": 123456789012345678,
    "mod_log_channel_id": 123456789012345679
  }
  ```

---

### Security, Moderation & Automod

#### `GET /api/v1/guilds/{guild_id}/moderation/cases`
Lists logged moderation infractions, disciplinary actions, reasons, and responsible moderators.

#### `GET /api/v1/guilds/{guild_id}/automod/config`
Retrieves automated filtering thresholds (spam detection, anti-invite, bad words, mention floods).

#### `PUT /api/v1/guilds/{guild_id}/automod/config`
Updates content filter rules and punishment types (`timeout`, `kick`, `ban`).

#### `GET /api/v1/guilds/{guild_id}/antinuke/config`
Retrieves sub-second anti-raid protections, whitelist IDs, and emergency armor states.

---

### Community Telemetry & Analytics

#### `GET /api/v1/guilds/{guild_id}/analytics/overview`
Returns 24-hour message volume curves, total voice channel hours, and command executions.
- **Response**:
  ```json
  {
    "guild_id": 123456789,
    "totals": {
      "total_messages": 145200,
      "total_voice_minutes": 89400,
      "total_commands": 12300
    },
    "hourly_24h": [
      {
        "timestamp": 1710000000,
        "messages": 540,
        "voice_minutes": 120,
        "commands": 45
      }
    ]
  }
  ```

#### `GET /api/v1/guilds/{guild_id}/analytics/channels`
Retrieves the most active text channels ranked by historical message traffic.

---

### Server Snapshots & Backups

#### `GET /api/v1/guilds/{guild_id}/backups`
Lists all archived server snapshots.

#### `GET /api/v1/guilds/{guild_id}/backups/{backup_id}`
Returns complete serialized JSON of roles, categories, channels, permissions, and emojis.

#### `DELETE /api/v1/guilds/{guild_id}/backups/{backup_id}`
Removes a snapshot from storage.

---

### Automated Triggers & Auto-Responder

#### `GET /api/v1/guilds/{guild_id}/autoresponder/triggers`
Lists all active and inactive keyword/regex triggers for the guild.

#### `POST /api/v1/guilds/{guild_id}/autoresponder/triggers`
Registers a new automated response trigger.
- **Body**:
  ```json
  {
    "trigger_text": "!rules",
    "response_text": "Please review guidelines in #rules!",
    "match_mode": "exact",
    "is_embed": true,
    "cooldown_seconds": 5
  }
  ```

#### `DELETE /api/v1/guilds/{guild_id}/autoresponder/triggers/{trigger_id}`
Deletes a trigger.

---

### Anti-Phishing Link Protection

#### `GET /api/v1/guilds/{guild_id}/antiphishing/config`
Retrieves link inspection configuration and domain whitelists.

#### `PUT /api/v1/guilds/{guild_id}/antiphishing/config`
Updates violation punishment and whitelisted hostnames.
