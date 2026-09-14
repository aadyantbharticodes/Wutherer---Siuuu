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
import { AIConfig } from "@/types";

export default function AIPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [config, setConfig] = useState<AIConfig>({
    enabled: 0,
    persona: "You are a helpful Discord bot assistant.",
    cooldown: 5,
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" } | null>(null);

  useEffect(() => {
    if (guildId) {
      api.getAIConfig(guildId)
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
      await api.updateAIConfig(guildId, config);
      setMessage({ text: "AI configuration saved successfully.", variant: "success" });
    } catch {
      setMessage({ text: "Failed to save AI configuration.", variant: "error" });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Google Gemini AI"
        description="Configure conversational assistant personas, system instructions, and query cooldowns."
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
            <h4 className="text-xs font-medium text-white">Enable AI Chat & Queries</h4>
            <p className="text-[11px] text-slate-500 mt-0.5">Allow server members to converse with Gemini AI and use assistant tools</p>
          </div>
          <Switch
            checked={config.enabled === 1}
            onCheckedChange={(val: boolean) => setConfig((p) => ({ ...p, enabled: val ? 1 : 0 }))}
          />
        </div>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>System Persona Instructions</CardTitle>
          <CardDescription>Direct instructions guiding the AI model&apos;s tone, personality, and contextual guidelines</CardDescription>
        </CardHeader>
        <CardContent>
          <Textarea
            rows={4}
            value={config.persona}
            onChange={(e) => setConfig((p) => ({ ...p, persona: e.target.value }))}
            placeholder="System persona prompt..."
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Per-User Cooldown</CardTitle>
          <CardDescription>Rate limit interval between consecutive AI queries in seconds</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="max-w-xs space-y-1">
            <label className="text-xs text-slate-400">Cooldown Seconds (1-60)</label>
            <Input
              type="number"
              min="1"
              max="60"
              value={config.cooldown}
              onChange={(e) => setConfig((p) => ({ ...p, cooldown: parseInt(e.target.value) || 5 }))}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
