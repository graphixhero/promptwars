# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file first for layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port (GCP Cloud Run defaults to 8080)
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
