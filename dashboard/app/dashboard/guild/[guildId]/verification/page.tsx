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
import { VerificationConfig } from "@/types";

export default function VerificationPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [config, setConfig] = useState<VerificationConfig>({
    enabled: 0,
    difficulty: "medium",
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" } | null>(null);

  useEffect(() => {
    if (guildId) {
      api.getVerificationConfig(guildId)
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
      await api.updateVerificationConfig(guildId, config);
      setMessage({ text: "Verification settings saved successfully.", variant: "success" });
    } catch {
      setMessage({ text: "Failed to save verification settings.", variant: "error" });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Entry Verification"
        description="Mitigate automated raid attacks and self-bots using distorted visual CAPTCHAs."
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
            <h4 className="text-xs font-medium text-white">Enable Entry Verification</h4>
            <p className="text-[11px] text-slate-500 mt-0.5">Require new members to pass a CAPTCHA challenge before chatting</p>
          </div>
          <Switch
            checked={config.enabled === 1}
            onCheckedChange={(val: boolean) => setConfig((p) => ({ ...p, enabled: val ? 1 : 0 }))}
          />
        </div>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Challenge Difficulty</CardTitle>
          <CardDescription>Adjust noise level, distortion, and line density in generated CAPTCHA images</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="max-w-xs space-y-1">
            <label className="text-xs text-slate-400">Distortion Level</label>
            <Select
              value={config.difficulty}
              onChange={(e) => setConfig((p) => ({ ...p, difficulty: e.target.value }))}
            >
              <option value="easy">Easy (Clean text, low noise)</option>
              <option value="medium">Medium (Standard distortion & noise)</option>
              <option value="hard">Hard (Heavy distortion, rotation & lines)</option>
            </Select>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
