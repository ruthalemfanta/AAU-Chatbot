import { useState, useCallback } from "react";
import { apiService, type ChatResponse } from "@/lib/api";

export interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: string;
  intent?: string;
  confidence?: number;
  parameters?: Record<string, any>;
  missing_parameters?: string[];
  related_news?: ChatResponse['related_news'];
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      content:
        "Welcome to AAU Helpdesk! 👋 I'm here to assist you with information about Addis Ababa University. How can I help you today?",
      isUser: false,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => `session-${Date.now()}`);

  const sendMessage = useCallback(async (content: string) => {
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      content,
      isUser: true,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response: ChatResponse = await apiService.sendMessage({
        message: content,
        session_id: sessionId,
      });

      const botMessage: Message = {
        id: `bot-${Date.now()}`,
        content: response.response,
        isUser: false,
        timestamp: new Date(response.timestamp).toLocaleTimeString([], { 
          hour: "2-digit", 
          minute: "2-digit" 
        }),
        intent: response.intent,
        confidence: response.confidence,
        parameters: response.parameters,
        missing_parameters: response.missing_parameters,
        related_news: response.related_news,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        content: "Sorry, I'm having trouble connecting to the server. Please try again later.",
        isUser: false,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  return { messages, sendMessage, isLoading };
}
