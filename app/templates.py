"""
Response Templates for AAU Helpdesk Chatbot
Handles template-based responses and follow-up questions
"""

from typing import Dict, List, Any, Optional
import random


def _initialize_templates() -> Dict[str, Dict[str, List[str]]]:
    """Initialize response templates for each intent"""
    return {
        'admission_inquiry': {
            'complete': [
                "For {department} admissions at AAU, here's what you need to know:\n\n"
                "**Requirements:**\n"
                "- Complete secondary education certificate\n"
                "- Entrance exam results\n"
                "- Application form\n\n"
                "**Application Period:** Usually opens in June-July\n"
                "**Application Fee:** 200 ETB\n\n"
                "For specific requirements for {department}, please visit the admissions office or check the AAU website.",

                "Welcome to AAU! For {department} admission information:\n\n"
                "**Steps to Apply:**\n"
                "1. Obtain application form from AAU or online\n"
                "2. Submit required documents\n"
                "3. Pay application fee\n"
                "4. Take entrance exam (if required)\n\n"
                "The {department} program has specific prerequisites. Contact the admissions office for detailed requirements."
            ],
            'partial': [
                "I can help you with admission information! To provide specific details, I need to know which department or program you're interested in.",
                "AAU offers various programs. Which department are you planning to apply to?"
            ]
        },

        'registration_help': {
            'complete': [
                "For {semester} {year} registration:\n\n"
                "**Registration Steps:**\n"
                "1. Meet with your academic advisor\n"
                "2. Select courses based on your curriculum\n"
                "3. Complete online registration\n"
                "4. Pay semester fees\n"
                "5. Confirm registration\n\n"
                "**Important:** Registration typically opens 2 weeks before semester start.\n"
                "**Need help?** Contact the registrar's office.",

                "Registration for {semester} {year}:\n\n"
                "**Key Points:**\n"
                "- Check your academic standing\n"
                "- Ensure all prerequisites are met\n"
                "- Register for required courses first\n"
                "- Add electives if space permits\n\n"
                "**Tip:** Register early to secure your preferred schedule!"
            ],
            'partial': [
                "I can help with registration! Which semester and year are you registering for?",
                "To provide specific registration guidance, please let me know the semester and academic year."
            ]
        },

        'fee_payment': {
            'complete': [
                "For fee payment of {fee_amount}:\n\n"
                "**Payment Methods:**\n"
                "- Bank transfer to AAU account\n"
                "- Cash payment at university cashier\n"
                "- Online payment portal (if available)\n\n"
                "**Bank Details:**\n"
                "- Commercial Bank of Ethiopia\n"
                "- Account: [Contact finance office for details]\n\n"
                "**Required:** Student ID and payment receipt\n"
                "**Deadline:** Check academic calendar for payment deadlines",

                "Payment information for {fee_amount}:\n\n"
                "**Payment Locations:**\n"
                "- AAU Finance Office (Main Campus)\n"
                "- Designated bank branches\n"
                "- Online portal (when available)\n\n"
                "**Bring with you:**\n"
                "- Student ID card\n"
                "- Fee notification slip\n"
                "- Valid identification\n\n"
                "Keep your payment receipt safe!"
            ],
            'partial': [
                "I can help with fee payment information. What's the amount you need to pay?",
                "To provide specific payment guidance, please tell me the fee amount or type of fee."
            ]
        },

        'transcript_request': {
            'complete': [
                "To request your {document_type}:\n\n"
                "**Required Documents:**\n"
                "- Completed application form\n"
                "- Copy of student ID\n"
                "- Copy of national ID\n"
                "- Payment receipt (50 ETB per copy)\n\n"
                "**Processing Time:** 3-5 working days\n"
                "**Submit at:** Registrar's Office, Main Campus\n"
                "**Contact:** +251-11-123-4567",

                "For {document_type} request:\n\n"
                "**Process:**\n"
                "1. Fill out transcript request form\n"
                "2. Pay required fee (50 ETB)\n"
                "3. Submit documents to registrar\n"
                "4. Collect after 3-5 days\n\n"
                "**Express Service:** Available for urgent requests (additional fee applies)\n"
                "**Email:** registrar@aau.edu.et"
            ],
            'partial': [
                "I can help with document requests. What type of document do you need (transcript, certificate, etc.)?",
                "Which document would you like to request from AAU?"
            ]
        },

        'grade_inquiry': {
            'complete': [
                "For {semester} {year} grade inquiry:\n\n"
                "**How to Check Grades:**\n"
                "- Student portal (online)\n"
                "- Academic office visit\n"
                "- Request official grade report\n\n"
                "**Grade Issues:**\n"
                "- Contact course instructor first\n"
                "- Submit grade appeal if necessary\n"
                "- Follow up with department head\n\n"
                "**Grade Release:** Usually 2 weeks after exams",

                "Grade information for {semester} {year}:\n\n"
                "**Grade Inquiry Steps:**\n"
                "1. Check student portal first\n"
                "2. Contact instructor if grades missing\n"
                "3. Visit academic office for assistance\n"
                "4. Submit formal inquiry if needed\n\n"
                "**Academic Office:** +251-11-123-4568"
            ],
            'partial': [
                "I can help with grade inquiries. Which semester and year are you asking about?",
                "To check your grades, please specify the semester and academic year."
            ]
        },

        'course_information': {
            'complete': [
                "Course information for {department}:\n\n"
                "**Available Resources:**\n"
                "- Course catalog (online/printed)\n"
                "- Academic advisor consultation\n"
                "- Department office visit\n\n"
                "**Course Details Include:**\n"
                "- Prerequisites and corequisites\n"
                "- Credit hours\n"
                "- Course descriptions\n"
                "- Semester offerings\n\n"
                "**Contact:** {department} department office"
            ],
            'partial': [
                "I can provide course information. Which department or specific course are you interested in?",
                "Which department's courses would you like to know about?"
            ]
        },

        'schedule_inquiry': {
            'complete': [
                "Schedule information for {semester} {year}:\n\n"
                "**Where to Find Schedules:**\n"
                "- Student portal\n"
                "- Department notice boards\n"
                "- Academic office\n\n"
                "**Schedule Includes:**\n"
                "- Class times and locations\n"
                "- Instructor information\n"
                "- Exam schedules\n"
                "- Important dates\n\n"
                "**Updates:** Check regularly for changes"
            ],
            'partial': [
                "I can help with schedule information. Which semester and year are you asking about?",
                "Please specify the semester and academic year for schedule details."
            ]
        },

        'document_request': {
            'complete': [
                "For {document_type} request:\n\n"
                "**Document Services:**\n"
                "- Official transcripts\n"
                "- Degree certificates\n"
                "- Enrollment verification\n"
                "- Grade reports\n\n"
                "**Fees:** Vary by document type\n"
                "**Processing:** 3-7 working days\n"
                "**Location:** Registrar's Office"
            ],
            'partial': [
                "I can help with document requests. What type of document do you need?",
                "Which document would you like to request from AAU?"
            ]
        },

        'general_info': {
            'complete': [
                "Welcome to AAU Helpdesk! 🎓\n\n"
                "I can help you with:\n"
                "• Admission inquiries\n"
                "• Registration assistance\n"
                "• Fee payment information\n"
                "• Document requests\n"
                "• Grade inquiries\n"
                "• Course information\n"
                "• Schedule details\n\n"
                "How can I assist you today?",

                "AAU Student Services \n\n"
                "**Main Campus:** Addis Ababa, Ethiopia\n"
                "**Phone:** +251-11-123-4567\n"
                "**Email:** info@aau.edu.et\n"
                "**Website:** www.aau.edu.et\n\n"
                "What specific information do you need?"
            ],
            'partial': [
                "Hello! I'm here to help with AAU services. What can I assist you with?",
                "Welcome to AAU Helpdesk! How may I help you today?"
            ]
        },

        'technical_support': {
            'complete': [
                "Technical Support\n\n"
                "**Common Issues:**\n"
                "- Student portal access\n"
                "- Email account problems\n"
                "- WiFi connectivity\n"
                "- Online learning platforms\n\n"
                "**IT Support:** +251-11-123-4569\n"
                "**Email:** itsupport@aau.edu.et\n"
                "**Hours:** Mon-Fri, 8:00 AM - 5:00 PM"
            ],
            'partial': [
                "I can help with technical issues. What specific problem are you experiencing?",
                "What technical issue can I help you with today?"
            ]
        }
    }


def _initialize_follow_ups() -> Dict[str, List[str]]:
    """Initialize follow-up questions for missing parameters"""
    return {
        'department': [
            "Which department or program are you interested in?",
            "Could you specify the department?",
            "What's your field of study or intended major?"
        ],
        'semester': [
            "Which semester are you referring to (1st, 2nd, etc.)?",
            "Could you specify the semester?",
            "What semester do you need information about?"
        ],
        'year': [
            "Which academic year are you asking about?",
            "Could you specify the year?",
            "What year is this for?"
        ],
        'document_type': [
            "What type of document do you need (transcript, certificate, etc.)?",
            "Which document are you requesting?",
            "Could you specify the document type?"
        ],
        'fee_amount': [
            "What's the fee amount you need to pay?",
            "Could you specify the amount?",
            "How much do you need to pay?"
        ],
        'student_id': [
            "Could you provide your student ID number?",
            "What's your student ID?",
            "Please share your student identification number."
        ]
    }


def _initialize_clarifications() -> List[str]:
    """Initialize clarification templates for low confidence"""
    return [
        "I'm not entirely sure I understood your request correctly. Could you please rephrase or provide more details?",
        "Could you clarify what you're looking for? I want to make sure I give you the right information.",
        "I'd like to help you better. Could you provide more specific details about your request?",
        "Let me make sure I understand correctly. Could you elaborate on what you need help with?"
    ]

