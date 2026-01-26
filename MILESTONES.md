# AAU Helpdesk Chatbot - Detailed Milestone Specifications

## Milestone 0: Environment & Repository Setup

### Objectives
- [x] Establish project structure and development environment
- [x] Configure Python environment with all dependencies
- [x] Initialize FastAPI application with health endpoint
- [x] Set up version control and documentation

### Tasks
- [x] **Project Structure Setup**
  - [x] Create directory structure:
    ```
    ├── app/
    │   ├── __init__.py
    │   ├── main.py (FastAPI app)
    │   ├── nlp_engine.py
    │   ├── dialogue_manager.py
    │   ├── templates.py
    │   └── utils.py
    ├── data/
    │   ├── raw/ (raw scraped data)
    │   ├── processed/ (cleaned data)
    │   └── annotated/ (labeled data)
    ├── models/ (trained models)
    ├── config/ (configuration files)
    ├── scripts/ (utility scripts)
    ├── tests/ (unit tests)
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    └── README.md
    ```

- [x] **Python Environment**
  - [x] Create `requirements.txt` with:
    - [x] fastapi>=0.104.0
    - [x] uvicorn>=0.24.0
    - [x] spacy>=3.7.0
    - [x] transformers>=4.35.0
    - [x] scikit-learn>=1.3.0
    - [x] pandas>=2.1.0
    - [x] python-dotenv>=1.0.0
    - [x] pydantic>=2.5.0
  - [x] Create `.env.example` with environment variables template
  - [x] Document Python version requirement (3.10+)

- [x] **FastAPI Initialization**
  - [x] Create `app/main.py` with:
    - [x] FastAPI app instance
    - [x] Health check endpoint (`GET /health`)
    - [x] CORS middleware configuration
    - [x] Basic error handling
  - [x] Create `app/config.py` for configuration management

- [x] **Documentation**
  - [x] Create comprehensive README.md with:
    - [x] Project description
    - [x] Installation instructions
    - [x] Environment setup guide
    - [x] API documentation structure

### Deliverables
- [x] Complete project directory structure
- [x] `requirements.txt` with all dependencies
- [x] `.env.example` file
- [x] FastAPI app with `/health` endpoint returning `{"status": "healthy"}`
- [x] README.md with setup instructions
- [x] `.gitignore` file

### Acceptance Criteria
- [x] `pip install -r requirements.txt` completes without errors
- [x] `uvicorn app.main:app --reload` starts server successfully
- [x] `GET /health` returns `200 OK` with `{"status": "healthy"}`
- [x] All directories are created and properly structured
- [x] Python 3.10+ is verified

### Dependencies
- Python 3.10+ installed
- pip package manager

---

## Milestone 1: Intent & Slot Specification

### Objectives
- [x] Define 10-15 MVP intents covering AAU helpdesk services
- [x] Specify required and optional slots (parameters) for each intent
- [x] Create single source-of-truth specification file
- [x] Design response templates and follow-up questions

### Tasks
- [x] **Intent Definition**
  - [x] Define 10-15 intents such as:
    - [x] `admission_inquiry` - Questions about admission requirements, deadlines
    - [x] `registration_help` - Course registration assistance
    - [x] `fee_payment` - Tuition fees, payment methods, deadlines
    - [x] `transcript_request` - Requesting official transcripts
    - [x] `grade_inquiry` - Checking grades, GPA calculation
    - [x] `schedule_inquiry` - Class schedules, exam schedules
    - [x] `library_services` - Library hours, book availability
    - [x] `dormitory_info` - Housing information, applications
    - [x] `graduation_requirements` - Graduation criteria, ceremony info
    - [x] `department_contact` - Department contact information
    - [x] `document_request` - Requesting various official documents
    - [x] `semester_info` - Academic calendar, semester dates
    - [x] `financial_aid` - Scholarships, financial assistance
    - [x] `campus_facilities` - Information about campus facilities
    - [x] `general_inquiry` - General questions not fitting other categories

- [x] **Slot (Parameter) Definition**
  - [x] For each intent, define:
    - [x] **Required slots**: Must be extracted before responding
    - [x] **Optional slots**: Enhance response but not mandatory
  - [x] Common slot types:
    - [x] `department` - Department name (e.g., "Computer Science", "Engineering")
    - [x] `document_type` - Type of document (e.g., "transcript", "certificate")
    - [x] `fee_type` - Type of fee (e.g., "tuition", "registration", "library")
    - [x] `semester` - Academic semester (e.g., "Fall 2024", "Spring 2025")
    - [x] `academic_year` - Academic year (e.g., "2024/2025")
    - [x] `student_id` - Student identification number
    - [x] `reference_number` - Transaction or request reference number
    - [x] `date` - Specific dates (deadlines, request dates)
    - [x] `amount` - Fee amounts or payment amounts
    - [x] `contact_method` - Preferred contact method

