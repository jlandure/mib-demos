
# Use the official Python image.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt fastapi uvicorn python-multipart

# Copy code
COPY agent.py .
COPY simple_server.py .

# Copy data directory (Important!)
# We assume the build runs from the bodysafety folder
# You may need to copy the data before the build if they live elsewhere
COPY data/ data/

CMD ["python", "simple_server.py"]
