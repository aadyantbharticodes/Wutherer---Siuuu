"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Alert } from "@/components/ui/alert";
import { SectionHeader } from "@/components/ui/section-header";
import { Download, ArrowRight, Trash2 } from "lucide-react";
import { api } from "@/lib/api";

interface PublicTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  roles_count: number;
  categories_count: number;
}

interface CustomTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  created_at: string;
  usage_count: number;
}

export default function TemplatesPage() {
  const params = useParams();
  const guildId = params.guildId as string;

  const [publicTemplates, setPublicTemplates] = useState<PublicTemplate[]>([]);
  const [customTemplates, setCustomTemplates] = useState<CustomTemplate[]>([]);

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [deploying, setDeploying] = useState<string | null>(null);
  const [notification, setNotification] = useState<string | null>(null);

  const loadTemplates = async () => {
    try {
      const [publicResult, customResult] = await Promise.all([api.getPublicTemplates(), api.getGuildTemplates(guildId)]);
      setPublicTemplates(publicResult.templates || []);
      setCustomTemplates(customResult.templates || []);
    } catch { setNotification("Templates could not be loaded from the bot API."); }
  };

  useEffect(() => { if (guildId) loadTemplates(); }, [guildId]);

  const handleCreateTemplate = async () => {
    if (!name.trim()) return;
    try {
      await api.createTemplate(guildId, { name: name.trim(), description: description.trim(), category: "Custom" });
      setName(""); setDescription("");
      await loadTemplates();
      setNotification("Server blueprint saved.");
    } catch { setNotification("Could not save this server blueprint."); }
  };

  const handleApplyTemplate = async (tmplId: string, tmplName: string, wipe: boolean = false) => {
    if (wipe && !window.confirm(`Wipe and rebuild this server using “${tmplName}”? Existing channels and roles can be changed.`)) return;
    setDeploying(tmplId);
    try {
      await api.applyTemplate(guildId, tmplId, wipe ? "wipe" : "merge");
      setNotification(`Deployed “${tmplName}” using ${wipe ? "wipe and rebuild" : "merge"} mode.`);
    } catch { setNotification(`Could not deploy “${tmplName}”.`); }
    finally {
      setDeploying(null);
    }
  };

  const handleDeleteTemplate = async (tmplId: string) => {
    if (!window.confirm("Delete this saved template? This cannot be undone.")) return;
    try { await api.deleteTemplate(tmplId); setCustomTemplates(customTemplates.filter((t) => t.id !== tmplId)); }
    catch { setNotification("Could not delete this saved template."); }
  };

  return (
    <div className="space-y-5">
      <SectionHeader
        title="Server Templates"
        description="Backup, share, and deploy full server layouts, roles, and channel hierarchies."
      />

      {notification && (
        <Alert variant="success" dismissible onDismiss={() => setNotification(null)}>
          {notification}
        </Alert>
      )}

      {/* Save Blueprint Card */}
      <Card>
        <CardHeader>
          <CardTitle>Save Server Blueprint</CardTitle>
          <CardDescription>
            Export current channels, categories, and role hierarchies as a reusable template
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-2">
            <Input
              type="text"
              placeholder="Template Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="flex-1"
            />
            <Input
              type="text"
              placeholder="Short Description (Optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="flex-1"
            />
            <Button size="sm" onClick={handleCreateTemplate} className="gap-1.5 shrink-0">
              <Download className="h-3.5 w-3.5" />
              Save Blueprint
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Custom Saved Templates */}
      <div className="space-y-3">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Custom Blueprints</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {customTemplates.map((t) => (
            <Card key={t.id} className="space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="text-xs font-semibold text-white">{t.name}</h4>
                  <p className="text-[11px] text-slate-500 mt-0.5">{t.description}</p>
                </div>
                <span className="font-mono text-[10px] text-slate-500 bg-surface px-1.5 py-0.5 rounded border border-card-border">
                  {t.id}
                </span>
              </div>
              <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1 border-t border-card-border">
                <span>Created: {t.created_at}</span>
                <span>Used {t.usage_count}x</span>
              </div>
              <div className="flex gap-2 pt-1">
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() => handleApplyTemplate(t.id, t.name, false)}
                  disabled={deploying === t.id}
                  className="flex-1"
                >
                  {deploying === t.id ? "Deploying..." : "Apply (Merge)"}
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => handleDeleteTemplate(t.id)}
                  className="text-slate-500 hover:text-red-400"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Curated Templates */}
      <div className="space-y-3">
        <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Curated Presets</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {publicTemplates.map((t) => (
            <Card key={t.id} className="flex flex-col justify-between hover:border-slate-700 transition-colors">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Badge variant="primary">{t.category}</Badge>
                  <span className="text-[10px] text-slate-500">
                    {t.categories_count} cats • {t.roles_count} roles
                  </span>
                </div>
                <h4 className="text-xs font-semibold text-white">{t.name}</h4>
                <p className="text-[11px] text-slate-400 leading-relaxed">{t.description}</p>
              </div>

              <div className="pt-3 mt-3 border-t border-card-border space-y-1.5">
                <Button
                  size="sm"
                  className="w-full gap-1"
                  onClick={() => handleApplyTemplate(t.id, t.name, false)}
                  disabled={deploying === t.id}
                >
                  {deploying === t.id ? "Deploying..." : "Apply (Merge)"}
                  <ArrowRight className="h-3 w-3" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="w-full text-slate-500 hover:text-red-400"
                  onClick={() => handleApplyTemplate(t.id, t.name, true)}
                  disabled={deploying === t.id}
                >
                  Wipe & Rebuild
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
