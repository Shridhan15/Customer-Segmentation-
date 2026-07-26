# Retail Banking AI Agent

An enterprise-grade AI-powered retail banking analytics platform that enables customer segmentation, churn prediction, and intelligent product recommendations through a conversational interface. Built using **LangGraph**, **FastAPI**, **React**, and **Machine Learning**, the platform transforms natural language queries into analytical insights and executive reports.

---

# Overview

The Retail Banking AI Agent is designed to assist banking strategists in analysing customer behaviour using artificial intelligence and data analytics. Users can interact with the system through natural language queries, while the backend automatically orchestrates machine learning workflows to generate customer insights, business recommendations, and interactive visualisations.

---

# Features

- AI-powered conversational analytics
- Customer segmentation using K-Means Clustering
- Customer churn prediction using Random Forest
- Intelligent banking product recommendation engine
- LangGraph-based agent workflow orchestration
- Executive report generation using LLMs
- Interactive analytics dashboard
- Persistent conversation memory
- Real-time visualisations and KPI reporting

---

# System Architecture

```text
                  User Query
                       │
                       ▼
              React Frontend (Vite)
                       │
                 REST API Request
                       │
                       ▼
                 FastAPI Backend
                       │
              LangGraph State Graph
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 Customer        Churn Prediction   Product
Segmentation         Tool       Recommendation
 (K-Means)      (Random Forest)      Engine
        │              │              │
        └──────────────┼──────────────┘
                       ▼
             ChatGroq (Llama-3.1-8B)
                       │
                       ▼
          Executive Report Generation
                       │
                       ▼
             React Dashboard Output
```

---

# Technology Stack

## Backend

- FastAPI
- LangGraph
- ChatGroq (Llama-3.1-8B-Instant)
- Pandas
- Scikit-Learn
- SQLite
- Pydantic

## Frontend

- React
- Vite
- Tailwind CSS
- Recharts
- Axios

## Machine Learning

- K-Means Clustering
- Random Forest Classification
- Rule-Based Product Recommendation Engine

---

# Project Structure

```text
retail-customer-agent/
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── graph.py
│   │   │   ├── nodes.py
│   │   │   ├── product_recommendation_node.py
│   │   │   ├── state.py
│   │   │   └── tools/
│   │   │       ├── churn_tool.py
│   │   │       ├── segmentation_tool.py
│   │   │       └── eda_tool.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── recommendation/
│   │   │   ├── product_catalog.py
│   │   │   ├── recommendation_engine.py
│   │   │   ├── recommendation_tool.py
│   │   │   └── scoring.py
│   │   └── main.py
│   ├── data_store/
│   │   ├── customer_banking_data.csv
│   │   └── generate_data.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatInterface.jsx
    │   │   ├── DashboardView.jsx
    │   │   └── PersonaCard.jsx
    │   ├── services/
    │   │   └── api.js
    │   ├── App.jsx
    │   └── main.jsx
    └── package.json
```

---

# Installation

## Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install the required dependencies.

```bash
pip install -r requirements.txt
```

---

# Configuration

Create a `.env` file inside the backend directory.

```env
GROQ_API_KEY=your_groq_api_key_here
DATASET_PATH=app/data_store/customer_banking_data.csv
```

Generate the synthetic customer dataset.

```bash
python app/data_store/generate_data.py
```

Start the FastAPI server.

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

---

# Frontend Setup

Open a new terminal and navigate to the frontend directory.

```bash
cd frontend
```

Install the required Node.js packages.

```bash
npm install
```

Start the development server.

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

# Running the Application

1. Start the FastAPI backend.
2. Start the React frontend.
3. Open your browser and navigate to:

```text
http://localhost:5173
```

4. Interact with the AI agent using queries such as:

```text
Predict customer churn
```

```text
Segment all customers
```

```text
Recommend banking products
```

```text
Show high-value customers
```

---

# API Documentation

## POST `/api/chat`

Processes conversational requests, executes the LangGraph workflow, invokes the required analytics pipeline, and returns AI-generated insights together with structured analytical data.

### Request

```json
{
  "query": "Predict Churn",
  "thread_id": "optional-thread-id",
  "human_clarification_response": null
}
```

### Response

```json
{
  "thread_id": "uuid-string",
  "needs_human_input": false,
  "clarification_question": null,
  "response_message": "Analysis completed successfully.",
  "agent_reasoning": {
    "detected_intent": "predict_churn",
    "features_used": [
      "avg_monthly_balance",
      "transaction_frequency"
    ],
    "evaluation_metrics": 0.85
  },
  "insights": "# Executive Report",
  "data_payload": {
    "n_clusters": 2,
    "cluster_centers": [],
    "segment_counts": {}
  }
}
```

---

# Workflow

1. User submits a natural language banking query.
2. FastAPI receives the request and forwards it to the LangGraph workflow.
3. ChatGroq identifies the user's intent.
4. LangGraph routes the request to the appropriate analytics node.
5. Machine learning models perform customer segmentation, churn prediction, or product recommendation.
6. Results are processed into structured insights and executive summaries.
7. The React dashboard displays charts, KPIs, reports, and customer personas.

---

# Future Enhancements

- Deep learning-based churn prediction
- Explainable AI using SHAP and LIME
- Customer lifetime value prediction
- Real-time transaction analytics
- Docker containerisation
- Kubernetes deployment
- CI/CD pipeline integration
- Cloud deployment on AWS, Azure, or Google Cloud
- Role-based authentication and authorisation
- Multi-language conversational support

---

# Built With

- LangGraph
- FastAPI
- React
- Tailwind CSS
- Scikit-Learn
- Pandas
- ChatGroq (Llama-3.1-8B-Instant)
- Recharts
- SQLite

---

# License

This project is intended for educational and research purposes. Modify and extend the platform according to your requirements.