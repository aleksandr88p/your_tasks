from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "database_url": os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./your_tasks.db"),
}
