"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Alert } from "@/components/ui/alert";
import { SectionHeader } from "@/components/ui/section-header";
import { api } from "@/lib/api";
import { LevelingConfig } from "@/types";

export default function LevelingPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [config, setConfig] = useState<LevelingConfig>({
    enabled: 0,
    announce_levelup: 1,
    xp_rate: 1.0,
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" } | null>(null);

  useEffect(() => {
    if (guildId) {
      api.getLevelingConfig(guildId)
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
      await api.updateLevelingConfig(guildId, config);
      setMessage({ text: "Leveling configuration saved.", variant: "success" });
    } catch {
      setMessage({ text: "Failed to save leveling configuration.", variant: "error" });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Leveling & XP"
        description="Text and voice engagement tracking, rank cards, and role reward progression."
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

      <Card className="divide-y divide-card-border p-0 overflow-hidden">
        <div className="flex items-center justify-between p-4 hover:bg-surface-hover/50 transition-colors">
          <div>
            <h4 className="text-xs font-medium text-white">Enable Leveling Progression</h4>
            <p className="text-[11px] text-slate-500 mt-0.5">Allow members to accumulate XP from text activity</p>
          </div>
          <Switch
            checked={config.enabled === 1}
            onCheckedChange={(val: boolean) => setConfig((p) => ({ ...p, enabled: val ? 1 : 0 }))}
          />
        </div>

        <div className="flex items-center justify-between p-4 hover:bg-surface-hover/50 transition-colors">
          <div>
            <h4 className="text-xs font-medium text-white">Announce Level Ups</h4>
            <p className="text-[11px] text-slate-500 mt-0.5">Send channel notifications when members level up</p>
          </div>
          <Switch
            checked={config.announce_levelup === 1}
            onCheckedChange={(val: boolean) => setConfig((p) => ({ ...p, announce_levelup: val ? 1 : 0 }))}
          />
        </div>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>XP Multiplier</CardTitle>
          <CardDescription>Adjust the speed at which members accumulate experience (default: 1.0x)</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="max-w-xs space-y-1">
            <label className="text-xs text-slate-400">Rate Multiplier</label>
            <Input
              type="number"
              step="0.1"
              min="0.1"
              max="5.0"
              value={config.xp_rate}
              onChange={(e) => setConfig((p) => ({ ...p, xp_rate: parseFloat(e.target.value) || 1.0 }))}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
