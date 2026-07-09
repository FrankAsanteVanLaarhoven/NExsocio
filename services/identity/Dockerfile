FROM python:3.11-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir hatchling
COPY libs/nexus-common /app/libs/nexus-common
COPY services/identity /app/services/identity
WORKDIR /app/services/identity
RUN pip install --no-cache-dir .

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY libs/nexus-common /app/libs/nexus-common
COPY services/identity /app/services/identity
ENV PYTHONPATH=/app/services:/app/libs/nexus-common
EXPOSE 8001
CMD ["python", "-m", "uvicorn", "services.identity.api.main:app", "--host", "0.0.0.0", "--port", "8001"]