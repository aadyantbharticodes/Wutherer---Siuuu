const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080/api";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "wutherer-dashboard-secret-key-change-me";

async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY,
    ...(options.headers || {}),
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

export const api = {
  getBotStats: () => fetchAPI("/bot/stats"),
  getGuilds: () => fetchAPI("/guilds"),
  getGuildDetails: (guildId: string) => fetchAPI(`/guilds/${guildId}`),
  updateGuildSettings: (guildId: string, data: any) =>
    fetchAPI(`/guilds/${guildId}/settings`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  getModerationCases: (guildId: string) => fetchAPI(`/guilds/${guildId}/moderation/cases`),
  getAutomodConfig: (guildId: string) => fetchAPI(`/guilds/${guildId}/moderation/automod`),
  updateAutomodConfig: (guildId: string, data: any) =>
    fetchAPI(`/guilds/${guildId}/moderation/automod`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  getAntinukeConfig: (guildId: string) => fetchAPI(`/guilds/${guildId}/moderation/antinuke`),
  updateAntinukeConfig: (guildId: string, data: any) =>
    fetchAPI(`/guilds/${guildId}/moderation/antinuke`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  getAntinukeStatus: (guildId: string) => fetchAPI(`/antinuke/${guildId}`),
  updateAntinukeStatus: (guildId: string, data: any) =>
    fetchAPI(`/antinuke/${guildId}`, { method: "POST", body: JSON.stringify(data) }),
  getAntinukeLogs: (guildId: string) => fetchAPI(`/antinuke/${guildId}/logs`),
  addAntinukeWhitelist: (guildId: string, entityId: string) =>
    fetchAPI(`/antinuke/${guildId}/whitelist`, { method: "POST", body: JSON.stringify({ entity_id: Number(entityId) }) }),
  removeAntinukeWhitelist: (guildId: string, entityId: string) =>
    fetchAPI(`/antinuke/${guildId}/whitelist/${entityId}`, { method: "DELETE" }),
  setPanicLockdown: (guildId: string, action: "lock" | "unlock") =>
    fetchAPI(`/antinuke/${guildId}/lockdown`, { method: "POST", body: JSON.stringify({ action }) }),
  getLevelingConfig: (guildId: string) => fetchAPI(`/guilds/${guildId}/leveling`),
  updateLevelingConfig: (guildId: string, data: any) =>
    fetchAPI(`/guilds/${guildId}/leveling`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  getTicketConfig: (guildId: string) => fetchAPI(`/guilds/${guildId}/tickets`),
  updateTicketConfig: (guildId: string, data: any) =>
    fetchAPI(`/guilds/${guildId}/tickets`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  getVerificationConfig: (guildId: string) => fetchAPI(`/guilds/${guildId}/verification`),
  updateVerificationConfig: (guildId: string, data: any) =>
    fetchAPI(`/guilds/${guildId}/verification`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  getAIConfig: (guildId: string) => fetchAPI(`/guilds/${guildId}/ai`),
  updateAIConfig: (guildId: string, data: any) =>
    fetchAPI(`/guilds/${guildId}/ai`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  getCustomCommands: (guildId: string) => fetchAPI(`/guilds/${guildId}/automation/commands`),
  createCustomCommand: (guildId: string, name: string, response: string) =>
    fetchAPI(`/guilds/${guildId}/automation/commands`, {
      method: "POST",
      body: JSON.stringify({ name, response }),
    }),
  deleteCustomCommand: (guildId: string, name: string) =>
    fetchAPI(`/guilds/${guildId}/automation/commands/${name}`, {
      method: "DELETE",
    }),
  getYouTubeSubs: (guildId: string) => fetchAPI(`/guilds/${guildId}/youtube`),
  getMinecraftServers: (guildId: string) => fetchAPI(`/guilds/${guildId}/minecraft`),
  getAnalytics: (guildId: string) => fetchAPI(`/guilds/${guildId}/analytics/overview`),
  getBackups: (guildId: string) => fetchAPI(`/guilds/${guildId}/backups`),
  createBackup: (guildId: string, notes: string) =>
    fetchAPI(`/guilds/${guildId}/backups`, { method: "POST", body: JSON.stringify({ notes }) }),
  deleteBackup: (guildId: string, backupId: string) =>
    fetchAPI(`/guilds/${guildId}/backups/${backupId}`, { method: "DELETE" }),
  getAutoResponders: (guildId: string) => fetchAPI(`/guilds/${guildId}/autoresponder/triggers`),
  createAutoResponder: (guildId: string, data: any) =>
    fetchAPI(`/guilds/${guildId}/autoresponder/triggers`, {
      method: "POST",
      body: JSON.stringify(data),
    }),
  deleteAutoResponder: (guildId: string, triggerId: number) =>
    fetchAPI(`/guilds/${guildId}/autoresponder/triggers/${triggerId}`, { method: "DELETE" }),
  createYouTubeSub: (guildId: string, data: any) =>
    fetchAPI(`/guilds/${guildId}/youtube`, { method: "POST", body: JSON.stringify(data) }),
  deleteYouTubeSub: (guildId: string, channelId: string) =>
    fetchAPI(`/guilds/${guildId}/youtube/${encodeURIComponent(channelId)}`, { method: "DELETE" }),
  createMinecraftServer: (guildId: string, data: any) =>
    fetchAPI(`/guilds/${guildId}/minecraft`, { method: "POST", body: JSON.stringify(data) }),
  deleteMinecraftServer: (guildId: string, serverIp: string) =>
    fetchAPI(`/guilds/${guildId}/minecraft/${encodeURIComponent(serverIp)}`, { method: "DELETE" }),
  getOnboarding: (guildId: string) => fetchAPI(`/onboarding/${guildId}`),
  updateAutoDM: (guildId: string, data: any) =>
    fetchAPI(`/onboarding/${guildId}/autodm`, { method: "POST", body: JSON.stringify(data) }),
  updateAutoPing: (guildId: string, data: any) =>
    fetchAPI(`/onboarding/${guildId}/autoping`, { method: "POST", body: JSON.stringify(data) }),
  updateAdvancedWelcome: (guildId: string, data: any) =>
    fetchAPI(`/onboarding/${guildId}/welcome`, { method: "POST", body: JSON.stringify(data) }),
  getPublicTemplates: () => fetchAPI("/templates/public"),
  getGuildTemplates: (guildId: string) => fetchAPI(`/templates/guild/${guildId}`),
  createTemplate: (guildId: string, data: any) =>
    fetchAPI(`/templates/guild/${guildId}/create`, { method: "POST", body: JSON.stringify(data) }),
  applyTemplate: (guildId: string, templateId: string, mode: "merge" | "wipe") =>
    fetchAPI(`/templates/guild/${guildId}/apply/${templateId}`, { method: "POST", body: JSON.stringify({ mode }) }),
  deleteTemplate: (templateId: string) => fetchAPI(`/templates/${templateId}`, { method: "DELETE" }),
  get: (endpoint: string) => fetchAPI(endpoint),
};