def _initialize_out_of_domain_templates() -> Dict[str, str]:
    """Initialize out-of-domain response templates"""
    return {
        'base_message': "I'm specifically designed to help with AAU (Addis Ababa University) services and I don't have information about that topic.",
        
        'medical': "I'm not able to provide medical advice or health information. For health-related questions, please consult with a qualified healthcare professional.",
        
        'weather': "I don't have access to weather information. You can check weather forecasts on weather websites or apps.",
        
        'entertainment': "I don't have information about entertainment topics. I'm focused on helping with university services.",
        
        'technology': "I don't provide general programming or technology support. However, if you need help with AAU's technical services or computer science courses, I can assist with that!",
        
        'general_knowledge': "I don't have general knowledge information. I'm specialized in AAU university services.",
        
        'personal': "I'm an AI assistant designed to help with AAU university services. I don't have personal information to share.",
        
        'math_problem': "I don't solve general math problems. If you need help with AAU mathematics courses or academic requirements, I can help with that!",
        
        'general': "I don't have information about that topic."
    }


def get_error_response() -> str:
    """Get an error response"""
    errors = [
        "I apologize, but I encountered an issue processing your request. Please try again or contact AAU support directly.",
        "Something went wrong on my end. Could you please rephrase your question?",
        "I'm having trouble understanding that request. Could you try asking in a different way?",
        "Sorry, I couldn't process that properly. Please contact AAU support for immediate assistance."
    ]
    return random.choice(errors)


def get_goodbye_response() -> str:
    """Get a goodbye response"""
    goodbyes = [
        "Thank you for using AAU Helpdesk! Have a great day! 🎓",
        "Goodbye! Feel free to reach out if you need more help with AAU services.",
        "Take care! Don't hesitate to ask if you have more questions about AAU.",
        "Have a wonderful day! I'm here whenever you need AAU assistance."
    ]
    return random.choice(goodbyes)


