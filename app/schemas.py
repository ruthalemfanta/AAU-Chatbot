"""Pydantic schemas for request/response validation and data models."""
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Slot(BaseModel):
    """Slot (parameter) definition model."""
    name: str = Field(..., description="Slot name (e.g., 'department', 'fee_type')")
    value: Optional[str] = Field(None, description="Extracted slot value")
    start: Optional[int] = Field(None, description="Start position in text (for annotation)")
    end: Optional[int] = Field(None, description="End position in text (for annotation)")
    confidence: Optional[float] = Field(None, description="Extraction confidence score (0-1)")


class ConversationState(BaseModel):
    """Conversation state management model."""
    session_id: str = Field(..., description="Unique session identifier")
    current_intent: Optional[str] = Field(None, description="Currently identified intent")
    filled_slots: Dict[str, str] = Field(default_factory=dict, description="Filled slots dictionary")
    conversation_history: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="Conversation history (messages and responses)"
    )
    turn_counter: int = Field(default=0, description="Number of conversation turns")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


class IntentRequest(BaseModel):
    """Input schema for chat requests."""
    message: str = Field(..., description="User message text", min_length=1)
    session_id: Optional[str] = Field(None, description="Optional session ID for multi-turn conversations")
    conversation_state: Optional[ConversationState] = Field(
        None, 
        description="Optional existing conversation state"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "How much is the tuition fee?",
                "session_id": "session_12345"
            }
        }


class IntentResponse(BaseModel):
    """Output schema for chat responses."""
    response: str = Field(..., description="Bot response text")
    intent: Optional[str] = Field(None, description="Detected intent name")
    confidence: Optional[float] = Field(None, description="Intent classification confidence (0-1)")
    slots: Dict[str, str] = Field(default_factory=dict, description="Extracted slots dictionary")
    conversation_state: ConversationState = Field(..., description="Updated conversation state")
    requires_followup: bool = Field(default=False, description="Whether follow-up is needed")
    missing_slots: List[str] = Field(
        default_factory=list, 
        description="List of missing required slots"
    )
    follow_up_question: Optional[str] = Field(
        None, 
        description="Follow-up question if required slots are missing"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Which type of fee are you asking about?",
                "intent": "fee_payment",
                "confidence": 0.95,
                "slots": {},
                "requires_followup": True,
                "missing_slots": ["fee_type"],
                "follow_up_question": "Which type of fee are you asking about?"
            }
        }


class IntentDefinition(BaseModel):
    """Intent definition model (from intent.yaml)."""
    description: str = Field(..., description="Intent description")
    required_slots: List[str] = Field(default_factory=list, description="Required slot names")
    optional_slots: List[str] = Field(default_factory=list, description="Optional slot names")
    example_utterances: List[str] = Field(default_factory=list, description="Example user utterances")
    response_template: str = Field(..., description="Response template with slot placeholders")
    follow_up_questions: List[str] = Field(
        default_factory=list, 
        description="Follow-up questions for missing required slots"
    )


class SlotDefinition(BaseModel):
    """Slot definition model (from intent.yaml)."""
    description: str = Field(..., description="Slot description")
    examples: List[str] = Field(default_factory=list, description="Example slot values")
    extraction_hints: List[str] = Field(
        default_factory=list, 
        description="Keywords that help identify this slot"
    )


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(..., description="Health status")
    models: Optional[Dict[str, str]] = Field(None, description="Model loading status")
    api_version: Optional[str] = Field(None, description="API version")


class EvaluationMetrics(BaseModel):
    """Evaluation metrics schema."""
    intent_accuracy: float = Field(..., description="Overall intent classification accuracy")
    per_intent_metrics: Dict[str, Dict[str, float]] = Field(
        default_factory=dict, 
        description="Per-intent precision, recall, F1"
    )
    slot_metrics: Dict[str, Dict[str, float]] = Field(
        default_factory=dict, 
        description="Per-slot precision, recall, F1"
    )
    macro_f1: Optional[float] = Field(None, description="Macro-averaged F1 score")
    weighted_f1: Optional[float] = Field(None, description="Weighted F1 score")
