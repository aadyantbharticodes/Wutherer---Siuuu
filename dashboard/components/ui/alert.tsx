import * as React from "react";
import { cn } from "@/lib/utils";
import { CheckCircle, AlertTriangle, XCircle, Info, X } from "lucide-react";

const variants = {
  success: {
    container: "bg-emerald-500/10 border-emerald-500/30 text-emerald-400",
    Icon: CheckCircle,
  },
  error: {
    container: "bg-red-500/10 border-red-500/30 text-red-400",
    Icon: XCircle,
  },
  warning: {
    container: "bg-amber-500/10 border-amber-500/30 text-amber-400",
    Icon: AlertTriangle,
  },
  info: {
    container: "bg-blue-500/10 border-blue-500/30 text-blue-400",
    Icon: Info,
  },
};

interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: keyof typeof variants;
  dismissible?: boolean;
  onDismiss?: () => void;
}

export function Alert({
  className,
  variant = "info",
  dismissible,
  onDismiss,
  children,
  ...props
}: AlertProps) {
  const { container, Icon } = variants[variant];

  return (
    <div
      className={cn(
        "flex items-start gap-3 rounded-md border px-3 py-2.5 text-sm",
        container,
        className
      )}
      {...props}
    >
      <Icon className="h-4 w-4 mt-0.5 shrink-0" />
      <div className="flex-1">{children}</div>
      {dismissible && onDismiss && (
        <button onClick={onDismiss} className="shrink-0 hover:opacity-70">
          <X className="h-3.5 w-3.5" />
        </button>
      )}
    </div>
  );
}
