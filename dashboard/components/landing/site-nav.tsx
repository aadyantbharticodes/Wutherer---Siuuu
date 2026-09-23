import Link from "next/link";
import { ChevronDown, User } from "lucide-react";
import { BrandMark } from "@/components/landing/brand-mark";

export function SiteNav() {
  return (
    <header className="outer-nav">
      <Link href="/" className="brand-lockup" aria-label="Wutherer home">
        <span className="brand-mark brand-mark-circle">
          <BrandMark />
        </span>
        <span className="brand-word">Wutherer</span>
      </Link>

      <nav className="nav-pill" aria-label="Primary">
        <a href="#product">Home</a>
        <Link href="/dashboard">Workspace</Link>
        <a href="#preview">Controls</a>
        <a href="#capabilities">Features</a>
        <a href="#capabilities">Signals</a>
        <a href="#preview">FAQ</a>
        <span className="nav-divider" aria-hidden="true" />
        <span className="nav-protect">
          Protection
          <ChevronDown size={12} aria-hidden="true" />
          <span className="nav-shield" aria-hidden="true">
            <BrandMark size={12} />
          </span>
        </span>
      </nav>

      <div className="nav-end">
        <Link href="/dashboard" className="create-account">
          <User size={14} aria-hidden="true" />
          <span>Create Account</span>
        </Link>
      </div>
    </header>
  );
}