- [x] **Create `config/intent.yaml`**
  - [x] Structure with all intents:
    - [x] Intent name
    - [x] Description
    - [x] Required slots list
    - [x] Optional slots list
    - [x] Example utterances (5-10 per intent)
    - [x] Response template
    - [x] Follow-up questions for missing required slots

- [x] **Validation Schema**
  - [x] Create `app/schemas.py` with Pydantic models:
    - [x] `IntentRequest` - Input schema
    - [x] `IntentResponse` - Output schema
    - [x] `Slot` - Slot definition model
    - [x] `ConversationState` - State management model

### Deliverables
- [x] `config/intent.yaml` with all 10-15 intents fully specified
- [x] `app/schemas.py` with Pydantic models
- [x] Documentation of intent definitions and slot requirements
- [x] Example utterances for each intent (5-10 per intent)

### Acceptance Criteria
- [x] All 10-15 intents are clearly defined with descriptions
- [x] Each intent has required/optional slots specified
- [x] Each intent has 5-10 example utterances
- [x] Response templates are defined for each intent
- [x] Follow-up questions are specified for missing required slots
- [x] YAML file is valid and parseable
- [x] Pydantic schemas validate correctly

### Dependencies
- Milestone 0 completed
- Understanding of AAU helpdesk domain

---

## Milestone 2: Data Collection

### Objectives
- [ ] Collect raw user-like questions from AAU sources
- [ ] Store data in unified format
- [ ] Perform basic cleaning and normalization
- [ ] Create data collection pipeline

### Tasks
- [ ] **Web Scraping Setup**
  - [ ] Enhance `scripts/web_scrapper.py`:
    - [ ] Scrape AAU official website pages (FAQ sections, help pages)
    - [ ] Extract Q&A pairs from web content
    - [ ] Handle pagination and dynamic content
    - [ ] Respect robots.txt and rate limiting
  - [ ] Target pages:
    - [ ] Admission pages
    - [ ] Registration guides
    - [ ] Fee payment information
    - [ ] Academic calendar pages
    - [ ] Department pages

- [ ] **Telegram Data Collection**
  - [ ] Enhance `scripts/telegram_cli.py`:
    - [ ] Connect to public AAU Telegram channels
    - [ ] Extract user questions and messages
    - [ ] Filter relevant helpdesk-related queries
    - [ ] Handle message history extraction
  - [ ] Data privacy considerations:
    - [ ] Only public channels
    - [ ] Anonymize user data
    - [ ] Remove personal identifiers

- [ ] **Data Storage**
  - [ ] Create unified CSV format:
    ```csv
    id,source,raw_text,cleaned_text,date_collected
    1,website,"What are admission requirements?","what are admission requirements",2024-01-15
    2,telegram,"How do I register for courses?","how do i register for courses",2024-01-15
    ```
  - [ ] Store in `data/raw/collected_data.csv`

- [ ] **Data Cleaning Pipeline**
  - [ ] Create `app/data_processor.py`:
    - [ ] Text normalization (lowercase, remove extra spaces)
    - [ ] Remove special characters (keep essential punctuation)
    - [ ] Handle Amharic/English text (if applicable)
    - [ ] Remove duplicates
    - [ ] Basic spell checking
  - [ ] Output: `data/processed/cleaned_data.csv`

- [ ] **Data Statistics**
  - [ ] Create `scripts/data_stats.py`:
    - [ ] Count total questions collected
    - [ ] Distribution by source (website vs telegram)
    - [ ] Text length statistics
    - [ ] Language distribution

### Deliverables
- [ ] `scripts/web_scrapper.py` functional
- [ ] `scripts/telegram_cli.py` functional
- [ ] `data/raw/collected_data.csv` with raw data
- [ ] `data/processed/cleaned_data.csv` with cleaned data
- [ ] `app/data_processor.py` with cleaning functions
- [ ] Data collection report (statistics, sources, counts)

### Acceptance Criteria
- [ ] At least 500+ raw questions collected
- [ ] Data from both website and Telegram sources
- [ ] CSV files are properly formatted and readable
- [ ] Cleaning pipeline removes duplicates and normalizes text
- [ ] Data statistics report generated
- [ ] No personal identifiable information in stored data

### Dependencies
- Milestone 0 completed
- Access to AAU website and Telegram channels
- Python libraries: requests, beautifulsoup4, python-telegram-bot (or similar)

---

## Milestone 3: Annotation & Labeling

### Objectives
- [ ] Design annotation schema for intents and slots
- [ ] Label training data (50+ examples per intent)
- [ ] Store labeled data in structured format
- [ ] Create annotation guidelines document

