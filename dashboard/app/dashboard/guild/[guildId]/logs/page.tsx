"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { SectionHeader } from "@/components/ui/section-header";
import { DataTable } from "@/components/dashboard/data-table";
import { Alert } from "@/components/ui/alert";
import { RefreshCw, FileText, Shield, ShieldAlert } from "lucide-react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

type Tab = "all" | "moderation" | "security";

type UnifiedLog = {
  id: string;
  source: "moderation" | "security";
  action: string;
  detail: string;
  target: string;
  timestamp: string;
};

export default function LogsPage() {
  const params = useParams();
  const guildId = params.guildId as string;
  const [tab, setTab] = useState<Tab>("all");
  const [cases, setCases] = useState<any[]>([]);
  const [security, setSecurity] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const load = async () => {
    setLoading(true);
    setError(false);
    try {
      const [caseResult, securityResult] = await Promise.allSettled([
        api.getModerationCases(guildId),
        api.getAntinukeLogs(guildId),
      ]);
      setCases(caseResult.status === "fulfilled" && Array.isArray(caseResult.value) ? caseResult.value : []);
      const logs =
        securityResult.status === "fulfilled"
          ? Array.isArray(securityResult.value?.logs)
            ? securityResult.value.logs
            : Array.isArray(securityResult.value)
              ? securityResult.value
              : []
          : [];
      setSecurity(logs);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (guildId) load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [guildId]);

  const rows: UnifiedLog[] = useMemo(() => {
    const modRows: UnifiedLog[] = cases.map((c) => ({
      id: `mod-${c.id}`,
      source: "moderation",
      action: String(c.action ?? "Moderation action"),
      detail: String(c.reason ?? "No reason provided"),
      target: String(c.user_id ?? "—"),
      timestamp: String(c.created_at ?? "—"),
    }));
    const secRows: UnifiedLog[] = security.map((log, index) => ({
      id: `sec-${log.id ?? index}`,
      source: "security",
      action: String(log.event_type ?? log.action_taken ?? "Security event").replaceAll("_", " "),
      detail: String(log.details ?? log.detail ?? "No details were recorded."),
      target: String(log.culprit_id ?? log.target ?? "—"),
      timestamp: String(log.created_at ?? "—"),
    }));
    const all = [...modRows, ...secRows];
    if (tab === "moderation") return modRows;
    if (tab === "security") return secRows;
    return all;
  }, [cases, security, tab]);

  const tabs: Array<{ key: Tab; label: string; count: number }> = [
    { key: "all", label: "All activity", count: cases.length + security.length },
    { key: "moderation", label: "Moderation", count: cases.length },
    { key: "security", label: "Security", count: security.length },
  ];

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Logs"
        description="Moderation cases and anti-nuke interventions recorded by the bot API for this server."
        action={
          <Button size="sm" variant="outline" onClick={load} disabled={loading} className="gap-1.5">
            <RefreshCw className="h-3.5 w-3.5" aria-hidden="true" />
            Refresh
          </Button>
        }
      />

      {error && (
        <Alert variant="error">Log data could not be loaded from the bot API. Confirm the bot is online and try again.</Alert>
      )}

      <div className="flex flex-wrap gap-2" role="tablist" aria-label="Log categories">
        {tabs.map((t) => (
          <button
            key={t.key}
            role="tab"
            aria-selected={tab === t.key}
            onClick={() => setTab(t.key)}
            className={cn(
              "inline-flex h-8 items-center gap-2 rounded-full border px-3 text-xs font-medium transition-colors",
              tab === t.key
                ? "border-primary/40 bg-primary-subtle text-primary"
                : "border-card-border bg-surface text-slate-400 hover:text-white"
            )}
          >
            {t.label}
            <span className="rounded-full bg-white/5 px-1.5 py-0.5 font-mono text-[10px]">{t.count}</span>
          </button>
        ))}
      </div>

      {rows.length === 0 && !loading ? (
        <Card>
          <EmptyState
            icon={FileText}
            title="No log entries"
            description="Moderation actions and security interventions will appear here once the bot records them for this server."
          />
        </Card>
      ) : (
        <DataTable<UnifiedLog>
          rows={rows}
          loading={loading}
          getRowKey={(row) => row.id}
          searchPlaceholder="Search actions, reasons, or user IDs…"
          searchKeys={(row) => `${row.action} ${row.detail} ${row.target}`}
          emptyTitle="No log entries"
          emptyDescription="New bot activity will appear here when it is recorded."
          emptyIcon={FileText}
          columns={[
            {
              key: "source",
              header: "Source",
              render: (row) => (
                <Badge variant={row.source === "security" ? "warning" : "primary"}>
                  {row.source === "security" ? (
                    <span className="inline-flex items-center gap-1">
                      <ShieldAlert className="h-3 w-3" aria-hidden="true" /> Security
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1">
                      <Shield className="h-3 w-3" aria-hidden="true" /> Moderation
                    </span>
                  )}
                </Badge>
              ),
            },
            { key: "action", header: "Action", render: (row) => <span className="font-medium text-white">{row.action}</span> },
            {
              key: "detail",
              header: "Reason / Details",
              render: (row) => <span className="block max-w-xs truncate text-slate-300">{row.detail}</span>,
            },
            {
              key: "target",
              header: "Target",
              render: (row) => <span className="font-mono text-slate-300">{row.target}</span>,
            },
            {
              key: "timestamp",
              header: "Timestamp",
              align: "right",
              render: (row) => <span className="whitespace-nowrap text-slate-500">{row.timestamp}</span>,
            },
          ]}
        />
      )}

      <p className="text-[11px] leading-relaxed text-slate-600">
        Sources: live moderation cases and anti-nuke security events from the bot API. No entries are
        fabricated — an empty list means the bot has not recorded activity for this server yet.
      </p>
    </div>
  );
}
