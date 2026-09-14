"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { SectionHeader } from "@/components/ui/section-header";
import { EmptyState } from "@/components/ui/empty-state";
import { Alert } from "@/components/ui/alert";
import { Archive, Trash2 } from "lucide-react";
import { api } from "@/lib/api";
import { BackupSnapshot } from "@/types";

export default function BackupsPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [backups, setBackups] = useState<BackupSnapshot[]>([]);
  const [loading, setLoading] = useState(true);
  const [notes, setNotes] = useState("");
  const [creating, setCreating] = useState(false);
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" } | null>(null);

  useEffect(() => {
    async function loadBackups() {
      try {
        const res = await api.getBackups(guildId);
        setBackups(res);
      } catch {
        setBackups([]);
        setMessage({ text: "Backups could not be loaded from the bot API.", variant: "error" });
      } finally {
        setLoading(false);
      }
    }
    if (guildId) {
      loadBackups();
    }
  }, [guildId]);

  const handleCreateSnapshot = async () => {
    setCreating(true);
    try {
      await api.createBackup(guildId, notes.trim());
      setBackups(await api.getBackups(guildId));
      setNotes("");
      setMessage({ text: "Backup snapshot created.", variant: "success" });
    } catch { setMessage({ text: "Could not create a backup snapshot.", variant: "error" }); }
    finally { setCreating(false); }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm("Delete this backup snapshot? This cannot be undone.")) return;
    try { await api.deleteBackup(guildId, id); setBackups(backups.filter((b) => b.backup_id !== id)); }
    catch { setMessage({ text: "Could not delete this backup snapshot.", variant: "error" }); }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Server Backups"
        description="Snapshots of channel structure, categories, roles, and permission overwrites."
      />

      {message && <Alert variant={message.variant} dismissible onDismiss={() => setMessage(null)}>{message.text}</Alert>}

      <Card>
        <CardHeader>
          <CardTitle>Create Snapshot</CardTitle>
          <CardDescription>Capture current channel hierarchy and roles</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex flex-col sm:flex-row gap-2">
            <Input
              type="text"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Snapshot label or description..."
              className="flex-1"
            />
            <Button size="sm" onClick={handleCreateSnapshot} disabled={creating} className="shrink-0">
              {creating ? "Creating…" : "Generate Snapshot"}
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Snapshots ({backups.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {backups.length === 0 ? (
            <EmptyState
              icon={Archive}
              title="No Snapshots Found"
              description="Generate a server snapshot above to create a backup."
            />
          ) : (
            <div className="divide-y divide-card-border">
              {backups.map((b) => (
                <div key={b.backup_id} className="py-3 flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-semibold text-white">{b.backup_id}</span>
                      <Badge variant="default">{new Date(b.created_at * 1000).toLocaleDateString()}</Badge>
                    </div>
                    <p className="text-xs text-slate-400">
                      {b.roles_count} roles • {b.channels_count} channels • {b.categories_count} categories
                    </p>
                    {b.notes && <p className="text-[11px] text-slate-500 italic">&ldquo;{b.notes}&rdquo;</p>}
                  </div>

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(b.backup_id)}
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
