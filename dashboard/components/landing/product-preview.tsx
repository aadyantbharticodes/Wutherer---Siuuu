"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowRight, Bot, MessageSquare, ShieldCheck, Zap } from "lucide-react";
import { cn } from "@/lib/utils";

const views = {
  safety: {
    label: "Safety",
    icon: ShieldCheck,
    title: "Keep changes visible",
    description: "Review moderation activity, tune filters, and reach anti-nuke controls from one focused workspace.",
    rows: ["Moderation case history", "Message filter controls", "Verification settings"],
  },
  automation: {
    label: "Automation",
    icon: Zap,
    title: "Make repeated work predictable",
    description: "Configure custom commands and response triggers with live lists that reflect what your bot has stored.",
    rows: ["Custom command library", "Auto-responder triggers", "YouTube upload alerts"],
  },
  community: {
    label: "Community",
    icon: Bot,
    title: "Set up a better arrival",
    description: "Give new members a clearer first path with onboarding, tickets, and optional AI assistance.",
    rows: ["Onboarding messages", "Support ticket settings", "AI channel controls"],
  },
} as const;

type ViewKey = keyof typeof views;

export function ProductPreview() {
  const [active, setActive] = useState<ViewKey>("safety");
  const view = views[active];
  const Icon = view.icon;

  return (
    <section className="overflow-hidden rounded-xl border border-card-border bg-card shadow-2xl shadow-black/20" aria-label="Product preview">
      <div className="flex items-center justify-between border-b border-card-border bg-surface px-4 py-3">
        <div className="flex items-center gap-2 text-xs font-medium text-slate-300">
          <span className="h-2 w-2 rounded-full bg-primary" aria-hidden="true" />
          Wutherer workspace
        </div>
        <span className="text-[11px] text-slate-500">Interactive preview</span>
      </div>
      <div className="grid min-h-[320px] grid-cols-[9.5rem_1fr]">
        <div className="border-r border-card-border bg-secondary p-2">
          {(Object.keys(views) as ViewKey[]).map((key) => {
            const item = views[key];
            const ItemIcon = item.icon;
            return (
              <button
                key={key}
                type="button"
                onClick={() => setActive(key)}
                className={cn(
                  "mb-1 flex w-full items-center gap-2 rounded-md px-2 py-2 text-left text-xs font-medium transition-colors",
                  active === key ? "bg-primary-subtle text-primary-light" : "text-slate-500 hover:bg-surface-hover hover:text-slate-200"
                )}
              >
                <ItemIcon className="h-3.5 w-3.5" aria-hidden="true" />
                {item.label}
              </button>
            );
          })}
        </div>
        <div className="flex min-w-0 flex-col p-5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-subtle text-primary-light">
            <Icon className="h-4 w-4" aria-hidden="true" />
          </div>
          <h2 className="mt-4 text-lg font-semibold tracking-tight text-white">{view.title}</h2>
          <p className="mt-2 text-sm leading-relaxed text-slate-400">{view.description}</p>
          <div className="mt-5 space-y-2 border-t border-card-border pt-4">
            {view.rows.map((row) => (
              <div key={row} className="flex items-center gap-2 text-xs text-slate-300">
                <MessageSquare className="h-3.5 w-3.5 text-primary" aria-hidden="true" />
                {row}
              </div>
            ))}
          </div>
          <Link href="/dashboard" className="mt-auto inline-flex items-center gap-1.5 pt-5 text-xs font-semibold text-primary-light hover:text-white">
            Open the workspace <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
          </Link>
        </div>
      </div>
    </section>
  );
}
