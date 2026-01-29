// API service for AAU Helpdesk Chatbot
const API_BASE_URL = 'http://localhost:8000';

export interface ChatRequest {
  message: string;
  user_id?: string;
  session_id?: string;
}

export interface ChatResponse {
  response: string;
  intent: string;
  confidence: number;
  parameters: Record<string, any>;
  missing_parameters: string[];
  needs_clarification: boolean;
  timestamp: string;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  nlp_engine_trained: boolean;
}

export interface IntentsResponse {
  intents: string[];
  total_intents: number;
}

export interface TrainingRequest {
  training_data: Array<{
    text: string;
    intent: string;
    parameters?: Record<string, any>;
  }>;
}

export interface EvaluationResponse {
  intent_accuracy: number;
  parameter_metrics: Record<string, {
    precision: number;
    recall: number;
    f1: number;
  }>;
  total_samples: number;
}

class ApiService {
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Chat endpoint
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    return this.request<ChatResponse>('/chat', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Health check endpoint
  async getHealth(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/health');
  }

  // Get supported intents
  async getIntents(): Promise<IntentsResponse> {
    return this.request<IntentsResponse>('/intents');
  }

  // Train model
  async trainModel(request: TrainingRequest): Promise<{ message: string; samples_trained: number; timestamp: string }> {
    return this.request('/train', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Evaluate model
  async evaluateModel(testData: Array<{
    text: string;
    intent: string;
    parameters?: Record<string, any>;
  }>): Promise<EvaluationResponse> {
    return this.request<EvaluationResponse>('/evaluate', {
      method: 'POST',
      body: JSON.stringify(testData),
    });
  }

  // Get API info
  async getApiInfo(): Promise<any> {
    return this.request('/');
  }
}

export const apiService = new ApiService();