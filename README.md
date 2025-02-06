# Cahier des Charges: Automated Information Extraction System

## 1. *Project Overview*
### 1.1 *Objective*
The goal of this project is to develop an automated system for extracting structured information from unstructured documents using a fine-tuned LLM. Unlike pre-trained LLMs, we will fine-tune a model such as Ollama to tailor it to our specific document types and extraction needs. The system will handle tasks such as OCR processing, data parsing, entity recognition, and structured output generation.

### 1.2 *Scope*
- Extract relevant data (e.g., names, dates, contract terms) from scanned documents, PDFs, and images.
- Use OCR for text recognition and an LLM for contextual understanding.
- Implement a fine-tuning process for domain-specific adaptation.
- Provide structured output (JSON, CSV, or database insertion).
- Ensure accuracy and robustness across various document formats.
- Develop a user-friendly front-end for document upload and data visualization.
- Implement filtering options for extracted data based on location, date, etc.
- Optionally integrate an interview scheduling feature via call or email

## 2. *Technical Specifications*
### 2.1 *Hardware Requirements*
- *Development Machine:* Minimum 8GB RAM, Intel i5 11th Gen, Intel Xe GPU (limited local training, recommended cloud-based fine-tuning).
- *Virtual Machine (VM) Specs:*
  - Ubuntu 22.04
  - 4GB RAM allocated
  - 2 CPU cores
  - 50GB storage
- *Cloud Resources (if needed):*
  - GPU-accelerated instances (e.g., NVIDIA A100, RTX 3090) for fine-tuning.

### 2.2 *Software Requirements*
- *Operating System:* Ubuntu 22.04 (VM or dedicated machine)
- *Programming Language:* Python
- *Libraries & Frameworks:*
  - OCR: Tesseract, EasyOCR
  - LLM: Ollama, PyTorch, Hugging Face Transformers
  - Data Processing: Pandas, NLTK, SpaCy
  - Model Fine-Tuning: LoRA (Low-Rank Adaptation), PEFT (Parameter-Efficient Fine-Tuning)
  - API Deployment: FastAPI, Flask
  - Front-End: React, Vue.js, or a similar framework 

## 3. *Functional Requirements*
### 3.1 *Core Functionalities*
- *OCR Processing:*
  - Extract raw text from scanned documents.
  - Preprocessing (noise reduction, binarization, text alignment).
- *LLM-Based Information Extraction:*
  - Identify key entities (names, dates, amounts, clauses, etc.).
  - Understand context and relationships.
  - Output structured data in JSON or database format.
- *Fine-Tuning Pipeline:*
  - Use a labeled dataset for supervised fine-tuning.
  - Implement continuous learning for model improvement.
- *User Interface:*
  - Web-based UI for document upload (image or PDF).
  - Display extracted information (e.g., enterprise name, email, phone number).
  - Filtering options based on location, date, etc.
  - Optional feature for interview scheduling via call or email.
- *API for External Integration:*
  - RESTful API for seamless integration with other systems.

## 4. *Non-Functional Requirements*
- *Accuracy:* Ensure high precision and recall in extraction.
- *Performance:* Process documents efficiently (target ❤ seconds per page).
- *Scalability:* Capable of handling large document batches.

## 5. *Project Timeline & Milestones*
| Phase         | Tasks                                           | Duration  |
|--------------|---------------------------------|------------|
| *Phase 1* | Research & Initial Setup         | 2 weeks    |
| *Phase 2* | OCR Implementation & Testing    | 2 weeks    |
| *Phase 3* | LLM Fine-Tuning & Optimization   | 4 weeks    |
| *Phase 4* | API & UI Development & Integration   | 4 weeks    |
| *Phase 5* | Testing, Deployment & Refinement  | 3 weeks    |

## 6. *Risk & Mitigation Strategies*
- *Hardware Limitations:* Use cloud resources for training.
- *OCR Errors:* Improve preprocessing and use better models.
- *Data Biases:* Ensure diverse and well-labeled training data.
- *Performance Issues:* Optimize model size and use quantization techniques.

## 7. *Logging and Performance Monitoring*
- *Logging Mechanism:*
  - Implement structured logging with log levels (INFO, DEBUG, ERROR).
  
- *Performance Metrics:*
  - Track document processing time (OCR + LLM inference).
  - Monitor system resource usage (CPU, RAM, GPU if applicable).


## 8. *Budget & Resources*
- *Local Machine Costs:* Included
- *Cloud Training Costs:* Based on GPU usage
- *Software Costs:* Open-source tools, potential API hosting fees
- *Front-End Development Costs:* Open-source but may require UI framework setup

## 9. *Conclusion*
This project aims to create a robust system for automated document processing using a fine-tuned LLM. By combining OCR and contextual AI, we ensure high accuracy and efficiency in information extraction. The system will feature a user-friendly web interface, filtering capabilities, and an optional interview scheduling function. The final solution will be scalable and adaptable to various document types.
