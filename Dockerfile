# Use official Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# Expose the API port
EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "relay_api:app", "--host", "0.0.0.0", "--port", "8000"]

