"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { Users, ArrowRight, Server, Terminal, RefreshCw, Settings } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { SectionHeader } from "@/components/ui/section-header";
import { EmptyState } from "@/components/ui/empty-state";
import { api } from "@/lib/api";
import { Guild } from "@/types";

export default function DashboardServerSelector() {
  const [guilds, setGuilds] = useState<Guild[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [query, setQuery] = useState("");

  const loadGuilds = () => {
    setLoading(true);
    setError(false);
    api.getGuilds()
      .then((data) => setGuilds(data))
      .catch(() => {
        setGuilds([]);
        setError(true);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => { loadGuilds(); }, []);

  const visibleGuilds = useMemo(() => {
    const term = query.trim().toLowerCase();
    return guilds.filter((guild) => !term || guild.name.toLowerCase().includes(term));
  }, [guilds, query]);

  return (
    <div className="mx-auto w-full max-w-7xl px-4 py-7 sm:px-6 lg:px-8">
      <SectionHeader
        title="Your servers"
        description="Choose a server where Wutherer is available to manage its installed controls."
        action={<Button variant="outline" size="sm" onClick={loadGuilds} disabled={loading} className="gap-1.5"><RefreshCw className="h-3.5 w-3.5" aria-hidden="true" />Refresh</Button>}
      />

      <div className="mt-6">
        {!loading && guilds.length > 0 && <label className="relative mb-4 block max-w-sm"><span className="sr-only">Search your servers</span><Terminal className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" aria-hidden="true" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search servers" className="h-9 w-full rounded-md border border-card-border bg-surface py-2 pl-9 pr-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-primary" /></label>}

        {loading ? (
          <div className="divide-y divide-card-border rounded-lg border border-card-border bg-card animate-pulse">{[1, 2, 3].map((i) => <div key={i} className="h-[76px] bg-surface/30" />)}</div>
        ) : error ? (
          <Card><EmptyState icon={Server} title="Server list unavailable" description="Wutherer could not reach the bot API. Check that the bot service is running, then try again." action={<Button size="sm" onClick={loadGuilds}>Try again</Button>} /></Card>
        ) : guilds.length === 0 ? (
          <Card><EmptyState icon={Server} title="No servers are available" description="Wutherer only shows servers where its bot account is present. Add the bot to a server, verify it is online, then refresh this page." action={<a href="https://discord.com" target="_blank" rel="noreferrer"><Button size="sm">Open Discord</Button></a>} /></Card>
        ) : visibleGuilds.length === 0 ? (
          <Card><EmptyState icon={Terminal} title="No server matches" description="Try a different server name, or clear the search to view all available servers." /></Card>
        ) : (
          <div className="overflow-hidden rounded-lg border border-card-border bg-card">
            <div className="hidden grid-cols-[minmax(0,1fr)_10rem_9rem] gap-4 border-b border-card-border bg-surface px-5 py-2 text-[10px] font-semibold uppercase tracking-[0.12em] text-slate-500 sm:grid"><span>Server</span><span>Members</span><span className="text-right">Access</span></div>
            <div className="divide-y divide-card-border">
              {visibleGuilds.map((guild) => <div key={guild.id} className="grid gap-3 px-4 py-4 transition-colors hover:bg-surface-hover/40 sm:grid-cols-[minmax(0,1fr)_10rem_9rem] sm:items-center sm:px-5">
                <div className="flex min-w-0 items-center gap-3">{guild.icon ? <img src={guild.icon} alt="" className="h-10 w-10 rounded-lg object-cover" /> : <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-subtle text-sm font-semibold text-primary-light">{guild.name.charAt(0)}</div>}<div className="min-w-0"><p className="truncate text-sm font-semibold text-white">{guild.name}</p><p className="mt-0.5 flex items-center gap-1 text-xs text-slate-500"><Settings className="h-3 w-3" aria-hidden="true" />Available to configure</p></div></div>
                <p className="flex items-center gap-1.5 text-xs text-slate-400"><Users className="h-3.5 w-3.5 text-slate-500" aria-hidden="true" />{guild.member_count.toLocaleString()} members</p>
                <Link href={`/dashboard/guild/${guild.id}`} className="sm:justify-self-end"><Button className="w-full gap-1.5 sm:w-auto" size="sm" variant="secondary">Manage <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" /></Button></Link>
              </div>)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
