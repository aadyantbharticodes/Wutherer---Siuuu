# Advanced Onboarding & Arrival System

Wutherer features an end-to-end onboarding architecture designed to welcome, guide, and engage new server members.

---

## Features

### 1. Auto Direct Message on Join
- Sends customized direct messages when a user joins the server.
- Supports dynamic variables:
  - `{user}`: User string (e.g. `User#0001` or `User`)
  - `{user.mention}`: Clickable user mention
  - `{user.name}`: Username
  - `{user.id}`: Snowflake ID
  - `{guild.name}`: Server name
  - `{guild.member_count}`: Current guild member count
  - `{owner.name}`: Server owner username
- Action Buttons: Attach up to 5 URL link buttons (e.g., links to Server Rules, Verification, Discord vanity link).
- Delay Dispatch: Configurable timer before sending the DM to avoid Discord bot spam detection.

### 2. Auto / Ghost Ping on Join
- Mentions newly arrived members in designated orientation channels (e.g. `#verification`, `#rules-info`, `#get-roles`).
- **Ghost Ping Mode**: Mentions the user and automatically deletes the ping after a set duration (e.g., 5 seconds) to trigger the notification badge on mobile/desktop without cluttering chat history.
- **Persistent Mode**: Keeps the greeting message visible in the channel.

### 3. Timed Delayed Autoroles
- Assigns specific roles (e.g., Verified Member, Resident) only after a member has been in the guild for a configurable delay (e.g., 10 minutes).
- Acts as a deterrent against bot account spam.

### 4. Farewell Announcements
- Dispatches customizable departure messages and embedded member cards when an account leaves or is evicted from the guild.

---

## Discord Commands

| Command | Arguments | Permission | Description |
| :--- | :--- | :--- | :--- |
| `s!autodm` | *None* | Manage Server | Displays Auto DM settings and current message. |
| `s!autodm toggle` | *None* | Manage Server | Enables or disables Auto DM. |
| `s!autodm message` | `<text>` | Manage Server | Configures custom welcome DM message. |
| `s!autodm delay` | `<seconds>` | Manage Server | Sets delay before dispatching DM (0-300s). |
| `s!autodm button add` | `<label> <url>` | Manage Server | Adds an interactive URL button to the DM. |
| `s!autodm button clear` | *None* | Manage Server | Removes all action buttons. |
| `s!autodm test` | *None* | Manage Server | Sends a test DM to the command author. |
| `s!autoping` | *None* | Manage Server | Displays Auto Ping settings. |
| `s!autoping toggle` | *None* | Manage Server | Enables or disables Auto Ping. |
| `s!autoping channel add` | `<#channel>` | Manage Server | Adds channel to auto-ping list. |
| `s!autoping channel remove` | `<#channel>` | Manage Server | Removes channel from auto-ping list. |
| `s!autoping mode` | `<ghost/persistent>` | Manage Server | Toggles between ghost ping and persistent message. |
| `s!autoping delay` | `<seconds>` | Manage Server | Sets ghost ping deletion timer (1-60s). |
| `s!autoping test` | *None* | Manage Server | Sends test ping in target channels. |
| `s!farewell` | *None* | Manage Server | Displays Farewell announcement settings. |
| `s!farewell toggle` | *None* | Manage Server | Enables or disables farewell messages. |
| `s!farewell channel` | `<#channel>` | Manage Server | Sets departure announcement channel. |
| `s!farewell message` | `<text>` | Manage Server | Sets custom departure message. |
| `s!delayedrole delay` | `<minutes>` | Manage Roles | Sets probationary duration before autorole. |
| `s!delayedrole add` | `<@role>` | Manage Roles | Adds role to delayed assignment list. |
| `s!delayedrole remove` | `<@role>` | Manage Roles | Removes role from delayed assignment list. |
