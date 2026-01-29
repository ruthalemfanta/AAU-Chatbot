import { cn } from "@/lib/utils";
import { Bot, User, Info } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
  intent?: string;
  confidence?: number;
  parameters?: Record<string, any>;
  missing_parameters?: string[];
}

export function ChatMessage({ 
  message, 
  isUser, 
  timestamp, 
  intent, 
  confidence, 
  parameters, 
  missing_parameters 
}: ChatMessageProps) {
  const [showDebug, setShowDebug] = useState(false);

  const hasDebugInfo = !isUser && (intent || confidence !== undefined || parameters || missing_parameters);

  return (
    <div
      className={cn(
        "flex gap-3 animate-slide-up",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
    >
      <div
        className={cn(
          "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
          isUser ? "bg-primary" : "bg-accent"
        )}
      >
        {isUser ? (
          <User className="w-4 h-4 text-primary-foreground" />
        ) : (
          <Bot className="w-4 h-4 text-accent-foreground" />
        )}
      </div>
      <div className="flex-1 max-w-[75%]">
        <div
          className={cn(
            "rounded-2xl px-4 py-3",
            isUser
              ? "chat-gradient text-primary-foreground rounded-tr-md"
              : "bg-chat-bot text-chat-bot-foreground rounded-tl-md"
          )}
        >
          <p className="text-sm leading-relaxed">{message}</p>
          {timestamp && (
            <span className="text-xs opacity-70 mt-1 block">{timestamp}</span>
          )}
        </div>
        
        {/* Debug Info */}
        {hasDebugInfo && (
          <div className="mt-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowDebug(!showDebug)}
              className="h-6 px-2 text-xs text-muted-foreground hover:text-foreground"
            >
              <Info className="w-3 h-3 mr-1" />
              {showDebug ? 'Hide' : 'Show'} Debug Info
            </Button>
            
            {showDebug && (
              <div className="mt-2 p-3 bg-muted/50 rounded-lg border text-xs space-y-2">
                {intent && (
                  <div className="flex items-center gap-2">
                    <span className="text-muted-foreground">Intent:</span>
                    <Badge variant="secondary" className="text-xs">
                      {intent}
                    </Badge>
                  </div>
                )}
                
                {confidence !== undefined && (
                  <div className="flex items-center gap-2">
                    <span className="text-muted-foreground">Confidence:</span>
                    <Badge 
                      variant={confidence > 0.7 ? "default" : confidence > 0.4 ? "secondary" : "destructive"}
                      className="text-xs"
                    >
                      {(confidence * 100).toFixed(1)}%
                    </Badge>
                  </div>
                )}
                
                {parameters && Object.keys(parameters).length > 0 && (
                  <div>
                    <span className="text-muted-foreground">Parameters:</span>
                    <div className="mt-1 flex flex-wrap gap-1">
                      {Object.entries(parameters).map(([key, value]) => (
                        <Badge key={key} variant="outline" className="text-xs">
                          {key}: {Array.isArray(value) ? value.join(', ') : String(value)}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
                
                {missing_parameters && missing_parameters.length > 0 && (
                  <div>
                    <span className="text-muted-foreground">Missing:</span>
                    <div className="mt-1 flex flex-wrap gap-1">
                      {missing_parameters.map((param) => (
                        <Badge key={param} variant="destructive" className="text-xs">
                          {param}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
