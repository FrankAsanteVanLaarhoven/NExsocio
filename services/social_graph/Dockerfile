FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
COPY libs/nexus-common /app/libs/nexus-common
COPY services/social_graph /app/services/social_graph
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app/services:/app/libs/nexus-common
EXPOSE 8002
CMD ["python", "-m", "uvicorn", "services.social_graph.api.main:app", "--host", "0.0.0.0", "--port", "8002"]