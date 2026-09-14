"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";
import { Alert } from "@/components/ui/alert";
import { SectionHeader } from "@/components/ui/section-header";
import { api } from "@/lib/api";
import { AutomodConfig } from "@/types";

export default function AutomodPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [config, setConfig] = useState<AutomodConfig>({
    antispam: 0,
    anticaps: 0,
    antilink: 0,
    antiinvite: 0,
    antimention: 0,
    punishment: "delete",
  });
  const [saving, setSaving] = useState(false);
  const [savedConfig, setSavedConfig] = useState<string>("");
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" } | null>(null);

  useEffect(() => {
    if (guildId) {
      api.getAutomodConfig(guildId)
        .then((data) => {
          if (data) { setConfig(data); setSavedConfig(JSON.stringify(data)); }
        })
        .catch(() => {});
    }
  }, [guildId]);

  const toggle = (key: keyof AutomodConfig) => {
    setConfig((prev) => ({
      ...prev,
      [key]: prev[key] === 1 ? 0 : 1,
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage(null);
    try {
      await api.updateAutomodConfig(guildId, config);
      setSavedConfig(JSON.stringify(config));
      setMessage({ text: "Automod configuration updated.", variant: "success" });
    } catch {
      setMessage({ text: "Failed to save automod configuration.", variant: "error" });
    } finally {
      setSaving(false);
    }
  };

  const filters = [
    { key: "antispam" as const, title: "Anti-Spam", desc: "Detect and delete rapid duplicate message floods." },
    { key: "antiinvite" as const, title: "Anti-Invite", desc: "Block unauthorized Discord server invitation links." },
    { key: "antilink" as const, title: "Anti-Link", desc: "Block external URLs outside trusted whitelists." },
    { key: "anticaps" as const, title: "Anti-Caps", desc: "Filter messages exceeding excessive uppercase character thresholds." },
    { key: "antimention" as const, title: "Anti-Mass Mention", desc: "Prevent users from tagging multiple roles or users at once." },
  ];

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Automated Moderation"
        description="Configure real-time message filtering rules and automated violation responses."
        action={
          <Button onClick={handleSave} disabled={saving || JSON.stringify(config) === savedConfig} size="sm">
            {saving ? "Saving..." : "Save Changes"}
          </Button>
        }
      />

      {message && (
        <Alert variant={message.variant} dismissible onDismiss={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      {savedConfig && JSON.stringify(config) !== savedConfig && <p className="text-xs font-medium text-amber-400">You have unsaved changes.</p>}

      {/* Punishment setting */}
      <Card>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-1">
          <div>
            <h3 className="text-sm font-medium text-white">Default Violation Penalty</h3>
            <p className="text-xs text-slate-500 mt-0.5">Automated penalty applied upon rule violation</p>
          </div>
          <div className="w-full sm:w-56">
            <Select
              value={config.punishment || "delete"}
              onChange={(e) => setConfig((p) => ({ ...p, punishment: e.target.value }))}
            >
              <option value="delete">Delete Message Only</option>
              <option value="warn">Delete & Issue Warning</option>
              <option value="timeout">Delete & 10m Timeout</option>
              <option value="kick">Delete & Kick Member</option>
            </Select>
          </div>
        </div>
      </Card>

      {/* Filter Toggles in one grouped Card */}
      <Card className="divide-y divide-card-border p-0 overflow-hidden">
        {filters.map((f) => (
          <div key={f.key} className="flex items-center justify-between p-4 hover:bg-surface-hover/50 transition-colors">
            <div>
              <h4 className="text-xs font-medium text-white">{f.title}</h4>
              <p className="text-[11px] text-slate-500 mt-0.5">{f.desc}</p>
            </div>
            <Switch
              checked={config[f.key] === 1}
              onCheckedChange={() => toggle(f.key)}
            />
          </div>
        ))}
      </Card>
    </div>
  );
}
