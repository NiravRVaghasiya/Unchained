# HuggingFace Spaces Dockerfile
# Deploy: push this folder to a HF Space with "Docker" SDK
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY ../../../unchained.py /app/unchained.py
COPY ../ /app/pickmystack/
COPY . /app/

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run
ENTRYPOINT ["streamlit", "run", "app_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
