import Link from "next/link";
import { ArrowRight, Play } from "lucide-react";

export function Hero() {
  return (
    <div className="hero-layer">
      <a href="#preview" className="hero-play" aria-label="Jump to interactive preview">
        <Play size={16} fill="currentColor" />
      </a>
      <a href="#preview" className="hero-chip">
        <span className="hero-chip-dot">
          <ArrowRight size={11} />
        </span>
        Live server safeguards are ready
        <ArrowRight size={12} />
      </a>
      <h1 className="hero-title">One console for server safety and momentum.</h1>
      <p className="hero-copy">
        Wutherer keeps moderation, member onboarding, and routine automation in a single quiet workspace — so small teams can run large Discord servers without the chaos.
      </p>
      <div className="hero-actions">
        <Link href="/dashboard" className="cta-dark">
          Open Workspace
          <ArrowRight size={14} />
        </Link>
        <a href="#capabilities" className="cta-light">
          Explore Controls
        </a>
      </div>
      <p className="hero-note">Connect a server to see its real modules and activity.</p>
      <div className="light-streaks" aria-hidden="true">
        <span />
        <span />
        <span />
        <span />
        <span />
        <span />
        <span />
      </div>
    </div>
  );
}
