# Use the official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirement list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose fastAPI port
EXPOSE 8000

# Run database migrations & start the FastAPI application
CMD ["sh", "-c", "alembic upgrade head && uvicorn scripts.main:app --host 0.0.0.0 --port 8000"]