### Tasks
- [ ] **Annotation Schema Design**
  - [ ] Create `config/annotation_schema.json`:
    - [ ] Define format (JSONL)
    - [ ] Define fields (text, intent, slots with positions)
    - [ ] Slot format with value, start, end positions

- [ ] **Annotation Guidelines**
  - [ ] Create `docs/annotation_guidelines.md`:
    - [ ] Intent labeling rules
    - [ ] Slot extraction rules
    - [ ] Handling ambiguous cases
    - [ ] Examples of correct/incorrect annotations
    - [ ] Edge cases and special scenarios

- [ ] **Annotation Tool/Process**
  - [ ] Option A: Manual annotation in CSV/JSON
  - [ ] Option B: Use annotation tool (e.g., Label Studio, Doccano)
  - [ ] Create `scripts/annotation_helper.py`:
    - [ ] Load cleaned data
    - [ ] Present questions for labeling
    - [ ] Validate annotations
    - [ ] Export to training format

- [ ] **Label Training Data**
  - [ ] Annotate at least 50 examples per intent
  - [ ] Target: 750+ labeled examples (50 × 15 intents)
  - [ ] Distribution:
    - [ ] 70% training set
    - [ ] 15% validation set
    - [ ] 15% test set
  - [ ] Store in `data/annotated/`:
    - [ ] `train.jsonl`
    - [ ] `val.jsonl`
    - [ ] `test.jsonl`

- [ ] **Annotation Quality**
  - [ ] Inter-annotator agreement check (if multiple annotators)
  - [ ] Review and fix inconsistencies
  - [ ] Create annotation statistics report

### Deliverables
- [ ] `config/annotation_schema.json`
- [ ] `docs/annotation_guidelines.md`
- [ ] `data/annotated/train.jsonl` (525+ examples)
- [ ] `data/annotated/val.jsonl` (112+ examples)
- [ ] `data/annotated/test.jsonl` (112+ examples)
- [ ] Annotation statistics report
- [ ] `scripts/annotation_helper.py` (if custom tool)

### Acceptance Criteria
- [ ] At least 50 labeled examples per intent
- [ ] All examples have intent labels
- [ ] Slot annotations include value and position (start/end)
- [ ] Train/val/test split is properly done
- [ ] JSONL format is valid and parseable
- [ ] Annotation guidelines document is complete
- [ ] No missing required slots in annotations

### Dependencies
- Milestone 1 completed (intent definitions)
- Milestone 2 completed (cleaned data)
- Human annotators (or annotation tool)

---

## Milestone 4: Baseline NLP Models

### Objectives
- [ ] Train baseline intent classifier (TF-IDF + Logistic Regression)
- [ ] Implement rule-based parameter extraction
- [ ] Create evaluation framework
- [ ] Establish performance baselines

### Tasks
- [ ] **Intent Classifier - Baseline**
  - [ ] Create `app/models/intent_classifier.py`:
    - [ ] TF-IDF vectorization
    - [ ] Logistic Regression classifier
    - [ ] Training pipeline
    - [ ] Prediction function
  - [ ] Features:
    - [ ] Unigram and bigram features
    - [ ] Text preprocessing (tokenization, normalization)
    - [ ] Class balancing (if needed)

- [ ] **Parameter Extraction - Rule-Based**
  - [ ] Create `app/models/parameter_extractor.py`:
    - [ ] **Department extraction**:
      - [ ] Keyword matching (known department names)
      - [ ] Pattern matching (e.g., "CS department", "Computer Science")
    - [ ] **Document type extraction**:
      - [ ] Keywords: transcript, certificate, diploma, letter
    - [ ] **Fee type extraction**:
      - [ ] Keywords: tuition, registration, library, lab
    - [ ] **Semester extraction**:
      - [ ] Pattern: "Fall 2024", "Spring 2025", "Semester 1"
      - [ ] Date parsing for academic periods
    - [ ] **Student ID extraction**:
      - [ ] Regex patterns for ID formats
    - [ ] **Date extraction**:
      - [ ] Date parsing (various formats)
    - [ ] **Amount extraction**:
      - [ ] Currency and number patterns

- [ ] **Model Training Pipeline**
  - [ ] Create `scripts/train_baseline.py`:
    - [ ] Load annotated data
    - [ ] Preprocess text
    - [ ] Train intent classifier
    - [ ] Save model to `models/baseline_intent_model.pkl`
    - [ ] Save vectorizer to `models/tfidf_vectorizer.pkl`

- [ ] **Evaluation Framework**
  - [ ] Create `app/evaluation.py`:
    - [ ] Intent classification metrics:
      - [ ] Accuracy
      - [ ] Per-intent precision, recall, F1
      - [ ] Confusion matrix
    - [ ] Parameter extraction metrics:
      - [ ] Per-slot precision, recall, F1
      - [ ] Exact match accuracy
      - [ ] Partial match (overlap) metrics

