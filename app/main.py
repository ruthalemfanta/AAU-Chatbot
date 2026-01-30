"""
AAU Helpdesk Chatbot - Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uvicorn
import random
from datetime import datetime

from nlp_engine import AAUNLPEngine
from templates import ResponseTemplates
from utils import DataLoader, TextProcessor, config, logger
from news_retriever import NewsRetriever

# Initialize FastAPI app
app = FastAPI(
    title="AAU Helpdesk Chatbot",
    description="Scalable chatbot for Addis Ababa University helpdesk services with NLP-based intent recognition and parameter extraction",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
nlp_engine = AAUNLPEngine()
news_retriever = NewsRetriever()
response_templates = ResponseTemplates()

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    parameters: Dict[str, Any]
    missing_parameters: List[str]
    needs_clarification: bool
    related_news: Optional[List[Dict[str, Any]]] = None
    timestamp: str

class TrainingRequest(BaseModel):
    training_data: List[Dict[str, Any]]

class EvaluationResponse(BaseModel):
    intent_accuracy: float
    parameter_metrics: Dict[str, Dict[str, float]]
    total_samples: int

# Global conversation context (in production, use Redis or database)
conversation_context = {}

@app.on_event("startup")
async def startup_event():
    """Initialize the chatbot on startup"""
    logger.info("Starting AAU Helpdesk Chatbot...")
    
    # Load and train with sample data
    training_data = DataLoader.get_sample_training_data()
    nlp_engine.train_intent_classifier(training_data)
    
    logger.info("Chatbot initialized successfully!")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AAU Helpdesk Chatbot API",
        "version": "1.0.0",
        "description": "NLP-powered chatbot for Addis Ababa University helpdesk services",
        "endpoints": {
            "/chat": "POST - Send a message to the chatbot",
            "/train": "POST - Train the chatbot with new data",
            "/evaluate": "POST - Evaluate chatbot performance",
            "/health": "GET - Health check",
            "/intents": "GET - List supported intents"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "nlp_engine_trained": nlp_engine.intent_classifier.is_trained
    }

@app.get("/intents")
async def get_intents():
    """Get list of supported intents"""
    return {
        "intents": nlp_engine.intent_classifier.intent_labels,
        "total_intents": len(nlp_engine.intent_classifier.intent_labels)
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        # Clean and validate input
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        cleaned_message = TextProcessor.clean_text(request.message)
        
        # Handle greetings
        if _is_greeting(cleaned_message):
            return ChatResponse(
                response=get_greeting_response(),
                intent="general_info",
                confidence=1.0,
                parameters={},
                missing_parameters=[],
                needs_clarification=False,
                timestamp=datetime.now().isoformat()
            )
        
        # Handle goodbyes
        if _is_goodbye(cleaned_message):
            return ChatResponse(
                response=get_goodbye_response(),
                intent="general_info",
                confidence=1.0,
                parameters={},
                missing_parameters=[],
                needs_clarification=False,
                timestamp=datetime.now().isoformat()
            )
        
        # Check for conversation context
        context = None
        if request.session_id and request.session_id in conversation_context:
            context = conversation_context[request.session_id]
        
        # Process with NLP engine (with context)
        result = nlp_engine.process_query(cleaned_message, context)
        
        # Generate response
        response_text = response_templates.generate_response(
            intent=result['intent'],
            parameters=result['parameters'],
            missing_parameters=result['missing_parameters'],
            confidence=result['confidence']
        )
        
        # News Retrieval (Assignment Feature)
        # Check if we can find real-time info from Telegram to augment the response
        related_news_items = None
        if result['confidence'] > 0.4:
            related_news_items = news_retriever.find_relevant_news(
                intent=result['intent'],
                parameters=result['parameters'],
                limit=3
            )
            
        # Store conversation context (merge with previous parameters)
        if request.session_id:
            # Merge current parameters with previous ones
            merged_parameters = {}
            if context and 'last_parameters' in context:
                merged_parameters.update(context['last_parameters'])
            merged_parameters.update(result['parameters'])
            
            conversation_context[request.session_id] = {
                'last_intent': result['intent'],
                'last_parameters': merged_parameters,
                'all_parameters': merged_parameters,  # Keep all collected parameters
                'conversation_history': conversation_context.get(request.session_id, {}).get('conversation_history', []) + [
                    {'user': cleaned_message, 'bot': response_text, 'timestamp': datetime.now().isoformat()}
                ],
                'timestamp': datetime.now().isoformat()
            }
        
        # Log conversation if enabled
        if config.get('log_conversations', True):
            conversation_log = {
                'user_message': request.message,
                'bot_response': response_text,
                'intent': result['intent'],
                'confidence': result['confidence'],
                'parameters': result['parameters'],
                'user_id': request.user_id,
                'session_id': request.session_id
            }
            # In production, save to database
            logger.info(f"Conversation: {conversation_log}")
        
        return ChatResponse(
            response=response_text,
            intent=result['intent'],
            confidence=result['confidence'],
            parameters=result['parameters'],
            missing_parameters=result['missing_parameters'],
            needs_clarification=result['needs_clarification'],
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return ChatResponse(
            response=response_templates.get_error_response(),
            intent="error",
            confidence=0.0,
            parameters={},
            missing_parameters=[],
            needs_clarification=True,
            timestamp=datetime.now().isoformat()
        )

@app.post("/train")
async def train_chatbot(request: TrainingRequest):
    """Train the chatbot with new data"""
    try:
        if not request.training_data:
            raise HTTPException(status_code=400, detail="Training data cannot be empty")
        
        # Validate training data format
        for item in request.training_data:
            if 'text' not in item or 'intent' not in item:
                raise HTTPException(status_code=400, detail="Each training item must have 'text' and 'intent' fields")
        
        # Train the model
        nlp_engine.train_intent_classifier(request.training_data)
        
        logger.info(f"Chatbot retrained with {len(request.training_data)} samples")
        
        return {
            "message": "Chatbot trained successfully",
            "samples_trained": len(request.training_data),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error training chatbot: {e}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_chatbot(test_data: List[Dict[str, Any]]):
    """Evaluate chatbot performance"""
    try:
        if not test_data:
            raise HTTPException(status_code=400, detail="Test data cannot be empty")
        
        results = []
        for item in test_data:
            if 'text' not in item or 'intent' not in item:
                continue
            
            # Process query
            result = nlp_engine.process_query(item['text'])
            
            results.append({
                'predicted_intent': result['intent'],
                'true_intent': item['intent'],
                'predicted_parameters': result['parameters'],
                'true_parameters': item.get('parameters', {}),
                'confidence': result['confidence']
            })
        
        # Calculate metrics
        intent_correct = sum(1 for r in results if r['predicted_intent'] == r['true_intent'])
        intent_accuracy = intent_correct / len(results) if results else 0.0
        
        # Calculate parameter metrics for common parameters
        parameter_metrics = {}
        common_params = ['department', 'semester', 'year', 'document_type', 'fee_amount']
        
        for param in common_params:
            param_results = []
            for result in results:
                pred_values = set(result['predicted_parameters'].get(param, []))
                true_values = set(result['true_parameters'].get(param, []))
                
                if pred_values or true_values:
                    param_results.append({
                        'predicted': pred_values,
                        'true': true_values
                    })
            
            if param_results:
                tp = sum(len(r['predicted'] & r['true']) for r in param_results)
                fp = sum(len(r['predicted'] - r['true']) for r in param_results)
                fn = sum(len(r['true'] - r['predicted']) for r in param_results)
                
                precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
                
                parameter_metrics[param] = {
                    'precision': precision,
                    'recall': recall,
                    'f1': f1
                }
        
        return EvaluationResponse(
            intent_accuracy=intent_accuracy,
            parameter_metrics=parameter_metrics,
            total_samples=len(results)
        )
        
    except Exception as e:
        logger.error(f"Error evaluating chatbot: {e}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

def _is_greeting(text: str) -> bool:
    """Check if message is a greeting"""
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings']
    text_lower = text.lower()
    return any(greeting in text_lower for greeting in greetings)

def _is_goodbye(text: str) -> bool:
    """Check if message is a goodbye"""
    goodbyes = ['bye', 'goodbye', 'see you', 'farewell', 'take care', 'thanks', 'thank you']
    text_lower = text.lower()
    return any(goodbye in text_lower for goodbye in goodbyes)

def get_greeting_response() -> str:
    """Get a random greeting response"""
    responses = [
        "Hello! Welcome to AAU Helpdesk. How can I assist you today?",
        "Hi there! I'm here to help with your AAU-related questions.",
        "Greetings! What can I help you with regarding Addis Ababa University?",
        "Good day! How may I be of service to you today?"
    ]
    return random.choice(responses)

def get_goodbye_response() -> str:
    """Get a random goodbye response"""
    responses = [
        "Goodbye! Feel free to return if you have more questions.",
        "Have a great day! Contact us again if you need any help.",
        "Bye! Best of luck with your studies at AAU.",
        "Farewell! We're here 24/7 if you need assistance."
    ]
    return random.choice(responses)

def get_error_response() -> str:
    """Get a random error response"""
    responses = [
        "I apologize, but I encountered an error processing your request. Please try again.",
        "Something went wrong on my end. Could you please rephrase your question?",
        "I'm having trouble understanding that right now. Please try again later.",
        "An unexpected error occurred. Our team has been notified."
    ]
    return random.choice(responses)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )