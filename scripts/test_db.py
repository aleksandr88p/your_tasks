"""Проверка подключения к БД. Запуск: python scripts/test_db.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from app.core.database import AsyncSessionLocal
from sqlalchemy import text


async def check_connection():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        row = result.scalar()
        print("OK: SELECT 1 вернул", row)


if __name__ == "__main__":
    asyncio.run(check_connection())
