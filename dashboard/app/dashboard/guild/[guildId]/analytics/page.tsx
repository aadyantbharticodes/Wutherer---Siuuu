"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/ui/empty-state";
import { SectionHeader } from "@/components/ui/section-header";
import { api } from "@/lib/api";
import { AnalyticsData } from "@/types";
import { BarChart3, RefreshCw } from "lucide-react";

export default function AnalyticsPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  async function loadStats() {
      setLoading(true);
      setError(false);
      try {
        const res = await api.getAnalytics(guildId);
        setData(res);
      } catch {
        setData(null);
        setError(true);
      } finally {
        setLoading(false);
      }
  }

  useEffect(() => {
    if (guildId) {
      loadStats();
    }
  }, [guildId]);

  if (loading) {
    return (
      <div className="space-y-4 animate-pulse">
        <div className="h-8 w-48 bg-surface rounded-md border border-card-border" />
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-20 bg-surface rounded-md border border-card-border" />
          ))}
        </div>
      </div>
    );
  }

  if (error || !data) {
    return <div className="space-y-5"><SectionHeader title="Analytics" description="Recorded activity from Wutherer’s analytics service." /><Card><EmptyState icon={BarChart3} title="Analytics are unavailable" description="The bot API could not return activity for this server. Check the service connection and retry." action={<Button size="sm" onClick={loadStats}>Try again</Button>} /></Card></div>;
  }

  const totals = data?.totals || { total_messages: 0, total_voice_minutes: 0, total_commands: 0 };
  const hourly = data?.hourly_24h || [];
  const maxMsgs = Math.max(...hourly.map((h) => h.messages), 1);

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Analytics"
        description="Activity recorded by Wutherer across this server."
        action={<Button size="sm" variant="outline" onClick={loadStats} className="gap-1.5"><RefreshCw className="h-3.5 w-3.5" aria-hidden="true" />Refresh</Button>}
      />

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <Card>
          <span className="text-xs font-medium text-slate-400">All-Time Messages</span>
          <div className="text-xl font-semibold text-white mt-1">
            {totals.total_messages.toLocaleString()}
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Total conversation events across channels</p>
        </Card>

        <Card>
          <span className="text-xs font-medium text-slate-400">Voice Activity</span>
          <div className="text-xl font-semibold text-white mt-1">
            {(totals.total_voice_minutes / 60).toFixed(1)} hrs
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Accumulated member voice presence</p>
        </Card>

        <Card>
          <span className="text-xs font-medium text-slate-400">Commands Processed</span>
          <div className="text-xl font-semibold text-white mt-1">
            {totals.total_commands.toLocaleString()}
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Dispatched automations and bot actions</p>
        </Card>
      </div>

      {hourly.length > 0 ? <Card>
        <CardHeader>
          <CardTitle>24-Hour Message Activity</CardTitle>
          <CardDescription>Hourly distribution of recorded message traffic</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-36 flex items-end gap-1 pt-4 pb-1 border-b border-card-border">
            {hourly.map((h, idx) => {
              const heightPercent = Math.max(6, (h.messages / maxMsgs) * 100);
              return (
                <div key={idx} className="flex-1 flex flex-col items-center group relative h-full justify-end">
                  <div
                    style={{ height: `${heightPercent}%` }}
                    className="w-full rounded-t bg-gradient-to-t from-primary/70 to-sky-400/80 group-hover:from-primary group-hover:to-sky-300 transition-colors"
                  />
                  <div className="opacity-0 group-hover:opacity-100 absolute -top-7 bg-surface border border-card-border text-white text-[10px] px-1.5 py-0.5 rounded pointer-events-none whitespace-nowrap z-10 font-mono">
                    {h.messages}
                  </div>
                </div>
              );
            })}
          </div>
          <div className="flex justify-between text-[11px] text-slate-500 mt-2">
            <span>24h ago</span>
            <span>12h ago</span>
            <span>Now</span>
          </div>
        </CardContent>
      </Card> : <Card><EmptyState icon={BarChart3} title="No hourly activity yet" description="Wutherer has not recorded activity in the last 24 hours." /></Card>}
    </div>
  );
}
