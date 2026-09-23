"use client";

import { useEffect, useRef } from "react";
import { AmbientBackground } from "@/components/landing/ambient-background";
import { FloatingScene } from "@/components/landing/floating-scene";
import { Hero } from "@/components/landing/hero";
import { SiteNav } from "@/components/landing/site-nav";
import { ArrowDown } from "lucide-react";

export function LandingShell() {
  const stageRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const stage = stageRef.current;
    if (!stage) return;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

    const onMove = (event: PointerEvent) => {
      if (reduce.matches) return;
      const rect = stage.getBoundingClientRect();
      const x = (event.clientX - rect.left) / Math.max(rect.width, 1);
      const y = (event.clientY - rect.top) / Math.max(rect.height, 1);
      stage.style.setProperty("--px", x.toFixed(4));
      stage.style.setProperty("--py", y.toFixed(4));
    };

    stage.addEventListener("pointermove", onMove);
    return () => stage.removeEventListener("pointermove", onMove);
  }, []);

  return (
    <>
      <SiteNav />
      <div className="landing-pad">
        <section id="product" ref={stageRef} className="landing-stage">
          <AmbientBackground />
          <div className="landing-cursor-glow" />
          <FloatingScene />
          <Hero />
          <a href="#preview" className="stage-meta">
            <span className="stage-meta-btn">
              <ArrowDown size={12} />
            </span>
            02 / 03 · Scroll down
          </a>
          <div className="stage-progress">
            <p className="stage-caption">Control horizons</p>
            <div className="stage-segments" aria-hidden="true">
              <span data-active="true" />
              <span />
              <span />
            </div>
          </div>
        </section>
      </div>
    </>
  );
}
