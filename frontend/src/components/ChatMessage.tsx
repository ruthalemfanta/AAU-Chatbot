import { cn } from "@/lib/utils";
import { Bot, User, Info, Newspaper } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
  intent?: string;
  confidence?: number;
  parameters?: Record<string, any>;
  missing_parameters?: string[];
  related_news?: Array<{
    text: string;
    channel: string;
    date: string;
    message_id: number;
  }>;
}

// Simple markdown-like formatting function
const formatMessage = (text: string): JSX.Element => {
  const lines = text.split('\n');
  
  // Helper for bold text processing
  const processBold = (text: string) => {
    return text.split(/(\*\*.*?\*\*)/g).map((part, idx) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={`b-${idx}`} className="font-semibold">{part.slice(2, -2)}</strong>;
      }
      return <span key={`s-${idx}`}>{part}</span>;
    });
  };

  // Helper for inline formatting (bold + links)
  const formatInline = (text: string) => {
    const elements = [];
    let lastIndex = 0;
    
    // Regex for markdown links: [label](url)
    const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    let match;
    
    while ((match = linkRegex.exec(text)) !== null) {
      // Text before link
      if (match.index > lastIndex) {
        const preText = text.substring(lastIndex, match.index);
        elements.push(...processBold(preText));
      }
      
      // The link itself
      const label = match[1];
      const url = match[2];
      elements.push(
        <a 
          key={`link-${match.index}`} 
          href={url} 
          target="_blank" 
          rel="noopener noreferrer" 
          className="text-primary hover:underline font-medium break-all"
        >
          {processBold(label)}
        </a>
      );
      
      lastIndex = match.index + match[0].length;
    }
    
    // Remaining text
    if (lastIndex < text.length) {
      elements.push(...processBold(text.substring(lastIndex)));
    }
    
    return elements.length > 0 ? elements : processBold(text);
  };

  return (
    <div className="space-y-1">
      {lines.map((line, i) => {
        if (!line.trim()) return <div key={i} className="h-2" />;
        
        // Lists
        if (/^\d+\./.test(line.trim())) {
           return <div key={i} className="ml-4 pl-1">{formatInline(line)}</div>;
        }
        if (line.trim().startsWith('- ')) {
           return (
             <div key={i} className="ml-4 pl-1 flex items-start">
               <span className="mr-2 mt-1.5 w-1 h-1 rounded-full bg-current shrink-0"></span>
               <span>{formatInline(line.trim().substring(2))}</span>
             </div>
           );
        }

        return <div key={i} className="leading-relaxed break-words">{formatInline(line)}</div>;
      })}
    </div>
  );
};

export function ChatMessage({ 
  message, 
  isUser, 
  timestamp, 
  intent, 
  confidence, 
  parameters, 
  missing_parameters,
  related_news
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
          <div className="text-sm">
            {isUser ? (
              <p className="leading-relaxed">{message}</p>
            ) : (
              formatMessage(message)
            )}
          </div>

          {related_news && related_news.length > 0 && (
            <div className="mt-4 pt-3 border-t border-primary/20">
              <div className="flex items-center gap-2 mb-3 text-sm font-bold text-primary">
                <Newspaper className="w-4 h-4" />
                <span>Latest Announcements</span>
              </div>
              <div className="space-y-3">
                {related_news.map((news, idx) => (
                  <div key={idx} className="bg-background/80 rounded-md p-3 text-sm border border-border/50 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-center mb-2 pb-2 border-b border-border/30">
                      <span className="font-semibold text-xs text-primary">{news.channel}</span>
                      <span className="text-[10px] text-muted-foreground bg-muted px-1.5 py-0.5 rounded">{news.date.split('T')[0]}</span>
                    </div>
                    <div className="text-foreground/90 leading-snug">
                      {formatMessage(news.text)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {timestamp && (
            <span className="text-xs opacity-70 mt-2 block">{timestamp}</span>
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
