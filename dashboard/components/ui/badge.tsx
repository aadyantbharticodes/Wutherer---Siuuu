import * as React from "react";
import { cn } from "@/lib/utils";

const variants = {
  default: "bg-surface border border-card-border text-slate-300",
  primary: "bg-primary-subtle border border-primary/30 text-primary-light",
  success: "bg-emerald-500/10 border border-emerald-500/30 text-emerald-400",
  danger: "bg-red-500/10 border border-red-500/30 text-red-400",
  warning: "bg-amber-500/10 border border-amber-500/30 text-amber-400",
};

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: keyof typeof variants;
}

export function Badge({
  className,
  variant = "default",
  ...props
}: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded px-2 py-0.5 text-xs font-medium",
        variants[variant],
        className
      )}
      {...props}
    />
  );
}