- [ ] **Baseline Results**
  - [ ] Run evaluation on test set
  - [ ] Generate report: `reports/baseline_results.md`
  - [ ] Save confusion matrix visualization

### Deliverables
- [ ] `app/models/intent_classifier.py`
- [ ] `app/models/parameter_extractor.py`
- [ ] `scripts/train_baseline.py`
- [ ] `app/evaluation.py`
- [ ] `models/baseline_intent_model.pkl`
- [ ] `models/tfidf_vectorizer.pkl`
- [ ] `reports/baseline_results.md` with metrics

### Acceptance Criteria
- [ ] Intent classifier trains without errors
- [ ] Baseline intent accuracy > 70% on test set
- [ ] Rule-based extractor handles all defined slot types
- [ ] Evaluation metrics are calculated correctly
- [ ] Models are saved and loadable
- [ ] Confusion matrix is generated
- [ ] Per-slot F1 scores are reported

### Dependencies
- Milestone 3 completed (annotated data)
- scikit-learn installed
- regex library for pattern matching

---

## Milestone 5: Dialogue Management

### Objectives
- [ ] Implement conversation state management
- [ ] Create slot-filling logic
- [ ] Handle follow-up questions
- [ ] Manage multi-turn conversations

### Tasks
- [ ] **Conversation State Management**
  - [ ] Create `app/dialogue_manager.py`:
    - [ ] `ConversationState` class:
      - [ ] Current intent (if identified)
      - [ ] Filled slots dictionary
      - [ ] Conversation history
      - [ ] Turn counter
      - [ ] Session ID
    - [ ] State persistence (in-memory or database)

- [ ] **Slot-Filling Logic**
  - [ ] Implement slot-filling algorithm:
    - [ ] Check required slots for current intent
    - [ ] Compare with filled slots
    - [ ] Identify missing required slots
    - [ ] Trigger follow-up questions for missing slots
  - [ ] Slot update logic:
    - [ ] Extract parameters from user input
    - [ ] Update conversation state
    - [ ] Handle slot corrections

- [ ] **Response Generation**
  - [ ] Create `app/response_generator.py`:
    - [ ] Load response templates from `intent.yaml`
    - [ ] Fill templates with slot values
    - [ ] Generate follow-up questions
    - [ ] Handle incomplete information scenarios
  - [ ] Response types:
    - [ ] Complete answer (all required slots filled)
    - [ ] Follow-up question (missing required slots)
    - [ ] Clarification request (ambiguous input)

- [ ] **Multi-Turn Flow**
  - [ ] Implement conversation flow:
    - [ ] User: "I want to know about fees"
      - [ ] Identify intent: fee_payment
      - [ ] Check required slots: [fee_type] missing
      - [ ] Response: "Which type of fee are you asking about?"
    - [ ] User: "tuition fee"
      - [ ] Extract slot: fee_type = "tuition"
      - [ ] Check required slots: all filled
      - [ ] Generate complete response with template

- [ ] **Integration**
  - [ ] Integrate with intent classifier and parameter extractor
  - [ ] Create `app/chatbot.py`:
    - [ ] Main chatbot class
    - [ ] Process user message
    - [ ] Update state
    - [ ] Generate response

### Deliverables
- [ ] `app/dialogue_manager.py` with state management
- [ ] `app/response_generator.py` with template filling
- [ ] `app/chatbot.py` with integrated chatbot
- [ ] Unit tests for dialogue management
- [ ] Example conversation flows documented

### Acceptance Criteria
- [ ] Conversation state persists across turns
- [ ] Required slots trigger follow-up questions
- [ ] Templates are filled correctly with slot values
- [ ] Multi-turn conversations work end-to-end
- [ ] State can be reset/cleared
- [ ] Handles slot corrections gracefully
- [ ] Unit tests pass

### Dependencies
- Milestone 1 completed (intent.yaml with templates)
- Milestone 4 completed (intent classifier, parameter extractor)

---

## Milestone 6: FastAPI Backend

### Objectives
- [ ] Expose `/chat` endpoint for chatbot interactions
- [ ] Implement health checks and monitoring
- [ ] Add CORS support for frontend integration
- [ ] Create API documentation

### Tasks
- [ ] **Chat Endpoint**
  - [ ] Create `POST /chat` endpoint:
    - [ ] Request body:
      ```json
      {
        "message": "user message text",
        "session_id": "optional session id",
        "conversation_state": "optional existing state"
      }
      ```
    - [ ] Response:
      ```json
      {
        "response": "bot response text",
        "intent": "detected intent",
        "slots": {"slot_name": "value"},
        "conversation_state": "updated state",
        "requires_followup": true/false
      }
      ```

