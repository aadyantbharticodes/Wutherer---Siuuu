"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Alert } from "@/components/ui/alert";
import { SectionHeader } from "@/components/ui/section-header";
import { api } from "@/lib/api";
import { TicketConfig } from "@/types";

export default function TicketsPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [config, setConfig] = useState<TicketConfig>({
    enabled: 0,
    greeting: "A staff member will assist you shortly.",
    max_open: 3,
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" } | null>(null);

  useEffect(() => {
    if (guildId) {
      api.getTicketConfig(guildId)
        .then((data) => {
          if (data) setConfig(data);
        })
        .catch(() => {});
    }
  }, [guildId]);

  const handleSave = async () => {
    setSaving(true);
    setMessage(null);
    try {
      await api.updateTicketConfig(guildId, config);
      setMessage({ text: "Ticket settings saved successfully.", variant: "success" });
    } catch {
      setMessage({ text: "Failed to save ticket settings.", variant: "error" });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Support Tickets"
        description="Automated private support channels, greeting prompts, and concurrent limits."
        action={
          <Button onClick={handleSave} disabled={saving} size="sm">
            {saving ? "Saving..." : "Save Changes"}
          </Button>
        }
      />

      {message && (
        <Alert variant={message.variant} dismissible onDismiss={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      <Card>
        <div className="flex items-center justify-between p-1">
          <div>
            <h4 className="text-xs font-medium text-white">Enable Ticket System</h4>
            <p className="text-[11px] text-slate-500 mt-0.5">Allow server members to open private support channels</p>
          </div>
          <Switch
            checked={config.enabled === 1}
            onCheckedChange={(val: boolean) => setConfig((p) => ({ ...p, enabled: val ? 1 : 0 }))}
          />
        </div>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Welcome Greeting Message</CardTitle>
          <CardDescription>First message dispatched when a member creates a new ticket</CardDescription>
        </CardHeader>
        <CardContent>
          <Textarea
            rows={3}
            value={config.greeting}
            onChange={(e) => setConfig((p) => ({ ...p, greeting: e.target.value }))}
            placeholder="Greeting text dispatched on ticket creation..."
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Concurrent Ticket Limit</CardTitle>
          <CardDescription>Maximum open tickets a single user can have open simultaneously</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="max-w-xs space-y-1">
            <label className="text-xs text-slate-400">Maximum Tickets (1-10)</label>
            <Input
              type="number"
              min="1"
              max="10"
              value={config.max_open}
              onChange={(e) => setConfig((p) => ({ ...p, max_open: parseInt(e.target.value) || 1 }))}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
