"use client";

import Link from "next/link";
import { ArrowLeft, Server, ShieldCheck } from "lucide-react";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

export function DashboardHeader() {
  const pathname = usePathname();
  const inGuild = pathname.includes("/dashboard/guild/");

  return (
    <header className="sticky top-0 z-40 border-b border-card-border bg-background/95 backdrop-blur">
      <div className="flex h-16 items-center gap-4 px-4 sm:px-6">
        <Link href="/" className="flex shrink-0 items-center gap-2.5" aria-label="Wutherer home">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-sky-400 text-slate-950 shadow-sm shadow-primary/20">
            <ShieldCheck className="h-4.5 w-4.5" aria-hidden="true" />
          </span>
          <span className="text-sm font-semibold tracking-tight text-white">Wutherer</span>
        </Link>

        <span className="hidden h-5 w-px bg-card-border sm:block" />
        <div className="min-w-0 flex-1 text-sm">
          <span className="text-slate-500">Workspace</span>
          {inGuild && <span className="ml-2 text-slate-300">/ server controls</span>}
        </div>

        <nav className="flex items-center gap-1" aria-label="Workspace navigation">
          <Link
            href="/dashboard"
            className={cn(
              "inline-flex h-8 items-center gap-1.5 rounded-md px-2.5 text-xs font-medium transition-colors",
              pathname === "/dashboard" ? "bg-primary-subtle text-primary-light" : "text-slate-400 hover:bg-surface-hover hover:text-white"
            )}
          >
            <Server className="h-3.5 w-3.5" aria-hidden="true" />
            <span className="hidden sm:inline">Servers</span>
          </Link>
          <Link
            href="/"
            className="inline-flex h-8 items-center gap-1.5 rounded-md px-2.5 text-xs font-medium text-slate-400 transition-colors hover:bg-surface-hover hover:text-white"
          >
            <ArrowLeft className="h-3.5 w-3.5" aria-hidden="true" />
            <span className="hidden sm:inline">Home</span>
          </Link>
        </nav>
      </div>
    </header>
  );
}
