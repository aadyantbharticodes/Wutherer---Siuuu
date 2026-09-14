import Link from "next/link";
import { ArrowRight, BarChart3, ShieldCheck, Terminal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Navbar } from "@/components/dashboard/navbar";
import { ProductPreview } from "@/components/landing/product-preview";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Navbar />

      <main className="flex-1">
        <section id="product" className="border-b border-card-border">
          <div className="mx-auto grid max-w-7xl gap-10 px-4 py-12 sm:px-6 sm:py-16 lg:grid-cols-[minmax(0,0.9fr)_minmax(28rem,1.1fr)] lg:items-center lg:py-20">
            <div className="max-w-xl">
              <p className="text-xs font-semibold uppercase tracking-[0.16em] text-primary-light">Discord server control</p>
              <h1 className="mt-4 text-4xl font-semibold tracking-[-0.035em] text-white sm:text-5xl">Run a calmer, more capable community.</h1>
              <p className="mt-5 max-w-lg text-base leading-relaxed text-slate-400">Wutherer brings the bot controls your team uses together: safety, member workflows, automations, and integrations—without burying the useful settings.</p>
              <div className="mt-8 flex flex-wrap items-center gap-3">
                <Link href="/dashboard"><Button size="lg" className="gap-2">Open workspace <ArrowRight className="h-3.5 w-3.5" /></Button></Link>
                <a href="#capabilities"><Button size="lg" variant="secondary">Explore controls</Button></a>
              </div>
              <p className="mt-5 text-xs text-slate-500">Configure only the modules your server actually uses.</p>
            </div>
            <ProductPreview />
          </div>
        </section>

        <section id="capabilities" className="bg-surface/45">
          <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 sm:py-18">
            <div className="grid gap-8 border-b border-card-border pb-8 lg:grid-cols-[0.8fr_1.2fr]">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-primary-light">Built around real jobs</p>
                <h2 className="mt-3 text-2xl font-semibold tracking-tight text-white">A control center, not a wall of tiles.</h2>
              </div>
              <p className="max-w-2xl text-sm leading-relaxed text-slate-400">Each module uses the data Wutherer already manages. Open a server, see the available controls, and make focused changes with clear feedback.</p>
            </div>
            <div className="grid gap-px overflow-hidden border-b border-card-border md:grid-cols-3">
              {[
                { icon: ShieldCheck, title: "Safety that stays legible", text: "Review moderation cases, adjust message filters, set verification, and access anti-nuke controls." },
                { icon: Terminal, title: "Useful automation", text: "Build custom commands and response triggers instead of relying on a generic configuration maze." },
                { icon: BarChart3, title: "Context when it matters", text: "Use server analytics, backup inventory, and integrations to inform the next change." },
              ].map((feature) => {
                const Icon = feature.icon;
                return <article key={feature.title} className="border-r border-card-border px-0 py-7 last:border-r-0 md:px-6 first:md:pl-0"><Icon className="h-5 w-5 text-primary-light" aria-hidden="true" /><h3 className="mt-4 text-sm font-semibold text-white">{feature.title}</h3><p className="mt-2 text-sm leading-relaxed text-slate-400">{feature.text}</p></article>;
              })}
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-card-border py-6 bg-surface text-center text-xs text-slate-500">
        <p>© 2026 Wutherer. All rights reserved.</p>
      </footer>
    </div>
  );
}
