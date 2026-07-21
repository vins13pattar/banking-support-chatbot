.PHONY: start stop restart logs clean setup seed

# Start all services (Database, Admin Dashboard, Customer Chat, FastAPI Backend, and LangGraph Server)
start:
	@echo "Starting Docker Compose services (Postgres, FastAPI, Admin Dashboard, Customer Chat)..."
	docker-compose up -d
	@echo "Starting LangGraph Agent Server in development mode..."
	cd backend && . .venv/bin/activate && langgraph dev

# Stop all services
stop:
	@echo "Stopping Docker Compose services..."
	docker-compose down
	@echo "Note: Stop the LangGraph server by pressing Ctrl+C in the terminal where it is running."

# Restart all services
restart: stop start

# View logs for docker services
logs:
	docker-compose logs -f

# Clean up docker volumes (WARNING: deletes database data)
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
