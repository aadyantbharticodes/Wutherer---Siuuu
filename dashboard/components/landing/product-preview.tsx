"use client";

import Link from "next/link";
import { useRef, useState } from "react";
import { ArrowRight, Bot, MessageSquare, ShieldCheck, Zap } from "lucide-react";
import { BrandMark } from "@/components/landing/brand-mark";

const views = {
  safety: {
    label: "Safety",
    icon: ShieldCheck,
    title: "Keep changes visible",
    description: "Review moderation activity, tune filters, and reach anti-nuke controls from one focused workspace.",
    rows: ["Moderation case history", "Message filter controls", "Verification settings"],
    stats: [
      { label: "Filters", value: "Armed" },
      { label: "Cases", value: "Live" },
      { label: "Antinuke", value: "Ready" },
    ],
  },
  automation: {
    label: "Automation",
    icon: Zap,
    title: "Make repeated work predictable",
    description: "Configure custom commands and response triggers with live lists that reflect what your bot has stored.",
    rows: ["Custom command library", "Auto-responder triggers", "YouTube upload alerts"],
    stats: [
      { label: "Commands", value: "Mapped" },
      { label: "Relays", value: "Active" },
      { label: "Alerts", value: "Queued" },
    ],
  },
  community: {
    label: "Community",
    icon: Bot,
    title: "Set up a better arrival",
    description: "Give new members a clearer first path with onboarding, tickets, and optional AI assistance.",
    rows: ["Onboarding messages", "Support ticket settings", "AI channel controls"],
    stats: [
      { label: "Onboarding", value: "Guided" },
      { label: "Tickets", value: "Open" },
      { label: "AI", value: "Optional" },
    ],
  },
} as const;

type ViewKey = keyof typeof views;

export function ProductPreview() {
  const [active, setActive] = useState<ViewKey>("safety");
  const frameRef = useRef<HTMLDivElement>(null);
  const view = views[active];
  const Icon = view.icon;

  const onMove = (event: React.PointerEvent<HTMLDivElement>) => {
    const frame = frameRef.current;
    if (!frame || window.matchMedia("(prefers-reduced-motion: reduce)").matches || window.innerWidth < 900) return;
    const rect = frame.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width - 0.5;
    const y = (event.clientY - rect.top) / rect.height - 0.5;
    frame.style.transform = `rotateX(${8 - y * 6}deg) rotateY(${-8 + x * 8}deg) translateZ(0)`;
  };

  const onLeave = () => {
    const frame = frameRef.current;
    if (!frame) return;
    frame.style.transform = "";
  };

  return (
    <section id="preview" className="section-wrap" aria-label="Product preview">
      <p className="section-kicker reveal">Interactive workspace</p>
      <h2 className="section-title reveal" data-delay="1">A miniature of the control center you actually open.</h2>
      <p className="section-copy reveal" data-delay="2">
        Switch between installed modules the same way your team will inside Wutherer. This preview is a visual slice of the live dashboard—not a marketing mock.
      </p>

      <div className="preview-orbit reveal" data-delay="3" onPointerMove={onMove} onPointerLeave={onLeave}>
        <div className="preview-frame" ref={frameRef}>
          <div className="preview-chrome">
            <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12, color: "#d5e2e8" }}>
              <span className="brand-mark" style={{ width: 26, height: 26, borderRadius: 8 }}>
                <BrandMark size={14} />
              </span>
              Wutherer workspace
            </div>
            <span style={{ fontSize: 11, color: "#7f93a0" }}>Live module map</span>
          </div>
          <div className="preview-body">
            <div className="preview-side">
              {(Object.keys(views) as ViewKey[]).map((key) => {
                const item = views[key];
                const ItemIcon = item.icon;
                return (
                  <button
                    key={key}
                    type="button"
                    className="preview-tab"
                    data-active={active === key}
                    onClick={() => setActive(key)}
                  >
                    <ItemIcon size={14} aria-hidden="true" />
                    {item.label}
                  </button>
                );
              })}
            </div>
            <div className="preview-main">
              <div className="feature-icon">
                <Icon size={16} aria-hidden="true" />
              </div>
              <h3 style={{ marginTop: 16, fontSize: 22, fontWeight: 500, letterSpacing: "-0.03em" }}>{view.title}</h3>
              <p style={{ marginTop: 8, maxWidth: "36rem", color: "#9bb0bc", fontSize: 14, lineHeight: 1.65 }}>{view.description}</p>
              <div className="preview-stat-row">
                {view.stats.map((stat) => (
                  <div key={stat.label} className="preview-stat">
                    <span style={{ fontSize: 11, color: "#7f93a0", letterSpacing: "0.08em", textTransform: "uppercase" }}>{stat.label}</span>
                    <b>{stat.value}</b>
                    <span className="pulse-bar" aria-hidden="true"><i /></span>
                  </div>
                ))}
              </div>
              <div style={{ marginTop: 18, display: "grid", gap: 8 }}>
                {view.rows.map((row) => (
                  <div key={row} style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13, color: "#d5e2e8" }}>
                    <MessageSquare size={14} color="#18D8C0" aria-hidden="true" />
                    {row}
                  </div>
                ))}
              </div>
              <Link href="/dashboard" className="cta-dark" style={{ marginTop: 22 }}>
                Open the workspace
                <ArrowRight size={14} aria-hidden="true" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
