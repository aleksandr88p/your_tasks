"""Создание таблиц в БД. Запуск: python scripts/create_tables.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from app.core.database import engine
from app.models import Base


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("OK: Таблицы созданы (users, tasks, timelogs)")


if __name__ == "__main__":
    asyncio.run(create_tables())