- [ ] **Session Management**
  - [ ] Implement session handling:
    - [ ] Generate session IDs
    - [ ] Store conversation states per session
    - [ ] Session timeout/cleanup
  - [ ] Options: In-memory dict or Redis

- [ ] **Health & Monitoring**
  - [ ] `GET /health`: Basic health check
  - [ ] `GET /health/detailed`: Model loading status, dependencies
  - [ ] Add logging:
    - [ ] Request/response logging
    - [ ] Error logging
    - [ ] Performance metrics

- [ ] **CORS Configuration**
  - [ ] Configure CORS middleware:
    - [ ] Allow specific origins (or all for development)
    - [ ] Handle preflight requests
    - [ ] Set appropriate headers

- [ ] **Error Handling**
  - [ ] Custom exception handlers:
    - [ ] Validation errors
    - [ ] Model loading errors
    - [ ] Processing errors
  - [ ] Return appropriate HTTP status codes

- [ ] **API Documentation**
  - [ ] FastAPI auto-generated docs (`/docs`)
  - [ ] OpenAPI schema
  - [ ] Example requests/responses

- [ ] **Configuration**
  - [ ] Environment-based configuration:
    - [ ] Model paths
    - [ ] API settings
    - [ ] Logging levels

### Deliverables
- [ ] `app/main.py` with `/chat` endpoint
- [ ] `GET /health` and `/health/detailed` endpoints
- [ ] CORS middleware configured
- [ ] Error handling implemented
- [ ] API documentation accessible at `/docs`
- [ ] `app/config.py` with configuration management
- [ ] Logging setup

### Acceptance Criteria
- [ ] `POST /chat` accepts messages and returns responses
- [ ] Session management works correctly
- [ ] Health endpoints return proper status
- [ ] CORS allows frontend requests
- [ ] Error responses are properly formatted
- [ ] API docs are accessible and complete
- [ ] Server handles concurrent requests

### Dependencies
- Milestone 5 completed (dialogue manager, chatbot)
- FastAPI installed
- uvicorn for ASGI server

---

## Milestone 7: Evaluation

### Objectives
- [ ] Evaluate intent classification performance
- [ ] Evaluate parameter extraction per slot
- [ ] Generate comprehensive evaluation reports
- [ ] Identify improvement areas

### Tasks
- [ ] **Intent Classification Evaluation**
  - [ ] Calculate metrics:
    - [ ] Overall accuracy
    - [ ] Per-intent precision, recall, F1
    - [ ] Macro-averaged F1
    - [ ] Weighted F1
  - [ ] Generate confusion matrix:
    - [ ] Visualize with matplotlib/seaborn
    - [ ] Identify confusion patterns
    - [ ] Save to `reports/confusion_matrix.png`

- [ ] **Parameter Extraction Evaluation**
  - [ ] Per-slot evaluation:
    - [ ] Precision: correct extractions / total extractions
    - [ ] Recall: correct extractions / total expected
    - [ ] F1-score per slot
  - [ ] Evaluation modes:
    - [ ] Exact match (value must match exactly)
    - [ ] Partial match (overlap or similarity)
  - [ ] Handle:
    - [ ] False positives
    - [ ] False negatives
    - [ ] Multiple extractions

- [ ] **End-to-End Evaluation**
  - [ ] Test complete conversation flows:
    - [ ] Intent + slot filling accuracy
    - [ ] Multi-turn success rate
    - [ ] Response quality (manual or automated)

- [ ] **Evaluation Script**
  - [ ] Create `scripts/evaluate.py`:
    - [ ] Load test set
    - [ ] Run predictions
    - [ ] Calculate all metrics
    - [ ] Generate reports
  - [ ] Output:
    - [ ] `reports/evaluation_report.md`
    - [ ] `reports/metrics.json`
    - [ ] Visualizations

- [ ] **Error Analysis**
  - [ ] Identify common errors:
    - [ ] Intent misclassifications
    - [ ] Slot extraction failures
    - [ ] Ambiguous cases
  - [ ] Create `reports/error_analysis.md`

### Deliverables
- [ ] `scripts/evaluate.py` evaluation script
- [ ] `reports/evaluation_report.md` with all metrics
- [ ] `reports/metrics.json` with numerical results
- [ ] `reports/confusion_matrix.png` visualization
- [ ] `reports/error_analysis.md` with error patterns
- [ ] Per-slot F1 scores documented

### Acceptance Criteria
- [ ] Intent accuracy > 75% (baseline target)
- [ ] All metrics calculated correctly
- [ ] Confusion matrix generated and saved
- [ ] Per-slot F1 scores reported
- [ ] Error analysis identifies improvement areas
- [ ] Evaluation is reproducible

