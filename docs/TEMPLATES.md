# Xenon-Style Server Template Engine

The Wutherer Server Template Engine provides full-fidelity server layout serialization, backup, community sharing, and automated deployment — analogous to Xenon bot.

---

## Capabilities

1. **Full Guild Topology Serialization**:
   - Channel categories, text channels, voice channels, stage channels, forum channels.
   - Channel configuration: topic, slowmode delay, audio bitrate, user limits, and category groupings.
   - Role hierarchy: role name, color, hoist status, mentionable flag, and permission bits.
   - Channel overwrites: detailed role-specific permission maps per channel.
   - Guild settings: AFK channels, verification level, default notification level, and explicit content filters.

2. **Deployment Modes**:
   - `Merge Mode` (Default): Non-destructive. Creates missing categories, channels, and roles while preserving existing channels and messages.
   - `Wipe & Apply Mode` (`--wipe`): Completely resets and purges non-bot channels and rebuilds the server topology from the blueprint.

3. **Public Community Catalog**:
   - `gaming_community`: Esports/LFG hub, voice lobbies, stream alerts, clip showcases.
   - `tech_developer`: Software engineering hub with code review, stack-specific channels, dev huddles.
   - `community_lounge`: Aesthetic hangout with parlor channels, media hubs, and lo-fi audio rooms.
   - `study_university`: Academic campus with subject departments, pomodoro checkins, and silent libraries.
   - `esports_clan`: Competitive clan HQ with scrim schedules, tactics reviews, and roster war rooms.

---

## Discord Commands

| Command | Arguments | Permission | Description |
| :--- | :--- | :--- | :--- |
| `s!template create` | `<name> [description]` | Administrator | Serializes current guild layout and saves it with a unique template ID. |
| `s!template list` | *None* | Manage Server | Lists all custom templates created for this server. |
| `s!template public` | *None* | Everyone | Browses curated public community templates. |
| `s!template preview` | `<template_id>` | Everyone | Displays role and channel hierarchy of a template. |
| `s!template apply` | `<template_id> [--wipe]` | Administrator | Deploys a template to the current server (interactive confirmation required). |
| `s!template export` | `<template_id>` | Manage Server | Exports template definition as raw JSON. |
| `s!template delete` | `<template_id>` | Administrator | Deletes a custom server template. |

---

## REST API Specification

### List Public Templates
- **Endpoint**: `GET /api/templates/public`
- **Response**: Array of curated template metadata.

### List Guild Templates
- **Endpoint**: `GET /api/templates/guild/{guild_id}`
- **Response**: List of saved templates for the specified guild.

### Create Template
- **Endpoint**: `POST /api/templates/guild/{guild_id}/create`
- **Body**:
  ```json
  {
    "name": "Production Blueprint",
    "description": "Base server setup",
    "is_public": false,
    "category": "general"
  }
  ```

### Apply Template
- **Endpoint**: `POST /api/templates/guild/{guild_id}/apply/{template_id}`
- **Body**:
  ```json
  {
    "mode": "merge"
  }
  ```