def get_greeting_response() -> str:
    """Get a greeting response"""
    greetings = [
        "Hello! Welcome to AAU Helpdesk. How can I assist you today? 🎓",
        "Hi there! I'm here to help with your AAU-related questions. What do you need help with?",
        "Welcome to Addis Ababa University Helpdesk! How may I help you today?",
        "Hello! I'm your AAU virtual assistant. What can I help you with?"
    ]
    return random.choice(greetings)


class ResponseTemplates:
    """Manages response templates and follow-up questions"""
    
    def __init__(self):
        self.templates = _initialize_templates()
        self.follow_up_questions = _initialize_follow_ups()
        self.clarification_templates = _initialize_clarifications()
        self.out_of_domain_templates = _initialize_out_of_domain_templates()

    def generate_response(self, intent: str, parameters: Dict[str, Any],
                         missing_parameters: List[str], confidence: float, 
                         out_of_domain_info: Optional[Dict] = None) -> str:
        """Generate appropriate response based on intent and parameters"""
        
        # Handle out-of-domain queries
        if out_of_domain_info and out_of_domain_info.get('is_out_of_domain'):
            return self._generate_out_of_domain_response(out_of_domain_info)
        
        # Low confidence - ask for clarification (lowered threshold)
        if confidence < 0.25:
            return random.choice(self.clarification_templates)
        
        # Missing required parameters - ask follow-up questions
        if missing_parameters:
            return self._generate_follow_up_response(intent, missing_parameters, parameters)
        
        # Complete information - provide full response
        return self._generate_complete_response(intent, parameters)
    
    def _generate_out_of_domain_response(self, out_of_domain_info: Dict) -> str:
        """Generate response for out-of-domain queries"""
        detected_topic = out_of_domain_info.get('detected_topic', 'general')
        
        # Get topic-specific message
        topic_message = self.out_of_domain_templates.get(detected_topic, 
                                                        self.out_of_domain_templates['general'])
        
        # Base message
        base_message = self.out_of_domain_templates['base_message']
        
        # Domain suggestions
        suggestions = [
            "• Admission inquiries and requirements",
            "• Course registration assistance", 
            "• Fee payment information",
            "• Transcript and document requests",
            "• Grade inquiries and academic records",
            "• University schedules and contacts",
            "• Department information",
            "• Technical support for student services"
        ]
        
        # Combine messages
        if detected_topic != 'general':
            response = f"{topic_message}\n\n{base_message}"
        else:
            response = base_message
        
        response += f"\n\nI can help you with:\n" + "\n".join(suggestions)
        response += "\n\nHow can I assist you with AAU services today?"
        
        return response
    
    def _generate_follow_up_response(self, intent: str, missing_parameters: List[str], 
                                   existing_parameters: Dict[str, Any]) -> str:
        """Generate follow-up questions for missing parameters"""
        
        # Get partial template if available
        if intent in self.templates and 'partial' in self.templates[intent]:
            base_response = random.choice(self.templates[intent]['partial'])
        else:
            base_response = "I need a bit more information to help you better."
        
        # Add specific follow-up questions
        follow_ups = []
        for param in missing_parameters[:2]:  # Limit to 2 questions to avoid overwhelming
            if param in self.follow_up_questions:
                follow_ups.append(random.choice(self.follow_up_questions[param]))
        
        if follow_ups:
            return f"{base_response}\n\n" + "\n".join(f"• {q}" for q in follow_ups)
        
        return base_response
    
    def _generate_complete_response(self, intent: str, parameters: Dict[str, Any]) -> str:
        """Generate complete response with all parameters filled"""
        
        if intent not in self.templates or 'complete' not in self.templates[intent]:
            return "I understand your request, but I don't have specific information available right now. Please contact the relevant AAU office for assistance."
        
        # Select random template
        template = random.choice(self.templates[intent]['complete'])
        
        # Fill in parameters
        try:
            # Convert list parameters to strings
            formatted_params = {}
            for key, value in parameters.items():
                if isinstance(value, list):
                    formatted_params[key] = ', '.join(str(v) for v in value)
                else:
                    formatted_params[key] = str(value)
            
            return template.format(**formatted_params)
        except KeyError:
            # If template formatting fails, return template as-is
            return template
    
