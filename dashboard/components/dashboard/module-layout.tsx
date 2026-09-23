import * as React from "react";
import { cn } from "@/lib/utils";
import { SectionHeader } from "@/components/ui/section-header";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";

interface ModuleLayoutProps {
  title: string;
  description: string;
  enabled?: boolean;
  onToggleEnabled?: (enabled: boolean) => void;
  enableLabel?: string;
  statusLabel?: string;
  statusVariant?: "default" | "success" | "warning" | "danger" | "primary";
  saveLabel?: string;
  saving?: boolean;
  dirty?: boolean;
  onSave?: () => void;
  onReset?: () => void;
  message?: { text: string; variant: "success" | "error" | "warning" | "info" } | null;
  onDismissMessage?: () => void;
  children: React.ReactNode;
  className?: string;
}

export function ModuleLayout({
  title,
  description,
  enabled,
  onToggleEnabled,
  enableLabel = "Enable this module",
  statusLabel,
  statusVariant = "default",
  saveLabel = "Save Changes",
  saving,
  dirty,
  onSave,
  onReset,
  message,
  onDismissMessage,
  children,
  className,
}: ModuleLayoutProps) {
  return (
    <div className={cn("space-y-5", className)}>
      <SectionHeader
        title={title}
        description={description}
        action={
          <div className="flex shrink-0 items-center gap-2">
            {statusLabel && <Badge variant={statusVariant}>{statusLabel}</Badge>}
            {onReset && (
              <Button variant="ghost" size="sm" onClick={onReset} disabled={saving}>
                Reset
              </Button>
            )}
            {onSave && (
              <Button size="sm" onClick={onSave} disabled={saving || dirty === false}>
                {saving ? "Saving…" : saveLabel}
              </Button>
            )}
          </div>
        }
      />

      {message && (
        <Alert variant={message.variant} dismissible onDismiss={onDismissMessage}>
          {message.text}
        </Alert>
      )}

      {dirty && (
        <p className="text-xs font-medium text-amber-400">You have unsaved changes.</p>
      )}

      {typeof enabled === "boolean" && onToggleEnabled && (
        <div className="glass-card flex items-center justify-between rounded-2xl border border-card-border p-4">
          <div>
            <h2 className="text-sm font-medium text-white">{enableLabel}</h2>
            <p className="mt-0.5 text-[11px] text-slate-500">
              The bot only enforces this module while it is enabled.
            </p>
          </div>
          <Switch checked={enabled} onCheckedChange={onToggleEnabled} aria-label={enableLabel} />
        </div>
      )}

      {children}
    </div>
  );
}

export function ConfigSection({
  title,
  description,
  children,
  className,
}: {
  title: string;
  description?: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <section className={cn("glass-card rounded-2xl border border-card-border p-4", className)}>
      <h2 className="text-sm font-semibold text-white">{title}</h2>
      {description && <p className="mt-1 text-xs text-slate-500">{description}</p>}
      <div className="mt-4">{children}</div>
    </section>
  );
}
