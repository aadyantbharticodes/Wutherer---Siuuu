"use client";

import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { SectionHeader } from "@/components/ui/section-header";
import { DataTable } from "@/components/dashboard/data-table";
import { Alert } from "@/components/ui/alert";
import { Terminal } from "lucide-react";
import { cn } from "@/lib/utils";

type CommandEntry = {
  id: string;
  name: string;
  usage: string;
  category: string;
  permission: string;
  description: string;
};

const CATALOG: CommandEntry[] = [
  { id: "ban", name: "ban", usage: "<user> [duration] [reason]", category: "Moderation", permission: "Ban Members", description: "Ban a member with optional duration and logging." },
  { id: "unban", name: "unban", usage: "<user_id> [reason]", category: "Moderation", permission: "Ban Members", description: "Unban a user by ID." },
  { id: "softban", name: "softban", usage: "<user> [reason]", category: "Moderation", permission: "Ban Members", description: "Ban and immediately unban to purge recent messages." },
  { id: "kick", name: "kick", usage: "<user> [reason]", category: "Moderation", permission: "Kick Members", description: "Eject a member from the server." },
  { id: "timeout", name: "timeout", usage: "<user> <duration> [reason]", category: "Moderation", permission: "Moderate Members", description: "Apply a native timeout such as 10m, 2h, or 1d." },
  { id: "untimeout", name: "untimeout", usage: "<user>", category: "Moderation", permission: "Moderate Members", description: "Remove an active timeout." },
  { id: "warn", name: "warn", usage: "<user> <reason>", category: "Moderation", permission: "Moderate Members", description: "Issue a formal warning record." },
  { id: "warnings", name: "warnings", usage: "<user>", category: "Moderation", permission: "Moderate Members", description: "View recorded infractions for a user." },
  { id: "purge", name: "purge", usage: "<amount>", category: "Moderation", permission: "Manage Messages", description: "Bulk delete messages, up to 100 at once." },
  { id: "lock", name: "lock", usage: "[channel]", category: "Moderation", permission: "Manage Channels", description: "Lock a channel for regular members." },
  { id: "unlock", name: "unlock", usage: "[channel]", category: "Moderation", permission: "Manage Channels", description: "Reopen a locked channel." },
  { id: "slowmode", name: "slowmode", usage: "<seconds> [channel]", category: "Moderation", permission: "Manage Channels", description: "Adjust channel slowmode delay." },
  { id: "nuke", name: "nuke", usage: "[channel]", category: "Moderation", permission: "Manage Channels", description: "Clone and clear a channel to wipe history." },
  { id: "automod-cmd", name: "automod", usage: "<status/toggle/rules>", category: "Moderation", permission: "Administrator", description: "Configure spam, link, invite, and caps filters." },
  { id: "antinuke-cmd", name: "antinuke", usage: "<on/off/whitelist>", category: "Moderation", permission: "Server Owner", description: "Configure anti-raid defense." },
  { id: "setprefix", name: "setprefix", usage: "<prefix>", category: "Server", permission: "Administrator", description: "Customize the server command prefix." },
  { id: "welcome", name: "welcome", usage: "channel | message", category: "Server", permission: "Administrator", description: "Set up join greeting messages." },
  { id: "verification-setup", name: "verification setup", usage: "", category: "Server", permission: "Administrator", description: "Deploy the CAPTCHA verification panel." },
  { id: "ticket-setup", name: "ticket setup", usage: "", category: "Server", permission: "Administrator", description: "Create interactive support ticket panels." },
  { id: "autorole", name: "autorole", usage: "add | remove", category: "Server", permission: "Administrator", description: "Automatic role assignment on join." },
  { id: "cc", name: "cc", usage: "add | delete | list", category: "Server", permission: "Administrator", description: "Server-defined custom text responses." },
  { id: "sticky", name: "sticky", usage: "set | remove", category: "Server", permission: "Administrator", description: "Keep a message pinned to the bottom of busy chats." },
  { id: "rank", name: "rank", usage: "[member]", category: "Community", permission: "Everyone", description: "Show XP progression and rank card." },
  { id: "leaderboard", name: "leaderboard", usage: "", category: "Community", permission: "Everyone", description: "Show the server XP leaderboard." },
  { id: "giveaway", name: "g start", usage: "<time> <winners> <prize>", category: "Community", permission: "Moderator", description: "Timed giveaways with automated drawing." },
  { id: "poll", name: "poll", usage: "<question> <options…>", category: "Community", permission: "Everyone", description: "Multi-option voting polls." },
  { id: "suggest", name: "suggest", usage: "<text>", category: "Community", permission: "Everyone", description: "Submit a community suggestion." },
  { id: "ai-ask", name: "ai ask", usage: "<prompt>", category: "AI", permission: "Everyone", description: "Chat with the assistant with memory." },
  { id: "ai-clear", name: "ai clear", usage: "", category: "AI", permission: "Everyone", description: "Clear personal conversation memory." },
  { id: "ai-summarize", name: "ai summarize", usage: "<text>", category: "AI", permission: "Everyone", description: "Summarize long text into key points." },
  { id: "ai-translate", name: "ai translate", usage: "<language> <text>", category: "AI", permission: "Everyone", description: "Translate text into another language." },
  { id: "ai-code", name: "ai code", usage: "<language> <question>", category: "AI", permission: "Everyone", description: "Coding help and bug-fix guidance." },
  { id: "mc-server", name: "mc server", usage: "<ip> [java/bedrock]", category: "Gaming", permission: "Everyone", description: "Live server ping, players, and version." },
  { id: "mc-skin", name: "mc skin", usage: "<player>", category: "Gaming", permission: "Everyone", description: "Player skin render and avatar." },
  { id: "yt-channel", name: "yt channel", usage: "<query>", category: "Gaming", permission: "Everyone", description: "Channel subscribers and video totals." },
  { id: "yt-subscribe", name: "yt subscribe", usage: "<channel_id>", category: "Gaming", permission: "Administrator", description: "Automatic upload notifications." },
  { id: "balance", name: "balance", usage: "[member]", category: "Economy", permission: "Everyone", description: "View wallet, bank, and net worth." },
  { id: "daily", name: "daily", usage: "", category: "Economy", permission: "Everyone", description: "Claim the daily reward." },
  { id: "work", name: "work", usage: "", category: "Economy", permission: "Everyone", description: "Work a shift for credits." },
  { id: "pay", name: "pay", usage: "<member> <amount>", category: "Economy", permission: "Everyone", description: "Transfer credits to another member." },
  { id: "shop", name: "shop", usage: "", category: "Economy", permission: "Everyone", description: "Display the server store catalog." },
  { id: "buy", name: "buy", usage: "<item_id>", category: "Economy", permission: "Everyone", description: "Purchase an item with wallet credits." },
  { id: "ping", name: "ping", usage: "", category: "Utility", permission: "Everyone", description: "Check bot latency and uptime." },
  { id: "serverinfo", name: "serverinfo", usage: "", category: "Utility", permission: "Everyone", description: "Show server details and counts." },
  { id: "userinfo", name: "userinfo", usage: "[member]", category: "Utility", permission: "Everyone", description: "Show member details and roles." },
  { id: "remindme", name: "remindme", usage: "<time> <message>", category: "Utility", permission: "Everyone", description: "Schedule a personal reminder." },
  { id: "calc", name: "calc", usage: "<expression>", category: "Utility", permission: "Everyone", description: "Evaluate a math expression." },
  { id: "backup-create", name: "backup create", usage: "[notes]", category: "Backups", permission: "Administrator", description: "Snapshot roles, channels, and permissions." },
  { id: "backup-list", name: "backup list", usage: "", category: "Backups", permission: "Administrator", description: "List stored snapshots for this server." },
  { id: "backup-restore", name: "backup restore", usage: "<backup_id>", category: "Backups", permission: "Server Owner", description: "Recreate missing roles and channels." },
  { id: "stats-overview", name: "stats overview", usage: "", category: "Analytics", permission: "Everyone", description: "24-hour message, voice, and command totals." },
  { id: "autoresponder-add", name: "autoresponder add", usage: "<trigger> | <response>", category: "Automation", permission: "Administrator", description: "Create an automated trigger response." },
  { id: "antiphishing-scan", name: "antiphishing scan", usage: "<url>", category: "Automation", permission: "Everyone", description: "Test a URL against link protection." },
];

