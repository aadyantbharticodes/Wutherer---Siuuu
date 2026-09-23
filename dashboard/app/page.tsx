import { FeatureSection } from "@/components/landing/feature-section";
import { LandingShell } from "@/components/landing/landing-shell";
import { ProductPreview } from "@/components/landing/product-preview";
import { Activity, Layers, Shield, Workflow } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="landing-root">
      <LandingShell />

      <div className="logo-rail" aria-hidden="true">
        <span><Shield size={14} /> Sentinel</span>
        <span><Workflow size={14} /> Relay</span>
        <span><Activity size={14} /> Pulse</span>
        <span><Layers size={14} /> Harbor</span>
        <span>Automod</span>
        <span>Tickets</span>
        <span>Analytics</span>
      </div>

      <ProductPreview />
      <FeatureSection />

      <footer className="landing-footer">
        <p>© 2026 Wutherer. Quiet control for Discord servers.</p>
      </footer>
    </div>
  );
}
