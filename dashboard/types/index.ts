export interface Guild {
  id: string;
  name: string;
  icon: string | null;
  member_count: number;
  owner_id: string;
}

export interface GuildSettings {
  guild_id: number;
  prefix: string;
  language: string;
  log_channel_id?: number;
  mod_log_channel_id?: number;
  suggestion_channel_id?: number;
  starboard_channel_id?: number;
  starboard_threshold?: number;
}

export interface AutomodConfig {
  antispam: number;
  anticaps: number;
  antilink: number;
  antiinvite: number;
  antimention: number;
  punishment: string;
}

export interface AntinukeConfig {
  enabled: number;
  punishment: string;
  antibot: number;
  antiban: number;
  antikick: number;
  antichannel_create: number;
  antichannel_delete: number;
}

export interface LevelingConfig {
  enabled: number;
  channel_id?: number;
  announce_levelup: number;
  xp_rate: number;
}

export interface TicketConfig {
  enabled: number;
  category_id?: number;
  log_channel_id?: number;
  support_role_id?: number;
  greeting: string;
  max_open: number;
}

export interface VerificationConfig {
  enabled: number;
  channel_id?: number;
  role_id?: number;
  difficulty: string;
}

export interface AIConfig {
  enabled: number;
  channel_id?: number;
  persona: string;
  cooldown: number;
}

export interface BackupSnapshot {
  backup_id: string;
  guild_id: number;
  guild_name: string;
  created_by: number;
  created_at: number;
  roles_count: number;
  channels_count: number;
  categories_count: number;
  notes?: string;
}

export interface AnalyticsData {
  guild_id: number;
  totals: {
    total_messages: number;
    total_voice_minutes: number;
    total_commands: number;
  };
  hourly_24h: Array<{
    timestamp: number;
    messages: number;
    voice_minutes: number;
    commands: number;
  }>;
}

export interface AutoResponseTrigger {
  trigger_id: number;
  trigger_text: string;
  response_text: string;
  match_mode: string;
  is_embed: boolean;
  cooldown_seconds: number;
  delete_trigger: boolean;
  enabled: boolean;
  uses_count: number;
}

export interface ShopItem {
  item_id: number;
  guild_id: number;
  name: string;
  description: string;
  price: number;
  item_type: string;
  role_id?: number;
  stock: number;
  enabled: boolean;
}


