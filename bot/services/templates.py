from __future__ import annotations
import json
import asyncio
import logging
from typing import Optional, Any, Union
import discord

log = logging.getLogger("wutherer.templates")

PUBLIC_TEMPLATES: dict[str, dict] = {
    "gaming_community": {
        "name": "Gaming Community & Esports Hub",
        "description": "Complete setup for gaming communities, LFG, stream alerts, clip showcases, and voice lobbies.",
        "category": "gaming",
        "roles": [
            {"name": "Server Director", "color": 0xFF4500, "hoist": True, "mentionable": True, "permissions": 8},
            {"name": "Moderator", "color": 0x1E90FF, "hoist": True, "mentionable": True, "permissions": 1099511627775},
            {"name": "Content Creator", "color": 0x9932CC, "hoist": True, "mentionable": True, "permissions": 1071698529},
            {"name": "Tournament MVP", "color": 0xFFD700, "hoist": True, "mentionable": True, "permissions": 1071698529},
            {"name": "Verified Gamer", "color": 0x00FA9A, "hoist": True, "mentionable": False, "permissions": 1071698529},
            {"name": "Member", "color": 0x708090, "hoist": False, "mentionable": False, "permissions": 1071698529},
        ],
        "categories": [
            {
                "name": "📌 INFORMATION",
                "channels": [
                    {"name": "welcome-hub", "type": "text", "topic": "Welcome to our gaming community!"},
                    {"name": "rules-and-info", "type": "text", "topic": "Official community guidelines"},
                    {"name": "announcements", "type": "text", "topic": "Important server & tournament announcements"},
                    {"name": "stream-alerts", "type": "text", "topic": "Live stream notifications from creators"},
                ]
            },
            {
                "name": "💬 COMMUNITY CHAT",
                "channels": [
                    {"name": "general-chat", "type": "text", "topic": "Hang out and talk games"},
                    {"name": "bot-commands", "type": "text", "topic": "Bot interactions and minigames"},
                    {"name": "clips-and-highlights", "type": "text", "topic": "Share your best gaming plays"},
                    {"name": "game-setups", "type": "text", "topic": "Battlestation & hardware showcases"},
                ]
            },
            {
                "name": "🎮 LOOKING FOR GROUP",
                "channels": [
                    {"name": "lfg-general", "type": "text", "topic": "Find teammates across all games"},
                    {"name": "lfg-fps", "type": "text", "topic": "Valorant, CS2, Apex, Overwatch LFG"},
                    {"name": "lfg-survival", "type": "text", "topic": "Rust, Minecraft, Ark, DayZ LFG"},
                ]
            },
            {
                "name": "🔊 SQUAD VOICE LOBBIES",
                "channels": [
                    {"name": "Squad Alpha (Duos)", "type": "voice", "user_limit": 2},
                    {"name": "Squad Bravo (Trios)", "type": "voice", "user_limit": 3},
                    {"name": "Squad Charlie (Squads)", "type": "voice", "user_limit": 5},
                    {"name": "Casual Lounge 1", "type": "voice", "user_limit": 0},
                    {"name": "AFK Sanctuary", "type": "voice", "user_limit": 0},
                ]
            }
        ]
    },
    "tech_developer": {
        "name": "Software Engineering & Tech Hub",
        "description": "Collaborative hub for developers, open source projects, code review, and stack discussions.",
        "category": "tech",
        "roles": [
            {"name": "Lead Architect", "color": 0x5865F2, "hoist": True, "mentionable": True, "permissions": 8},
            {"name": "Core Maintainer", "color": 0x2ECC71, "hoist": True, "mentionable": True, "permissions": 1099511627775},
            {"name": "Senior Engineer", "color": 0x3498DB, "hoist": True, "mentionable": True, "permissions": 1071698529},
            {"name": "Junior Developer", "color": 0x9B59B6, "hoist": True, "mentionable": False, "permissions": 1071698529},
            {"name": "Student / Learner", "color": 0xE67E22, "hoist": False, "mentionable": False, "permissions": 1071698529},
        ],
        "categories": [
            {
                "name": "🧭 DIRECTORY",
                "channels": [
                    {"name": "welcome-dev", "type": "text", "topic": "Welcome developers & tech builders"},
                    {"name": "guidelines", "type": "text", "topic": "Code of conduct & contribution rules"},
                    {"name": "tech-news", "type": "text", "topic": "Latest engineering and open-source updates"},
                ]
            },
            {
                "name": "💻 ENGINEERING DISCUSSIONS",
                "channels": [
                    {"name": "general-dev", "type": "text", "topic": "General programming chat"},
                    {"name": "python-rust-backend", "type": "text", "topic": "APIs, databases, and systems code"},
                    {"name": "web-and-frontend", "type": "text", "topic": "React, Next.js, CSS, UI/UX design"},
                    {"name": "ai-and-ml", "type": "text", "topic": "LLMs, neural networks, PyTorch, Gemini"},
                    {"name": "devops-cloud-infra", "type": "text", "topic": "Docker, Kubernetes, AWS, GCP, CI/CD"},
                ]
            },
            {
                "name": "🛠️ COLLABORATION & HELP",
                "channels": [
                    {"name": "code-review", "type": "text", "topic": "Post snippets and PRs for feedback"},
                    {"name": "debug-assistance", "type": "text", "topic": "Get help troubleshooting tricky stack traces"},
                    {"name": "project-showcase", "type": "text", "topic": "Showcase your GitHub repos and side projects"},
                ]
            },
            {
                "name": "🎧 DEV HUDDLES",
                "channels": [
                    {"name": "Pair Programming 1", "type": "voice", "user_limit": 2},
                    {"name": "Pair Programming 2", "type": "voice", "user_limit": 2},
                    {"name": "Engineering Lounge", "type": "voice", "user_limit": 0},
                    {"name": "Focus / Silent Co-working", "type": "voice", "user_limit": 0},
                ]
            }
        ]
    },
    "community_lounge": {
        "name": "Aesthetic Community Lounge",
        "description": "Vibrant, elegant server layout for social gatherings, hobbies, music, and media.",
        "category": "social",
        "roles": [
            {"name": "Founder", "color": 0xFF69B4, "hoist": True, "mentionable": True, "permissions": 8},
            {"name": "Council", "color": 0xBA55D3, "hoist": True, "mentionable": True, "permissions": 1099511627775},
            {"name": "VIP Enthusiast", "color": 0xFFD700, "hoist": True, "mentionable": True, "permissions": 1071698529},
            {"name": "Regular", "color": 0x40E0D0, "hoist": True, "mentionable": False, "permissions": 1071698529},
            {"name": "Newcomer", "color": 0xDCDCDC, "hoist": False, "mentionable": False, "permissions": 1071698529},
        ],
        "categories": [
            {
                "name": "✨ ARRIVAL",
                "channels": [
                    {"name": "welcome-lounge", "type": "text", "topic": "Step into our cozy space"},
                    {"name": "server-rules", "type": "text", "topic": "Community etiquette"},
                    {"name": "announcements", "type": "text", "topic": "Server updates & giveaways"},
                ]
            },
            {
                "name": "☕ PARLOR",
                "channels": [
                    {"name": "general-hangout", "type": "text", "topic": "Daily banter and chats"},
                    {"name": "photography-and-art", "type": "text", "topic": "Share your aesthetic creations"},
                    {"name": "food-and-recipes", "type": "text", "topic": "Culinary delights & recipes"},
                    {"name": "music-and-vibes", "type": "text", "topic": "Spotify links, playlists, and reviews"},
                ]
            },
            {
                "name": "🎲 RECREATION",
                "channels": [
                    {"name": "bot-games", "type": "text", "topic": "Blackjack, Minesweeper, Wordle, Trivia"},
                    {"name": "counting-sanctuary", "type": "text", "topic": "Can we reach 10,000?"},
                    {"name": "starboard-hall", "type": "text", "topic": "Community hall of fame"},
                ]
            },
            {
                "name": "🎵 AUDIO LOUNGES",
                "channels": [
                    {"name": "Lo-Fi Coffee Shop", "type": "voice", "user_limit": 0},
                    {"name": "Late Night Talks", "type": "voice", "user_limit": 0},
                    {"name": "Private Booth (Duos)", "type": "voice", "user_limit": 2},
                    {"name": "AFK Pillow Room", "type": "voice", "user_limit": 0},
                ]
            }
        ]
    },
    "study_university": {
        "name": "University & Study Academy",
        "description": "Structured academic community with dedicated subject departments, study timers, and group rooms.",
        "category": "academic",
        "roles": [
            {"name": "Head Dean", "color": 0x800000, "hoist": True, "mentionable": True, "permissions": 8},
            {"name": "Teaching Assistant", "color": 0x228B22, "hoist": True, "mentionable": True, "permissions": 1099511627775},
            {"name": "Honor Scholar", "color": 0xDAA520, "hoist": True, "mentionable": True, "permissions": 1071698529},
            {"name": "Undergraduate", "color": 0x4682B4, "hoist": False, "mentionable": False, "permissions": 1071698529},
        ],
        "categories": [
            {
                "name": "🏛️ CAMPUS INFO",
                "channels": [
                    {"name": "orientation", "type": "text", "topic": "Academic campus introduction"},
                    {"name": "campus-rules", "type": "text", "topic": "Study hall guidelines"},
                    {"name": "resource-library", "type": "text", "topic": "Curated textbooks, notes, and study guides"},
                ]
            },
            {
                "name": "📚 ACADEMIC DEPARTMENTS",
                "channels": [
                    {"name": "mathematics-and-stats", "type": "text", "topic": "Calculus, Linear Algebra, Statistics"},
                    {"name": "physics-and-engineering", "type": "text", "topic": "Physics, circuits, mechanical design"},
                    {"name": "computer-science", "type": "text", "topic": "Algorithms, data structures, theory"},
                    {"name": "humanities-and-writing", "type": "text", "topic": "Essays, philosophy, literature"},
                ]
            },
            {
                "name": "⏱️ PRODUCTIVITY & TIMERS",
                "channels": [
                    {"name": "pomodoro-checkin", "type": "text", "topic": "Log study sessions and goals"},
                    {"name": "accountability-group", "type": "text", "topic": "Keep each other on track"},
                ]
            },
            {
                "name": "🔇 STUDY HALLS",
                "channels": [
                    {"name": "Silent Library (Mic Muted)", "type": "voice", "user_limit": 0},
                    {"name": "Study Pod A", "type": "voice", "user_limit": 4},
                    {"name": "Study Pod B", "type": "voice", "user_limit": 4},
                    {"name": "Study Break Room", "type": "voice", "user_limit": 0},
                ]
            }
        ]
    },
    "esports_clan": {
        "name": "Esports Clan & Competitive Roster",
        "description": "Tactical scrims, tournament coordination, roster channels, and private team strategy rooms.",
        "category": "gaming",
        "roles": [
            {"name": "Clan General", "color": 0xDC143C, "hoist": True, "mentionable": True, "permissions": 8},
            {"name": "Team Captain", "color": 0xFF8C00, "hoist": True, "mentionable": True, "permissions": 1099511627775},
            {"name": "Starting Roster", "color": 0x00CED1, "hoist": True, "mentionable": True, "permissions": 1071698529},
            {"name": "Sub / Academy", "color": 0x7B68EE, "hoist": True, "mentionable": False, "permissions": 1071698529},
            {"name": "Trial Candidate", "color": 0xA9A9A9, "hoist": False, "mentionable": False, "permissions": 1071698529},
        ],
        "categories": [
            {
                "name": "🏆 COMMAND & HQ",
                "channels": [
                    {"name": "hq-welcome", "type": "text", "topic": "Official Clan HQ"},
                    {"name": "tournament-schedule", "type": "text", "topic": "Upcoming scrims and matches"},
                    {"name": "scrim-results", "type": "text", "topic": "Match records and stats"},
                ]
            },
            {
                "name": "🎯 TACTICS & REVIEWS",
                "channels": [
                    {"name": "vod-reviews", "type": "text", "topic": "Match replay analysis"},
                    {"name": "strats-and-lineups", "type": "text", "topic": "Tactics, callouts, and playbook"},
                    {"name": "recruitment-trials", "type": "text", "topic": "Candidate applications"},
                ]
            },
            {
                "name": "🎙️ WAR ROOMS",
                "channels": [
                    {"name": "Main Roster War Room", "type": "voice", "user_limit": 5},
                    {"name": "Academy War Room", "type": "voice", "user_limit": 5},
                    {"name": "Coaching & Spectator", "type": "voice", "user_limit": 10},
                    {"name": "Lobby & Warmup", "type": "voice", "user_limit": 0},
                ]
            }
        ]
    }
}


