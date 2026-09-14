"use client";

import { AntinukeControl } from "@/components/dashboard/antinuke-control";

import { useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Alert } from "@/components/ui/alert";
import { SectionHeader } from "@/components/ui/section-header";
import { Lock, Unlock, UserCheck, AlertTriangle } from "lucide-react";

interface AuditLog {
  id: number;
  event_type: string;
  culprit_id: number;
  details: string;
  action_taken: string;
  created_at: string;
}

function LegacyAntiNukePage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [enabled, setEnabled] = useState(true);
  const [panicLocked, setPanicLocked] = useState(false);
  const [channelLimit, setChannelLimit] = useState(3);
  const [roleLimit, setRoleLimit] = useState(3);
  const [banLimit, setBanLimit] = useState(5);
  const [windowSec, setWindowSec] = useState(15);
  const [actionType, setActionType] = useState("ban");

  const [whitelistUser, setWhitelistUser] = useState("");
  const [whitelist, setWhitelist] = useState<string[]>([
    "123456789012345678",
    "987654321098765432",
  ]);

  const [logs] = useState<AuditLog[]>([
    {
      id: 1,
      event_type: "channel_delete",
      culprit_id: 112233445566778899,
      details: "Triggered threshold with 4 channel deletes within 15s",
      action_taken: "Banned",
      created_at: "2026-09-14 10:24:18",
    },
    {
      id: 2,
      event_type: "role_delete",
      culprit_id: 998877665544332211,
      details: "Triggered threshold with 3 role deletions within 15s",
      action_taken: "Quarantined",
      created_at: "2026-09-13 18:42:01",
    },
  ]);

  const [notification, setNotification] = useState<{ msg: string; variant: "success" | "warning" | "info" } | null>(null);

  const handleToggleShield = () => {
    const next = !enabled;
    setEnabled(next);
    setNotification({
      msg: `Anti-Nuke Shield is now ${next ? "active" : "disabled"}.`,
      variant: next ? "success" : "warning",
    });
    setTimeout(() => setNotification(null), 3500);
  };

  const handlePanicToggle = () => {
    const next = !panicLocked;
    setPanicLocked(next);
    setNotification({
      msg: next
        ? "Panic lockdown initiated across all server channels."
        : "Lockdown lifted and channel permissions restored.",
      variant: next ? "warning" : "success",
    });
    setTimeout(() => setNotification(null), 4000);
  };

  const handleAddWhitelist = () => {
    if (!whitelistUser.trim() || whitelist.includes(whitelistUser.trim())) return;
    setWhitelist([...whitelist, whitelistUser.trim()]);
    setNotification({
      msg: `User ID ${whitelistUser.trim()} added to whitelist.`,
      variant: "success",
    });
    setWhitelistUser("");
    setTimeout(() => setNotification(null), 3500);
  };

  const handleRemoveWhitelist = (id: string) => {
    setWhitelist(whitelist.filter((u) => u !== id));
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Antinuke & Defense"
        description="Real-time mitigation against mass destructive actions and rogue administrators."
        action={
          <Button
            variant={panicLocked ? "secondary" : "danger"}
            size="sm"
            onClick={handlePanicToggle}
            className="gap-1.5"
          >
            {panicLocked ? <Unlock className="h-3.5 w-3.5" /> : <Lock className="h-3.5 w-3.5" />}
            {panicLocked ? "Lift Panic Lockdown" : "Panic Lockdown"}
          </Button>
        }
      />

      {notification && (
        <Alert variant={notification.variant} dismissible onDismiss={() => setNotification(null)}>
          {notification.msg}
        </Alert>
      )}

      {/* Control Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">Shield Status</span>
              <Badge variant={enabled ? "success" : "danger"}>
                {enabled ? "Active" : "Disabled"}
              </Badge>
            </div>
            <p className="text-[11px] text-slate-500 mt-1">Master antinuke watcher</p>
          </div>
          <div className="mt-3">
            <Button
              size="sm"
              variant={enabled ? "secondary" : "primary"}
              onClick={handleToggleShield}
              className="w-full"
            >
              {enabled ? "Disable Shield" : "Enable Shield"}
            </Button>
          </div>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <span className="text-xs font-medium text-slate-400">Countermeasure</span>
            <p className="text-[11px] text-slate-500 mt-0.5">Automated penalty for culprits</p>
          </div>
          <div className="mt-2">
            <Select value={actionType} onChange={(e) => setActionType(e.target.value)}>
              <option value="ban">Instant Ban</option>
              <option value="kick">Instant Kick</option>
              <option value="quarantine">Isolate to Quarantine Role</option>
              <option value="strip">Strip All Administrative Roles</option>
            </Select>
          </div>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">Rate Window</span>
              <span className="text-xs font-mono text-primary-light">{windowSec}s</span>
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">Detection timeframe window</p>
          </div>
          <div className="mt-3">
            <input
              type="range"
              min="5"
              max="60"
              value={windowSec}
              onChange={(e) => setWindowSec(Number(e.target.value))}
              className="w-full accent-primary h-1.5 bg-surface rounded cursor-pointer"
            />
          </div>
        </Card>
      </div>

      {/* Thresholds */}
      <Card>
        <CardHeader>
          <CardTitle>Action Thresholds</CardTitle>
          <CardDescription>Max actions allowed within {windowSec} seconds before automated interception</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="space-y-1.5">
              <label className="text-xs text-slate-400">Max Channel Deletions</label>
              <Input
                type="number"
                min="1"
                max="20"
                value={channelLimit}
                onChange={(e) => setChannelLimit(Number(e.target.value))}
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs text-slate-400">Max Role Deletions</label>
              <Input
                type="number"
                min="1"
                max="20"
                value={roleLimit}
                onChange={(e) => setRoleLimit(Number(e.target.value))}
              />
            </div>
            <div className="space-y-1.5">
              <label className="text-xs text-slate-400">Max Bans / Kicks</label>
              <Input
                type="number"
                min="1"
                max="50"
                value={banLimit}
                onChange={(e) => setBanLimit(Number(e.target.value))}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Whitelist and Audit Logs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <UserCheck className="h-4 w-4 text-emerald-400" />
              <CardTitle>Trusted Whitelist</CardTitle>
            </div>
            <CardDescription>Accounts exempt from antinuke limits. Server owner is exempt by default.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex gap-2">
              <Input
                type="text"
                placeholder="Discord User ID"
                value={whitelistUser}
                onChange={(e) => setWhitelistUser(e.target.value)}
              />
              <Button size="sm" onClick={handleAddWhitelist}>Add</Button>
            </div>
            <div className="space-y-1.5 max-h-40 overflow-y-auto">
              {whitelist.map((id) => (
                <div key={id} className="flex items-center justify-between rounded border border-card-border bg-surface px-2.5 py-1.5 text-xs">
                  <span className="font-mono text-slate-300">{id}</span>
                  <button onClick={() => handleRemoveWhitelist(id)} className="text-slate-500 hover:text-red-400 text-xs">
                    Remove
                  </button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-amber-400" />
              <CardTitle>Recent Interceptions</CardTitle>
            </div>
            <CardDescription>Security threshold triggers and automated actions</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {logs.map((log) => (
                <div key={log.id} className="rounded border border-red-500/20 bg-red-500/5 p-2.5 text-xs space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-red-400 uppercase tracking-wide">{log.event_type}</span>
                    <Badge variant="danger">{log.action_taken}</Badge>
                  </div>
                  <p className="text-slate-400 text-[11px]">{log.details}</p>
                  <div className="flex justify-between text-slate-500 text-[10px] pt-0.5">
                    <span>Target: {log.culprit_id}</span>
                    <span>{log.created_at}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default function AntiNukePage() {
  return <AntinukeControl />;
}
