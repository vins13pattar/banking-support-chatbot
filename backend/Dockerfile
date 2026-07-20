FROM langchain/langgraph-api:latest

# Copy backend source
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -e /app

WORKDIR /app
