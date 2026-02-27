# Hướng dẫn tích hợp SmartFinanceAI vào SmartFinanceBE

## Kiến trúc tổng quan

```
[User] → [React FE :3000] → [SmartFinanceBE :3001] ──HTTP──▶ [SmartFinanceAI :5000]
                                    │                               │
                                    └──────── MySQL DB ─────────────┘
```

- **SmartFinanceBE** xác thực user bằng JWT → lấy `user_id`
- **SmartFinanceBE** gọi **SmartFinanceAI** qua HTTP, truyền `user_id` + `message`
- **SmartFinanceAI** xác thực request bằng header `X-API-Key`

## Cài đặt trên Backend (SmartFinanceBE)

### 1. Thêm config vào `.env`

```env
AI_SERVICE_URL=http://localhost:5000
AI_SERVICE_API_KEY=smartfinance-ai-secret-key-change-in-production
```

### 2. Tạo endpoint proxy trong SmartFinanceBE

Thêm file `app/api/v1/chat.py`:

```python
import httpx
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.core.config import settings

router = APIRouter()

@router.post("")
async def send_message(body: dict, current_user = Depends(get_current_user)):
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{settings.AI_SERVICE_URL}/api/ai/chat",
            json={
                "user_id": current_user.id,
                "message": body["message"],
                "session_id": body.get("session_id"),
            },
            headers={"X-API-Key": settings.AI_SERVICE_API_KEY},
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.json())
    return resp.json()

@router.get("/sessions")
async def list_sessions(current_user = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.AI_SERVICE_URL}/api/ai/chat/sessions/{current_user.id}",
            headers={"X-API-Key": settings.AI_SERVICE_API_KEY},
        )
    return resp.json()

@router.get("/health")
async def ai_health():
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(f"{settings.AI_SERVICE_URL}/api/ai/health")
    return resp.json()
```

### 3. Đăng ký router

Trong `app/api/v1/router.py`:
```python
from app.api.v1 import chat
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
```

## API Reference (SmartFinanceAI)

Tất cả endpoint đều cần header: `X-API-Key: <AI_SERVICE_API_KEY>`

| Method | Endpoint | Body | Response |
|--------|----------|------|----------|
| POST | `/api/ai/chat` | `{user_id, message, session_id?}` | `{message, session_id, intent}` |
| GET | `/api/ai/chat/sessions/{user_id}` | - | `[{session_id, title, created_at, message_count}]` |
| GET | `/api/ai/chat/sessions/{user_id}/{session_id}` | - | `[{id, role, content, created_at}]` |
| DELETE | `/api/ai/chat/sessions/{user_id}/{session_id}` | - | `{message, deleted_count}` |
| POST | `/api/ai/embeddings/sync` | `{user_id}` | `{message, count}` |
| GET | `/api/ai/health` | - | `{service, status, ollama}` |

## Database

SmartFinanceAI cần đọc các bảng:
- `users` (read-only)
- `accounts` (read-only)
- `transactions` (read-only)
- `categories` (read-only)
- `budgets` (read-only)
- `chat_histories` (read-write, AI tự quản lý)

Backend cần tạo bảng `chat_histories` bằng migration đã cung cấp.
