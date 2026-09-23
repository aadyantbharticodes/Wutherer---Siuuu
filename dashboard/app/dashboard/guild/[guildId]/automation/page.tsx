"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Alert } from "@/components/ui/alert";
import { SectionHeader } from "@/components/ui/section-header";
import { EmptyState } from "@/components/ui/empty-state";
import { ConfirmModal } from "@/components/dashboard/confirm-modal";
import { Terminal, Trash2 } from "lucide-react";
import { api } from "@/lib/api";

interface CustomCommand {
  name: string;
  response: string;
}

export default function AutomationPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [commands, setCommands] = useState<CustomCommand[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState("");
  const [trigger, setTrigger] = useState("prefix");
  const [response, setResponse] = useState("");
  const [permission, setPermission] = useState("everyone");
  const [cooldown, setCooldown] = useState("5");
  const [pendingDelete, setPendingDelete] = useState<string | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" | "info" } | null>(null);

  useEffect(() => {
    if (guildId) {
      api.getCustomCommands(guildId)
        .then((data) => setCommands(Array.isArray(data) ? data : []))
        .catch(() => {
          setCommands([]);
          setMessage({ text: "Custom commands could not be loaded from the bot API.", variant: "error" });
        })
        .finally(() => setLoading(false));
    }
  }, [guildId]);

  const handleAdd = async () => {
    if (!name.trim() || !response.trim()) return;
    try {
      await api.createCustomCommand(guildId, name.trim(), response.trim());
      setCommands([...commands, { name: name.trim(), response: response.trim() }]);
      setName("");
      setResponse("");
      setMessage({ text: `Command "${name.trim()}" created. Only the name and response are stored by the bot API.`, variant: "success" });
    } catch {
      setMessage({ text: "Could not create the custom command.", variant: "error" });
    }
  };

  const confirmDelete = async () => {
    if (!pendingDelete) return;
    setDeleting(true);
    try {
      await api.deleteCustomCommand(guildId, pendingDelete);
      setCommands(commands.filter((c) => c.name !== pendingDelete));
      setPendingDelete(null);
    } catch {
      setMessage({ text: "Could not delete the custom command.", variant: "error" });
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Custom Commands"
        description="Server-defined command names with stored bot responses. The bot API stores a name and response per command."
      />

      {message && (
        <Alert variant={message.variant} dismissible onDismiss={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Command builder</CardTitle>
          <CardDescription>Structured fields. Only name and response are sent to the bot — the rest guide usage in Discord.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div className="space-y-1">
              <label className="text-xs text-slate-400" htmlFor="cc-name">Command name</label>
              <Input id="cc-name" type="text" placeholder="e.g. socials" value={name} onChange={(e) => setName(e.target.value)} />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400" htmlFor="cc-trigger">Trigger style</label>
              <Select id="cc-trigger" value={trigger} onChange={(e) => setTrigger(e.target.value)}>
                <option value="prefix">Server prefix (e.g. w!socials)</option>
                <option value="slash">Slash-style reference (/socials)</option>
              </Select>
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs text-slate-400" htmlFor="cc-response">Response</label>
            <Textarea id="cc-response" rows={3} placeholder="Bot reply. Supports multiple lines…" value={response} onChange={(e) => setResponse(e.target.value)} />
            <p className="text-[11px] text-slate-500">
              Variables depend on the bot&apos;s renderer. Common placeholders used in onboarding also work in some responses: {"{user.mention}"}, {"{guild.name}"}. Test in Discord after saving.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div className="space-y-1">
              <label className="text-xs text-slate-400" htmlFor="cc-permission">Intended audience</label>
              <Select id="cc-permission" value={permission} onChange={(e) => setPermission(e.target.value)}>
                <option value="everyone">Everyone</option>
                <option value="moderator">Moderators (enforce via Discord permissions)</option>
                <option value="admin">Administrators (enforce via Discord permissions)</option>
              </Select>
              <p className="text-[11px] text-slate-600">Not stored by the bot API — enforce with channel or role permissions in Discord.</p>
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400" htmlFor="cc-cooldown">Cooldown note (seconds)</label>
              <Input id="cc-cooldown" type="number" min="0" max="300" value={cooldown} onChange={(e) => setCooldown(e.target.value)} />
              <p className="text-[11px] text-slate-600">Not stored by the bot API — a reminder for how often members should use it.</p>
            </div>
          </div>

          <div className="flex justify-end pt-1">
            <Button size="sm" onClick={handleAdd} disabled={!name.trim() || !response.trim()}>Create Command</Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Registered Commands ({commands.length})</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="space-y-2 animate-pulse">
              {[1, 2].map((i) => (
                <div key={i} className="h-10 bg-surface rounded" />
              ))}
            </div>
          ) : commands.length === 0 ? (
            <EmptyState
              icon={Terminal}
              title="No Custom Commands"
              description="Build a command above. It is stored through the live bot API."
            />
          ) : (
            <div className="divide-y divide-card-border">
              {commands.map((cmd) => (
                <div key={cmd.name} className="py-3 flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-semibold text-primary-light bg-primary-subtle px-1.5 py-0.5 rounded border border-primary/20">
                        /{cmd.name}
                      </span>
                      <Badge variant="default">Custom</Badge>
                    </div>
                    <p className="text-xs text-slate-300">{cmd.response}</p>
                  </div>

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setPendingDelete(cmd.name)}
                    className="text-slate-500 hover:text-red-400"
                    aria-label={`Delete ${cmd.name}`}
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <ConfirmModal
        open={pendingDelete !== null}
        title="Delete custom command?"
        description={`"${pendingDelete ?? ""}" will be removed from the bot API and members will no longer be able to use it. This cannot be undone.`}
        confirmLabel="Delete command"
        danger
        busy={deleting}
        onConfirm={confirmDelete}
        onClose={() => !deleting && setPendingDelete(null)}
      />
    </div>
  );
}
