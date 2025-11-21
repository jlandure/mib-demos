
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
# On suppose que le build se fait depuis le dossier bodysafety
# Il faudra peut-être copier les données avant le build si elles sont ailleurs
COPY data/ data/

CMD ["python", "simple_server.py"]
