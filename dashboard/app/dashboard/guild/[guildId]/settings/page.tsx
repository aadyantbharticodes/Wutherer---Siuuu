"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Alert } from "@/components/ui/alert";
import { SectionHeader } from "@/components/ui/section-header";
import { api } from "@/lib/api";

export default function GuildSettingsPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [prefix, setPrefix] = useState("w!");
  const [savedPrefix, setSavedPrefix] = useState("w!");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" } | null>(null);

  useEffect(() => {
    if (guildId) {
      api.getGuildDetails(guildId)
        .then((data) => {
          if (data.settings?.prefix) {
            setPrefix(data.settings.prefix);
            setSavedPrefix(data.settings.prefix);
          }
        })
        .catch(() => {});
    }
  }, [guildId]);

  const handleSave = async () => {
    setSaving(true);
    setMessage(null);
    try {
      await api.updateGuildSettings(guildId, { prefix });
      setSavedPrefix(prefix);
      setMessage({ text: "Server preferences saved successfully.", variant: "success" });
    } catch {
      setMessage({ text: "Failed to save server preferences.", variant: "error" });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="General Settings"
        description="Global bot configuration and command preferences for this server."
        action={
          <Button onClick={handleSave} disabled={saving || prefix === savedPrefix} size="sm">
            {saving ? "Saving..." : "Save Settings"}
          </Button>
        }
      />

      {message && (
        <Alert variant={message.variant} dismissible onDismiss={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      {prefix !== savedPrefix && <p className="text-xs font-medium text-amber-400">You have unsaved changes.</p>}

      <Card>
        <CardHeader>
          <CardTitle>Command Prefix</CardTitle>
          <CardDescription>The symbol or keyword preceding text commands (e.g. w!help)</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="max-w-xs space-y-1">
            <label className="text-xs text-slate-400">Server Prefix</label>
            <Input
              type="text"
              value={prefix}
              onChange={(e) => setPrefix(e.target.value)}
              maxLength={10}
              placeholder="e.g. w!"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
