FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
COPY libs/nexus-common /app/libs/nexus-common
COPY services/professional /app/services/professional
RUN pip install --no-cache-dir -r requirements.txt httpx
ENV PYTHONPATH=/app/services:/app/libs/nexus-common
EXPOSE 8004
CMD ["python", "-m", "uvicorn", "services.professional.api.main:app", "--host", "0.0.0.0", "--port", "8004"]