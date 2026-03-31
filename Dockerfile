# Use slim Python image for production container
FROM python:3.12-slim

# Avoid buffering to make logs show in real time
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first for layer cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . ./

# Health check basic command (optional)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s CMD python -m pytest -q > /dev/null 2>&1 || exit 1

# Default command for container
CMD ["python", "app.py"]