class TemplateEngine:
    @staticmethod
    def serialize_guild(guild: discord.Guild) -> dict:
        data = {
            "name": guild.name,
            "description": guild.description or "",
            "afk_timeout": guild.afk_timeout,
            "verification_level": int(guild.verification_level),
            "default_notifications": int(guild.default_notifications),
            "explicit_content_filter": int(guild.explicit_content_filter),
            "roles": [],
            "categories": []
        }

        roles_list = []
        for role in reversed(guild.roles):
            if role.is_default() or role.managed:
                continue
            roles_list.append({
                "name": role.name,
                "color": role.color.value,
                "hoist": role.hoist,
                "mentionable": role.mentionable,
                "permissions": role.permissions.value,
            })
        data["roles"] = roles_list

        categories_data = []
        for cat in guild.categories:
            cat_obj = {
                "name": cat.name,
                "position": cat.position,
                "channels": []
            }
            for ch in cat.channels:
                ch_type = "text" if isinstance(ch, discord.TextChannel) else "voice" if isinstance(ch, discord.VoiceChannel) else "stage" if isinstance(ch, discord.StageChannel) else "forum" if isinstance(ch, discord.ForumChannel) else "text"
                ch_dict = {
                    "name": ch.name,
                    "type": ch_type,
                    "position": ch.position,
                }
                if hasattr(ch, "topic"):
                    ch_dict["topic"] = ch.topic or ""
                if hasattr(ch, "slowmode_delay"):
                    ch_dict["slowmode_delay"] = ch.slowmode_delay
                if hasattr(ch, "bitrate"):
                    ch_dict["bitrate"] = ch.bitrate
                if hasattr(ch, "user_limit"):
                    ch_dict["user_limit"] = ch.user_limit
                cat_obj["channels"].append(ch_dict)
            categories_data.append(cat_obj)

        uncategorized = []
        for ch in guild.channels:
            if ch.category is None and not isinstance(ch, discord.CategoryChannel):
                ch_type = "text" if isinstance(ch, discord.TextChannel) else "voice" if isinstance(ch, discord.VoiceChannel) else "text"
                uncategorized.append({
                    "name": ch.name,
                    "type": ch_type,
                    "topic": getattr(ch, "topic", "") or "",
                })
        if uncategorized:
            categories_data.insert(0, {
                "name": "UNCATEGORIZED",
                "position": -1,
                "channels": uncategorized
            })

        data["categories"] = categories_data
        return data

    @staticmethod
    async def apply_template(
        guild: discord.Guild,
        template_data: dict,
        mode: str = "merge",
        progress_callback=None
    ) -> dict:
        results = {
            "roles_created": 0,
            "categories_created": 0,
            "channels_created": 0,
            "errors": []
        }

        if mode == "wipe":
            for ch in guild.channels:
                try:
                    await ch.delete(reason="Wutherer Template Engine: Wipe and Apply")
                    await asyncio.sleep(0.4)
                except Exception as e:
                    results["errors"].append(f"Failed deleting channel {ch.name}: {e}")

        existing_role_names = {r.name.lower(): r for r in guild.roles}
        role_map: dict[str, discord.Role] = {}

        for r_spec in template_data.get("roles", []):
            name = r_spec.get("name")
            if not name:
                continue
            if name.lower() in existing_role_names and mode == "merge":
                role_map[name] = existing_role_names[name.lower()]
                continue
            try:
                perms = discord.Permissions(r_spec.get("permissions", 1071698529))
                color = discord.Color(r_spec.get("color", 0))
                new_role = await guild.create_role(
                    name=name,
                    permissions=perms,
                    color=color,
                    hoist=r_spec.get("hoist", False),
                    mentionable=r_spec.get("mentionable", False),
                    reason="Wutherer Template Engine"
                )
                role_map[name] = new_role
                results["roles_created"] += 1
                await asyncio.sleep(0.4)
            except Exception as exc:
                results["errors"].append(f"Role {name}: {exc}")

        for cat_spec in template_data.get("categories", []):
            cat_name = cat_spec.get("name", "GENERAL")
            target_cat = None
            if cat_name != "UNCATEGORIZED":
                try:
                    target_cat = await guild.create_category(
                        name=cat_name,
                        reason="Wutherer Template Engine"
                    )
                    results["categories_created"] += 1
                    await asyncio.sleep(0.4)
                except Exception as exc:
                    results["errors"].append(f"Category {cat_name}: {exc}")

            for ch_spec in cat_spec.get("channels", []):
                ch_name = ch_spec.get("name")
                ch_type = ch_spec.get("type", "text")
                topic = ch_spec.get("topic", "")
                try:
                    if ch_type == "voice":
                        await guild.create_voice_channel(
                            name=ch_name,
                            category=target_cat,
                            user_limit=ch_spec.get("user_limit", 0),
                            reason="Wutherer Template Engine"
                        )
                    else:
                        await guild.create_text_channel(
                            name=ch_name,
                            category=target_cat,
                            topic=topic,
                            slowmode_delay=ch_spec.get("slowmode_delay", 0),
                            reason="Wutherer Template Engine"
                        )
                    results["channels_created"] += 1
                    await asyncio.sleep(0.4)
                except Exception as exc:
                    results["errors"].append(f"Channel {ch_name}: {exc}")

        return results
