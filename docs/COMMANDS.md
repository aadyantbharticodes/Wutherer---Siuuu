# Wutherer Command Directory

All commands support the dynamic server prefix (default `s!`) as well as Discord application slash commands (`/`).

---

## 1. Moderation (`bot/extensions/moderation/` & `bot/extensions/automod/` & `bot/extensions/antinuke/`)

| Command | Arguments | Permissions | Description |
|---|---|---|---|
| `s!ban` | `<user> [duration] [reason]` | Ban Members | Ban a member with optional duration and logging |
| `s!unban` | `<user_id> [reason]` | Ban Members | Unban a user by ID |
| `s!softban` | `<user> [reason]` | Ban Members | Ban and immediately unban to purge recent messages |
| `s!kick` | `<user> [reason]` | Kick Members | Eject a member from the guild |
| `s!timeout` | `<user> <duration> [reason]` | Moderate Members | Apply Discord native timeout (e.g. `10m`, `2h`, `1d`) |
| `s!untimeout` | `<user>` | Moderate Members | Remove an active timeout from a member |
| `s!warn` | `<user> <reason>` | Moderate Members | Issue a formal warning record |
| `s!warnings` | `<user>` | Moderate Members | View all recorded infractions for a user |
| `s!delwarn` | `<warn_id>` | Manage Messages | Remove an infraction record |
| `s!clearwarns` | `<user>` | Administrator | Clear all warnings for a user |
| `s!purge` | `<amount>` | Manage Messages | Bulk delete messages (up to 100 at once) |
| `s!lock` | `[channel]` | Manage Channels | Lock a channel to prevent regular members from speaking |
| `s!unlock` | `[channel]` | Manage Channels | Reopen a locked channel |
| `s!slowmode` | `<seconds> [channel]` | Manage Channels | Adjust channel slowmode delay (0-21600s) |
| `s!nuke` | `[channel]` | Manage Channels | Clone and delete a channel to wipe history completely |
| `s!automod` | `<status/toggle/rules>` | Administrator | Configure automated spam, link, invite, and caps filters |
| `s!antinuke` | `<on/off/whitelist>` | Server Owner | Configure anti-raid defense against channel/role deletions |

---

## 2. Server Management & Automation (`bot/extensions/server/` & `automation/` & `tickets/` & `verification/`)

| Module | Core Commands | Description |
|---|---|---|
| **Prefix & Config** | `s!setprefix`, `s!prefix` | Customize server command prefix |
| **Welcome & Leaves** | `s!welcome channel`, `s!welcome message` | Setup customizable join greeting messages |
| **Verification** | `s!verification setup` | Deploy visual CAPTCHA verification panel |
| **Tickets** | `s!ticket setup`, `s!ticket close` | Interactive button support ticket panels |
| **Autorole** | `s!autorole add`, `s!autorole remove` | Automatic role assignment on member join |
| **Reaction Roles** | `s!reactionrole`, `s!rr` | Interactive role reaction message bindings |
| **Custom Commands** | `s!cc add`, `s!cc delete`, `s!cc list` | Server-defined custom text responses |
| **Sticky Messages** | `s!sticky set`, `s!sticky remove` | Pin important messages to the bottom of busy chats |

---

## 3. Community & Leveling (`bot/extensions/community/` & `leveling/`)

| Module | Core Commands | Description |
|---|---|---|
| **Leveling** | `s!rank [member]`, `s!leaderboard`, `s!setxp` | XP progression engine with graphical Pillow rank cards |
| **Level Rewards** | `s!addreward <level> <role>` | Automatically assign roles at specified levels |
| **Giveaways** | `s!g start <time> <winners> <prize>`, `s!g reroll` | Timed giveaways with automated prize drawing |
| **Polls** | `s!poll <question> <options...>` | Multi-option voting polls with emoji reactions |
| **Suggestions** | `s!suggest <text>` | Community suggestion voting system |
| **Starboard** | Reactions with ⭐ | Highlight popular messages in a dedicated starboard channel |

---

## 4. Artificial Intelligence (`bot/extensions/ai/`)

| Command | Arguments | Description |
|---|---|---|
| `s!ai ask` | `<prompt>` | Chat with Google Gemini with persistent memory |
| `s!ai clear` | None | Clear your personal conversation memory |
| `s!ai summarize` | `<text>` | Summarize long articles or messages into key points |
| `s!ai rewrite` | `<style> <text>` | Rewrite text in a specified tone (professional, casual, etc.) |
| `s!ai translate` | `<language> <text>` | Translate text into any world language |
| `s!ai code` | `<language> <question>` | Ask for coding help, bug fixes, or architecture advice |
| `s!ai persona` | `<persona>` | Configure server-wide AI system prompt (Admin) |

---

## 5. Gaming, Minecraft & YouTube (`bot/extensions/gaming/` & `youtube/`)

| Module | Core Commands | Description |
|---|---|---|
| **Minecraft Server** | `s!mc server <ip> [java/bedrock]` | Live server ping, player count, MOTD, and version |
| **Minecraft Skin** | `s!mc skin <player>` | 3D body render and isometric avatar of player |
| **Minecraft UUID** | `s!mc uuid <player>` | Lookup player Mojang UUID |
| **Server Tracking** | `s!mc track <ip> [channel]` | Auto-updating server status embed in channel |
| **YouTube Channel** | `s!yt channel <query>` | Channel subscriber count, total views, and video counts |
| **YouTube Video** | `s!yt video <query>` | Search YouTube for video links |
| **Upload Alerts** | `s!yt subscribe <channel_id>`, `s!yt list` | Automatic notifications when a channel uploads |

---

## 6. Economy & Casino (`bot/extensions/economy/`)

