"""
Comprehensive tests for AAU Helpdesk Chatbot
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add app directory to path
sys.path.append(str(Path(__file__).parent.parent / 'app'))

from nlp_engine import AAUNLPEngine, IntentClassifier, ParameterExtractor
from templates import ResponseTemplates
from utils import DataLoader, TextProcessor, ValidationUtils, ConfigManager

class TestIntentClassifier:
    """Test intent classification functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.classifier = IntentClassifier()
        self.sample_data = [
            {"text": "I want to apply for computer science", "intent": "admission_inquiry"},
            {"text": "How do I register for courses?", "intent": "registration_help"},
            {"text": "I need to pay my fees", "intent": "fee_payment"},
            {"text": "Can I get my transcript?", "intent": "transcript_request"},
            {"text": "What are my grades?", "intent": "grade_inquiry"}
        ]
    
    def test_training(self):
        """Test classifier training"""
        texts = [item["text"] for item in self.sample_data]
        labels = [item["intent"] for item in self.sample_data]
        
        self.classifier.train(texts, labels)
        assert self.classifier.is_trained == True
    
    def test_prediction(self):
        """Test intent prediction"""
        texts = [item["text"] for item in self.sample_data]
        labels = [item["intent"] for item in self.sample_data]
        
        self.classifier.train(texts, labels)
        
        intent, confidence = self.classifier.predict("I want to apply for engineering")
        assert intent in self.classifier.intent_labels
        assert 0 <= confidence <= 1
    
    def test_prediction_without_training(self):
        """Test prediction without training"""
        intent, confidence = self.classifier.predict("Hello")
        assert intent == "general_info"
        assert confidence == 0.5

class TestParameterExtractor:
    """Test parameter extraction functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.extractor = ParameterExtractor()
    
    def test_department_extraction(self):
        """Test department parameter extraction"""
        text = "I want to apply for computer science admission"
        params = self.extractor.extract_parameters(text, "admission_inquiry")
        
        assert "department" in params
        assert "computer science" in params["department"]
    
    def test_semester_extraction(self):
        """Test semester parameter extraction"""
        text = "I need help with second semester registration"
        params = self.extractor.extract_parameters(text, "registration_help")
        
        assert "semester" in params
        assert any("second" in sem for sem in params["semester"])
    
    def test_year_extraction(self):
        """Test year parameter extraction"""
        text = "What are my grades for 2024?"
        params = self.extractor.extract_parameters(text, "grade_inquiry")
        
        assert "year" in params
        assert "2024" in params["year"]
    
    def test_document_extraction(self):
        """Test document type extraction"""
        text = "I need my transcript urgently"
        params = self.extractor.extract_parameters(text, "transcript_request")
        
        assert "document_type" in params
        assert "transcript" in params["document_type"]
    
    def test_fee_amount_extraction(self):
        """Test fee amount extraction"""
        text = "I need to pay 5000 birr for tuition"
        params = self.extractor.extract_parameters(text, "fee_payment")
        
        assert "fee_amount" in params
        assert "5000" in params["fee_amount"]
    
    def test_empty_text(self):
        """Test parameter extraction with empty text"""
        params = self.extractor.extract_parameters("", "general_info")
        assert isinstance(params, dict)

class TestAAUNLPEngine:
    """Test main NLP engine"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.engine = AAUNLPEngine()
        self.sample_training_data = [
            {"text": "I want to apply for computer science", "intent": "admission_inquiry"},
            {"text": "How do I register for second semester?", "intent": "registration_help"},
            {"text": "I need to pay 5000 birr", "intent": "fee_payment"},
            {"text": "Can I get my transcript?", "intent": "transcript_request"},
            {"text": "What are my first semester grades?", "intent": "grade_inquiry"}
        ]
        self.engine.train_intent_classifier(self.sample_training_data)
    
    def test_process_query_complete(self):
        """Test processing query with complete information"""
        result = self.engine.process_query("I want to apply for computer science admission")
        
        assert "intent" in result
        assert "confidence" in result
        assert "parameters" in result
        assert "missing_parameters" in result
        assert "needs_clarification" in result
        assert isinstance(result["parameters"], dict)
        assert isinstance(result["missing_parameters"], list)
    
    def test_process_query_missing_params(self):
        """Test processing query with missing parameters"""
        result = self.engine.process_query("I want to apply for admission")
        
        assert result["needs_clarification"] == True
        assert len(result["missing_parameters"]) > 0
    
    def test_preprocess_text(self):
        """Test text preprocessing"""
        text = "I want to apply for CS at AAU"
        processed = self.engine._preprocess_text(text)
        
        assert "computer science" in processed.lower()
        assert "addis ababa university" in processed.lower()
    
    def test_get_required_parameters(self):
        """Test required parameters for different intents"""
        admission_params = self.engine._get_required_parameters("admission_inquiry")
        assert "department" in admission_params
        
        registration_params = self.engine._get_required_parameters("registration_help")
        assert "semester" in registration_params
        assert "year" in registration_params
        
        general_params = self.engine._get_required_parameters("general_info")
        assert len(general_params) == 0

