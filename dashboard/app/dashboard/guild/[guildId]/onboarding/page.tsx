"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Alert } from "@/components/ui/alert";
import { SectionHeader } from "@/components/ui/section-header";
import { Plus, Trash2, ExternalLink } from "lucide-react";
import { api } from "@/lib/api";

interface ActionButton {
  label: string;
  url: string;
}

export default function OnboardingPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [dmEnabled, setDmEnabled] = useState(false);
  const [dmMessage, setDmMessage] = useState(
    "Welcome to **{guild.name}**, {user.mention}! Please make sure to check out the rules and verify your account."
  );
  const [dmDelay, setDmDelay] = useState(0);
  const [buttons, setButtons] = useState<ActionButton[]>([
    { label: "Server Rules", url: "https://discord.com" },
    { label: "Get Roles", url: "https://discord.com" },
  ]);
  const [newBtnLabel, setNewBtnLabel] = useState("");
  const [newBtnUrl, setNewBtnUrl] = useState("");

  const [pingEnabled, setPingEnabled] = useState(false);
  const [pingMode, setPingMode] = useState<"ghost" | "persistent">("ghost");
  const [pingDelay, setPingDelay] = useState(5);
  const [pingMessage, setPingMessage] = useState("Welcome {user.mention} to {guild.name}!");
  const [delayedRoleMins, setDelayedRoleMins] = useState(10);

  const [notification, setNotification] = useState<string | null>(null);

  const handleAddButton = () => {
    if (!newBtnLabel || !newBtnUrl) return;
    setButtons([...buttons, { label: newBtnLabel, url: newBtnUrl }]);
    setNewBtnLabel("");
    setNewBtnUrl("");
  };

  const handleRemoveButton = (idx: number) => {
    setButtons(buttons.filter((_, i) => i !== idx));
  };

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getOnboarding(guildId)
      .then((data) => {
        const autodm = data.autodm || {};
        const autoping = data.autoping || {};
        const welcome = data.welcome || {};
        setDmEnabled(autodm.enabled === 1);
        setDmMessage(autodm.message || dmMessage);
        setDmDelay(autodm.delay_seconds || 0);
        setButtons(Array.isArray(autodm.buttons) ? autodm.buttons : []);
        setPingEnabled(autoping.enabled === 1);
        setPingMode(autoping.ping_mode === "persistent" ? "persistent" : "ghost");
        setPingDelay(autoping.delete_after_seconds || 5);
        setPingMessage(autoping.message_template || pingMessage);
        setDelayedRoleMins(welcome.autorole_delay_minutes || 0);
      })
      .catch(() => setNotification("Onboarding settings could not be loaded from the bot API."))
      .finally(() => setLoading(false));
  }, [guildId]);

  const handleSave = async () => {
    try {
      await Promise.all([
        api.updateAutoDM(guildId, { enabled: dmEnabled ? 1 : 0, message: dmMessage, buttons, delay_seconds: dmDelay }),
        api.updateAutoPing(guildId, { enabled: pingEnabled ? 1 : 0, ping_mode: pingMode, delete_after_seconds: pingDelay, message_template: pingMessage }),
        api.updateAdvancedWelcome(guildId, { autorole_delay_minutes: delayedRoleMins }),
      ]);
      setNotification("Onboarding preferences saved successfully.");
    } catch { setNotification("Could not save onboarding preferences."); }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Onboarding & Welcomer"
        description="Configure join direct messages, ghost pings, and delayed autoroles."
        action={
          <Button onClick={handleSave} size="sm">
            Save Changes
          </Button>
        }
      />

      {loading && <div className="h-1 overflow-hidden rounded bg-surface"><div className="h-full w-1/3 animate-pulse bg-primary" /></div>}

      {notification && (
        <Alert variant="success" dismissible onDismiss={() => setNotification(null)}>
          {notification}
        </Alert>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Welcome DM Card */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Welcome Direct Message</CardTitle>
              <Switch checked={dmEnabled} onCheckedChange={setDmEnabled} />
            </div>
            <CardDescription>Send an automated DM greeting with button links on join</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3.5">
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Message Template</label>
              <Textarea
                rows={3}
                value={dmMessage}
                onChange={(e) => setDmMessage(e.target.value)}
              />
              <p className="text-[10px] text-slate-500 font-mono">
                Variables: {"{user}"}, {"{user.mention}"}, {"{guild.name}"}, {"{guild.member_count}"}
              </p>
            </div>

            <div className="space-y-1">
              <div className="flex justify-between text-xs text-slate-400">
                <span>Dispatch Delay</span>
                <span className="font-mono text-primary-light">{dmDelay}s</span>
              </div>
              <input
                type="range"
                min="0"
                max="60"
                value={dmDelay}
                onChange={(e) => setDmDelay(Number(e.target.value))}
                className="w-full accent-primary h-1.5 bg-surface rounded cursor-pointer"
              />
            </div>

            <div className="space-y-2 pt-1 border-t border-card-border">
              <label className="text-xs text-slate-400">Action Button Links</label>
              <div className="space-y-1.5">
                {buttons.map((b, i) => (
                  <div key={i} className="flex items-center justify-between rounded border border-card-border bg-surface px-2.5 py-1.5 text-xs">
                    <span className="text-white font-medium flex items-center gap-1.5">
                      <ExternalLink className="h-3 w-3 text-slate-500" />
                      {b.label}
                    </span>
                    <span className="text-slate-500 text-[11px] truncate max-w-xs">{b.url}</span>
                    <button onClick={() => handleRemoveButton(i)} className="text-slate-500 hover:text-red-400">
                      <Trash2 className="h-3.5 w-3.5" />
                    </button>
                  </div>
                ))}
              </div>

              <div className="flex gap-2 pt-1">
                <Input
                  type="text"
                  placeholder="Label"
                  value={newBtnLabel}
                  onChange={(e) => setNewBtnLabel(e.target.value)}
                  className="w-1/3 text-xs"
                />
                <Input
                  type="text"
                  placeholder="https://..."
                  value={newBtnUrl}
                  onChange={(e) => setNewBtnUrl(e.target.value)}
                  className="flex-1 text-xs"
                />
                <Button size="sm" onClick={handleAddButton}>
                  <Plus className="h-3.5 w-3.5" />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Channel Mentions Card */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Channel Ping Notifications</CardTitle>
              <Switch checked={pingEnabled} onCheckedChange={setPingEnabled} />
            </div>
            <CardDescription>Direct new arrival attention toward rules or verification</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3.5">
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Ping Mode</label>
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={() => setPingMode("ghost")}
                  className={`rounded border p-2.5 text-left text-xs transition-colors ${
                    pingMode === "ghost"
                      ? "border-primary bg-primary-subtle text-white"
                      : "border-card-border bg-surface text-slate-400"
                  }`}
                >
                  <div className="font-medium">Ghost Ping</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Mentions and auto-deletes immediately</div>
                </button>
                <button
                  onClick={() => setPingMode("persistent")}
                  className={`rounded border p-2.5 text-left text-xs transition-colors ${
                    pingMode === "persistent"
                      ? "border-primary bg-primary-subtle text-white"
                      : "border-card-border bg-surface text-slate-400"
                  }`}
                >
                  <div className="font-medium">Persistent Ping</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">Retains message in designated channel</div>
                </button>
              </div>
            </div>

            {pingMode === "ghost" && (
              <div className="space-y-1">
                <div className="flex justify-between text-xs text-slate-400">
                  <span>Deletion Delay</span>
                  <span className="font-mono text-primary-light">{pingDelay}s</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="30"
                  value={pingDelay}
                  onChange={(e) => setPingDelay(Number(e.target.value))}
                  className="w-full accent-primary h-1.5 bg-surface rounded cursor-pointer"
                />
              </div>
            )}

            <div className="space-y-1">
              <label className="text-xs text-slate-400">Ping Message</label>
              <Input
                type="text"
                value={pingMessage}
                onChange={(e) => setPingMessage(e.target.value)}
              />
            </div>

            <div className="pt-2 border-t border-card-border space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <div>
                  <span className="font-medium text-white">Timed Autorole Delay</span>
                  <p className="text-[10px] text-slate-500">Probationary period before auto-assigning member role</p>
                </div>
                <span className="font-mono text-primary-light">{delayedRoleMins} mins</span>
              </div>
              <input
                type="range"
                min="0"
                max="60"
                value={delayedRoleMins}
                onChange={(e) => setDelayedRoleMins(Number(e.target.value))}
                className="w-full accent-primary h-1.5 bg-surface rounded cursor-pointer"
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