| Command | Arguments | Description |
|---|---|---|
| `s!balance` | `[member]` | View wallet, bank, and total net worth |
| `s!daily` | None | Claim 250 daily reward credits |
| `s!work` | None | Work an hourly job shift for credits |
| `s!deposit` | `<amount/all>` | Move credits from wallet into bank |
| `s!withdraw` | `<amount/all>` | Move credits from bank into wallet |
| `s!pay` | `<member> <amount>` | Transfer credits to another user |
| `s!coinflip` | `<bet> <heads/tails>` | Gamble credits on a 50/50 coinflip |
| `s!slots` | `<bet>` | Spin the slot machine for up to 5x jackpot |
| `s!economyleaderboard` | None | View the server wealth leaderboard |

---

## 7. Productivity & Utility (`bot/extensions/productivity/` & `utility/` & `developer/` & `fun/` & `social/`)

| Module | Core Commands | Description |
|---|---|---|
| **Productivity** | `s!remindme <time> <msg>`, `s!timer <time>`, `s!calc <expr>`, `s!convert <val> <from> <to>` | Reminders, timers, math, unit converter |
| **Utility** | `s!ping`, `s!uptime`, `s!botinfo`, `s!userinfo`, `s!serverinfo`, `s!avatar`, `s!banner` | Bot and server information, avatars |
| **Developer** | `s!dev json <str>`, `s!dev regex <pattern> <str>`, `s!dev base64 <mode> <str>`, `s!dev hash <algo> <str>`, `s!dev timestamp`, `s!dev color <hex>` | Dev formatting, regex, base64, hash |
| **Fun & Games** | `s!rps`, `s!8ball <q>`, `s!roll [sides]`, `s!flip`, `s!choose <opts...>`, `s!rate <item>`, `s!trivia` | Interactive mini-games & decisions |
| **Social** | `s!afk [reason]`, `s!profile [member]` | AFK status alerts & member profiles |
| **Music** | `s!join`, `s!play <query>`, `s!pause`, `s!resume`, `s!skip`, `s!queue`, `s!nowplaying`, `s!leave` | Voice audio streaming and queue |
| **Admin** | `s!reload <ext>`, `s!load <ext>`, `s!unload <ext>`, `s!sync`, `s!eval <code>`, `s!broadcast <msg>` | Bot owner management controls |

---

## 8. Server Backups & Snapshots (`bot/extensions/backup/`)

| Command | Arguments | Permissions | Description |
|---|---|---|---|
| `s!backup create` | `[notes]` | Administrator | Compiles a full snapshot of roles, channels, permissions, and emojis |
| `s!backup list` | None | Administrator | Lists all stored backups for this server |
| `s!backup info` | `<backup_id>` | Administrator | Inspects metadata, channel counts, and roles within a snapshot |
| `s!backup download`| `<backup_id>` | Administrator | Exports the snapshot JSON file directly to Discord chat |
| `s!backup restore` | `<backup_id>` | Server Owner | Recreates missing roles and channel structures with interactive modal confirmation |
| `s!backup delete`  | `<backup_id>` | Administrator | Permanently deletes a snapshot archive |

---

## 9. Community Telemetry & Analytics (`bot/extensions/analytics/`)

| Command | Arguments | Permissions | Description |
|---|---|---|---|
| `s!stats overview` | None | Everyone | Displays 24-hour message volume, voice minutes, and total commands |
| `s!stats channels` | None | Everyone | Ranks the top text channels by message velocity |
| `s!stats heatmap`  | None | Everyone | Renders a 24-hour ASCII bar chart showing peak chatter hours |
| `s!insights`       | None | Moderator | Comprehensive demographic health audit (human/bot ratio, boost tier) |

---

## 10. Automated Triggers & Auto-Responder (`bot/extensions/autoresponder/`)

| Command | Arguments | Permissions | Description |
|---|---|---|---|
| `s!autoresponder add` | `<trigger> \| <response>` | Administrator | Creates an automated trigger (supports `--mode=exact/wildcard/regex`, `--embed`) |
| `s!autoresponder list`| None | Administrator | Lists all configured automated responses and usage counters |
| `s!autoresponder toggle`| `<trigger_id>` | Administrator | Enables or disables an existing trigger |
| `s!autoresponder delete`| `<trigger_id>` | Administrator | Deletes a trigger from the guild |

---

## 11. Anti-Phishing Link Protection (`bot/extensions/antiphishing/`)

| Command | Arguments | Permissions | Description |
|---|---|---|---|
| `s!antiphishing enable` | None | Administrator | Enables real-time heuristic link scanning |
| `s!antiphishing disable`| None | Administrator | Disables real-time link scanning |
| `s!antiphishing action` | `<delete\|timeout\|kick\|ban>` | Administrator | Sets punishment executed against scam link posters |
| `s!antiphishing scan`   | `<url>` | Everyone | Tests a target URL against Wutherer's typosquatting engine |

---

## 12. Economy Shop & User Inventory (`bot/extensions/shop/`)

| Command | Arguments | Permissions | Description |
|---|---|---|---|
| `s!shop` | None | Everyone | Displays the server item and role catalog |
| `s!buy` | `<item_id>` | Everyone | Purchases an item or role using earned wallet credits |
| `s!inventory` | `[member]` | Everyone | Inspects personal item inventory and badges |
| `s!gift` | `<@member> <item_id>` | Everyone | Transfers an item from inventory to another member |
| `s!shop add role` | `<@role> <price> [desc]` | Administrator | Adds a purchasable Discord role to the server store |
| `s!shop delete` | `<item_id>` | Administrator | Removes an item from the shop |
| `s!welcome testcard` | None | Administrator | Previews dynamic Pillow welcome card rendering |

