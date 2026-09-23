"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { SectionHeader } from "@/components/ui/section-header";
import { EmptyState } from "@/components/ui/empty-state";
import { DataTable } from "@/components/dashboard/data-table";
import { Shield } from "lucide-react";
import { api } from "@/lib/api";

type Case = {
  id: number | string;
  action: string;
  user_id: string | number;
  reason?: string;
  created_at?: string;
};

export default function ModerationPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (guildId) {
      api.getModerationCases(guildId)
        .then((data) => setCases(Array.isArray(data) ? data : []))
        .catch(() => setCases([]))
        .finally(() => setLoading(false));
    }
  }, [guildId]);

  const getActionBadgeVariant = (action: string): "default" | "primary" | "warning" | "danger" => {
    const act = (action || "").toLowerCase();
    if (act.includes("ban")) return "danger";
    if (act.includes("kick") || act.includes("timeout") || act.includes("mute")) return "warning";
    if (act.includes("warn")) return "primary";
    return "default";
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Moderation Cases"
        description="Audit log of automated and staff moderation actions recorded for this server."
      />

      {loading || cases.length > 0 ? (
        <DataTable<Case>
          rows={cases}
          loading={loading}
          getRowKey={(row) => String(row.id)}
          searchPlaceholder="Search actions, reasons, or user IDs…"
          searchKeys={(row) => `${row.action} ${row.reason ?? ""} ${row.user_id}`}
          emptyTitle="No Moderation Cases"
          emptyDescription="No infractions, warnings, or enforcement actions recorded yet."
          emptyIcon={Shield}
          columns={[
            {
              key: "case",
              header: "Case",
              render: (row) => <span className="font-mono text-slate-400">#{row.id}</span>,
            },
            {
              key: "action",
              header: "Action",
              render: (row) => <Badge variant={getActionBadgeVariant(row.action)}>{row.action}</Badge>,
            },
            {
              key: "target",
              header: "Target User",
              render: (row) => <span className="font-mono text-white">{row.user_id}</span>,
            },
            {
              key: "reason",
              header: "Reason",
              render: (row) => (
                <span className="block max-w-xs truncate text-slate-300">{row.reason || "No reason provided"}</span>
              ),
            },
            {
              key: "timestamp",
              header: "Timestamp",
              align: "right",
              render: (row) => <span className="whitespace-nowrap text-slate-500">{row.created_at}</span>,
            },
          ]}
        />
      ) : (
        <Card>
          <EmptyState
            icon={Shield}
            title="No Moderation Cases"
            description="No infractions, warnings, or enforcement actions recorded yet."
          />
        </Card>
      )}

      <p className="text-[11px] leading-relaxed text-slate-600">
        Read-only history from the bot API. Moderation actions themselves are taken in Discord;
        destructive actions there require staff confirmation.
      </p>
    </div>
  );
}
