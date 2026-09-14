import logging

log = logging.getLogger("wutherer.db")

SCHEMA_VERSION = 1

TABLES = [
    """CREATE TABLE IF NOT EXISTS schema_version (
        version INTEGER PRIMARY KEY
    )""",


    """CREATE TABLE IF NOT EXISTS guild_settings (
        guild_id INTEGER PRIMARY KEY,
        prefix TEXT DEFAULT 's!',
        language TEXT DEFAULT 'en',
        dj_role_id INTEGER,
        mute_role_id INTEGER,
        jail_role_id INTEGER,
        log_channel_id INTEGER,
        mod_log_channel_id INTEGER,
        suggestion_channel_id INTEGER,
        starboard_channel_id INTEGER,
        starboard_threshold INTEGER DEFAULT 3,
        counting_channel_id INTEGER,
        counting_current INTEGER DEFAULT 0,
        counting_last_user_id INTEGER,
        nightmode_enabled INTEGER DEFAULT 0,
        nightmode_start TEXT,
        nightmode_end TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )""",


    """CREATE TABLE IF NOT EXISTS welcome_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        channel_id INTEGER,
        message TEXT,
        embed_json TEXT,
        dm_enabled INTEGER DEFAULT 0,
        dm_message TEXT,
        goodbye_enabled INTEGER DEFAULT 0,
        goodbye_channel_id INTEGER,
        goodbye_message TEXT,
        goodbye_embed_json TEXT
    )""",


    """CREATE TABLE IF NOT EXISTS autoroles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        role_id INTEGER NOT NULL,
        target TEXT DEFAULT 'all',
        UNIQUE(guild_id, role_id)
    )""",


    """CREATE TABLE IF NOT EXISTS reaction_roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        message_id INTEGER NOT NULL,
        emoji TEXT NOT NULL,
        role_id INTEGER NOT NULL,
        mode TEXT DEFAULT 'toggle',
        UNIQUE(message_id, emoji)
    )""",


    """CREATE TABLE IF NOT EXISTS warnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        moderator_id INTEGER NOT NULL,
        reason TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
    "CREATE INDEX IF NOT EXISTS idx_warnings_guild_user ON warnings(guild_id, user_id)",


    """CREATE TABLE IF NOT EXISTS mod_cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        moderator_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        reason TEXT,
        duration INTEGER,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
    "CREATE INDEX IF NOT EXISTS idx_mod_cases_guild ON mod_cases(guild_id)",


    """CREATE TABLE IF NOT EXISTS ticket_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        category_id INTEGER,
        log_channel_id INTEGER,
        support_role_id INTEGER,
        panel_channel_id INTEGER,
        panel_message_id INTEGER,
        greeting TEXT DEFAULT 'A staff member will assist you shortly.',
        max_open INTEGER DEFAULT 3
    )""",
    """CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        channel_id INTEGER UNIQUE,
        user_id INTEGER NOT NULL,
        subject TEXT,
        status TEXT DEFAULT 'open',
        claimed_by INTEGER,
        created_at TEXT DEFAULT (datetime('now')),
        closed_at TEXT
    )""",


    """CREATE TABLE IF NOT EXISTS verification_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        channel_id INTEGER,
        role_id INTEGER,
        log_channel_id INTEGER,
        difficulty TEXT DEFAULT 'medium',
        max_attempts INTEGER DEFAULT 3,
        cooldown INTEGER DEFAULT 300,
        timeout INTEGER DEFAULT 120
    )""",
    """CREATE TABLE IF NOT EXISTS verification_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        success INTEGER DEFAULT 0,
        ip_hash TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
    "CREATE INDEX IF NOT EXISTS idx_verify_guild_user ON verification_attempts(guild_id, user_id)",


    """CREATE TABLE IF NOT EXISTS leveling_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        channel_id INTEGER,
        announce_levelup INTEGER DEFAULT 1,
        xp_rate REAL DEFAULT 1.0,
        ignored_channels TEXT DEFAULT '[]',
        ignored_roles TEXT DEFAULT '[]',
        stack_roles INTEGER DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS user_levels (
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 0,
        messages INTEGER DEFAULT 0,
        last_xp_at TEXT,
        PRIMARY KEY (guild_id, user_id)
    )""",
    """CREATE TABLE IF NOT EXISTS level_rewards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        level INTEGER NOT NULL,
        role_id INTEGER NOT NULL,
        UNIQUE(guild_id, level)
    )""",


    """CREATE TABLE IF NOT EXISTS giveaways (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        message_id INTEGER,
        host_id INTEGER NOT NULL,
        prize TEXT NOT NULL,
        winners INTEGER DEFAULT 1,
        ends_at TEXT NOT NULL,
        ended INTEGER DEFAULT 0,
        required_role_id INTEGER,
        entries TEXT DEFAULT '[]',
        created_at TEXT DEFAULT (datetime('now'))
    )""",


    """CREATE TABLE IF NOT EXISTS afk (
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        reason TEXT DEFAULT 'AFK',
        set_at TEXT DEFAULT (datetime('now')),
        PRIMARY KEY (guild_id, user_id)
    )""",


    """CREATE TABLE IF NOT EXISTS automod_config (
        guild_id INTEGER PRIMARY KEY,
        antispam INTEGER DEFAULT 0,
        antispam_threshold INTEGER DEFAULT 5,
        antispam_interval INTEGER DEFAULT 5,
        anticaps INTEGER DEFAULT 0,
        anticaps_threshold INTEGER DEFAULT 70,
        anticaps_min_length INTEGER DEFAULT 10,
        antilink INTEGER DEFAULT 0,
        antilink_whitelist TEXT DEFAULT '[]',
        antiinvite INTEGER DEFAULT 0,
        antimention INTEGER DEFAULT 0,
        antimention_threshold INTEGER DEFAULT 5,
        antiemoji INTEGER DEFAULT 0,
        antiemoji_threshold INTEGER DEFAULT 10,
        badwords TEXT DEFAULT '[]',
        punishment TEXT DEFAULT 'delete',
        ignored_channels TEXT DEFAULT '[]',
        ignored_roles TEXT DEFAULT '[]',
        log_channel_id INTEGER
    )""",


    """CREATE TABLE IF NOT EXISTS antinuke_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        punishment TEXT DEFAULT 'ban',
        antibot INTEGER DEFAULT 0,
        antiban INTEGER DEFAULT 0,
        antiban_threshold INTEGER DEFAULT 3,
        antikick INTEGER DEFAULT 0,
        antikick_threshold INTEGER DEFAULT 3,
        antichannel_create INTEGER DEFAULT 0,
        antichannel_delete INTEGER DEFAULT 0,
        antichannel_update INTEGER DEFAULT 0,
        antirole_create INTEGER DEFAULT 0,
        antirole_delete INTEGER DEFAULT 0,
        antirole_update INTEGER DEFAULT 0,
        antiwebhook INTEGER DEFAULT 0,
        antiguild_update INTEGER DEFAULT 0,
        antieveryone INTEGER DEFAULT 0,
        antiprune INTEGER DEFAULT 0,
        antiintegration INTEGER DEFAULT 0,
        log_channel_id INTEGER,
        threshold_window INTEGER DEFAULT 10
    )""",
    """CREATE TABLE IF NOT EXISTS antinuke_whitelist (
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        added_by INTEGER NOT NULL,
        created_at TEXT DEFAULT (datetime('now')),
        PRIMARY KEY (guild_id, user_id)
    )""",
    """CREATE TABLE IF NOT EXISTS antinuke_actions (
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        timestamp TEXT DEFAULT (datetime('now'))
    )""",
    "CREATE INDEX IF NOT EXISTS idx_antinuke_actions ON antinuke_actions(guild_id, user_id, action, timestamp)",


    """CREATE TABLE IF NOT EXISTS logging_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        channel_id INTEGER,
        message_edit INTEGER DEFAULT 1,
        message_delete INTEGER DEFAULT 1,
        member_join INTEGER DEFAULT 1,
        member_leave INTEGER DEFAULT 1,
        member_ban INTEGER DEFAULT 1,
        member_unban INTEGER DEFAULT 1,
        member_update INTEGER DEFAULT 1,
        role_changes INTEGER DEFAULT 1,
        channel_changes INTEGER DEFAULT 1,
        voice_changes INTEGER DEFAULT 1,
        nickname_changes INTEGER DEFAULT 1,
        ignored_channels TEXT DEFAULT '[]',
        ignored_roles TEXT DEFAULT '[]'
    )""",


    """CREATE TABLE IF NOT EXISTS youtube_subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        channel_id_yt TEXT NOT NULL,
        channel_name TEXT,
        notify_channel_id INTEGER NOT NULL,
        notify_role_id INTEGER,
        custom_message TEXT,
        last_video_id TEXT,
        last_check TEXT,
        UNIQUE(guild_id, channel_id_yt)
    )""",


    """CREATE TABLE IF NOT EXISTS minecraft_servers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        message_id INTEGER,
        server_ip TEXT NOT NULL,
        server_port INTEGER,
        server_type TEXT DEFAULT 'java',
        setup_by INTEGER NOT NULL,
        auto_refresh INTEGER DEFAULT 1,
        created_at TEXT DEFAULT (datetime('now')),
        UNIQUE(guild_id, server_ip)
    )""",


    """CREATE TABLE IF NOT EXISTS ai_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        channel_id INTEGER,
        persona TEXT DEFAULT 'You are a helpful Discord bot assistant.',
        cooldown INTEGER DEFAULT 5,
        max_history INTEGER DEFAULT 20,
        auto_respond INTEGER DEFAULT 0,
        moderate_responses INTEGER DEFAULT 1
    )""",
    """CREATE TABLE IF NOT EXISTS ai_conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
    "CREATE INDEX IF NOT EXISTS idx_ai_conv ON ai_conversations(guild_id, user_id)",


    """CREATE TABLE IF NOT EXISTS economy (
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        wallet INTEGER DEFAULT 0,
        bank INTEGER DEFAULT 0,
        last_daily TEXT,
        last_work TEXT,
        PRIMARY KEY (guild_id, user_id)
    )""",


    """CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        guild_id INTEGER,
        message TEXT NOT NULL,
        remind_at TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
    )""",


    """CREATE TABLE IF NOT EXISTS suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message_id INTEGER,
        channel_id INTEGER,
        content TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        response TEXT,
        responded_by INTEGER,
        created_at TEXT DEFAULT (datetime('now'))
    )""",


    """CREATE TABLE IF NOT EXISTS custom_commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        response TEXT NOT NULL,
        embed_json TEXT,
        created_by INTEGER NOT NULL,
        uses INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now')),
        UNIQUE(guild_id, name)
    )""",


    """CREATE TABLE IF NOT EXISTS sticky_messages (
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL PRIMARY KEY,
        content TEXT NOT NULL,
        embed_json TEXT,
        message_id INTEGER,
        counter INTEGER DEFAULT 0,
        threshold INTEGER DEFAULT 5
    )""",


    """CREATE TABLE IF NOT EXISTS user_settings (
        user_id INTEGER PRIMARY KEY,
        noprefix INTEGER DEFAULT 0,
        badges TEXT DEFAULT '[]'
    )""",


    """CREATE TABLE IF NOT EXISTS polls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        message_id INTEGER,
        creator_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        options TEXT NOT NULL,
        votes TEXT DEFAULT '{}',
        ends_at TEXT,
        ended INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now'))
    )""",


    """CREATE TABLE IF NOT EXISTS starboard_entries (
        original_message_id INTEGER PRIMARY KEY,
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        starboard_message_id INTEGER,
        star_count INTEGER DEFAULT 0,
        author_id INTEGER NOT NULL
    )""",


    """CREATE TABLE IF NOT EXISTS blacklist (
        user_id INTEGER PRIMARY KEY,
        reason TEXT,
        blacklisted_by INTEGER,
        created_at TEXT DEFAULT (datetime('now'))
    )""",


    """CREATE TABLE IF NOT EXISTS snipes (
        channel_id INTEGER PRIMARY KEY,
        author_id INTEGER NOT NULL,
        content TEXT,
        attachment_url TEXT,
        deleted_at TEXT DEFAULT (datetime('now'))
    )""",
    """CREATE TABLE IF NOT EXISTS edit_snipes (
        channel_id INTEGER PRIMARY KEY,
        author_id INTEGER NOT NULL,
        before_content TEXT,
        after_content TEXT,
        edited_at TEXT DEFAULT (datetime('now'))
    )""",


    """CREATE TABLE IF NOT EXISTS invite_tracking (
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        inviter_id INTEGER,
        invite_code TEXT,
        joined_at TEXT DEFAULT (datetime('now')),
        PRIMARY KEY (guild_id, user_id)
    )""",
    """CREATE TABLE IF NOT EXISTS invite_counts (
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        total INTEGER DEFAULT 0,
        regular INTEGER DEFAULT 0,
        leaves INTEGER DEFAULT 0,
        fake INTEGER DEFAULT 0,
        PRIMARY KEY (guild_id, user_id)
    )""",


    """CREATE TABLE IF NOT EXISTS gaming_profiles (
        user_id INTEGER PRIMARY KEY,
        minecraft_username TEXT,
        minecraft_uuid TEXT,
        display_name TEXT,
        bio TEXT,
        favorite_games TEXT DEFAULT '[]',
        created_at TEXT DEFAULT (datetime('now'))
    )""",


    """CREATE TABLE IF NOT EXISTS scheduled_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        content TEXT,
        embed_json TEXT,
        cron_expression TEXT,
        next_run TEXT,
        created_by INTEGER NOT NULL,
        enabled INTEGER DEFAULT 1,
        created_at TEXT DEFAULT (datetime('now'))
    )""",


    """CREATE TABLE IF NOT EXISTS vanity_roles (
        guild_id INTEGER PRIMARY KEY,
        vanity TEXT,
        role_id INTEGER,
        log_channel_id INTEGER
    )""",


    """CREATE TABLE IF NOT EXISTS j2c_config (
        guild_id INTEGER PRIMARY KEY,
        join_channel_id INTEGER,
        control_channel_id INTEGER,
        category_id INTEGER
    )""",


    """CREATE TABLE IF NOT EXISTS join_dm (
        guild_id INTEGER PRIMARY KEY,
        message TEXT
    )""",


    """CREATE TABLE IF NOT EXISTS auto_react (
        guild_id INTEGER NOT NULL,
        trigger TEXT NOT NULL,
        emojis TEXT NOT NULL,
        PRIMARY KEY (guild_id, trigger)
    )""",


    """CREATE TABLE IF NOT EXISTS auto_responder (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        trigger TEXT NOT NULL,
        response TEXT NOT NULL,
        match_type TEXT DEFAULT 'contains',
        created_by INTEGER NOT NULL,
        UNIQUE(guild_id, trigger)
    )""",


    """CREATE TABLE IF NOT EXISTS server_backups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        created_by INTEGER NOT NULL,
        backup_data TEXT NOT NULL,
        description TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )""",


    """CREATE TABLE IF NOT EXISTS mod_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        moderator_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
    "CREATE INDEX IF NOT EXISTS idx_mod_notes_guild_user ON mod_notes(guild_id, user_id)",


    """CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        content TEXT NOT NULL,
        embed_json TEXT,
        created_by INTEGER NOT NULL,
        uses INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now')),
        UNIQUE(guild_id, name)
    )""",


    """CREATE TABLE IF NOT EXISTS tempbans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        moderator_id INTEGER NOT NULL,
        reason TEXT,
        expires_at TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
    "CREATE INDEX IF NOT EXISTS idx_tempbans_expires ON tempbans(expires_at)",


    """CREATE TABLE IF NOT EXISTS form_templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        questions TEXT NOT NULL,
        response_channel_id INTEGER,
        required_role_id INTEGER,
        enabled INTEGER DEFAULT 1,
        created_by INTEGER NOT NULL,
        created_at TEXT DEFAULT (datetime('now')),
        UNIQUE(guild_id, name)
    )""",
    """CREATE TABLE IF NOT EXISTS form_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        form_id INTEGER NOT NULL REFERENCES form_templates(id),
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        answers TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        reviewed_by INTEGER,
        created_at TEXT DEFAULT (datetime('now'))
    )""",


    """CREATE TABLE IF NOT EXISTS role_menus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        message_id INTEGER NOT NULL,
        title TEXT,
        roles TEXT NOT NULL,
        mode TEXT DEFAULT 'toggle',
        max_roles INTEGER DEFAULT 0
    )""",


    """CREATE TABLE IF NOT EXISTS admin_config (
        key TEXT PRIMARY KEY,
        value TEXT
    )""",


    """CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        actor_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        target_type TEXT,
        target_id INTEGER,
        detail TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
    "CREATE INDEX IF NOT EXISTS idx_audit_guild ON audit_log(guild_id, created_at)",


    """CREATE TABLE IF NOT EXISTS guild_backups (
        backup_id TEXT PRIMARY KEY,
        guild_id INTEGER NOT NULL,
        guild_name TEXT NOT NULL,
        created_by INTEGER NOT NULL,
        created_at INTEGER NOT NULL,
        roles_json TEXT,
        categories_json TEXT,
        channels_json TEXT,
        emojis_json TEXT,
        settings_json TEXT,
        notes TEXT
    )""",
    "CREATE INDEX IF NOT EXISTS idx_backups_guild ON guild_backups(guild_id, created_at)",


    """CREATE TABLE IF NOT EXISTS analytics_hourly (
        guild_id INTEGER NOT NULL,
        timestamp_hour INTEGER NOT NULL,
        message_count INTEGER DEFAULT 0,
        active_users INTEGER DEFAULT 0,
        voice_minutes INTEGER DEFAULT 0,
        commands_run INTEGER DEFAULT 0,
        PRIMARY KEY (guild_id, timestamp_hour)
    )""",
    """CREATE TABLE IF NOT EXISTS analytics_channels (
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        message_count INTEGER DEFAULT 0,
        last_active INTEGER DEFAULT 0,
        PRIMARY KEY (guild_id, channel_id)
    )""",


    """CREATE TABLE IF NOT EXISTS autoresponders (
        trigger_id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        trigger_text TEXT NOT NULL,
        response_text TEXT NOT NULL,
        match_mode TEXT DEFAULT 'exact',
        is_embed INTEGER DEFAULT 0,
        embed_color INTEGER,
        cooldown_seconds INTEGER DEFAULT 5,
        delete_trigger INTEGER DEFAULT 0,
        enabled INTEGER DEFAULT 1,
        created_by INTEGER NOT NULL,
        created_at INTEGER NOT NULL,
        uses_count INTEGER DEFAULT 0
    )""",
    "CREATE INDEX IF NOT EXISTS idx_autoresponder_guild ON autoresponders(guild_id)",


    """CREATE TABLE IF NOT EXISTS antiphishing_configs (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 1,
        action TEXT DEFAULT 'timeout',
        timeout_duration INTEGER DEFAULT 3600,
        log_channel_id INTEGER,
        whitelist_json TEXT,
        blacklist_json TEXT,
        alert_staff INTEGER DEFAULT 1
    )""",


    """CREATE TABLE IF NOT EXISTS shop_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER NOT NULL,
        item_type TEXT DEFAULT 'role',
        role_id INTEGER,
        stock INTEGER DEFAULT -1,
        enabled INTEGER DEFAULT 1,
        created_at INTEGER NOT NULL
    )""",
    "CREATE INDEX IF NOT EXISTS idx_shop_guild ON shop_items(guild_id)",
    """CREATE TABLE IF NOT EXISTS user_inventory (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        item_type TEXT NOT NULL,
        quantity INTEGER DEFAULT 1,
        acquired_at INTEGER NOT NULL,
        UNIQUE(guild_id, user_id, item_id)
    )""",
    "CREATE INDEX IF NOT EXISTS idx_inventory_user ON user_inventory(guild_id, user_id)",
    """CREATE TABLE IF NOT EXISTS server_templates (
        id TEXT PRIMARY KEY,
        guild_id INTEGER NOT NULL,
        creator_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        is_public INTEGER DEFAULT 0,
        category TEXT DEFAULT 'general',
        usage_count INTEGER DEFAULT 0,
        data_json TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
    "CREATE INDEX IF NOT EXISTS idx_templates_guild ON server_templates(guild_id)",
    "CREATE INDEX IF NOT EXISTS idx_templates_public ON server_templates(is_public)",
    """CREATE TABLE IF NOT EXISTS antinuke_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        log_channel_id INTEGER,
        quarantine_role_id INTEGER,
        max_channel_deletes INTEGER DEFAULT 3,
        max_role_deletes INTEGER DEFAULT 3,
        max_bans INTEGER DEFAULT 5,
        max_kicks INTEGER DEFAULT 5,
        max_webhook_creates INTEGER DEFAULT 2,
        rate_window_seconds INTEGER DEFAULT 15,
        action_type TEXT DEFAULT 'ban',
        panic_lockdown_enabled INTEGER DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS antinuke_whitelist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        entity_id INTEGER NOT NULL,
        entity_type TEXT DEFAULT 'user',
        created_at TEXT DEFAULT (datetime('now')),
        UNIQUE(guild_id, entity_id)
    )""",
    """CREATE TABLE IF NOT EXISTS antinuke_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        culprit_id INTEGER NOT NULL,
        event_type TEXT NOT NULL,
        details TEXT,
        action_taken TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
    "CREATE INDEX IF NOT EXISTS idx_antinuke_logs_guild ON antinuke_logs(guild_id, created_at)",
    """CREATE TABLE IF NOT EXISTS lockdown_state (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        overwrites_json TEXT NOT NULL,
        locked_at TEXT DEFAULT (datetime('now')),
        UNIQUE(guild_id, channel_id)
    )""",
    """CREATE TABLE IF NOT EXISTS autodm_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        message TEXT,
        embed_json TEXT,
        buttons_json TEXT,
        delay_seconds INTEGER DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS autoping_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        channel_ids TEXT,
        delete_after_seconds INTEGER DEFAULT 5,
        ping_mode TEXT DEFAULT 'ghost',
        message_template TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS advanced_welcome_config (
        guild_id INTEGER PRIMARY KEY,
        multi_channels_json TEXT,
        autorole_delay_minutes INTEGER DEFAULT 0,
        autorole_delay_ids TEXT,
        farewell_enabled INTEGER DEFAULT 0,
        farewell_channel_id INTEGER,
        farewell_message TEXT,
        farewell_embed_json TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS antialt_config (
        guild_id INTEGER PRIMARY KEY,
        enabled INTEGER DEFAULT 0,
        min_age_days INTEGER DEFAULT 7,
        require_avatar INTEGER DEFAULT 0,
        action_type TEXT DEFAULT 'quarantine',
        log_channel_id INTEGER,
        exempt_roles_json TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS antialt_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        account_age_days INTEGER NOT NULL,
        action_taken TEXT NOT NULL,
        reason TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
]


async def run_migrations(db):
    for sql in TABLES:
        await db.execute(sql)
    await db.commit()

    current = await db.fetchval("SELECT MAX(version) FROM schema_version")
    if current is None:
        await db.execute("INSERT INTO schema_version (version) VALUES (?)", (SCHEMA_VERSION,))
        await db.commit()
        log.info("Database schema created (v%d)", SCHEMA_VERSION)
    elif current < SCHEMA_VERSION:
        await _apply_migrations(db, current, SCHEMA_VERSION)
        await db.execute(
            "UPDATE schema_version SET version = ? WHERE version = ?",
            (SCHEMA_VERSION, current),
        )
        await db.commit()
        log.info("Database migrated from v%d to v%d", current, SCHEMA_VERSION)


async def _apply_migrations(db, from_v: int, to_v: int):
    pass

