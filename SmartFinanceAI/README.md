# SmartFinanceAI

AI Chatbot microservice cho hệ thống quản lý tài chính cá nhân SmartFinance.

## Kiến trúc

```
SmartFinanceBE (Backend chính)  ──HTTP──▶  SmartFinanceAI (AI Service)
     Port 3001                                    Port 5000
     MySQL DB ◀──────── read-only ────────────────┘
```

## Tech Stack
- **Framework**: FastAPI (Python)
- **LLM**: Ollama (Qwen 2.5 7B) - chạy local
- **Vector DB**: ChromaDB
- **Embeddings**: SentenceTransformers (multilingual)
- **Pipeline**: LangChain

## Cài đặt

```bash
# 1. Clone repo
git clone <repo-url>
cd SmartFinanceAI

# 2. Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux
# venv\Scripts\activate   # Windows

# 3. Cài dependencies
pip install -r requirements.txt

# 4. Copy .env
cp .env.example .env
# Chỉnh sửa DATABASE_URL và OLLAMA_BASE_URL

# 5. Cài Ollama & pull model
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull qwen2.5:7b

# 6. Chạy server
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/ai/chat` | Gửi tin nhắn, nhận AI response |
| GET | `/api/ai/chat/sessions` | Danh sách phiên hội thoại |
| GET | `/api/ai/chat/sessions/{id}` | Lịch sử 1 phiên |
| DELETE | `/api/ai/chat/sessions/{id}` | Xóa phiên |
| POST | `/api/ai/embeddings/sync` | Đồng bộ embeddings giao dịch |
| GET | `/api/ai/health` | Health check |

## Giao tiếp với Backend

Backend gọi AI service qua HTTP với header `X-API-Key` để xác thực service-to-service:

```bash
curl -X POST http://localhost:5000/api/ai/chat \
  -H "X-API-Key: <AI_SERVICE_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "uuid", "message": "Tháng này tôi chi bao nhiêu?"}'
```