### Dependencies
- Milestone 4 completed (trained models)
- Milestone 3 completed (test set)
- Evaluation libraries: scikit-learn, matplotlib

---

## Milestone 8: spaCy NER Upgrade

### Objectives
- [ ] Train custom spaCy NER model for key entities
- [ ] Combine NER with rule-based extraction
- [ ] Improve parameter extraction accuracy
- [ ] Evaluate improvements

### Tasks
- [ ] **spaCy Setup**
  - [ ] Install spaCy and language model:
    - [ ] `python -m spacy download en_core_web_sm`
    - [ ] Or use multilingual model if needed
  - [ ] Create `app/models/spacy_ner.py`

- [ ] **Training Data Preparation**
  - [ ] Convert annotations to spaCy format:
    - [ ] Create `scripts/convert_to_spacy.py`
    - [ ] Format: `.spacy` binary format
    - [ ] Entity labels:
      - [ ] `DEPARTMENT`
      - [ ] `DOCUMENT_TYPE`
      - [ ] `FEE_TYPE`
      - [ ] `SEMESTER`
      - [ ] `STUDENT_ID`
      - [ ] `REFERENCE_NUMBER`
      - [ ] `DATE`
      - [ ] `AMOUNT`

- [ ] **Model Training**
  - [ ] Create `scripts/train_spacy_ner.py`:
    - [ ] Load training data
    - [ ] Initialize spaCy model
    - [ ] Train NER component
    - [ ] Save model to `models/spacy_ner_model/`
  - [ ] Training configuration:
    - [ ] Number of iterations
    - [ ] Learning rate
    - [ ] Batch size
    - [ ] Early stopping

- [ ] **Hybrid Extraction**
  - [ ] Update `app/models/parameter_extractor.py`:
    - [ ] Combine spaCy NER + rule-based
    - [ ] Priority logic:
      - [ ] Use NER if confidence > threshold
      - [ ] Fall back to rules
      - [ ] Merge results intelligently
  - [ ] Conflict resolution:
    - [ ] Handle multiple extractions
    - [ ] Choose best match

- [ ] **Evaluation**
  - [ ] Evaluate NER model:
    - [ ] Per-entity F1 scores
    - [ ] Compare with baseline (rule-based)
  - [ ] End-to-end evaluation:
    - [ ] Test on test set
    - [ ] Compare metrics with Milestone 7

- [ ] **Model Optimization**
  - [ ] Fine-tune hyperparameters
  - [ ] Handle class imbalance
  - [ ] Add data augmentation if needed

### Deliverables
- [ ] `app/models/spacy_ner.py` with NER model
- [ ] `scripts/train_spacy_ner.py` training script
- [ ] `scripts/convert_to_spacy.py` data converter
- [ ] `models/spacy_ner_model/` trained model
- [ ] Updated `parameter_extractor.py` with hybrid approach
- [ ] Evaluation report comparing with baseline

### Acceptance Criteria
- [ ] spaCy NER model trains successfully
- [ ] Model loads and makes predictions
- [ ] Hybrid extraction works correctly
- [ ] Parameter extraction F1 improves over baseline
- [ ] All entity types are recognized
- [ ] Model is saved and loadable

### Dependencies
- Milestone 3 completed (annotated data with slot positions)
- Milestone 7 completed (baseline for comparison)
- spaCy installed
- Training data with entity spans

---

## Milestone 9: Transformer Intent Model (Optional)

### Objectives
- [ ] Fine-tune lightweight transformer for intent classification
- [ ] Improve intent classification accuracy
- [ ] Handle similar intents better
- [ ] Compare with baseline TF-IDF model

### Tasks
- [ ] **Model Selection**
  - [ ] Choose lightweight transformer:
    - [ ] DistilBERT (recommended)
    - [ ] Or BERT-base, RoBERTa
  - [ ] Consider model size vs. performance trade-off

- [ ] **Data Preparation**
  - [ ] Create `scripts/prepare_transformer_data.py`:
    - [ ] Format data for transformer training
    - [ ] Create train/val/test splits
    - [ ] Handle class imbalance

- [ ] **Fine-Tuning Setup**
  - [ ] Create `app/models/transformer_intent.py`:
    - [ ] Load pre-trained model
    - [ ] Add classification head
    - [ ] Configure training parameters
  - [ ] Use HuggingFace Transformers library

- [ ] **Training**
  - [ ] Create `scripts/train_transformer.py`:
    - [ ] Fine-tune on intent classification task
    - [ ] Hyperparameters:
      - [ ] Learning rate (2e-5 typical)
      - [ ] Batch size
      - [ ] Epochs
      - [ ] Weight decay
    - [ ] Save model to `models/transformer_intent_model/`

