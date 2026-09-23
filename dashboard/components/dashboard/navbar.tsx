"use client";

import Link from "next/link";
import { ArrowRight, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { BrandMark } from "@/components/landing/brand-mark";

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-white/10 bg-background/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2.5">
          <span className="brand-mark">
            <BrandMark />
          </span>
          <span className="text-sm font-medium tracking-tight text-white">Wutherer</span>
        </Link>

        <nav className="flex items-center gap-1 sm:gap-2" aria-label="Primary navigation">
          <a href="#product" className="hidden px-2 py-1.5 text-xs font-medium text-slate-400 transition-colors hover:text-white sm:block">Product</a>
          <a href="#capabilities" className="hidden px-2 py-1.5 text-xs font-medium text-slate-400 transition-colors hover:text-white sm:block">Capabilities</a>
          <Link href="/dashboard" className="px-2 py-1.5 text-xs font-medium text-slate-300 transition-colors hover:text-white">
            Servers
          </Link>
          <a
            href="https://discord.com"
            target="_blank"
            rel="noreferrer"
            className="hidden items-center gap-1 px-2 py-1.5 text-xs font-medium text-slate-400 transition-colors hover:text-white sm:flex"
          >
            Support
            <ArrowRight className="h-3 w-3" aria-hidden="true" />
          </a>
          <Link href="/dashboard">
            <Button size="sm">Open workspace</Button>
          </Link>
        </nav>
      </div>
    </header>
  );
}
