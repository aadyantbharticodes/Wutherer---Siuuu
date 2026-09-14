"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { SectionHeader } from "@/components/ui/section-header";
import { EmptyState } from "@/components/ui/empty-state";
import { Shield } from "lucide-react";
import { api } from "@/lib/api";

export default function ModerationPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [cases, setCases] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (guildId) {
      api.getModerationCases(guildId)
        .then((data) => setCases(data || []))
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

      {loading ? (
        <div className="space-y-2 animate-pulse">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-12 bg-surface rounded-md border border-card-border" />
          ))}
        </div>
      ) : cases.length === 0 ? (
        <Card>
          <EmptyState
            icon={Shield}
            title="No Moderation Cases"
            description="No infractions, warnings, or enforcement actions recorded yet."
          />
        </Card>
      ) : (
        <Card className="p-0 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b border-card-border bg-surface text-slate-400 font-medium">
                <tr>
                  <th className="px-4 py-2.5">Case</th>
                  <th className="px-4 py-2.5">Action</th>
                  <th className="px-4 py-2.5">Target User</th>
                  <th className="px-4 py-2.5">Reason</th>
                  <th className="px-4 py-2.5 text-right">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-card-border">
                {cases.map((c) => (
                  <tr key={c.id} className="hover:bg-surface-hover/50 transition-colors">
                    <td className="px-4 py-2.5 font-mono text-slate-400">#{c.id}</td>
                    <td className="px-4 py-2.5">
                      <Badge variant={getActionBadgeVariant(c.action)}>
                        {c.action}
                      </Badge>
                    </td>
                    <td className="px-4 py-2.5 font-mono text-white">{c.user_id}</td>
                    <td className="px-4 py-2.5 text-slate-300 max-w-xs truncate">
                      {c.reason || "No reason provided"}
                    </td>
                    <td className="px-4 py-2.5 text-right text-slate-500 whitespace-nowrap">
                      {c.created_at}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
    </div>
  );
}
