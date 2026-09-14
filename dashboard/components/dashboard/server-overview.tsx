"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ArrowRight, BarChart3, MessageSquare, Settings, ShieldCheck, Users } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { api } from "@/lib/api";

type OverviewData = {
  guild: any;
  automod: any | null;
  verification: any | null;
  tickets: any | null;
  ai: any | null;
  analytics: any | null;
  cases: any[] | null;
};

const moduleState = (config: any | null, label: string) => {
  if (!config) return { label: "Unavailable", variant: "default" as const };
  return { label: config.enabled === 1 ? "Enabled" : label, variant: config.enabled === 1 ? "success" as const : "default" as const };
};

export function ServerOverview() {
  const params = useParams();
  const guildId = params.guildId as string;
  const [data, setData] = useState<OverviewData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const load = async () => {
    setLoading(true);
    setError(false);
    try {
      const guild = await api.getGuildDetails(guildId);
      const results = await Promise.allSettled([
        api.getAutomodConfig(guildId),
        api.getVerificationConfig(guildId),
        api.getTicketConfig(guildId),
        api.getAIConfig(guildId),
        api.getAnalytics(guildId),
        api.getModerationCases(guildId),
      ]);
      const value = (index: number) => results[index].status === "fulfilled" ? results[index].value : null;
      setData({ guild, automod: value(0), verification: value(1), tickets: value(2), ai: value(3), analytics: value(4), cases: value(5) });
    } catch {
      setData(null);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { if (guildId) load(); }, [guildId]);

  if (loading) return <div className="space-y-5 animate-pulse"><div className="h-20 rounded-lg border border-card-border bg-surface" /><div className="grid gap-3 md:grid-cols-3">{[1, 2, 3].map((item) => <div key={item} className="h-28 rounded-lg border border-card-border bg-surface" />)}</div></div>;
  if (error || !data) return <Card><EmptyState icon={ShieldCheck} title="Server details unavailable" description="The bot API did not return this server’s details. Confirm the bot is online, then refresh the control center." action={<Button size="sm" onClick={load}>Try again</Button>} /></Card>;

  const { guild } = data;
  const cards = [
    { title: "Automod", detail: "Message filters and penalties", href: "automod", state: moduleState(data.automod, "Not enabled") },
    { title: "Verification", detail: "New-member CAPTCHA gate", href: "verification", state: moduleState(data.verification, "Not enabled") },
    { title: "Tickets", detail: "Private support channels", href: "tickets", state: moduleState(data.tickets, "Not enabled") },
    { title: "AI", detail: "Assistant channel controls", href: "ai", state: moduleState(data.ai, "Not enabled") },
  ];
  const totals = data.analytics?.totals;
  const cases = Array.isArray(data.cases) ? data.cases.slice(0, 4) : [];

  return <div className="space-y-6">
    <section className="flex flex-col gap-4 border-b border-card-border pb-5 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex min-w-0 items-center gap-3.5">
        {guild.icon ? <img src={guild.icon} alt="" className="h-12 w-12 rounded-xl object-cover" /> : <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary-subtle text-lg font-semibold text-primary-light">{guild.name.charAt(0)}</div>}
        <div className="min-w-0"><p className="text-xs font-medium text-primary-light">Server control center</p><h1 className="truncate text-xl font-semibold tracking-tight text-white">{guild.name}</h1><p className="mt-1 flex items-center gap-1.5 text-xs text-slate-500"><Users className="h-3.5 w-3.5" aria-hidden="true" />{guild.member_count.toLocaleString()} members <span className="text-slate-700">·</span> Prefix <code className="rounded bg-surface px-1.5 py-0.5 text-primary-light">{guild.settings?.prefix || "w!"}</code></p></div>
      </div>
      <Link href={`/dashboard/guild/${guildId}/settings`}><Button size="sm" variant="secondary" className="gap-1.5"><Settings className="h-3.5 w-3.5" aria-hidden="true" />Server settings</Button></Link>
    </section>

    <section className="grid gap-3 md:grid-cols-[1.2fr_1fr_1fr]">
      <Card className="border-primary/20 bg-gradient-to-br from-primary-subtle to-card">
        <div className="flex items-center justify-between"><p className="text-xs font-medium text-slate-400">Bot connection</p><ShieldCheck className="h-4 w-4 text-primary" aria-hidden="true" /></div>
        <p className="mt-5 text-lg font-semibold text-white">Connected to this server</p>
        <p className="mt-1 text-xs leading-relaxed text-slate-400">Wutherer returned live server details and its installed controls are ready to configure.</p>
      </Card>
      <Card><p className="text-xs font-medium text-slate-400">Messages recorded</p><p className="mt-4 text-2xl font-semibold tracking-tight text-white">{totals ? totals.total_messages.toLocaleString() : "—"}</p><p className="mt-1 text-xs text-slate-500">{totals ? "All-time analytics total" : "Analytics are not available"}</p></Card>
      <Card><p className="text-xs font-medium text-slate-400">Commands processed</p><p className="mt-4 text-2xl font-semibold tracking-tight text-white">{totals ? totals.total_commands.toLocaleString() : "—"}</p><p className="mt-1 text-xs text-slate-500">{totals ? "All-time analytics total" : "Analytics are not available"}</p></Card>
    </section>

    <section className="grid gap-6 xl:grid-cols-[1.25fr_0.75fr]">
      <div><div className="mb-3 flex items-center justify-between"><div><h2 className="text-sm font-semibold text-white">Installed controls</h2><p className="mt-1 text-xs text-slate-500">Configuration state from the bot API.</p></div><Link href={`/dashboard/guild/${guildId}/automod`} className="text-xs font-semibold text-primary-light hover:text-white">View safety <ArrowRight className="inline h-3.5 w-3.5" aria-hidden="true" /></Link></div>
        <div className="divide-y divide-card-border overflow-hidden rounded-lg border border-card-border bg-card">{cards.map((card) => <Link key={card.title} href={`/dashboard/guild/${guildId}/${card.href}`} className="flex items-center gap-3 px-4 py-3.5 transition-colors hover:bg-surface-hover/60"><div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-surface text-primary-light"><Settings className="h-3.5 w-3.5" aria-hidden="true" /></div><div className="min-w-0 flex-1"><p className="text-sm font-medium text-white">{card.title}</p><p className="mt-0.5 text-xs text-slate-500">{card.detail}</p></div><Badge variant={card.state.variant}>{card.state.label}</Badge></Link>)}</div>
      </div>
      <div><div className="mb-3"><h2 className="text-sm font-semibold text-white">Recent moderation</h2><p className="mt-1 text-xs text-slate-500">Latest recorded enforcement actions.</p></div><Card className="p-0">{cases.length ? <div className="divide-y divide-card-border">{cases.map((item) => <div key={item.id} className="px-4 py-3"><div className="flex items-center justify-between gap-3"><p className="text-xs font-semibold text-white">{item.action || "Moderation action"}</p><span className="text-[11px] text-slate-500">#{item.id}</span></div><p className="mt-1 truncate text-xs text-slate-400">{item.reason || "No reason provided"}</p></div>)}</div> : <EmptyState className="py-7" icon={MessageSquare} title="No recorded cases" description="New moderation actions will appear here when the bot records them." />}</Card></div>
    </section>

    <section className="border-t border-card-border pt-5"><Link href={`/dashboard/guild/${guildId}/analytics`} className="inline-flex items-center gap-2 text-sm font-semibold text-primary-light hover:text-white"><BarChart3 className="h-4 w-4" aria-hidden="true" />Open full analytics <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" /></Link></section>
  </div>;
}
