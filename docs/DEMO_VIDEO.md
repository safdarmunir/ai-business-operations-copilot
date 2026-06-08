# Demo Video Guide

Use this as a short recording plan for a Loom, YouTube, or LinkedIn demo. Keep the video around 90 seconds so recruiters and hiring managers can understand the project quickly.

## Recommended Title

AI Business Operations Copilot: RAG, Analytics, Forecasting, Dashboards, and Reports

## 90-Second Script

### 0:00-0:10 - Project Summary

"This is an AI Business Operations Copilot. It helps a business user upload documents and sales data, ask natural language questions, generate forecasts, view dashboards, and create executive-ready reports."

### 0:10-0:25 - Upload And Document QA

Show the upload tab. Upload or select a PDF/DOCX/TXT file.

Say:

"For documents, the backend extracts text, chunks it, stores embeddings in ChromaDB, and uses Gemini to answer with retrieved context."

Ask:

```text
Summarize the key points from this document.
```

### 0:25-0:45 - Business Analytics

Upload or select `dummy_sales.csv`.

Ask:

```text
Which products generate the highest revenue?
```

Say:

"For business data, the app uses Pandas for the calculations and the LLM for the executive-style interpretation."

### 0:45-1:00 - Forecasting

Ask:

```text
Forecast the next 3 months of revenue.
```

Say:

"Forecasting is routed to a forecasting workflow powered by Prophet, then the app returns a table, chart, and recommendation."

### 1:00-1:15 - Dashboard

Open the dashboard tab and show revenue KPIs, top product, top customer, top region, and charts.

Say:

"The dashboard turns the uploaded dataset into business KPIs and visual summaries."

### 1:15-1:30 - Report Generation

Generate a DOCX report and show the download.

Say:

"The final output is not just a chat response. The copilot can generate a downloadable executive report with the analysis, chart, and recommendations."

## Recording Checklist

- Start with the app already running.
- Keep the browser zoom at 100 percent.
- Use one document and one sales CSV.
- Show the architecture diagram from the README for 3-5 seconds.
- End on the generated report or dashboard.
- Add the video link to the README demo table after uploading.

## Suggested LinkedIn Caption

I built an AI Business Operations Copilot that combines document RAG, business analytics, revenue forecasting, dashboards, and DOCX report generation in one workflow.

The project uses FastAPI, Streamlit, LangGraph, Gemini, ChromaDB, Pandas, Prophet, Plotly, SQLite, and Docker Compose.

What makes it more than a chatbot: the LLM handles language and recommendations, while deterministic tools handle calculations, forecasting, persistence, and reports.
