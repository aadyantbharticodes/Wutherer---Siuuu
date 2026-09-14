"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Shield,
  ShieldAlert,
  Sliders,
  Award,
  Ticket,
  Bot,
  Youtube,
  Gamepad2,
  Terminal,
  Settings,
  ArrowLeft,
  BarChart3,
  MessageSquare,
  Archive,
  Layers,
  UserPlus,
  ShieldCheck,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface SidebarProps {
  guildId: string;
}

const sections = (guildId: string) => [
  {
    label: "Control center",
    links: [
      { name: "Overview", href: `/dashboard/guild/${guildId}`, icon: LayoutDashboard },
      { name: "Analytics", href: `/dashboard/guild/${guildId}/analytics`, icon: BarChart3 },
    ],
  },
  {
    label: "Safety",
    links: [
      { name: "Moderation", href: `/dashboard/guild/${guildId}/moderation`, icon: Shield },
      { name: "Automod", href: `/dashboard/guild/${guildId}/automod`, icon: Sliders },
      { name: "Antinuke", href: `/dashboard/guild/${guildId}/antinuke`, icon: ShieldAlert },
      { name: "Verification", href: `/dashboard/guild/${guildId}/verification`, icon: ShieldCheck },
    ],
  },
  {
    label: "Engagement",
    links: [
      { name: "Onboarding", href: `/dashboard/guild/${guildId}/onboarding`, icon: UserPlus },
      { name: "Leveling", href: `/dashboard/guild/${guildId}/leveling`, icon: Award },
      { name: "Tickets", href: `/dashboard/guild/${guildId}/tickets`, icon: Ticket },
    ],
  },
  {
    label: "Automation",
    links: [
      { name: "Auto-responder", href: `/dashboard/guild/${guildId}/autoresponder`, icon: MessageSquare },
      { name: "AI", href: `/dashboard/guild/${guildId}/ai`, icon: Bot },
      { name: "Custom commands", href: `/dashboard/guild/${guildId}/automation`, icon: Terminal },
    ],
  },
  {
    label: "Connections",
    links: [
      { name: "YouTube", href: `/dashboard/guild/${guildId}/youtube`, icon: Youtube },
      { name: "Minecraft", href: `/dashboard/guild/${guildId}/minecraft`, icon: Gamepad2 },
    ],
  },
  {
    label: "Server",
    links: [
      { name: "Settings", href: `/dashboard/guild/${guildId}/settings`, icon: Settings },
      { name: "Templates", href: `/dashboard/guild/${guildId}/templates`, icon: Layers },
      { name: "Backups", href: `/dashboard/guild/${guildId}/backup`, icon: Archive },
    ],
  },
];

export function Sidebar({ guildId }: SidebarProps) {
  const pathname = usePathname();
  const [query, setQuery] = useState("");
  const navSections = useMemo(() => {
    const term = query.trim().toLowerCase();
    return sections(guildId)
      .map((section) => ({ ...section, links: section.links.filter((link) => !term || link.name.toLowerCase().includes(term)) }))
      .filter((section) => section.links.length > 0);
  }, [guildId, query]);

  return (
    <aside className="w-full shrink-0 border-b border-card-border bg-secondary lg:sticky lg:top-16 lg:h-[calc(100vh-4rem)] lg:w-64 lg:border-b-0 lg:border-r lg:overflow-y-auto">
      <div className="px-3 pt-3 pb-3">
        <Link
          href="/dashboard"
          className="flex h-8 items-center gap-2 rounded-md px-2 text-xs font-medium text-slate-400 transition-colors hover:bg-surface-hover hover:text-white"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          <span>Switch Server</span>
        </Link>
        <label className="relative mt-2 block">
          <span className="sr-only">Search server tools</span>
          <Terminal className="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-slate-500" aria-hidden="true" />
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Find a tool"
            className="h-8 w-full rounded-md border border-card-border bg-surface py-1 pl-8 pr-2 text-xs text-white outline-none placeholder:text-slate-600 focus:border-primary"
          />
        </label>
      </div>

      <nav className="grid grid-cols-2 gap-x-3 gap-y-4 px-3 pb-4 sm:grid-cols-3 lg:block lg:space-y-4" aria-label="Server controls">
        {navSections.map((section, idx) => (
          <section key={idx}>
            <div className="px-2 pb-1.5">
              <span className="text-[10px] font-semibold uppercase tracking-[0.14em] text-slate-600">
                {section.label}
              </span>
            </div>
            <div className="space-y-0.5">
              {section.links.map((link) => {
                const Icon = link.icon;
                const isActive = pathname === link.href;
                return (
                  <Link
                    key={link.name}
                    href={link.href}
                    className={cn(
                      "flex min-h-8 items-center gap-2.5 rounded-md px-2.5 py-1.5 text-[13px] font-medium transition-colors",
                      isActive
                        ? "bg-primary-subtle text-primary-light"
                        : "text-slate-400 hover:bg-surface-hover hover:text-white"
                    )}
                  >
                    <Icon className={cn("h-3.5 w-3.5 shrink-0", isActive ? "text-primary-light" : "text-slate-500")} />
                    <span>{link.name}</span>
                  </Link>
                );
              })}
            </div>
          </section>
        ))}
        {navSections.length === 0 && <p className="px-2 text-xs text-slate-500">No installed tools match that search.</p>}
      </nav>
    </aside>
  );
}
