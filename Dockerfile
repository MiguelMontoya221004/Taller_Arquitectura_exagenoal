FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY .env.example .env

RUN mkdir -p data

EXPOSE 8000

CMD ["uvicorn", "src.awesome_agent_api.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]