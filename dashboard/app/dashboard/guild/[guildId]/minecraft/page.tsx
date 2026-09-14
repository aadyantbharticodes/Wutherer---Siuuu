"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Alert } from "@/components/ui/alert";
import { SectionHeader } from "@/components/ui/section-header";
import { EmptyState } from "@/components/ui/empty-state";
import { Gamepad2, Trash2, Plus } from "lucide-react";
import { api } from "@/lib/api";

interface MinecraftServer {
  id?: number;
  channel_id: number;
  server_ip: string;
  server_port?: number | null;
  server_type?: string | null;
}

export default function MinecraftTrackerPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [servers, setServers] = useState<MinecraftServer[]>([]);
  const [loading, setLoading] = useState(true);
  const [serverIp, setServerIp] = useState("");
  const [serverPort, setServerPort] = useState("25565");
  const [serverType, setServerType] = useState("java");
  const [channelId, setChannelId] = useState("");
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" } | null>(null);

  useEffect(() => {
    if (guildId) {
      api.getMinecraftServers(guildId)
        .then((data) => setServers(data || []))
        .catch(() => {
          setServers([]);
          setMessage({ text: "Minecraft trackers could not be loaded from the bot API.", variant: "error" });
        })
        .finally(() => setLoading(false));
    }
  }, [guildId]);

  const handleAdd = async () => {
    if (!serverIp.trim()) return;
    const newSrv: MinecraftServer = {
      channel_id: parseInt(channelId) || 0,
      server_ip: serverIp.trim(),
      server_port: parseInt(serverPort) || 25565,
      server_type: serverType,
    };
    try {
      await api.createMinecraftServer(guildId, newSrv);
      setServers([...servers, newSrv]);
    } catch {
      setMessage({ text: "Could not start tracking this Minecraft server.", variant: "error" });
      return;
    }
    setServerIp("");
    setMessage({ text: `Tracking server ${newSrv.server_ip}.`, variant: "success" });
  };

  const handleDelete = async (ip: string) => {
    try { await api.deleteMinecraftServer(guildId, ip); setServers(servers.filter((s) => s.server_ip !== ip)); }
    catch { setMessage({ text: "Could not remove this Minecraft tracker.", variant: "error" }); }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Minecraft Server Tracker"
        description="Query live player counts, MOTD, latency, and online status of Minecraft servers."
      />

      {message && (
        <Alert variant={message.variant} dismissible onDismiss={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Track Minecraft Server</CardTitle>
          <CardDescription>Enter server domain/IP and the status broadcast channel</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
            <div className="space-y-1 sm:col-span-2">
              <label className="text-xs text-slate-400">Server Address / IP</label>
              <Input
                type="text"
                placeholder="e.g. mc.hypixel.net"
                value={serverIp}
                onChange={(e) => setServerIp(e.target.value)}
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Port</label>
              <Input
                type="number"
                placeholder="25565"
                value={serverPort}
                onChange={(e) => setServerPort(e.target.value)}
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Edition</label>
              <Select value={serverType} onChange={(e) => setServerType(e.target.value)}>
                <option value="java">Java Edition</option>
                <option value="bedrock">Bedrock Edition</option>
              </Select>
            </div>
          </div>
          <div className="flex justify-end pt-1">
            <Button size="sm" onClick={handleAdd} className="gap-1.5">
              <Plus className="h-3.5 w-3.5" />
              Track Server
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Monitored Servers ({servers.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="space-y-2 animate-pulse">
              {[1, 2].map((i) => (
                <div key={i} className="h-10 bg-surface rounded" />
              ))}
            </div>
          ) : servers.length === 0 ? (
            <EmptyState
              icon={Gamepad2}
              title="No Tracked Servers"
              description="Add a Minecraft server above to query real-time server telemetry."
            />
          ) : (
            <div className="divide-y divide-card-border">
              {servers.map((s) => (
                <div key={s.server_ip} className="py-3 flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-semibold text-white">{s.server_ip}:{s.server_port || 25565}</span>
                      <Badge variant="success">Tracking</Badge>
                      <Badge variant="default">{s.server_type?.toUpperCase() || "JAVA"}</Badge>
                    </div>
                    {s.channel_id ? (
                      <p className="text-[11px] text-slate-500">
                        Broadcasting to channel ID: <code className="text-slate-400">{s.channel_id}</code>
                      </p>
                    ) : null}
                  </div>

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(s.server_ip)}
                    className="text-slate-500 hover:text-red-400"
                  >
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