class TestResponseTemplates:
    """Test response template system"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.templates = ResponseTemplates()
    
    def test_generate_complete_response(self):
        """Test generating complete response"""
        response = self.templates.generate_response(
            intent="admission_inquiry",
            parameters={"department": ["computer science"]},
            missing_parameters=[],
            confidence=0.8
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert "computer science" in response
    
    def test_generate_follow_up_response(self):
        """Test generating follow-up response"""
        response = self.templates.generate_response(
            intent="admission_inquiry",
            parameters={},
            missing_parameters=["department"],
            confidence=0.8
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
        # Should ask for department information
        assert any(word in response.lower() for word in ["department", "program", "field"])
    
    def test_low_confidence_response(self):
        """Test response for low confidence"""
        response = self.templates.generate_response(
            intent="admission_inquiry",
            parameters={},
            missing_parameters=[],
            confidence=0.3
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
        # Should ask for clarification
        assert any(word in response.lower() for word in ["clarify", "understand", "rephrase"])
    
    def test_greeting_response(self):
        """Test greeting response"""
        response = self.templates.get_greeting_response()
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_goodbye_response(self):
        """Test goodbye response"""
        response = self.templates.get_goodbye_response()
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_error_response(self):
        """Test error response"""
        response = self.templates.get_error_response()
        assert isinstance(response, str)
        assert len(response) > 0

class TestDataLoader:
    """Test data loading utilities"""
    
    def test_get_sample_training_data(self):
        """Test sample training data generation"""
        data = DataLoader.get_sample_training_data()
        
        assert isinstance(data, list)
        assert len(data) > 0
        
        for item in data:
            assert "text" in item
            assert "intent" in item
            assert "parameters" in item
            assert isinstance(item["text"], str)
            assert isinstance(item["intent"], str)
            assert isinstance(item["parameters"], dict)
    
    def test_load_nonexistent_file(self):
        """Test loading non-existent training file"""
        data = DataLoader.load_training_data("nonexistent_file.json")
        
        # Should return sample data when file doesn't exist
        assert isinstance(data, list)
        assert len(data) > 0

class TestTextProcessor:
    """Test text processing utilities"""
    
    def test_clean_text(self):
        """Test text cleaning"""
        dirty_text = "  Hello   world!  \n\n  "
        clean_text = TextProcessor.clean_text(dirty_text)
        
        assert clean_text == "Hello world!"
    
    def test_clean_empty_text(self):
        """Test cleaning empty text"""
        assert TextProcessor.clean_text("") == ""
        assert TextProcessor.clean_text(None) == ""
    
    def test_extract_numbers(self):
        """Test number extraction"""
        text = "I need to pay 5,000.50 birr and 1000 ETB"
        numbers = TextProcessor.extract_numbers(text)
        
        assert "5,000.50" in numbers
        assert "1000" in numbers
    
    def test_normalize_department_name(self):
        """Test department name normalization"""
        assert TextProcessor.normalize_department_name("CS") == "computer science"
        assert TextProcessor.normalize_department_name("eng") == "engineering"
        assert TextProcessor.normalize_department_name("Computer Science") == "computer science"

class TestValidationUtils:
    """Test validation utilities"""
    
    def test_validate_student_id(self):
        """Test student ID validation"""
        assert ValidationUtils.validate_student_id("CS/2024/01") == True
        assert ValidationUtils.validate_student_id("12345678") == True
        assert ValidationUtils.validate_student_id("invalid") == False
    
    def test_validate_year(self):
        """Test year validation"""
        assert ValidationUtils.validate_year("2024") == True
        assert ValidationUtils.validate_year("2000") == True
        assert ValidationUtils.validate_year("1999") == False
        assert ValidationUtils.validate_year("invalid") == False
    
    def test_validate_year_future(self):
        """Test validation of future years"""
        from datetime import datetime
        current_year = datetime.now().year
        future_year = str(current_year + 1)
        far_future_year = str(current_year + 5)
        
        assert ValidationUtils.validate_year(future_year) == True
        assert ValidationUtils.validate_year(far_future_year) == False

class TestConfigManager:
    """Test configuration management"""
    
    def test_config_initialization(self):
        """Test config manager initialization"""
        config = ConfigManager()
        
        assert config.get("confidence_threshold") is not None
        assert config.get("max_follow_up_questions") is not None
        assert config.get("log_conversations") is not None
    
    def test_config_get_default(self):
        """Test getting config with default value"""
        config = ConfigManager()
        
        value = config.get("nonexistent_key", "default_value")
        assert value == "default_value"

class TestIntegration:
    """Integration tests"""
    
    def setup_method(self):
        """Setup integration test fixtures"""
        self.engine = AAUNLPEngine()
        self.templates = ResponseTemplates()
        
        # Train with sample data
        training_data = DataLoader.get_sample_training_data()
        self.engine.train_intent_classifier(training_data)
    
    def test_full_conversation_flow(self):
        """Test complete conversation flow"""
        # Test admission inquiry
        result = self.engine.process_query("I want to apply for computer science admission")
        response = self.templates.generate_response(
            result["intent"], result["parameters"], 
            result["missing_parameters"], result["confidence"]
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert result["intent"] == "admission_inquiry"
    
    def test_parameter_precision_evaluation(self):
        """Test parameter extraction precision"""
        test_cases = [
            {
                "text": "I want to apply for computer science admission",
                "expected_params": {"department": ["computer science"]}
            },
            {
                "text": "How do I register for second semester 2024?",
                "expected_params": {"semester": ["second"], "year": ["2024"]}
            },
            {
                "text": "I need to pay 5000 birr for fees",
                "expected_params": {"fee_amount": ["5000"]}
            }
        ]
        
        correct_extractions = 0
        total_parameters = 0
        
        for case in test_cases:
            result = self.engine.process_query(case["text"])
            extracted_params = result["parameters"]
            expected_params = case["expected_params"]
            
            for param_type, expected_values in expected_params.items():
                total_parameters += len(expected_values)
                if param_type in extracted_params:
                    extracted_values = extracted_params[param_type]
                    for expected_value in expected_values:
                        if any(expected_value.lower() in str(extracted_value).lower() 
                              for extracted_value in extracted_values):
                            correct_extractions += 1
        
        precision = correct_extractions / total_parameters if total_parameters > 0 else 0
        assert precision > 0.5  # At least 50% precision

# Test runner
if __name__ == "__main__":
    pytest.main([__file__, "-v"])