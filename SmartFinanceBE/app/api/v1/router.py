from fastapi import APIRouter

from app.api.v1 import auth, users, accounts, transactions, budgets, investments, chat

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(investments.router, prefix="/investments", tags=["investments"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