- [ ] **Evaluation**
  - [ ] Compare with baseline:
    - [ ] Accuracy improvement
    - [ ] Per-intent F1 scores
    - [ ] Confusion matrix comparison
  - [ ] Performance metrics:
    - [ ] Inference time
    - [ ] Model size

- [ ] **Integration**
  - [ ] Update `app/models/intent_classifier.py`:
    - [ ] Support both TF-IDF and transformer models
    - [ ] Model selection via configuration
  - [ ] Update `app/chatbot.py` to use transformer

### Deliverables
- [ ] `app/models/transformer_intent.py`
- [ ] `scripts/train_transformer.py`
- [ ] `models/transformer_intent_model/` trained model
- [ ] Evaluation report comparing with baseline
- [ ] Updated intent classifier with model selection

### Acceptance Criteria
- [ ] Transformer model trains without errors
- [ ] Intent accuracy improves over baseline (>5% improvement target)
- [ ] Model inference time is acceptable (<500ms)
- [ ] Model can be loaded and used in chatbot
- [ ] Better handling of similar intents

### Dependencies
- Milestone 3 completed (annotated data)
- Milestone 7 completed (baseline for comparison)
- HuggingFace Transformers installed
- GPU recommended for training

---

## Milestone 10: Knowledge Grounding

### Objectives
- [ ] Create knowledge base from official AAU content
- [ ] Implement retrieval mechanism
- [ ] Ground chatbot responses in official information
- [ ] Improve response accuracy and relevance

### Tasks
- [ ] **Knowledge Base Creation**
  - [ ] Extract structured information:
    - [ ] FAQ entries from AAU website
    - [ ] Official documents (PDFs, web pages)
    - [ ] Policy documents
    - [ ] Contact information
  - [ ] Create `data/knowledge_base/`:
    - [ ] Store as structured format (JSON, CSV, or vector DB)
    - [ ] Each entry: question, answer, source, metadata

- [ ] **Text Processing**
  - [ ] Create `app/knowledge_processor.py`:
    - [ ] Chunk large documents
    - [ ] Extract key information
    - [ ] Index for retrieval
  - [ ] Format:
    ```json
    {
      "id": "kb_001",
      "intent": "fee_payment",
      "question": "What is the tuition fee?",
      "answer": "The tuition fee for undergraduate students is...",
      "source": "AAU official website",
      "metadata": {"department": "all", "semester": "2024"}
    }
    ```

- [ ] **Retrieval System**
  - [ ] Create `app/retrieval.py`:
    - [ ] Semantic search (using embeddings)
    - [ ] Or keyword-based search (TF-IDF)
    - [ ] Rank results by relevance
  - [ ] Options:
    - [ ] Simple: TF-IDF similarity
    - [ ] Advanced: Sentence transformers (e.g., all-MiniLM-L6-v2)

- [ ] **Response Grounding**
  - [ ] Update `app/response_generator.py`:
    - [ ] Retrieve relevant knowledge base entries
    - [ ] Combine template responses with KB information
    - [ ] Cite sources in responses
  - [ ] Logic:
    - [ ] If KB entry found → use KB answer
    - [ ] If no KB entry → use template
    - [ ] Hybrid: combine both

- [ ] **Knowledge Base Management**
  - [ ] Create `scripts/manage_kb.py`:
    - [ ] Add new entries
    - [ ] Update existing entries
    - [ ] Search and filter
  - [ ] Version control for KB updates

### Deliverables
- [ ] `data/knowledge_base/` with structured KB entries
- [ ] `app/knowledge_processor.py` for processing
- [ ] `app/retrieval.py` for search/retrieval
- [ ] Updated `response_generator.py` with grounding
- [ ] `scripts/manage_kb.py` for KB management
- [ ] Documentation of KB structure

### Acceptance Criteria
- [ ] Knowledge base contains 100+ entries
- [ ] Retrieval finds relevant entries for queries
- [ ] Responses are grounded in KB when available
- [ ] Source citations are included in responses
- [ ] KB can be updated and maintained
- [ ] Retrieval performance is acceptable (<200ms)

### Dependencies
- Milestone 2 completed (scraped data)
- Optional: sentence-transformers for semantic search
- Milestone 5 completed (response generator)

---

## Milestone 11: UI (Optional)

### Objectives
- [ ] Build simple chat interface
- [ ] Demonstrate chatbot functionality
- [ ] Provide user-friendly interaction

### Tasks
- [ ] **UI Framework Selection**
  - [ ] Option A: Streamlit (simplest)
  - [ ] Option B: HTML/JavaScript frontend
  - [ ] Option C: Gradio

