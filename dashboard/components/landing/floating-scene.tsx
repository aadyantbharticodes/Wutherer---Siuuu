import { Shield, Sparkles, Ticket, Waves } from "lucide-react";

const nodes = [
  { className: "node-tl", title: "Sentinel", meta: "Safety graph", icon: Shield },
  { className: "node-tr", title: "Pulse", meta: "Live telemetry", icon: Sparkles },
  { className: "node-bl", title: "Relay", meta: "Automations", icon: Waves },
  { className: "node-br", title: "Harbor", meta: "Member flow", icon: Ticket },
];

export function FloatingScene() {
  return (
    <>
      <svg className="constellation" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
        <path d="M 8 24 C 24 24, 30 38, 50 40" />
        <path d="M 92 25 C 78 26, 70 38, 51 40" />
        <path d="M 9 74 C 26 74, 32 60, 49 58" />
        <path d="M 91 72 C 76 72, 68 60, 51 58" />
        <path d="M 8 24 C 6 44, 7 56, 9 74" />
        <path d="M 92 25 C 94 44, 93 56, 91 72" />
      </svg>
      {nodes.map((node) => {
        const Icon = node.icon;
        return (
          <div key={node.title} className={`floating-node ${node.className}`}>
            <span className="node-orb">
              <Icon size={14} />
            </span>
            <div>
              <strong>{node.title}</strong>
              <span>{node.meta}</span>
            </div>
          </div>
        );
      })}
    </>
  );
}
