# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY autonomous-gpt-middleware/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY autonomous-gpt-middleware/ .

# Expose the API port
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "relay_api:app", "--host", "0.0.0.0", "--port", "8000"]
