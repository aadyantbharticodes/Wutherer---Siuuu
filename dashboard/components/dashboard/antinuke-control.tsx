"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { AlertTriangle, Lock, ShieldAlert, Unlock, UserPlus, X } from "lucide-react";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { Input } from "@/components/ui/input";
import { SectionHeader } from "@/components/ui/section-header";
import { Select } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { api } from "@/lib/api";

const defaultConfig = { enabled: 0, max_channel_deletes: 3, max_role_deletes: 3, max_bans: 5, max_kicks: 5, max_webhook_creates: 2, rate_window_seconds: 15, action_type: "ban", panic_lockdown_enabled: 0 };

export function AntinukeControl() {
  const params = useParams();
  const guildId = params.guildId as string;
  const [config, setConfig] = useState<any>(defaultConfig);
  const [whitelist, setWhitelist] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [userId, setUserId] = useState("");
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" | "warning" } | null>(null);

  const load = async () => {
    setLoading(true);
    try {
      const [status, logResult] = await Promise.all([api.getAntinukeStatus(guildId), api.getAntinukeLogs(guildId)]);
      setConfig({ ...defaultConfig, ...(status.config || {}) });
      setWhitelist(Array.isArray(status.whitelist) ? status.whitelist : []);
      setLogs(Array.isArray(logResult.logs) ? logResult.logs : []);
      setMessage(null);
    } catch {
      setMessage({ text: "Anti-nuke controls could not be loaded from the bot API.", variant: "error" });
    } finally { setLoading(false); }
  };

  useEffect(() => { if (guildId) load(); }, [guildId]);

  const save = async () => {
    setSaving(true);
    try {
      await api.updateAntinukeStatus(guildId, config);
      setMessage({ text: "Anti-nuke configuration saved.", variant: "success" });
      await load();
    } catch { setMessage({ text: "Could not save anti-nuke configuration.", variant: "error" }); }
    finally { setSaving(false); }
  };

  const toggleLockdown = async () => {
    const locking = config.panic_lockdown_enabled !== 1;
    const confirmation = locking ? "Lock all server channels now? This changes channel permissions for members." : "Lift the active panic lockdown?";
    if (!window.confirm(confirmation)) return;
    try {
      await api.setPanicLockdown(guildId, locking ? "lock" : "unlock");
      setConfig((current: any) => ({ ...current, panic_lockdown_enabled: locking ? 1 : 0 }));
      setMessage({ text: locking ? "Panic lockdown was requested from the bot." : "Lockdown release was requested from the bot.", variant: "warning" });
    } catch { setMessage({ text: "The bot could not change lockdown state.", variant: "error" }); }
  };

  const addWhitelist = async () => {
    if (!/^\d{5,}$/.test(userId.trim())) { setMessage({ text: "Enter a valid numeric Discord user ID.", variant: "error" }); return; }
    try { await api.addAntinukeWhitelist(guildId, userId.trim()); setUserId(""); await load(); setMessage({ text: "Trusted user added to the whitelist.", variant: "success" }); }
    catch { setMessage({ text: "Could not add that user to the whitelist.", variant: "error" }); }
  };

  const removeWhitelist = async (id: string) => {
    if (!window.confirm("Remove this trusted user from the anti-nuke whitelist?")) return;
    try { await api.removeAntinukeWhitelist(guildId, id); await load(); }
    catch { setMessage({ text: "Could not remove that trusted user.", variant: "error" }); }
  };

  if (loading) return <div className="space-y-4 animate-pulse"><div className="h-14 w-1/2 rounded-lg bg-surface" /><div className="h-56 rounded-lg border border-card-border bg-surface" /></div>;

  const thresholds = [
    { key: "max_channel_deletes", label: "Channel deletions", help: "Maximum deletions in the window" },
    { key: "max_role_deletes", label: "Role deletions", help: "Maximum deletions in the window" },
    { key: "max_bans", label: "Member bans", help: "Maximum bans in the window" },
    { key: "max_kicks", label: "Member kicks", help: "Maximum kicks in the window" },
    { key: "max_webhook_creates", label: "Webhook creates", help: "Maximum new webhooks in the window" },
  ];

  return <div className="space-y-5">
    <SectionHeader title="Anti-nuke" description="Detect destructive bursts and let the bot apply the response you choose." action={<div className="flex gap-2"><Button variant={config.panic_lockdown_enabled === 1 ? "secondary" : "danger"} size="sm" onClick={toggleLockdown} className="gap-1.5">{config.panic_lockdown_enabled === 1 ? <Unlock className="h-3.5 w-3.5" /> : <Lock className="h-3.5 w-3.5" />}{config.panic_lockdown_enabled === 1 ? "Lift lockdown" : "Panic lockdown"}</Button><Button size="sm" onClick={save} disabled={saving}>{saving ? "Saving…" : "Save changes"}</Button></div>} />
    {message && <Alert variant={message.variant} dismissible onDismiss={() => setMessage(null)}>{message.text}</Alert>}

    <Card className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center"><div><div className="flex items-center gap-2"><h2 className="text-sm font-semibold text-white">Protection status</h2><Badge variant={config.enabled === 1 ? "success" : "default"}>{config.enabled === 1 ? "Enabled" : "Disabled"}</Badge></div><p className="mt-1 text-xs text-slate-500">When enabled, the bot evaluates configured actions inside the selected rate window.</p></div><Switch checked={config.enabled === 1} onCheckedChange={(checked) => setConfig((current: any) => ({ ...current, enabled: checked ? 1 : 0 }))} aria-label="Enable anti-nuke protection" /></Card>

    <section className="grid gap-4 lg:grid-cols-[1.4fr_0.6fr]"><Card><h2 className="text-sm font-semibold text-white">Detection limits</h2><p className="mt-1 text-xs text-slate-500">Set thresholds the bot should treat as suspicious activity.</p><div className="mt-4 grid gap-3 sm:grid-cols-2">{thresholds.map((item) => <label key={item.key} className="block"><span className="text-xs font-medium text-slate-300">{item.label}</span><span className="mt-0.5 block text-[11px] text-slate-500">{item.help}</span><Input className="mt-2" type="number" min="1" value={config[item.key]} onChange={(event) => setConfig((current: any) => ({ ...current, [item.key]: Number(event.target.value) || 1 }))} /></label>)}</div></Card>
      <Card><h2 className="text-sm font-semibold text-white">Response</h2><p className="mt-1 text-xs text-slate-500">Applied when a limit is breached.</p><label className="mt-4 block text-xs font-medium text-slate-300">Rate window <Input className="mt-2" type="number" min="5" max="300" value={config.rate_window_seconds} onChange={(event) => setConfig((current: any) => ({ ...current, rate_window_seconds: Number(event.target.value) || 5 }))} /></label><label className="mt-3 block text-xs font-medium text-slate-300">Action <Select className="mt-2" value={config.action_type} onChange={(event) => setConfig((current: any) => ({ ...current, action_type: event.target.value }))}><option value="ban">Ban the culprit</option><option value="kick">Kick the culprit</option><option value="quarantine">Quarantine the culprit</option><option value="strip">Remove administrative roles</option></Select></label></Card>
    </section>

    <section className="grid gap-5 xl:grid-cols-2"><Card><div className="flex items-center gap-2"><UserPlus className="h-4 w-4 text-primary-light" aria-hidden="true" /><h2 className="text-sm font-semibold text-white">Trusted users</h2></div><p className="mt-1 text-xs text-slate-500">Whitelisted users bypass anti-nuke thresholds. Use this sparingly.</p><div className="mt-4 flex gap-2"><Input value={userId} onChange={(event) => setUserId(event.target.value)} placeholder="Discord user ID" inputMode="numeric" /><Button size="sm" onClick={addWhitelist}>Add</Button></div><div className="mt-4 divide-y divide-card-border">{whitelist.length ? whitelist.map((entry) => <div key={entry.entity_id} className="flex items-center justify-between py-2.5"><span className="font-mono text-xs text-slate-300">{entry.entity_id}</span><button type="button" onClick={() => removeWhitelist(String(entry.entity_id))} className="rounded p-1 text-slate-500 hover:bg-surface-hover hover:text-red-400" aria-label={`Remove ${entry.entity_id} from whitelist`}><X className="h-3.5 w-3.5" /></button></div>) : <p className="py-4 text-xs text-slate-500">No trusted users have been added.</p>}</div></Card>
      <Card className="p-0"><div className="p-4"><div className="flex items-center gap-2"><ShieldAlert className="h-4 w-4 text-primary-light" aria-hidden="true" /><h2 className="text-sm font-semibold text-white">Security events</h2></div><p className="mt-1 text-xs text-slate-500">Recorded anti-nuke interventions from this server.</p></div>{logs.length ? <div className="divide-y divide-card-border">{logs.slice(0, 6).map((log) => <div key={log.id} className="px-4 py-3"><div className="flex items-center justify-between gap-3"><p className="text-xs font-semibold text-white">{String(log.event_type || "Security event").replaceAll("_", " ")}</p><Badge variant="warning">{log.action_taken || "Recorded"}</Badge></div><p className="mt-1 text-xs text-slate-400">{log.details || "No details were recorded."}</p></div>)}</div> : <EmptyState className="py-7" icon={AlertTriangle} title="No security events" description="Interventions recorded by the bot will appear here." />}</Card></section>
  </div>;
}
