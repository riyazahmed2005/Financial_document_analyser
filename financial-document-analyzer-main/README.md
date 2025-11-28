


# 🚀 Financial Document Analyzer – A Debugging & Refactoring Journey

## Project Overview

This project is an AI-powered **financial document analysis tool** built with **CrewAI** and **FastAPI**. It accepts a PDF financial report, processes it with a team of AI agents running on a local LLM, and provides a comprehensive analysis.

This repository documents the end-to-end process of taking a deliberately broken application and transforming it into a robust, functional tool. The journey involved fixing core application logic, resolving complex dependency conflicts, configuring system-level environments, and implementing advanced features like background processing and database persistence for a complete **MVP (Minimum Viable Product)** architecture.

---

## ✨ Key Features

- 🧠 **AI-Powered Analysis:** Leverages a multi-agent system (CrewAI) to perform in-depth analysis of PDF financial reports.  
- ⚡ **Asynchronous API:** Uses FastAPI's `BackgroundTasks` for a non-blocking user experience, immediately returning a `job_id` while processing happens in the background.  
- 💾 **Database Persistence:** Implements a SQLite database to track job status and store final analysis results, which can be retrieved at any time.  
- 💻 **Local LLM Integration:** Powered by Ollama (`Llama 3`) for privacy, cost-effectiveness, and to eliminate external API key dependencies.  

---

## 🏛️ System Architecture

The application follows an asynchronous worker model. The user interacts with a FastAPI server, which offloads the heavy AI processing to a background task and stores the result in a database.
```bash
[User] --(1. Upload PDF)--> [FastAPI Server] --(2. Returns Job ID Instantly)--> [User]
     |
     '--(6. Check Status w/ Job ID)--> [FastAPI Server] --(3. Dispatches Background Task)--> [CrewAI Worker] --> [AI Agents] --(4. Analyze Document)--> [AI Agents] --(5. Stores Result)--> [SQLite DB]
```


---

## 🚀 Getting Started & Setup Instructions

Follow these steps to set up and run the project on a Windows machine.

### 1. Prerequisites
- [Git](https://git-scm.com/downloads)  
- [Python 3.10+](https://www.python.org/downloads/)  
- [Ollama](https://ollama.com)  

### 2. Clone the Repository
```bash
git clone [https://github.com/YourUsername/financial-document-analyzer.git](https://github.com/YourUsername/financial-document-analyzer.git)
cd financial-document-analyzer

(Remember to replace YourUsername with your actual GitHub username.)

```
### 3. Set Up Dependencies
```bash

Local LLM (Ollama): Once Ollama is installed, pull the Llama 3 model:

ollama pull llama3
```

Python Environment: Create and activate a virtual environment using Command Prompt (CMD):
```bash
python -m venv .venv
.venv\Scripts\activate
```

###Install Python Packages:
```bash
pip install -r requirements.txt
```

System-Level Dependencies:

NLTK Data: Run the helper script to download the 'punkt' data package:

```bash
python download_nltk.py
```


Poppler Utility: Download the Poppler binary from this link and extract it to C:\poppler. The application is hardcoded to find it there.

### 4. Run the Application

Start Ollama: In a separate terminal, ensure the Ollama model is running:
```bash
ollama run llama3
```

Start the FastAPI Server: In your original Command Prompt (with .venv activated), run:
```bash

python main.py
```


The server will be live at http://127.0.0.1:8000
.

### 📄 API Documentation

For full interactive documentation, run the application and visit http://127.0.0.1:8000/docs
.

POST /analyze
Kicks off a new analysis job asynchronously.

Request Body: multipart/form-data with a file (PDF) and optional query (string).

Success Response: 202 Accepted with a job_id.
```bash
{ "message": "Analysis has been started.", "job_id": "unique-id-string" }
```


GET /results/{job_id}
Checks the status and retrieves the result of an analysis job.

Path Parameter: The job_id from the /analyze response.

Success Response: 200 OK with the job status and the final analysis once completed.
```bash
{ "job_id": "unique-id-string", "status": "completed", "result": "The full text of the financial analysis..." }

```
### 🐞 The Debugging Journey: From Bug to Feature

### This section details the methodical process of identifying and resolving the application's issues.

 ### Phase 1: Core Application Logic

Bug: Missing LLM Initialization
Symptom: Application crashed on startup with a NameError for the 'llm' variable.
Diagnosis: The AI agents were declared without an underlying language model.
Solution: Implemented a local LLM using Ollama to provide intelligence to the agents.

Bug: Incorrect Tool Definition
Symptom: The agent failed with a KeyError: 'tools' during validation.
Diagnosis: A custom tool was passed as a class method, not a valid Tool object.
Solution: Refactored the tool using the @tool decorator from crewai_tools to ensure proper parsing by the agent framework.

### Phase 2: Environment & Dependency Management

Bug: Widespread Dependency Conflicts ("Dependency Hell")
Symptom: The application failed to install or crashed on startup with various errors (ResolutionImpossible, AttributeError, ImportError).
Diagnosis: Multiple library conflicts were identified: crewai vs. python-dotenv, chromadb vs. NumPy 2.0, and unstructured vs. pdfminer.six.
Solution: Systematically resolved each conflict by pinning specific, stable versions of the problematic libraries (e.g., numpy==1.26.4, pdfminer.six==20221105) in requirements.txt.

### Phase 3: LLM Integration & Optimization

Bug: Ineffective Tool Usage by LLM
Symptom: The llama2 agent understood what to do but failed to format its tool-use commands correctly, causing an infinite loop.
Diagnosis: The chosen LLM lacked sufficient "function calling" capabilities for reliable agentic work.
Solution: Upgraded the model to Llama 3, which has superior instruction-following and formatting abilities, completely resolving the reliability issue.

### Phase 4: System-Level Configuration

Bug: Missing System Dependencies
Symptom: The PDF reader tool failed with Resource not found and Is poppler installed and in PATH? errors.
Diagnosis: The environment was missing the NLTK 'punkt' data package and the Poppler system binary.
Solution: Created a script to download the NLTK package and manually installed Poppler, adding its path to the system environment to ensure the application could find it.

### 📂 Project Structure
```bash
├── .venv/              # Virtual environment files (ignored by Git)
├── data/               # Sample PDF documents
├── .gitignore          # Specifies files for Git to ignore
├── README.md           # This file
├── agents.py           # Defines the CrewAI agents (Analyst, Advisor)
├── database.py         # Handles SQLite database setup and operations
├── main.py             # FastAPI application, API endpoints, and background tasks
├── requirements.txt    # List of Python dependencies
├── task.py             # Defines the tasks for the CrewAI agents
└── tools.py            # Custom tools for the agents (e.g., PDF reader)

```

