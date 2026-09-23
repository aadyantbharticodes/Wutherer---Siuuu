"use client";

import { useEffect, useRef } from "react";

type Particle = { x: number; y: number; vx: number; vy: number; r: number; a: number };
type Node = { x: number; y: number; z: number; phase: number; sx?: number; sy?: number };

export function AmbientBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d", { alpha: true });
    if (!ctx) return;

    const parent = canvas.parentElement ?? canvas;
    const mouse = { x: 0.5, y: 0.42 };
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
    let visible = true;
    let raf = 0;
    let width = 0;
    let height = 0;
    let dpr = 1;

    const isMobile = () => window.innerWidth < 720;
    const nodeCount = () => (isMobile() ? 8 : 14);
    const particleCount = () => (isMobile() ? 18 : 42);

    let nodes: Node[] = [];
    let particles: Particle[] = [];
    let orbits = [
      { rx: 0.22, ry: 0.12, rot: 0.2 },
      { rx: 0.34, ry: 0.18, rot: -0.35 },
      { rx: 0.16, ry: 0.28, rot: 0.8 },
    ];

    const seed = () => {
      nodes = Array.from({ length: nodeCount() }, () => ({
        x: 0.12 + Math.random() * 0.76,
        y: 0.16 + Math.random() * 0.68,
        z: 0.3 + Math.random() * 0.7,
        phase: Math.random() * Math.PI * 2,
      }));
      particles = Array.from({ length: particleCount() }, () => ({
        x: Math.random(),
        y: Math.random(),
        vx: (Math.random() - 0.5) * 0.00022,
        vy: (Math.random() - 0.5) * 0.00018,
        r: 0.6 + Math.random() * 1.4,
        a: 0.18 + Math.random() * 0.35,
      }));
    };

    const resize = () => {
      const rect = parent.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      width = Math.max(1, Math.floor(rect.width));
      height = Math.max(1, Math.floor(rect.height));
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      seed();
    };

    const drawStatic = () => {
      ctx.clearRect(0, 0, width, height);
      paintScene(0, 0.5, 0.42, true);
    };

    const paintScene = (t: number, mx: number, my: number, frozen: boolean) => {
      const cx = width * (0.54 + (mx - 0.5) * 0.04);
      const cy = height * (0.38 + (my - 0.4) * 0.04);

      ctx.fillStyle = "rgba(8, 18, 24, 0.08)";
      ctx.fillRect(0, 0, width, height);

      const gridY = height * 0.62;
      ctx.beginPath();
      ctx.strokeStyle = "rgba(120, 170, 185, 0.08)";
      ctx.lineWidth = 1;
      for (let i = -8; i <= 8; i += 1) {
        const x = cx + i * (width * 0.08);
        ctx.moveTo(x, gridY);
        ctx.lineTo(cx + i * 18, height);
      }
      for (let j = 0; j < 7; j += 1) {
        const y = gridY + j * j * 7;
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
      }
      ctx.stroke();

      orbits.forEach((orbit, index) => {
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(orbit.rot + (frozen ? 0 : t * (index % 2 === 0 ? 0.08 : -0.06)));
        ctx.beginPath();
        ctx.ellipse(0, 0, width * orbit.rx, height * orbit.ry, 0, 0, Math.PI * 2);
        ctx.strokeStyle = index === 1 ? "rgba(34, 199, 242, 0.16)" : "rgba(24, 216, 192, 0.12)";
        ctx.lineWidth = 1;
        ctx.stroke();
        const ang = frozen ? index : t * 0.4 + index;
        const px = Math.cos(ang) * width * orbit.rx;
        const py = Math.sin(ang) * height * orbit.ry;
        ctx.beginPath();
        ctx.arc(px, py, 2.2, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(232, 248, 246, 0.8)";
        ctx.fill();
        ctx.restore();
      });

      nodes.forEach((node, i) => {
        const drift = frozen ? 0 : Math.sin(t * 0.35 + node.phase) * 8 * node.z;
        const nx = node.x * width + (mx - 0.5) * 18 * node.z + drift;
        const ny = node.y * height + (my - 0.4) * 14 * node.z;
        node.sx = nx;
        node.sy = ny;
        for (let j = i + 1; j < nodes.length; j += 1) {
          const other = nodes[j];
          const ox = other.x * width + (mx - 0.5) * 18 * other.z;
          const oy = other.y * height + (my - 0.4) * 14 * other.z;
          const dx = nx - ox;
          const dy = ny - oy;
          const dist = Math.hypot(dx, dy);
          if (dist < 180) {
            ctx.beginPath();
            ctx.moveTo(nx, ny);
            ctx.lineTo(ox, oy);
            ctx.strokeStyle = `rgba(24, 216, 192, ${0.12 * (1 - dist / 180)})`;
            ctx.stroke();
          }
        }
      });

      nodes.forEach((node) => {
        const nx = node.sx ?? node.x * width;
        const ny = node.sy ?? node.y * height;
        ctx.beginPath();
        ctx.arc(nx, ny, 2.4 + node.z, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(34, 199, 242, 0.7)";
        ctx.fill();
      });

      particles.forEach((p) => {
        if (!frozen) {
          p.x += p.vx + (mx - 0.5) * 0.00004;
          p.y += p.vy + (my - 0.4) * 0.00003;
          if (p.x < 0) p.x = 1;
          if (p.x > 1) p.x = 0;
          if (p.y < 0) p.y = 1;
          if (p.y > 1) p.y = 0;
        }
        ctx.beginPath();
        ctx.arc(p.x * width, p.y * height, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(210, 236, 240, ${p.a})`;
        ctx.fill();
      });
    };

    const loop = (stamp: number) => {
      if (!visible || document.hidden || reduce.matches) return;
      const t = stamp / 1000;
      ctx.clearRect(0, 0, width, height);
      paintScene(t, mouse.x, mouse.y, false);
      raf = requestAnimationFrame(loop);
    };

    const start = () => {
      cancelAnimationFrame(raf);
      if (!reduce.matches && visible && !document.hidden) {
        raf = requestAnimationFrame(loop);
      } else {
        drawStatic();
      }
    };

    const onPointer = (event: PointerEvent) => {
      const rect = parent.getBoundingClientRect();
      mouse.x = (event.clientX - rect.left) / Math.max(rect.width, 1);
      mouse.y = (event.clientY - rect.top) / Math.max(rect.height, 1);
    };

    const observer = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      start();
    }, { threshold: 0.05 });
    observer.observe(canvas);

    resize();
    window.addEventListener("resize", resize);
    parent.addEventListener("pointermove", onPointer);
    document.addEventListener("visibilitychange", start);
    start();
    reduce.addEventListener("change", start);

    return () => {
      cancelAnimationFrame(raf);
      observer.disconnect();
      window.removeEventListener("resize", resize);
      parent.removeEventListener("pointermove", onPointer);
      document.removeEventListener("visibilitychange", start);
      reduce.removeEventListener("change", start);
    };
  }, []);

  return <canvas ref={canvasRef} className="amb-canvas" aria-hidden="true" />;
}