const CATEGORIES = ["All", ...Array.from(new Set(CATALOG.map((c) => c.category)))];

export default function CommandsPage() {
  const [category, setCategory] = useState("All");
  const rows = useMemo(
    () => (category === "All" ? CATALOG : CATALOG.filter((c) => c.category === category)),
    [category]
  );

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Commands"
        description="The real command set shipped with the bot. Run these in Discord with your server prefix — per-command toggles are not exposed by the bot API."
      />

      <Alert variant="info">
        Reference catalog from the bot&apos;s documented modules. Prefix defaults to your server&apos;s
        configured prefix (see Server settings). This list is descriptive — enabling or disabling
        individual commands is managed through Discord permissions, not this dashboard.
      </Alert>

      <div className="flex flex-wrap gap-2" aria-label="Command categories">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setCategory(cat)}
            aria-pressed={category === cat}
            className={cn(
              "inline-flex h-8 items-center rounded-full border px-3 text-xs font-medium transition-colors",
              category === cat
                ? "border-primary/40 bg-primary-subtle text-primary"
                : "border-card-border bg-surface text-slate-400 hover:text-white"
            )}
          >
            {cat}
          </button>
        ))}
      </div>

      <DataTable<CommandEntry>
        rows={rows}
        getRowKey={(row) => row.id}
        searchPlaceholder="Search commands or descriptions…"
        searchKeys={(row) => `${row.name} ${row.description} ${row.usage}`}
        emptyTitle="No commands"
        emptyDescription="No documented commands match this category."
        emptyIcon={Terminal}
        columns={[
          {
            key: "name",
            header: "Command",
            render: (row) => (
              <span className="rounded border border-primary/20 bg-primary-subtle px-1.5 py-0.5 font-mono text-xs font-semibold text-primary-light">
                {row.name}
              </span>
            ),
          },
          {
            key: "usage",
            header: "Usage",
            render: (row) => (
              <span className="font-mono text-[11px] text-slate-400">{row.usage || "—"}</span>
            ),
          },
          {
            key: "category",
            header: "Category",
            render: (row) => <Badge variant="default">{row.category}</Badge>,
          },
          {
            key: "description",
            header: "Description",
            render: (row) => <span className="block min-w-48 text-slate-300">{row.description}</span>,
          },
          {
            key: "permission",
            header: "Permission",
            align: "right",
            render: (row) => <span className="whitespace-nowrap text-slate-500">{row.permission}</span>,
          },
        ]}
      />

      <p className="text-[11px] leading-relaxed text-slate-600">
        Custom server responses live under Automation → Custom commands, and pattern triggers live under
        Automation → Auto-responder. Both are stored through the bot API.
      </p>
    </div>
  );
}
