import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost" | "outline";
  size?: "sm" | "md" | "lg";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", ...props }, ref) => {
    const base = "inline-flex items-center justify-center rounded-full font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary disabled:pointer-events-none disabled:opacity-50 cursor-pointer";

    const variants = {
      primary: "bg-primary hover:bg-primary-hover text-slate-950 shadow-[0_8px_24px_rgba(24,216,192,0.18)]",
      secondary: "bg-surface/80 hover:bg-surface-hover text-foreground border border-card-border",
      danger: "bg-red-600 hover:bg-red-500 text-white",
      ghost: "hover:bg-surface-hover text-slate-300 hover:text-white",
      outline: "border border-card-border hover:border-primary/40 hover:bg-surface-hover text-foreground",
    };

    const sizes = {
      sm: "h-8 px-3 text-xs",
      md: "h-9 px-3.5 text-sm",
      lg: "h-10 px-4 text-sm",
    };

    return (
      <button
        ref={ref}
        className={cn(base, variants[variant], sizes[size], className)}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";
