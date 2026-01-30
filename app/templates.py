"""
Response Templates for AAU Helpdesk Chatbot
Handles template-based responses and follow-up questions
"""

from typing import Dict, List, Any, Optional
import random


def _initialize_templates() -> Dict[str, Dict[str, List[str]]]:
    """Initialize response templates for each intent"""
    return {
        # ADMISSION & APPLICATION INTENTS
        'undergraduate_admission': {
            'complete': [
                "**Undergraduate Admission at AAU - {department}**\n\n"
                "**Requirements:**\n"
                "• Ethiopian Secondary School Leaving Certificate Examination (ESSLCE) - Grade 12\n"
                "• Minimum CGPA requirements vary by program\n"
                "• Complete application form\n"
                "• Medical certificate\n\n"
                "**Application Process:**\n"
                "1. Submit updated Grade 12 results via: https://forms.gle/WwBC8cRXi3ss6TtE6\n"
                "2. Complete online application\n"
                "3. Pay application fees\n"
                "4. Attend placement process\n\n"
                "**Important:** Regular and non-regular programs follow the same admission criteria.\n"
                "**Contact:** Office of the Registrar, Main Campus",

                "**AAU Undergraduate Programs - {department}**\n\n"
                "**Admission Standards:**\n"
                "• Same quality standards for regular and non-regular programs\n"
                "• Program-specific requirements vary greatly\n"
                "• Academic year: September to June\n"
                "• Summer semester: July 1 - September 7\n\n"
                "**Key Dates:**\n"
                "• Application deadline updates posted regularly\n"
                "• Grade 12 result submission deadline: January 5, 2026\n\n"
                "Visit the Office of the Registrar for {department}-specific requirements."
            ],
            'partial': [
                "I can help with undergraduate admission! Which department or program are you interested in?",
                "AAU offers undergraduate programs across multiple colleges. Please specify your intended field of study."
            ]
        },

        'graduate_admission': {
            'complete': [
                "**Graduate Admission at AAU - {department}**\n\n"
                "**Masters Programs:**\n"
                "• Bachelor's degree with minimum CGPA requirements\n"
                "• Entrance examination (program-specific)\n"
                "• Research proposal (for thesis programs)\n"
                "• Letters of recommendation\n\n"
                "**PhD Programs:**\n"
                "• Masters degree in relevant field\n"
                "• Research proposal and methodology\n"
                "• Academic references\n"
                "• Interview process\n\n"
                "**Current Opportunities:**\n"
                "• Second Semester 2025/26 applications open\n"
                "• PhD in Sustainable Development - adjusted dates available\n\n"
                "**Contact:** Graduate Programs Office, {department}",

                "**AAU Graduate Studies - {department}**\n\n"
                "**Application Process:**\n"
                "1. Check program-specific requirements\n"
                "2. Prepare research proposal\n"
                "3. Submit application with documents\n"
                "4. Take entrance exam (if required)\n"
                "5. Attend interview\n\n"
                "**Fees (Ethiopian Students):**\n"
                "• Masters: 900-3,461 ETB per ECTS\n"
                "• PhD: 1,200-4,615 ETB per ECTS\n"
                "• Thesis fees: 20,250-27,000 ETB\n\n"
                "Visit the specific college for {department} requirements."
            ],
            'partial': [
                "I can help with graduate admission information. Are you interested in Masters or PhD programs? Which field?",
                "AAU offers various graduate programs. Please specify the department and degree level you're interested in."
            ]
        },

        'gat_exam_inquiry': {
            'complete': [
                "**GAT (Graduate Aptitude Test) Information**\n\n"
                "**Recent Schedule:**\n"
                "• Date: Monday, January 5, 2026\n"
                "• Sessions: Morning and Afternoon\n"
                "• Registration period: December 9-30, 2025\n\n"
                "**Exam Venues:**\n"
                "• Multiple locations across AAU campuses\n"
                "• Disability Center, Lab 1 (Main Campus) for visually impaired candidates\n"
                "• Check your specific venue in the schedule files\n\n"
                "**Important Notes:**\n"
                "• Bring valid identification\n"
                "• Arrive early for check-in\n"
                "• Late registrants (Dec 31) have separate afternoon session\n\n"
                "**Documents:** GAT brochure and schedules available for download\n"
                "**Contact:** AAU Testing Center"
            ],
            'partial': [
                "I can help with GAT exam information. Are you looking for schedules, venues, or general exam details?",
                "The GAT exam is administered regularly. What specific information do you need about the test?"
            ]
        },

        'international_admission': {
            'complete': [
                "**International Student Admission at AAU**\n\n"
                "**Student Categories:**\n"
                "• Refugees: Special fee structure in ETB\n"
                "• IGAD Members & East African Countries: USD rates\n"
                "• Other International Students: Higher USD rates\n\n"
                "**Undergraduate Fees (USD):**\n"
                "• Medicine/Dental: $150-300 per ECTS\n"
                "• Engineering/Computer Science: $90-180 per ECTS\n"
                "• Business/Law: $60-120 per ECTS\n"
                "• Social Sciences: $60-120 per ECTS\n\n"
                "**Graduate Fees (USD):**\n"
                "• Masters: $225-300 per ECTS\n"
                "• PhD: $300-450 per ECTS\n\n"
                "**Additional Requirements:**\n"
                "• Visa and immigration documents\n"
                "• Academic credential evaluation\n"
                "• English proficiency (if required)\n\n"
                "**Contact:** International Students Office"
            ],
            'partial': [
                "I can help with international admission information. Are you a refugee, from an IGAD/East African country, or another international location?",
                "AAU welcomes international students with different fee structures. Which category applies to you?"
            ]
        },

        # FEE & PAYMENT INTENTS
        'undergraduate_fee_inquiry': {
            'complete': [
                "**AAU Undergraduate Fees (Ethiopian Students) - {department}**\n\n"
                "**Fee Structure by Program Category:**\n"
                "• Medicine & Dental Medicine: 2,307.69 ETB per ECTS\n"
                "• Pharmacy/Veterinary Medicine: 1,153.17 ETB per ECTS\n"
                "• Computer Science/Software Engineering: 1,500.00 ETB per ECTS\n"
                "• Architecture: 1,500.00 ETB per ECTS\n"
                "• Engineering: 900 ETB per ECTS\n"
                "• Law/Business: 700 ETB per ECTS\n"
                "• Social Sciences/Education: 600 ETB per ECTS\n\n"
                "**Additional Fees:**\n"
                "• Internship/Practicum: 5,400 ETB per student\n"
                "• Senior Essay/Research Project: 375 ETB per student\n"
                "• Laboratory work: 175-440 ETB per ECTS\n\n"
                "**Payment:** Contact Finance Office for payment methods"
            ],
            'partial': [
                "I can provide undergraduate fee information. Which program or department are you asking about?",
                "AAU undergraduate fees vary by program. Please specify your field of study for accurate fee information."
            ]
        },

        'graduate_fee_inquiry': {
            'complete': [
                "**AAU Graduate Fees (Ethiopian Students) - {department}**\n\n"
                "**Masters Programs (ETB per ECTS):**\n"
                "• Medicine & Dental Medicine: 3,461.54\n"
                "• Computer Science/Software Engineering: 2,250.00\n"
                "• Architecture: 2,250.00\n"
                "• Engineering: 1,350.00\n"
                "• Law/Business: 1,050.00\n"
                "• Social Sciences/Education: 900.00\n\n"
                "**PhD Programs (ETB per ECTS):**\n"
                "• Medicine & Dental Medicine: 4,615.38\n"
                "• Computer Science/Software Engineering: 3,000.00\n"
                "• Engineering: 1,800.00\n"
                "• Law/Business: 1,400.00\n"
                "• Social Sciences/Education: 1,200.00\n\n"
                "**Research Fees:**\n"
                "• Masters Thesis: 20,250-27,000 ETB\n"
                "• PhD Dissertation: 15,000 ETB per semester\n\n"
                "**Specialty Programs:** 3,461.54-4,615.38 ETB as recommended"
            ],
            'partial': [
                "I can provide graduate fee information. Are you interested in Masters or PhD programs? Which department?",
                "Graduate fees vary by program level and field. Please specify your intended degree and department."
            ]
        },

        'payment_methods_inquiry': {
            'complete': [
                "**AAU Fee Payment Methods**\n\n"
                "**Available Payment Options:**\n"
                "• Bank transfer to AAU account (Commercial Bank of Ethiopia)\n"
                "• Cash payment at University Finance Office\n"
                "• TeleBirr service platform (Ethio Telecom partnership)\n"
                "• Online payment portal (when available)\n\n"
                "**Required Documents:**\n"
                "• Student ID card\n"
                "• Fee notification slip\n"
                "• Valid identification\n"
                "• Payment receipt (keep safe!)\n\n"
                "**Payment Locations:**\n"
                "• AAU Finance Office (Main Campus)\n"
                "• Designated bank branches\n"
                "• Campus cashier offices\n\n"
                "**Important:** Check academic calendar for payment deadlines\n"
                "**Contact:** Finance Office for specific account details"
            ],
            'partial': [
                "I can help with payment method information. Are you looking for fee payment options or specific account details?",
                "AAU accepts various payment methods. What type of fee are you planning to pay?"
            ]
        },

        # ACADEMIC & COURSE INTENTS
        'academic_calendar_inquiry': {
            'complete': [
                "**AAU Academic Calendar {year}**\n\n"
                "**Regular Academic Year:**\n"
                "• Start: September\n"
                "• End: June\n"
                "• Semester Duration: 16 weeks + 1 week break before exams\n\n"
                "**Summer Semester:**\n"
                "• Duration: July 1 - September 7\n"
                "• Length: 8-12 weeks\n"
                "• Reduced course load (2/3 of normal semester)\n\n"
                "**Key Academic Activities:**\n"
                "• Senate meetings: Once per semester\n"
                "• Inter-semester break: Minimum 4 weeks\n"
                "• Registration periods\n"
                "• Add/drop deadlines\n"
                "• Examination periods\n"
                "• Graduation ceremonies\n\n"
                "**Special Programs:** Medical and modular programs may have different schedules\n"
                "**Prepared by:** University Registrar in consultation with AVP"
            ],
            'partial': [
                "I can provide academic calendar information. Are you looking for semester dates, exam periods, or specific academic year details?",
                "The AAU academic calendar includes regular and summer semesters. What specific dates do you need?"
            ]
        },

        'exam_schedule_inquiry': {
            'complete': [
                "**AAU Examination Schedule {semester} {year}**\n\n"
                "**Current Exam Information:**\n"
                "• First-Year Students Final Online Exam: January 25, 2026\n"
                "• Inclusiveness Course (2nd Year): January 12, 2026\n"
                "  - Session 1: 8:30 AM - 10:30 AM\n"
                "  - Session 2: 11:00 AM - 1:00 PM\n"
                "• GAT Exam: January 5, 2026 (Morning & Afternoon)\n\n"
                "**Exam Venues:**\n"
                "• Multiple campus locations\n"
                "• Check specific venue assignments\n"
                "• Disability accommodations at Disability Center, Lab 1\n\n"
                "**Important Notes:**\n"
                "• Arrive early for check-in\n"
                "• Bring valid student ID\n"
                "• Check your assigned session carefully\n\n"
                "**Contact:** Academic offices for specific exam details"
            ],
            'partial': [
                "I can help with exam schedule information. Which semester, year, or specific exam are you asking about?",
                "AAU exam schedules are posted regularly. Please specify the exam or time period you need information about."
            ]
        },

        # DOCUMENT & SERVICE INTENTS
        'official_transcript_request': {
            'complete': [
                "**Official Transcript Request at AAU**\n\n"
                "**Required Documents:**\n"
                "• Completed transcript request form\n"
                "• Copy of student ID\n"
                "• Copy of national ID\n"
                "• Payment receipt (50 ETB per copy)\n\n"
                "**Process:**\n"
                "1. Fill out transcript request form\n"
                "2. Pay required fee (50 ETB per transcript)\n"
                "3. Submit documents to Registrar's Office\n"
                "4. Collect after 3-5 working days\n\n"
                "**Service Options:**\n"
                "• Regular processing: 3-5 working days\n"
                "• Express service: Available for urgent requests (additional fee)\n\n"
                "**Location:** Registrar's Office, Main Campus\n"
                "**Contact:** +251-11-123-4567 | registrar@aau.edu.et"
            ],
            'partial': [
                "I can help with official transcript requests. Do you need information about the process, fees, or required documents?",
                "Official transcripts are processed by the Registrar's Office. What specific information do you need?"
            ]
        },

        'library_services_inquiry': {
            'complete': [
                "**AAU Library Services**\n\n"
                "**Main Services:**\n"
                "• Loan Service\n"
                "• Research Data Portal\n"
                "• Training and Consultancy\n"
                "• Subscribed Journals Access\n"
                "• Open Access Resources\n"
                "• AAU Library Catalog\n"
                "• Ethiopian Journals Online\n"
                "• Electronic Thesis and Dissertation\n"
                "• E-Book Collections\n\n"
                "**Branch Libraries:**\n"
                "• 10 college branches across AAU campuses\n"
                "• Science Campus Library\n"
                "• AAU Digital Library\n\n"
                "**Partnerships:**\n"
                "• Elsevier and Wiley publishers\n"
                "• EIFL collaboration\n"
                "• Ministry of Education (APC waivers)\n"
                "• CEARL (Consortium of Ethiopian Academic Libraries)\n\n"
                "**Resources:** Extensive electronic resources, journals, and research tools"
            ],
            'partial': [
                "I can help with library services information. Are you looking for specific services, branch locations, or digital resources?",
                "AAU Libraries offer comprehensive academic support. What specific library service do you need information about?"
            ]
        },

        # CAMPUS & FACILITY INTENTS
        'campus_location_inquiry': {
            'complete': [
                "**AAU Campus Locations**\n\n"
                "**Main Campuses:**\n"
                "• Sidist Kilo Campus (Main Campus) - 6 Kilo\n"
                "• Sefere Selam Campus - Medical training and research hub\n"
                "• Science Campus (4 Kilo) - Natural and Computational Sciences\n"
                "• Bishoftu Campus - Veterinary Medicine and Agriculture\n\n"
                "**Specialized Facilities:**\n"
                "• Tikur Anbessa Specialized Hospital (TASH)\n"
                "• Institute of Ethiopian Studies (IES)\n"
                "• AAU Museums and Cultural Center\n"
                "• National Herbarium\n"
                "• AAU Book Center\n\n"
                "**Campus Features:**\n"
                "• Multiple libraries across campuses\n"
                "• Student hostels and dining facilities\n"
                "• Sports and recreation facilities\n"
                "• Ashenafi Kebede Performance Arts Center\n\n"
                "**Transportation:** Various public transport options available to all campuses"
            ],
            'partial': [
                "I can help with campus location information. Which specific campus or facility are you looking for?",
                "AAU has multiple campuses across Addis Ababa. Please specify which location you need directions to."
            ]
        },

        'accommodation_inquiry': {
            'complete': [
                "**AAU Student Accommodation**\n\n"
                "**Housing Options:**\n"
                "• On-campus hostels (various campuses)\n"
                "• Sidist Kilo Hostel\n"
                "• Campus-specific accommodation\n\n"
                "**Eligibility:**\n"
                "• Based on AAU regulations and policies\n"
                "• Priority given to students from distant regions\n"
                "• Academic performance considerations\n"
                "• Financial need assessment\n\n"
                "**Dining Services:**\n"
                "• Campus canteens and dining halls\n"
                "• Meal plan options available\n"
                "• Variety of food choices\n\n"
                "**Application Process:**\n"
                "• Submit accommodation application\n"
                "• Provide required documentation\n"
                "• Wait for allocation based on availability\n\n"
                "**Contact:** Student Services Office for accommodation applications"
            ],
            'partial': [
                "I can help with accommodation information. Are you looking for on-campus housing, dining options, or application procedures?",
                "AAU provides various housing and dining options. What specific accommodation information do you need?"
            ]
        },

        # RESEARCH & GRADUATE INTENTS
        'research_opportunity_inquiry': {
            'complete': [
                "**Research Opportunities at AAU**\n\n"
                "**Current Opportunities:**\n"
                "• EfD-Ethiopia Postdoctoral Fellowships (3 positions)\n"
                "  - Climate Policy & Development\n"
                "  - Sustainable Agriculture\n"
                "  - Sustainable Energy Transition\n"
                "  - Green Industrialization & Urbanization\n"
                "• AAU Research Chair for Forced Displacement Studies\n"
                "  - Small grants and mentorship\n"
                "  - Postdoctoral fellowships\n"
                "  - Methodology training\n\n"
                "**Research Support:**\n"
                "• Research awards and seed grants\n"
                "• Collaborative research programs\n"
                "• Publication support\n"
                "• Training of Trainers (ToT) programs\n\n"
                "**Research Focus Areas:**\n"
                "• Sustainable development\n"
                "• Climate change and migration\n"
                "• Health entrepreneurship\n"
                "• Indigenous knowledge systems\n\n"
                "**Contact:** Research Office, AAU"
            ],
            'partial': [
                "I can help with research opportunity information. Are you interested in postdoctoral positions, student research, or faculty opportunities?",
                "AAU offers various research opportunities. Please specify your academic level and research interests."
            ]
        },

        'thesis_submission_process': {
            'complete': [
                "**Thesis/Dissertation Submission at AAU**\n\n"
                "**Submission Requirements:**\n"
                "• Completed thesis/dissertation\n"
                "• Supervisor approval\n"
                "• Committee review completion\n"
                "• Plagiarism check certificate\n"
                "• Required number of copies\n\n"
                "**Fees:**\n"
                "• Masters Thesis: 20,250-27,000 ETB (30 ECTS)\n"
                "• PhD Dissertation: 15,000 ETB per semester\n"
                "• Examination fees may apply\n\n"
                "**Process:**\n"
                "1. Complete thesis writing\n"
                "2. Get supervisor approval\n"
                "3. Submit to examination committee\n"
                "4. Pay required fees\n"
                "5. Schedule defense\n"
                "6. Submit final copies\n\n"
                "**Electronic Submission:** Available through AAU Digital Library\n"
                "**Contact:** Graduate Programs Office, respective college"
            ],
            'partial': [
                "I can help with thesis submission information. Are you submitting a Masters thesis or PhD dissertation?",
                "Thesis submission involves several steps and fees. What specific aspect of the process do you need help with?"
            ]
        },

        # SPECIALIZED AAU SERVICE INTENTS
        'hospital_services_inquiry': {
            'complete': [
                "**Tikur Anbessa Specialized Hospital (TASH)**\n\n"
                "**Overview:**\n"
                "• Ethiopia's largest referral hospital\n"
                "• Serves over 1 million patients annually\n"
                "• Located at Sefere Selam Campus\n"
                "• State-of-the-art clinical services\n\n"
                "**Services Available:**\n"
                "• Emergency services\n"
                "• Specialized medical departments\n"
                "• Surgical services\n"
                "• Diagnostic services\n"
                "• Outpatient clinics\n"
                "• Inpatient care\n\n"
                "**Staff Health Services:**\n"
                "• Regular health screening programs\n"
                "• Hypertension and diabetes screening\n"
                "• Specialized consultations\n"
                "• Preventive care services\n\n"
                "**Contact:** TASH Administration for specific service information"
            ],
            'partial': [
                "I can help with hospital services information. Are you looking for patient services, staff health programs, or general hospital information?",
                "Tikur Anbessa Hospital provides comprehensive medical services. What specific information do you need?"
            ]
        },

        'book_center_inquiry': {
            'complete': [
                "**AAU Book Center Services**\n\n"
                "**About:**\n"
                "• Founded in 1984\n"
                "• Official bookshop for entire AAU\n"
                "• Located on Main Campus\n\n"
                "**Available Items:**\n"
                "• Textbooks and reference materials\n"
                "• Monographs and journals\n"
                "• General-interest books and literature\n"
                "• Technical books and bestsellers\n"
                "• AAU Press publications\n"
                "• Educational and office stationery\n"
                "• Related academic supplies\n\n"
                "**Special Features:**\n"
                "• Books by Ethiopian and foreign authors\n"
                "• Covers virtually all academic fields\n"
                "• Special Book Fair prices during events\n"
                "• Support for academic growth\n\n"
                "**Services:** Sales, special orders, and academic resource support"
            ],
            'partial': [
                "I can help with Book Center information. Are you looking for specific books, stationery, or general services?",
                "The AAU Book Center offers textbooks and academic supplies. What specific items or services do you need?"
            ]
        },

        # Keep existing intents for backward compatibility
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
                "**AAU Registration for {semester} {year}**\n\n"
                "**Registration Steps:**\n"
                "1. Meet with your academic advisor\n"
                "2. Select courses based on your curriculum\n"
                "3. Complete online registration\n"
                "4. Pay semester fees\n"
                "5. Confirm registration\n\n"
                "**Important Dates:**\n"
                "• Registration typically opens 2 weeks before semester start\n"
                "• Add/drop period follows registration\n"
                "• Late registration may incur penalties\n\n"
                "**Academic Calendar:**\n"
                "• Regular semester: 16 weeks + 1 week break\n"
                "• Summer semester: 8-12 weeks (reduced load)\n\n"
                "**Contact:** Registrar's Office for assistance"
            ],
            'partial': [
                "I can help with registration! Which semester and year are you registering for?",
                "To provide specific registration guidance, please let me know the semester and academic year."
            ]
        },

        'readmission_inquiry': {
            'complete': [
                "**AAU Readmission Process**\n\n"
                "**Eligibility:**\n"
                "• Previous AAU students in good standing\n"
                "• Students who took approved leave of absence\n"
                "• Students dismissed for non-academic reasons (case-by-case)\n\n"
                "**Required Documents:**\n"
                "• Readmission application form\n"
                "• Academic transcripts\n"
                "• Reason for absence documentation\n"
                "• Medical certificate (if applicable)\n"
                "• Character reference letters\n\n"
                "**Process:**\n"
                "1. Submit readmission application\n"
                "2. Academic review by department\n"
                "3. Committee evaluation\n"
                "4. Decision notification\n"
                "5. Registration (if approved)\n\n"
                "**Deadlines:** Check academic calendar for readmission deadlines\n"
                "**Contact:** Academic office of your previous department"
            ],
            'partial': [
                "I can help with readmission information. Are you a former AAU student looking to return?",
                "Readmission processes vary by situation. What was the reason for your previous departure from AAU?"
            ]
        },

        'fee_payment': {
            'complete': [
                "**AAU Fee Payment Information - {fee_amount}**\n\n"
                "**Payment Methods:**\n"
                "• Bank transfer to AAU account (Commercial Bank of Ethiopia)\n"
                "• Cash payment at University Finance Office\n"
                "• TeleBirr service platform (Ethio Telecom)\n"
                "• Online payment portal (when available)\n\n"
                "**Required Documents:**\n"
                "• Student ID card\n"
                "• Fee notification slip\n"
                "• Valid identification\n\n"
                "**Payment Locations:**\n"
                "• AAU Finance Office (Main Campus)\n"
                "• Designated bank branches\n"
                "• Campus cashier offices\n\n"
                "**Important:** Keep payment receipt safe and check academic calendar for deadlines\n"
                "**Contact:** Finance Office for specific account details"
            ],
            'partial': [
                "I can help with fee payment information. What's the amount you need to pay or type of fee?",
                "To provide specific payment guidance, please tell me the fee amount or fee category."
            ]
        },

        'international_student_fees': {
            'complete': [
                "**International Student Fees at AAU**\n\n"
                "**Fee Categories:**\n"
                "• Refugees: ETB rates (same as Ethiopian students)\n"
                "• IGAD/East African Countries: Moderate USD rates\n"
                "• Other International Students: Higher USD rates\n\n"
                "**Undergraduate Programs (USD per ECTS):**\n"
                "• Medicine/Dental: $100-300 (varies by category)\n"
                "• Engineering/Computer Science: $60-180\n"
                "• Business/Law: $42-120\n"
                "• Social Sciences: $42-120\n\n"
                "**Graduate Programs (USD per ECTS):**\n"
                "• Masters: $150-300\n"
                "• PhD: $200-450\n\n"
                "**Research Fees:**\n"
                "• Masters Thesis: $500-1000\n"
                "• PhD Research: $1000-1500 per semester\n"
                "• Thesis Examination: $200-750\n\n"
                "**Payment:** USD payments required for international students"
            ],
            'partial': [
                "I can help with international student fees. Are you a refugee, from IGAD/East Africa, or another international location?",
                "International fees vary by student category and program. Which applies to your situation?"
            ]
        },

        'transcript_request': {
            'complete': [
                "**AAU Transcript Request - {document_type}**\n\n"
                "**Required Documents:**\n"
                "• Completed transcript request form\n"
                "• Copy of student ID\n"
                "• Copy of national ID\n"
                "• Payment receipt (50 ETB per copy)\n\n"
                "**Process:**\n"
                "1. Fill out transcript request form\n"
                "2. Pay required fee (50 ETB per transcript)\n"
                "3. Submit documents to Registrar's Office\n"
                "4. Collect after 3-5 working days\n\n"
                "**Service Options:**\n"
                "• Regular processing: 3-5 working days\n"
                "• Express service: Available for urgent requests (additional fee)\n\n"
                "**Location:** Registrar's Office, Main Campus\n"
                "**Contact:** +251-11-123-4567 | registrar@aau.edu.et"
            ],
            'partial': [
                "I can help with document requests. What type of document do you need (transcript, certificate, etc.)?",
                "Which document would you like to request from AAU?"
            ]
        },

        'certificate_request': {
            'complete': [
                "**AAU Certificate Request - {document_type}**\n\n"
                "**Available Certificates:**\n"
                "• Degree certificates\n"
                "• Diploma certificates\n"
                "• Enrollment verification letters\n"
                "• Graduation certificates\n"
                "• Academic standing certificates\n\n"
                "**Requirements:**\n"
                "• Completed request form\n"
                "• Student/Graduate ID\n"
                "• National ID copy\n"
                "• Payment receipt\n"
                "• Passport photo (for some certificates)\n\n"
                "**Processing:**\n"
                "• Standard: 5-7 working days\n"
                "• Express: 2-3 working days (additional fee)\n"
                "• Verification letters: Same day service\n\n"
                "**Fees:** Vary by certificate type\n"
                "**Location:** Registrar's Office, Main Campus"
            ],
            'partial': [
                "I can help with certificate requests. What type of certificate do you need?",
                "AAU issues various certificates. Please specify which type you're requesting."
            ]
        },

        'grade_inquiry': {
            'complete': [
                "**AAU Grade Inquiry - {semester} {year}**\n\n"
                "**How to Check Grades:**\n"
                "• Student portal (online access)\n"
                "• Academic office visit\n"
                "• Request official grade report\n\n"
                "**Grade Issues Resolution:**\n"
                "1. Contact course instructor first\n"
                "2. Submit grade appeal if necessary\n"
                "3. Follow up with department head\n"
                "4. Escalate to academic committee if needed\n\n"
                "**Grade Release Timeline:**\n"
                "• Usually 2 weeks after final exams\n"
                "• Delayed grades: Contact instructor\n"
                "• Missing grades: Visit academic office\n\n"
                "**Current Updates:**\n"
                "• Grade 12 result updates: Submit via Google Form\n"
                "• Deadline: January 5, 2026\n\n"
                "**Contact:** Academic Office +251-11-123-4568"
            ],
            'partial': [
                "I can help with grade inquiries. Which semester and year are you asking about?",
                "To check your grades, please specify the semester and academic year."
            ]
        },

        'grade_report_request': {
            'complete': [
                "**AAU Grade Report Request**\n\n"
                "**Available Reports:**\n"
                "• Semester grade reports\n"
                "• Cumulative grade reports\n"
                "• Course-specific grade reports\n"
                "• Official academic transcripts\n\n"
                "**Request Process:**\n"
                "1. Fill out grade report request form\n"
                "2. Pay applicable fees\n"
                "3. Submit to academic office\n"
                "4. Collect processed report\n\n"
                "**Processing Time:**\n"
                "• Regular reports: 2-3 working days\n"
                "• Official transcripts: 3-5 working days\n"
                "• Express service: Additional fee applies\n\n"
                "**Fees:**\n"
                "• Grade reports: Minimal fee\n"
                "• Official transcripts: 50 ETB per copy\n\n"
                "**Location:** Academic office of your college/department"
            ],
            'partial': [
                "I can help with grade report requests. What type of grade report do you need?",
                "Grade reports are available in various formats. Please specify your requirements."
            ]
        },

        'course_information': {
            'complete': [
                "**AAU Course Information - {department}**\n\n"
                "**Available Resources:**\n"
                "• Course catalog (online and printed)\n"
                "• Academic advisor consultation\n"
                "• Department office visits\n"
                "• Student handbook\n\n"
                "**Course Details Include:**\n"
                "• Prerequisites and corequisites\n"
                "• Credit hours (ECTS)\n"
                "• Course descriptions and objectives\n"
                "• Semester offerings\n"
                "• Assessment methods\n"
                "• Learning outcomes\n\n"
                "**Academic Structure:**\n"
                "• Regular semester: 16 weeks\n"
                "• Summer semester: 8-12 weeks\n"
                "• Modular courses: Variable duration\n\n"
                "**Contact:** {department} department office for specific course information"
            ],
            'partial': [
                "I can provide course information. Which department or specific course are you interested in?",
                "Which department's courses would you like to know about?"
            ]
        },

        'course_catalog_inquiry': {
            'complete': [
                "**AAU Course Catalog - {department}**\n\n"
                "**Catalog Access:**\n"
                "• Online course catalog\n"
                "• Printed versions at department offices\n"
                "• Student portal access\n"
                "• Academic advisor guidance\n\n"
                "**Catalog Information:**\n"
                "• Complete course listings\n"
                "• Program requirements\n"
                "• Course sequences\n"
                "• Credit requirements\n"
                "• Graduation requirements\n\n"
                "**Program Levels:**\n"
                "• Undergraduate programs\n"
                "• Masters programs\n"
                "• PhD programs\n"
                "• Certificate programs\n\n"
                "**Updates:** Catalogs updated annually\n"
                "**Contact:** Academic office for current catalog information"
            ],
            'partial': [
                "I can help with course catalog information. Which department or program level are you interested in?",
                "Course catalogs are available for all programs. Please specify your area of interest."
            ]
        },

        'prerequisite_inquiry': {
            'complete': [
                "**AAU Course Prerequisites - {department}**\n\n"
                "**Prerequisite Types:**\n"
                "• Academic prerequisites (completed courses)\n"
                "• Grade requirements (minimum CGPA)\n"
                "• Program-specific requirements\n"
                "• Language proficiency requirements\n\n"
                "**How to Check Prerequisites:**\n"
                "1. Review course catalog\n"
                "2. Consult academic advisor\n"
                "3. Check student portal\n"
                "4. Contact department office\n\n"
                "**Prerequisite Waiver:**\n"
                "• Petition process available\n"
                "• Department approval required\n"
                "• Academic justification needed\n"
                "• Alternative demonstration of competency\n\n"
                "**Important:** Prerequisites must be met before registration\n"
                "**Contact:** Academic advisor or {department} office"
            ],
            'partial': [
                "I can help with prerequisite information. Which course or program are you asking about?",
                "Prerequisites vary by course and program. Please specify what you're interested in."
            ]
        },

        'schedule_inquiry': {
            'complete': [
                "**AAU Schedule Information - {semester} {year}**\n\n"
                "**Where to Find Schedules:**\n"
                "• Student portal (online access)\n"
                "• Department notice boards\n"
                "• Academic office\n"
                "• Mobile app (if available)\n\n"
                "**Schedule Information Includes:**\n"
                "• Class times and locations\n"
                "• Instructor information\n"
                "• Room assignments\n"
                "• Exam schedules\n"
                "• Important academic dates\n\n"
                "**Current Exam Schedules:**\n"
                "• First-Year Final Exams: January 25, 2026\n"
                "• Inclusiveness Course: January 12, 2026\n"
                "• GAT Exam: January 5, 2026\n\n"
                "**Updates:** Check regularly for schedule changes\n"
                "**Contact:** Academic office for schedule assistance"
            ],
            'partial': [
                "I can help with schedule information. Which semester and year are you asking about?",
                "Please specify the semester and academic year for schedule details."
            ]
        },

        'student_id_services': {
            'complete': [
                "**AAU Student ID Services**\n\n"
                "**New Student ID:**\n"
                "• Issued during registration process\n"
                "• Required passport-size photo\n"
                "• Student information verification\n"
                "• Processing fee applies\n\n"
                "**ID Replacement:**\n"
                "• Lost/damaged ID replacement available\n"
                "• Police report required for lost IDs\n"
                "• Replacement fee: Contact student services\n"
                "• New photo may be required\n\n"
                "**ID Services Include:**\n"
                "• Library access\n"
                "• Exam admission\n"
                "• Campus facility access\n"
                "• Student discounts\n"
                "• Official identification\n\n"
                "**Processing Time:** 3-5 working days\n"
                "**Location:** Student Services Office\n"
                "**Contact:** Student Services for ID-related issues"
            ],
            'partial': [
                "I can help with student ID services. Do you need a new ID, replacement, or have questions about ID services?",
                "Student ID services include new issuance and replacements. What do you need help with?"
            ]
        },

        'document_request': {
            'complete': [
                "**AAU Document Request - {document_type}**\n\n"
                "**Available Documents:**\n"
                "• Official transcripts\n"
                "• Degree certificates\n"
                "• Enrollment verification letters\n"
                "• Grade reports\n"
                "• Academic standing certificates\n"
                "• Recommendation letters\n\n"
                "**General Requirements:**\n"
                "• Completed request form\n"
                "• Valid identification\n"
                "• Payment receipt\n"
                "• Passport photo (for some documents)\n\n"
                "**Processing Times:**\n"
                "• Transcripts: 3-5 working days\n"
                "• Certificates: 5-7 working days\n"
                "• Verification letters: Same day\n"
                "• Express service: Additional fee\n\n"
                "**Fees:** Vary by document type (50 ETB for transcripts)\n"
                "**Location:** Registrar's Office, Main Campus"
            ],
            'partial': [
                "I can help with document requests. What type of document do you need?",
                "Which document would you like to request from AAU?"
            ]
        },

        'alumni_services_inquiry': {
            'complete': [
                "**AAU Alumni Services**\n\n"
                "**Alumni Benefits:**\n"
                "• Alumni network access\n"
                "• Career services and job postings\n"
                "• Continuing education opportunities\n"
                "• Library access privileges\n"
                "• Alumni events and reunions\n\n"
                "**Current Alumni Events:**\n"
                "• Alumni Homecoming 2025: December 27, 2025 - January 2, 2026\n"
                "• 75th Anniversary celebrations\n"
                "• Distinguished lecture series\n"
                "• Networking events\n\n"
                "**Alumni Services:**\n"
                "• Transcript services\n"
                "• Employment verification\n"
                "• Alumni directory access\n"
                "• Mentorship programs\n\n"
                "**Motto:** Once AAU, Always AAU\n"
                "**Contact:** Alumni Relations Office"
            ],
            'partial': [
                "I can help with alumni services information. Are you looking for events, benefits, or specific services?",
                "AAU offers various alumni services. What specific information do you need?"
            ]
        },

        'general_info': {
            'complete': [
                "**Welcome to AAU - Ethiopia's Premier University! 🎓**\n\n"
                "**About AAU:**\n"
                "• Founded: 1950 (75+ years of excellence)\n"
                "• Ranking: #1 University in East Africa\n"
                "• Students: 280K+ graduates all-time\n"
                "• Research: 12,293+ scholarly outputs since 2014\n\n"
                "**I can help you with:**\n"
                "• Admission inquiries (undergraduate & graduate)\n"
                "• Registration assistance\n"
                "• Fee payment information\n"
                "• Document requests (transcripts, certificates)\n"
                "• Grade inquiries and academic records\n"
                "• Course information and schedules\n"
                "• Campus locations and facilities\n"
                "• Research opportunities\n\n"
                "**Motto:** Seek Wisdom, Elevate Your Intellect and Serve Humanity\n"
                "How can I assist you today?",

                "**AAU Student Services 🏛️**\n\n"
                "**Main Campus:** Sidist Kilo, Addis Ababa\n"
                "**Other Campuses:** Sefere Selam, Science Campus (4 Kilo), Bishoftu\n"
                "**Phone:** +251-11-123-4567\n"
                "**Email:** info@aau.edu.et\n"
                "**Website:** www.aau.edu.et\n\n"
                "**Key Services:**\n"
                "• Academic services and registration\n"
                "• Library services (10 branch libraries)\n"
                "• Tikur Anbessa Hospital\n"
                "• Student accommodation\n"
                "• Research and innovation support\n\n"
                "What specific information do you need?"
            ],
            'partial': [
                "Hello! I'm here to help with AAU services. What can I assist you with?",
                "Welcome to AAU Helpdesk! How may I help you today?"
            ]
        },

        'technical_support': {
            'complete': [
                "**AAU Technical Support**\n\n"
                "**Common Technical Issues:**\n"
                "• Student portal access problems\n"
                "• Email account setup and issues\n"
                "• WiFi connectivity on campus\n"
                "• Online learning platform access\n"
                "• Digital library access\n\n"
                "**IT Support Services:**\n"
                "• Account password resets\n"
                "• Software installation guidance\n"
                "• Network connectivity troubleshooting\n"
                "• Digital resource access\n"
                "• Online exam technical support\n\n"
                "**Contact Information:**\n"
                "• IT Support: +251-11-123-4569\n"
                "• Email: itsupport@aau.edu.et\n"
                "• Hours: Monday-Friday, 8:00 AM - 5:00 PM\n"
                "• Location: IT Services Office, Main Campus\n\n"
                "**Self-Service:** Many issues can be resolved through the student portal help section"
            ],
            'partial': [
                "I can help with technical issues. What specific problem are you experiencing?",
                "What technical issue can I help you with today?"
            ]
        },

        # Additional specialized intents
        'facility_booking_inquiry': {
            'complete': [
                "**AAU Facility Booking Services**\n\n"
                "**Available Facilities:**\n"
                "• Conference rooms and meeting halls\n"
                "• Ras Mekonnen Hall (Main Campus)\n"
                "• Eshetu Chole Hall\n"
                "• Mandela Hall\n"
                "• Laboratory spaces\n"
                "• Sports facilities\n"
                "• Cultural Center venues\n\n"
                "**Booking Process:**\n"
                "1. Submit facility request form\n"
                "2. Specify date, time, and purpose\n"
                "3. Get approval from relevant office\n"
                "4. Pay applicable fees\n"
                "5. Confirm booking\n\n"
                "**Requirements:**\n"
                "• Valid AAU affiliation\n"
                "• Event details and purpose\n"
                "• Insurance (for large events)\n"
                "• Setup and cleanup arrangements\n\n"
                "**Contact:** Facilities Management Office"
            ],
            'partial': [
                "I can help with facility booking. What type of facility or event space do you need?",
                "AAU has various bookable facilities. Please specify your requirements."
            ]
        },

        'radio_station_inquiry': {
            'complete': [
                "**AAU Community Radio FM 99.4**\n\n"
                "**About AAU Radio:**\n"
                "• Frequency: FM 99.4\n"
                "• Slogan: \"የማሕበረሰብ ድምፅ\" (Voice of the Community)\n"
                "• Community-focused programming\n"
                "• Educational content\n"
                "• Student involvement opportunities\n\n"
                "**Programming:**\n"
                "• Academic discussions\n"
                "• Community news and updates\n"
                "• Cultural programs\n"
                "• Student shows\n"
                "• Educational content\n\n"
                "**Get Involved:**\n"
                "• Student volunteer opportunities\n"
                "• Program hosting\n"
                "• Content creation\n"
                "• Technical training\n\n"
                "**Follow:** @AAUFM99point4 on Telegram\n"
                "**Contact:** AAU Radio Station for participation opportunities"
            ],
            'partial': [
                "I can help with AAU Radio information. Are you interested in listening, participating, or general information?",
                "AAU FM 99.4 is the community radio station. What would you like to know?"
            ]
        },

        'museum_services_inquiry': {
            'complete': [
                "**AAU Museums and Cultural Services**\n\n"
                "**AAU Museums:**\n"
                "• Ethnographic Museum (IES, Sidist Kilo Campus)\n"
                "  - Ethiopia's first university museum (1950s)\n"
                "  - Artifacts, traditional tools, historical heritage\n"
                "• National Herbarium (Science Campus)\n"
                "  - Mummified plants and animals\n"
                "  - Endemic Ethiopian species\n\n"
                "**Cultural Center:**\n"
                "• Event hosting and exhibitions\n"
                "• Book fairs and literary events\n"
                "• Cultural performances\n"
                "• Academic conferences\n\n"
                "**Services:**\n"
                "• Guided tours\n"
                "• Educational programs\n"
                "• Research access\n"
                "• Cultural events\n\n"
                "**Location:** Various campus locations\n"
                "**Contact:** Museum services for tour arrangements"
            ],
            'partial': [
                "I can help with museum and cultural services information. Are you interested in visits, exhibitions, or educational programs?",
                "AAU has several museums and cultural facilities. What specific information do you need?"
            ]
        },

        'out_of_domain': {
            'complete': [
                "I'm not sure about that question. For AAU-related information, please check our website at www.aau.edu.et or follow our official Telegram channel @aau_official for the latest updates.",
                "I don't have information about that topic. You can find more AAU-related information on our website (www.aau.edu.et) or our Telegram channel @aau_official.",
                "That's outside my area of expertise. For AAU services and information, visit www.aau.edu.et or check our Telegram @aau_official.",
                "I'm not able to help with that. For university-related questions, please visit www.aau.edu.et or follow @aau_official on Telegram.",
                "I don't have information about that. For AAU-specific questions, check www.aau.edu.et or our official Telegram channel @aau_official."
            ],
            'partial': [
                "I'm not sure about that. For AAU information, please check www.aau.edu.et or @aau_official on Telegram.",
                "That's not something I can help with. Visit www.aau.edu.et or @aau_official for AAU-related information."
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
        "I'm not entirely sure about that. You can find more information on the AAU website (www.aau.edu.et) or check our official Telegram channel @aau_official for the latest updates.",
        "I'm not completely certain about that query. For the most accurate information, please visit www.aau.edu.et or follow our Telegram channel @aau_official.",
        "I'm not sure I have the right information for that. Please check the AAU website at www.aau.edu.et or our Telegram channel @aau_official for official updates.",
        "I don't have enough confidence in my answer for that. For reliable information, visit www.aau.edu.et or check our Telegram @aau_official.",
        "I'm not certain about that specific question. You can get accurate information from the AAU website (www.aau.edu.et) or our official Telegram channel @aau_official."
    ]

def _initialize_out_of_domain_templates() -> Dict[str, str]:
    """Initialize out-of-domain response templates - REMOVED"""
    # This function is no longer used - keeping for backward compatibility
    return {}


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
        # Removed out_of_domain_templates - using simple confidence-based responses

    def generate_response(self, intent: str, parameters: Dict[str, Any],
                         missing_parameters: List[str], confidence: float) -> str:
        """Generate appropriate response based on intent and parameters"""
        
        # Missing required parameters - ask follow-up questions
        if missing_parameters:
            return self._generate_follow_up_response(intent, missing_parameters, parameters)
        
        # Complete information - provide full response
        return self._generate_complete_response(intent, parameters)
    
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
    