- [ ] **Streamlit Implementation** (if chosen)
  - [ ] Create `app/streamlit_ui.py`:
    - [ ] Chat interface with message history
    - [ ] Input field for user messages
    - [ ] Display bot responses
    - [ ] Show conversation state (optional)
    - [ ] Reset conversation button
  - [ ] Run with: `streamlit run app/streamlit_ui.py`

- [ ] **Web Frontend** (if chosen)
  - [ ] Create `frontend/` directory:
    - [ ] HTML/CSS/JavaScript
    - [ ] Connect to FastAPI backend
    - [ ] Real-time chat interface
  - [ ] Features:
    - [ ] Message bubbles
    - [ ] Typing indicators
    - [ ] Error handling
    - [ ] Responsive design

- [ ] **Integration**
  - [ ] Connect UI to FastAPI backend
  - [ ] Handle API calls
  - [ ] Error handling and loading states

- [ ] **Styling**
  - [ ] Modern, clean design
  - [ ] AAU branding (if applicable)
  - [ ] Mobile-responsive

### Deliverables
- [ ] `app/streamlit_ui.py` OR `frontend/` directory
- [ ] Functional chat interface
- [ ] Integration with FastAPI backend
- [ ] User documentation for running UI

### Acceptance Criteria
- [ ] Chat interface is functional
- [ ] Messages are sent and received correctly
- [ ] Conversation history is displayed
- [ ] UI is responsive and user-friendly
- [ ] Errors are handled gracefully
- [ ] Can reset/start new conversation

### Dependencies
- Milestone 6 completed (FastAPI backend)
- Streamlit OR web frontend framework

---

## Milestone 12: Deployment

### Objectives
- [ ] Dockerize the application
- [ ] Prepare for production deployment
- [ ] Ensure reliability and scalability
- [ ] Create deployment documentation

### Tasks
- [ ] **Docker Setup**
  - [ ] Create `Dockerfile`:
    - [ ] Base image (Python 3.10+)
    - [ ] Install dependencies
    - [ ] Copy application code
    - [ ] Set working directory
    - [ ] Expose port
    - [ ] CMD to run uvicorn
  - [ ] Create `docker-compose.yml` (optional):
    - [ ] Application service
    - [ ] Volume mounts
    - [ ] Environment variables

- [ ] **Environment Configuration**
  - [ ] Create `.env.example` with all variables
  - [ ] Document required environment variables
  - [ ] Use environment variables for:
    - [ ] Model paths
    - [ ] API keys
    - [ ] Database connections
    - [ ] Logging levels

- [ ] **Model Management**
  - [ ] Ensure models are included or downloadable
  - [ ] Create `scripts/download_models.py` if models are large
  - [ ] Document model requirements

- [ ] **Production Considerations**
  - [ ] Add logging configuration
  - [ ] Error handling and monitoring
  - [ ] Health checks
  - [ ] Rate limiting (if needed)
  - [ ] Security considerations

- [ ] **Deployment Documentation**
  - [ ] Create `docs/deployment.md`:
    - [ ] Docker build instructions
    - [ ] Environment setup
    - [ ] Running instructions
    - [ ] Troubleshooting guide

- [ ] **Testing Deployment**
  - [ ] Test Docker build locally
  - [ ] Verify all endpoints work
  - [ ] Test model loading
  - [ ] Performance testing

### Deliverables
- [ ] `Dockerfile`
- [ ] `docker-compose.yml` (optional)
- [ ] `.env.example` with all variables
- [ ] `docs/deployment.md` deployment guide
- [ ] `scripts/download_models.py` (if needed)
- [ ] Production-ready configuration

### Acceptance Criteria
- [ ] Docker image builds successfully
- [ ] Application runs in Docker container
- [ ] All endpoints are accessible
- [ ] Models load correctly in container
- [ ] Environment variables are properly configured
- [ ] Deployment documentation is complete
- [ ] Health checks pass

### Dependencies
- All previous milestones completed
- Docker installed
- Understanding of deployment target

---

## Overall Project Completion Checklist

- [ ] All 12 milestones completed
- [ ] Chatbot handles 10-15 intents
- [ ] Multi-turn conversations work
- [ ] Intent classification accuracy > 75%
- [ ] Parameter extraction F1 > 70% per slot
- [ ] FastAPI backend is functional
- [ ] Evaluation metrics documented
- [ ] Code is modular and extensible
- [ ] Documentation is complete
- [ ] Deployment is ready

---

## Notes

- **Dependencies between milestones**: Each milestone builds on previous ones
- **Optional milestones**: Milestone 9 (Transformer) and Milestone 11 (UI) are optional
- **Flexibility**: Adjust targets based on actual performance and requirements
- **Iteration**: Milestones can be iterated upon (e.g., improve models after evaluation)
