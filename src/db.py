import asyncio
import asyncpg

from src.config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

async def execute_sql(query):
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )
    result = await conn.fetch(query)
    await conn.close()
    return [dict(record) for record in result]

if __name__ == "__main__":
    res = asyncio.run(execute_sql(query="SELECT * FROM customers LIMIT 1;"))
    print(res)