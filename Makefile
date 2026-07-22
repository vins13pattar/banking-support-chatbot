.PHONY: start stop restart logs logs-server dev build-server clean setup seed

# Start the full stack, including the LangGraph server with Postgres-backed
# thread persistence (Postgres, Redis, LangGraph API, FastAPI, dashboards).
# --build ensures the langgraph-api image is (re)built from backend/Dockerfile.langgraph.
start:
	@echo "Building & starting all services (Postgres, Redis, LangGraph server w/ Postgres persistence, FastAPI, dashboards)..."
	docker-compose up -d --build
	@echo ""
	@echo "  LangGraph server : http://localhost:2024  (threads persisted in Postgres)"
	@echo "  FastAPI backend  : http://localhost:8000"
	@echo "  Customer chat    : http://localhost:3000"
	@echo "  Admin dashboard  : http://localhost:5173"

# Lightweight alternative: run the LangGraph server in dev mode (in-memory
# pickle store, no Postgres persistence). Brings up only the app Postgres.
dev:
	@echo "Starting app Postgres..."
	docker-compose up -d postgres
	@echo "Starting LangGraph Agent Server in dev mode (ephemeral in-memory threads)..."
	cd backend && . .venv/bin/activate && langgraph dev

# Stop all services
stop:
	@echo "Stopping Docker Compose services..."
	docker-compose down

# Restart all services
restart: stop start

# View logs for all docker services
logs:
	docker-compose logs -f

# Tail just the LangGraph server logs
logs-server:
	docker-compose logs -f langgraph-api

# Rebuild only the LangGraph server image
build-server:
	docker-compose build langgraph-api

# Clean up docker volumes (WARNING: deletes database data, incl. persisted threads)
clean:
	docker-compose down -v
	@echo "Cleaned up Docker containers and volumes."

# Setup the python environment
setup:
	@echo "Setting up backend environment..."
	cd backend && python3 -m venv .venv
	cd backend && . .venv/bin/activate && pip install -e .
	@echo "Setup complete. Don't forget to run 'make seed' to initialize the database."

# Run database migrations and seed
seed:
	@echo "Starting Postgres..."
	docker-compose up -d postgres
	@echo "Waiting for Postgres to be ready..."
	sleep 3
	@echo "Running migrations and seeding data..."
	cd backend && . .venv/bin/activate && alembic upgrade head && python src/database/run_seed.py
	@echo "Database seeded successfully!"
