# Banking Support Chatbot 🏦

A modern, multi-agent banking support chatbot built with LangGraph, LangChain, FastAPI, and React. 
This system uses a Supervisor agent to route customer requests to specialised domain agents, and implements a Human-in-the-Loop (HITL) workflow for sensitive operations like blocking cards or processing disputes.

## Architecture 🏗️

The system is split into multiple parts:
1. **LangGraph Agent Server**: Runs the multi-agent graph (Supervisor, Auth, FAQ, Account, Transaction, Card, Compliance, Response, HITL).
2. **FastAPI Backend**: Provides custom endpoints for the Admin Dashboard (approvals, tickets, audit).
3. **Admin Dashboard (Vite + React)**: A portal for human agents to review pending approvals and support tickets.
4. **Customer Chat UI**: Uses `langchain-ai/agent-chat-ui` (Next.js) for the customer-facing chat experience.
5. **PostgreSQL**: Stores application data (Customers, Accounts, Transactions, Tickets, Approvals, Knowledge Base) and LangGraph state.

## Prerequisites 📋

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose
- OpenAI API Key
- LangSmith API Key (for observability)

## Getting Started 🚀

### 1. Environment Setup

Copy the example environment file and fill in your keys:
```bash
cp .env.example .env
```

Edit `.env` and add your `OPENAI_API_KEY` and `LANGSMITH_API_KEY`.

### 2. Infrastructure & Database

Initialize the Python environment and run the database migrations and seed scripts:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .

# Start ONLY the postgres database first
docker-compose up -d postgres

# Run Alembic migrations to create tables
alembic upgrade head

# Seed the database with mock data
python src/database/run_seed.py
```

### 3. Start the Agent Server

Run the LangGraph Agent Server in development mode:
```bash
# From the backend directory
langgraph dev
```
The agent server will start at `http://localhost:2024`.

### 4. Start the Full Application Stack

Once the database is seeded and the LangGraph server is running, you can start the rest of the application stack (FastAPI Backend, Admin Dashboard, and Customer Chat) using Docker Compose:

```bash
# From the project root directory
docker-compose up -d
```

This will spin up:
- **FastAPI Backend** on `http://localhost:8000`
- **Admin Dashboard** on `http://localhost:5173`
- **Customer Chat UI** on `http://localhost:3000`
- **pgAdmin** on `http://localhost:5050`

## Testing the System 🧪

### Authentication Flow
To test authenticated features (accounts, transactions, cards), use these mock credentials from the seed data:
- **Customer Number**: `CUST-1001`
- **Date of Birth**: `1990-05-15`
- **Phone**: `8901` (Last 4 digits)

### Human-in-the-Loop (HITL) Flow
1. Ask the chatbot to "block my debit card because I lost it".
2. The agent will propose the action and route it to Compliance.
3. Compliance will assess the risk and pause the graph, sending an approval request.
4. Open the Admin Dashboard at `http://localhost:5173`.
5. You will see the pending approval. Click **Approve**.
6. The graph will resume, the action will execute, and the chatbot will notify you it is done.

## Project Structure 📁

- `/backend/src/agents`: LangGraph node implementations
- `/backend/src/graphs`: State schemas and main graph wiring
- `/backend/src/tools`: Tools used by the agents
- `/backend/src/services`: Business logic and database access
- `/backend/src/models`: SQLModel definitions
- `/backend/src/api`: FastAPI custom routes
- `/frontend/admin-dashboard`: React Vite application
- `/frontend/customer-chat`: Next.js LangGraph chat UI

## Observability 📊
All agent executions are traced in [LangSmith](https://smith.langchain.com/). Check your LangSmith dashboard to inspect traces, routing decisions, and tool executions.
