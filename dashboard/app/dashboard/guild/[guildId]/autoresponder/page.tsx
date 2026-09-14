"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { SectionHeader } from "@/components/ui/section-header";
import { EmptyState } from "@/components/ui/empty-state";
import { Alert } from "@/components/ui/alert";
import { MessageSquare, Trash2 } from "lucide-react";
import { api } from "@/lib/api";
import { AutoResponseTrigger } from "@/types";

export default function AutoResponderPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [triggers, setTriggers] = useState<AutoResponseTrigger[]>([]);
  const [loading, setLoading] = useState(true);
  const [keyword, setKeyword] = useState("");
  const [response, setResponse] = useState("");
  const [mode, setMode] = useState("exact");
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" } | null>(null);

  useEffect(() => {
    async function loadTriggers() {
      try {
        const res = await api.getAutoResponders(guildId);
        setTriggers(res);
      } catch {
        setTriggers([]);
        setMessage({ text: "Auto-responder triggers could not be loaded from the bot API.", variant: "error" });
      } finally {
        setLoading(false);
      }
    }
    if (guildId) {
      loadTriggers();
    }
  }, [guildId]);

  const handleAddTrigger = async () => {
    if (!keyword.trim() || !response.trim()) return;
    try {
      await api.createAutoResponder(guildId, { trigger_text: keyword.trim(), response_text: response.trim(), match_mode: mode });
      const updated = await api.getAutoResponders(guildId);
      setTriggers(updated || []);
      setKeyword(""); setResponse("");
      setMessage({ text: "Trigger created.", variant: "success" });
    } catch { setMessage({ text: "Could not create this trigger.", variant: "error" }); }
  };

  const handleDelete = async (id: number) => {
    try { await api.deleteAutoResponder(guildId, id); setTriggers(triggers.filter((t) => t.trigger_id !== id)); }
    catch { setMessage({ text: "Could not delete this trigger.", variant: "error" }); }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Auto-Responder"
        description="Keyword and pattern-matching automated message responses."
      />

      {message && <Alert variant={message.variant} dismissible onDismiss={() => setMessage(null)}>{message.text}</Alert>}

      <Card>
        <CardHeader>
          <CardTitle>Create Trigger</CardTitle>
          <CardDescription>Define trigger keyword, matching mode, and automated reply text</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Trigger Keyword / Phrase</label>
              <Input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="e.g. !help, discord link"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs text-slate-400">Match Mode</label>
              <Select value={mode} onChange={(e) => setMode(e.target.value)}>
                <option value="exact">Exact Match</option>
                <option value="wildcard">Contains Phrase</option>
                <option value="regex">Regular Expression</option>
              </Select>
            </div>

            <div className="space-y-1">
              <label className="text-xs text-slate-400">Response Text</label>
              <Input
                type="text"
                value={response}
                onChange={(e) => setResponse(e.target.value)}
                placeholder="Reply message content..."
              />
            </div>
          </div>

          <div className="flex justify-end pt-1">
            <Button size="sm" onClick={handleAddTrigger}>Create Trigger</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Active Triggers ({triggers.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {triggers.length === 0 ? (
            <EmptyState
              icon={MessageSquare}
              title="No Triggers"
              description="Create a keyword trigger above to get started."
            />
          ) : (
            <div className="divide-y divide-card-border">
              {triggers.map((t) => (
                <div key={t.trigger_id} className="py-3 flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-medium text-primary-light bg-primary-subtle px-1.5 py-0.5 rounded border border-primary/20">
                        {t.trigger_text}
                      </span>
                      <Badge variant="default">{t.match_mode}</Badge>
                      <span className="text-[11px] text-slate-500">{t.uses_count} uses</span>
                    </div>
                    <p className="text-xs text-slate-300">{t.response_text}</p>
                  </div>

                  <Button variant="ghost" size="sm" onClick={() => handleDelete(t.trigger_id)} className="text-slate-500 hover:text-red-400">
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
