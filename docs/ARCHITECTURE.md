# Architecture

AI Business Operations Copilot is organized as a service-backed AI workflow: Streamlit handles the user experience, FastAPI exposes application endpoints, and specialist backend modules handle document intelligence, analytics, forecasting, persistence, and reporting.

## High-Level Flow

```mermaid
flowchart LR
    User["Business user"] --> Streamlit["Streamlit UI"]
    Streamlit --> FastAPI["FastAPI service"]
    FastAPI --> Router["LangGraph router"]
    Router --> RAG["Document QA / RAG"]
    Router --> Analytics["Business analytics"]
    Router --> Forecast["Revenue forecasting"]
    FastAPI --> Reports["DOCX reports"]
    FastAPI --> History["SQLite history"]
```

## Data And Document Flow

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Streamlit
    participant API as FastAPI
    participant Store as ChromaDB
    participant LLM as Gemini
    participant DB as SQLite

    U->>UI: Upload PDF/DOCX/TXT
    UI->>API: POST /upload
    API->>API: Extract and chunk text
    API->>Store: Save embeddings with filename metadata
    U->>UI: Ask document question
    UI->>API: POST /ask or /copilot
    API->>Store: Retrieve relevant chunks
    API->>LLM: Generate grounded answer
    API->>DB: Save chat history
    API-->>UI: Answer and sources
```

## Analytics And Forecasting Flow

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Streamlit
    participant API as FastAPI
    participant Agent as Analytics Agent
    participant LLM as Gemini
    participant Reports as Report Generator

    U->>UI: Upload CSV/XLSX
    UI->>API: POST /upload
    U->>UI: Ask analytics or forecast question
    UI->>API: POST /analyze or /copilot
    API->>Agent: Load dataset and classify analysis
    Agent->>Agent: Calculate table, KPI, chart, or forecast
    Agent->>LLM: Generate business recommendation from calculated results
    API-->>UI: Table, chart, insight
    U->>UI: Generate report
    UI->>API: POST /generate-report
    API->>Reports: Build DOCX report
    API-->>UI: Download link
```

## Agent Responsibilities

| Component | Responsibility |
| --- | --- |
| `RouterAgent` | Classifies questions and routes to document QA, analytics, or forecasting |
| `RAGPipeline` | Retrieves relevant document chunks and asks Gemini for grounded answers |
| `AnalyticsAgent` | Loads CSV/XLSX data, calculates business metrics, builds charts, and creates recommendations |
| `ReportGenerator` | Converts analysis output into downloadable DOCX executive reports |
| `database.py` | Stores chat history and report history in SQLite |

## Production Notes

- Uploaded files, generated charts, generated reports, and SQLite data are runtime artifacts and should be persisted with a mounted volume in production.
- The current MVP uses filename-based selection. A production version should add user-scoped file IDs and authentication.
- LLM output is used for interpretation and narrative recommendations, while numeric calculations are handled with Pandas and Prophet.
- For a public hosted deployment, add CORS controls, authentication, rate limiting, and secret management.
