# Anti-Nuke & Server Defense Suite

Wutherer's Defense Core protects Discord servers from rogue administrators, token-stealer bot takeovers, coordinated raid assaults, and mass destructive actions.

---

## Defense Mechanisms

### 1. Rapid Action Watchdog
Tracks administrative actions within a rolling time window (default: 15 seconds) using Discord Audit Log correlation. If an account breaches thresholds, automated countermeasures trigger instantly:
- **Channel Deletion Throttling**: Limits channel purges (default: 3 per 15s).
- **Role Deletion Throttling**: Limits mass role purges (default: 3 per 15s).
- **Mass Ban / Kick Throttling**: Prevents mass guild member evictions (default: 5 per 15s).
- **Rogue Webhook Monitor**: Automatically removes unauthorized webhooks spawned during attacks.

### 2. Automated Countermeasures
When a threat is verified, Wutherer executes the configured penalty:
- `ban`: Permanently bans the offending account from the guild.
- `kick`: Evicts the account immediately.
- `quarantine`: Strips all administrative roles and assigns an isolated quarantine role with 0 channel permissions.
- `strip`: Removes all hoisted and privileged administrative roles.

### 3. Emergency Panic Lockdown
A server-wide fail-safe switch:
- Inspects all channels and records `@everyone` permission overwrites in the SQLite database.
- Revokes `send_messages`, `send_messages_in_threads`, `create_public_threads`, and `connect` across all text and voice channels.
- When `s!unlock all` is executed, the original permissions are restored with zero configuration loss.

### 4. Channel Nuke & Clone Utilities
- `s!nuke`: Clones the current channel with identical category, topic, permissions, position, and deletes the old corrupted channel.
- `s!clone <#channel>`: Creates an exact duplicate of any specified channel.

---

## Discord Commands

| Command | Arguments | Permission | Description |
| :--- | :--- | :--- | :--- |
| `s!nuke` | *None* | Manage Channels | Clones and purges the current channel. |
| `s!clone` | `[#channel]` | Manage Channels | Duplicates a channel. |
| `s!lockdown` | `[all]` | Manage Server | Locks down the current channel or all server channels. |
| `s!unlock` | `[all]` | Manage Server | Unlocks the current channel or lifts server-wide lockdown. |
| `s!raidmode` | `<on/off>` | Administrator | Sets guild verification level to HIGH and throttles joiners. |
| `s!quarantine` | `<@member> [reason]` | Manage Roles | Strips member roles and confines them to Quarantine role. |
| `s!antinuke` | *None* | Administrator | Displays current anti-nuke shield status and limits. |
| `s!antinuke toggle` | *None* | Administrator | Enables or disables the anti-nuke shield. |
| `s!antinuke whitelist` | `<add/remove> <@user>` | Administrator | Adds or removes trusted administrators. |
| `s!antinuke logs` | *None* | Administrator | Displays recent security violation audit logs. |
