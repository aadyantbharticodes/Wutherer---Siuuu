"use client";

import Link from "next/link";
import { ArrowLeft, Server } from "lucide-react";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { BrandMark } from "@/components/landing/brand-mark";

export function DashboardHeader() {
  const pathname = usePathname();
  const inGuild = pathname.includes("/dashboard/guild/");

  return (
    <header className="dash-header sticky top-0 z-40">
      <div className="flex h-16 items-center gap-4 px-4 sm:px-6">
        <Link href="/" className="flex shrink-0 items-center gap-2.5" aria-label="Wutherer home">
          <span className="brand-mark">
            <BrandMark />
          </span>
          <span className="text-sm font-medium tracking-tight text-white">Wutherer</span>
        </Link>

        <span className="hidden h-5 w-px bg-white/10 sm:block" />
        <div className="min-w-0 flex-1 text-sm">
          <span className="text-slate-500">Workspace</span>
          {inGuild && <span className="ml-2 text-slate-300">/ server controls</span>}
        </div>

        <nav className="flex items-center gap-1" aria-label="Workspace navigation">
          <Link
            href="/dashboard"
            className={cn(
              "inline-flex h-8 items-center gap-1.5 rounded-full px-3 text-xs font-medium transition-colors",
              pathname === "/dashboard" ? "bg-primary-subtle text-primary" : "text-slate-400 hover:bg-surface-hover hover:text-white"
            )}
          >
            <Server className="h-3.5 w-3.5" aria-hidden="true" />
            <span className="hidden sm:inline">Servers</span>
          </Link>
          <Link
            href="/"
            className="inline-flex h-8 items-center gap-1.5 rounded-full px-3 text-xs font-medium text-slate-400 transition-colors hover:bg-surface-hover hover:text-white"
          >
            <ArrowLeft className="h-3.5 w-3.5" aria-hidden="true" />
            <span className="hidden sm:inline">Home</span>
          </Link>
        </nav>
      </div>
    </header>
  );
}
