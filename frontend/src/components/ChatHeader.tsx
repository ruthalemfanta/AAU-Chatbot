import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { BarChart3 } from "lucide-react";
import aauLogo from "@/assets/aau-logo.png";

export function ChatHeader() {
  return (
    <header className="flex items-center justify-between px-4 py-3 border-b bg-card">
      <div className="flex items-center gap-3">
        <img
          src={aauLogo}
          alt="AAU Logo"
          className="w-10 h-10 object-contain"
        />
        <div>
          <h1 className="font-heading font-semibold text-foreground">AAU Helpdesk</h1>
          <p className="text-xs text-muted-foreground">Addis Ababa University Assistant</p>
        </div>
      </div>
      <Link to="/metrics">
        <Button variant="outline" size="sm" className="gap-2">
          <BarChart3 className="h-4 w-4" />
          <span className="hidden sm:inline">Metrics</span>
        </Button>
      </Link>
    </header>
  );
}
