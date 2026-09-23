"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import { Check, ChevronDown, Server } from "lucide-react";
import { api } from "@/lib/api";
import type { Guild } from "@/types";

export function ServerSelector() {
  const params = useParams();
  const guildId = params.guildId as string | undefined;
  const [guilds, setGuilds] = useState<Guild[]>([]);
  const [current, setCurrent] = useState<Guild | null>(null);
  const [open, setOpen] = useState(false);
  const boxRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api
      .getGuilds()
      .then((data) => setGuilds(Array.isArray(data) ? data : []))
      .catch(() => setGuilds([]));
  }, []);

  useEffect(() => {
    if (!guildId) {
      setCurrent(null);
      return;
    }
    const found = guilds.find((g) => g.id === guildId) ?? null;
    if (found) {
      setCurrent(found);
      return;
    }
    api
      .getGuildDetails(guildId)
      .then((data) =>
        setCurrent({
          id: String(data.id ?? guildId),
          name: String(data.name ?? "Server"),
          icon: (data.icon as string | null) ?? null,
          member_count: Number(data.member_count ?? 0),
          owner_id: "",
        })
      )
      .catch(() => setCurrent(null));
  }, [guildId, guilds]);

  useEffect(() => {
    if (!open) return;
    const onClick = (e: MouseEvent) => {
      if (boxRef.current && !boxRef.current.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("mousedown", onClick);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onClick);
      document.removeEventListener("keydown", onKey);
    };
  }, [open ]);

  return (
    <div ref={boxRef} className="relative">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-haspopup="listbox"
        className="flex h-10 items-center gap-2.5 rounded-xl border border-card-border bg-surface px-2.5 pr-3 text-left transition-colors hover:border-primary/40"
      >
        {current?.icon ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={current.icon} alt="" className="h-7 w-7 rounded-lg object-cover" />
        ) : (
          <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary-subtle text-xs font-semibold text-primary">
            {current ? current.name.charAt(0).toUpperCase() : <Server className="h-3.5 w-3.5" />}
          </span>
        )}
        <span className="min-w-0">
          <span className="block max-w-40 truncate text-xs font-semibold text-white">
            {current ? current.name : "Select server"}
          </span>
          <span className="block text-[10px] text-slate-500">
            {current ? `${current.member_count.toLocaleString()} members` : "Switch workspace"}
          </span>
        </span>
        <ChevronDown className="h-3.5 w-3.5 shrink-0 text-slate-500" aria-hidden="true" />
      </button>

      {open && (
        <div
          role="listbox"
          aria-label="Switch server"
          className="absolute left-0 top-12 z-50 max-h-72 w-64 overflow-y-auto rounded-2xl border border-card-border bg-card p-1.5 shadow-2xl"
        >
          {guilds.length === 0 && (
            <p className="px-3 py-3 text-xs text-slate-500">No other servers are available.</p>
          )}
          {guilds.map((guild) => {
            const active = guild.id === guildId;
            return (
              <Link
                key={guild.id}
                role="option"
                aria-selected={active}
                href={`/dashboard/guild/${guild.id}`}
                onClick={() => setOpen(false)}
                className="flex items-center gap-2.5 rounded-xl px-2 py-2 transition-colors hover:bg-surface-hover"
              >
                {guild.icon ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={guild.icon} alt="" className="h-8 w-8 rounded-lg object-cover" />
                ) : (
                  <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-subtle text-xs font-semibold text-primary">
                    {guild.name.charAt(0).toUpperCase()}
                  </span>
                )}
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-xs font-medium text-white">{guild.name}</span>
                  <span className="block text-[10px] text-slate-500">
                    {guild.member_count.toLocaleString()} members
                  </span>
                </span>
                {active && <Check className="h-3.5 w-3.5 shrink-0 text-primary" aria-hidden="true" />}
              </Link>
            );
          })}
          <Link
            href="/dashboard"
            onClick={() => setOpen(false)}
            className="mt-1 block rounded-xl px-3 py-2 text-center text-xs font-medium text-slate-400 transition-colors hover:bg-surface-hover hover:text-white"
          >
            View all servers
          </Link>
        </div>
      )}
    </div>
  );
}
