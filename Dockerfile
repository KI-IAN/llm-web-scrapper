# Use official Python base image
FROM python:3.10-slim-bookworm

# Set working directory
WORKDIR /app

# Upgrade system packages to patch vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Gradio default port
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
