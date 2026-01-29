import { useRef, useEffect } from "react";
import { ChatHeader } from "@/components/ChatHeader";
import { ChatMessage } from "@/components/ChatMessage";
import { ChatInput } from "@/components/ChatInput";
import { useChat } from "@/hooks/useChat";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Loader2 } from "lucide-react";

export default function Chat() {
  const { messages, sendMessage, isLoading } = useChat();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  return (
    <div className="flex flex-col h-screen bg-background">
      <ChatHeader />
      
      <ScrollArea ref={scrollRef} className="flex-1 p-4">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.map((msg) => (
            <ChatMessage
              key={msg.id}
              message={msg.content}
              isUser={msg.isUser}
              timestamp={msg.timestamp}
              intent={msg.intent}
              confidence={msg.confidence}
              parameters={msg.parameters}
              missing_parameters={msg.missing_parameters}
            />
          ))}
          {isLoading && (
            <div className="flex gap-3 animate-fade-in">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-accent flex items-center justify-center">
                <Loader2 className="w-4 h-4 text-accent-foreground animate-spin" />
              </div>
              <div className="bg-chat-bot rounded-2xl rounded-tl-md px-4 py-3">
                <div className="flex gap-1">
                  <span className="w-2 h-2 rounded-full bg-muted-foreground/40 animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-2 h-2 rounded-full bg-muted-foreground/40 animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="w-2 h-2 rounded-full bg-muted-foreground/40 animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </div>
          )}
        </div>
      </ScrollArea>

      <div className="max-w-3xl mx-auto w-full">
        <ChatInput onSend={sendMessage} disabled={isLoading} />
      </div>
    </div>
  );
}
