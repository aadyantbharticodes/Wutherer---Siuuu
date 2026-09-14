"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Alert } from "@/components/ui/alert";
import { SectionHeader } from "@/components/ui/section-header";
import { EmptyState } from "@/components/ui/empty-state";
import { Youtube, Trash2, Plus } from "lucide-react";
import { api } from "@/lib/api";

interface YouTubeSub {
  id?: number;
  channel_id_yt: string;
  channel_name: string;
  notify_channel_id: number;
  notify_role_id?: number | null;
  custom_message?: string | null;
}

export default function YouTubeAlertsPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [subs, setSubs] = useState<YouTubeSub[]>([]);
  const [loading, setLoading] = useState(true);
  const [channelId, setChannelId] = useState("");
  const [channelName, setChannelName] = useState("");
  const [notifyChannel, setNotifyChannel] = useState("");
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" } | null>(null);

  useEffect(() => {
    if (guildId) {
      api.getYouTubeSubs(guildId)
        .then((data) => setSubs(data || []))
        .catch(() => {
          setSubs([]);
          setMessage({ text: "YouTube subscriptions could not be loaded from the bot API.", variant: "error" });
        })
        .finally(() => setLoading(false));
    }
  }, [guildId]);

  const handleAdd = async () => {
    if (!channelId.trim() || !channelName.trim()) return;
    const newSub: YouTubeSub = {
      channel_id_yt: channelId.trim(),
      channel_name: channelName.trim(),
      notify_channel_id: parseInt(notifyChannel) || 0,
      custom_message: "New upload from {channel}! {url}",
    };
    try {
      await api.createYouTubeSub(guildId, newSub);
      setSubs([...subs, newSub]);
    } catch {
      setMessage({ text: "Could not create the YouTube subscription.", variant: "error" });
      return;
    }
    setChannelId("");
    setChannelName("");
    setNotifyChannel("");
    setMessage({ text: `Subscribed to ${newSub.channel_name}.`, variant: "success" });
  };

  const handleDelete = async (ytId: string) => {
    try { await api.deleteYouTubeSub(guildId, ytId); setSubs(subs.filter((s) => s.channel_id_yt !== ytId)); }
    catch { setMessage({ text: "Could not remove the YouTube subscription.", variant: "error" }); }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="YouTube Upload Alerts"
        description="Monitor YouTube channels and automatically dispatch notifications to text channels."
      />

      {message && (
        <Alert variant={message.variant} dismissible onDismiss={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Subscribe to YouTube Channel</CardTitle>
          <CardDescription>Enter the YouTube channel identifier and notification target channel</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Channel Name</label>
              <Input
                type="text"
                placeholder="e.g. Linus Tech Tips"
                value={channelName}
                onChange={(e) => setChannelName(e.target.value)}
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400">YouTube Channel ID</label>
              <Input
                type="text"
                placeholder="UC..."
                value={channelId}
                onChange={(e) => setChannelId(e.target.value)}
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Discord Channel ID</label>
              <Input
                type="text"
                placeholder="Target channel ID..."
                value={notifyChannel}
                onChange={(e) => setNotifyChannel(e.target.value)}
              />
            </div>
          </div>
          <div className="flex justify-end pt-1">
            <Button size="sm" onClick={handleAdd} className="gap-1.5">
              <Plus className="h-3.5 w-3.5" />
              Subscribe
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Monitored Channels ({subs.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="space-y-2 animate-pulse">
              {[1, 2].map((i) => (
                <div key={i} className="h-10 bg-surface rounded" />
              ))}
            </div>
          ) : subs.length === 0 ? (
            <EmptyState
              icon={Youtube}
              title="No YouTube Subscriptions"
              description="Subscribe to a YouTube channel above to receive automated upload alerts."
            />
          ) : (
            <div className="divide-y divide-card-border">
              {subs.map((s) => (
                <div key={s.channel_id_yt} className="py-3 flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-white">{s.channel_name}</span>
                      <Badge variant="success">Monitoring</Badge>
                      <span className="font-mono text-[10px] text-slate-500">{s.channel_id_yt}</span>
                    </div>
                    {s.notify_channel_id ? (
                      <p className="text-[11px] text-slate-400">
                        Posting to channel ID: <code className="text-slate-300">{s.notify_channel_id}</code>
                      </p>
                    ) : null}
                  </div>

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(s.channel_id_yt)}
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
