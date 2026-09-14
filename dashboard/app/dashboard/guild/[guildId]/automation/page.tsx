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
  const [response, setResponse] = useState("");
  const [message, setMessage] = useState<{ text: string; variant: "success" | "error" } | null>(null);

  useEffect(() => {
    if (guildId) {
      api.getCustomCommands(guildId)
        .then((data) => setCommands(data || []))
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
      setMessage({ text: `Command "${name.trim()}" created.`, variant: "success" });
    } catch {
      setMessage({ text: "Could not create the custom command.", variant: "error" });
    }
  };

  const handleDelete = async (cmdName: string) => {
    try {
      await api.deleteCustomCommand(guildId, cmdName);
      setCommands(commands.filter((c) => c.name !== cmdName));
    } catch {
      setMessage({ text: "Could not delete the custom command.", variant: "error" });
    }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Custom Automation"
        description="Create custom guild commands with static replies and multi-line responses."
      />

      {message && (
        <Alert variant={message.variant} dismissible onDismiss={() => setMessage(null)}>
          {message.text}
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Create Custom Command</CardTitle>
          <CardDescription>Define a command trigger name and the response the bot will send</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Command Name</label>
              <Input
                type="text"
                placeholder="e.g. socials, schedule"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Response Text</label>
              <Input
                type="text"
                placeholder="Bot reply content..."
                value={response}
                onChange={(e) => setResponse(e.target.value)}
              />
            </div>
          </div>
          <div className="flex justify-end pt-1">
            <Button size="sm" onClick={handleAdd}>Create Command</Button>
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
              description="Create a custom command above to get started."
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
                    onClick={() => handleDelete(cmd.name)}
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
