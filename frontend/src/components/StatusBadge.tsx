import { cn } from "@/lib/utils";

type Status = "healthy" | "warning" | "error" | "loading";

interface StatusBadgeProps {
  status: Status;
  label?: string;
}

export function StatusBadge({ status, label }: StatusBadgeProps) {
  const statusConfig = {
    healthy: {
      className: "bg-success/10 text-success border-success/20",
      dot: "bg-success",
      defaultLabel: "Healthy",
    },
    warning: {
      className: "bg-warning/10 text-warning-foreground border-warning/20",
      dot: "bg-warning",
      defaultLabel: "Warning",
    },
    error: {
      className: "bg-destructive/10 text-destructive border-destructive/20",
      dot: "bg-destructive",
      defaultLabel: "Error",
    },
    loading: {
      className: "bg-muted text-muted-foreground border-muted",
      dot: "bg-muted-foreground animate-pulse",
      defaultLabel: "Loading",
    },
  };

  const config = statusConfig[status];

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border",
        config.className
      )}
    >
      <span className={cn("w-1.5 h-1.5 rounded-full", config.dot)} />
      {label || config.defaultLabel}
    </span>
  );
}
