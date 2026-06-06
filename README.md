# AI Business Operations Copilot

## Overview

AI Business Operations Copilot is a multi-agent AI platform that combines document intelligence, business analytics, forecasting, dashboarding, and automated report generation into a single application.

The system enables users to upload documents and business datasets, ask natural language questions, generate insights, forecast future performance, and create executive-ready reports using Large Language Models and advanced analytics.

---

## Key Features

### Document Intelligence (RAG)

* Upload PDF, DOCX, TXT documents
* Semantic search using ChromaDB
* Retrieval-Augmented Generation (RAG)
* Filename-aware document retrieval
* Context-aware question answering
* Conversation memory

### Business Analytics

* Upload CSV and Excel datasets
* Revenue analysis
* Product performance analysis
* Customer analysis
* Regional sales analysis
* Trend analysis

### Revenue Forecasting

* Forecast future revenue using Prophet
* Generate forecast charts
* AI-generated business recommendations
* Confidence interval analysis

### Executive Dashboard

* Total Revenue KPI
* Total Orders KPI
* Average Order Value KPI
* Top Product KPI
* Top Customer KPI
* Top Region KPI
* Interactive Plotly visualizations

### Multi-Agent Architecture

* LangGraph Router Agent
* Document QA Agent
* Analytics Agent
* Forecast Agent

### Reporting

* DOCX report generation
* Historical report storage
* Downloadable reports
* Executive summaries

### Persistence

* SQLite chat history
* SQLite report history
* Persistent application state

### Deployment

* Dockerized architecture
* FastAPI backend
* Streamlit frontend

---

## System Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend
 │
 ▼
LangGraph Router
 ├── Document Agent
 ├── Analytics Agent
 └── Forecast Agent
 │
 ├── Gemini LLM
 ├── ChromaDB
 ├── SQLite
 ├── Pandas
 └── Prophet
```

---

## Technology Stack

### AI & LLM

* Google Gemini
* LangGraph
* ChromaDB
* Sentence Transformers

### Backend

* FastAPI
* Python

### Frontend

* Streamlit

### Data Analytics

* Pandas
* NumPy
* Prophet

### Visualization

* Plotly
* Matplotlib

### Database

* SQLite

### Deployment

* Docker
* Docker Compose

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd ai-business-copilot-mvp
```

### Configure Environment

Create `.env`

```env
GEMINI_API_KEY=your_api_key
```

### Run Using Docker

```bash
docker compose up --build
```

Frontend:

```text
http://localhost:8501
```

Backend:

```text
http://localhost:8000/docs
```

---

## Screenshots

### 1. Upload Interface
![Upload Interface](assets/screenshots/1.png)

### 2. Document Q&A
![Document Q&A](assets/screenshots/2.png)

### 3. Business Analytics
![Business Analytics](assets/screenshots/3.png)

### 4. AI Copilot
![AI Copilot](assets/screenshots/4.png)

### 5. Executive Dashboard
![Executive Dashboard](assets/screenshots/5.png)

### 6. Report History
![Report History](assets/screenshots/6.png)

### 7. Generated Report
![Generated Report](assets/screenshots/7.png)

## Project Modules

### 1. Document Intelligence

Upload and analyze business documents using Retrieval-Augmented Generation.

### 2. Analytics Engine

Perform business analysis on uploaded datasets using natural language.

### 3. Forecasting Engine

Predict future revenue trends and generate actionable recommendations.

### 4. Executive Dashboard

Monitor KPIs and business performance using interactive charts.

### 5. Report Generation

Generate downloadable executive reports with charts and insights.

---

## Future Enhancements

* Authentication & User Management
* Multi-user Support
* PostgreSQL Integration
* Cloud Deployment
* Advanced Agent Collaboration
* Automated Scheduled Reports
* Email Report Delivery
* Role-Based Access Control

---

## Author

Safdar Munir

AI Engineer | Machine Learning | Generative AI | LLM Applications
