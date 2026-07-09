# Identity & Verification Service

Bounded context for ZKP age verification, user registration, and mode selection.

## Local Run

```bash
cd services/identity
pip install -e ../../libs/nexus-common -e .
uvicorn services.identity.api.main:app --reload --port 8001
```

## API Endpoints

- `POST /api/v1/auth/register` - Register with ZKP age proof
- `POST /api/v1/auth/mode` - Select Kids/Prime/Professional mode
- `GET /api/v1/users/me` - Current user profile
- `POST /api/v1/zkp/stub-proof` - Generate stub proof (dev only)