import asyncio
import asyncpg

from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

async def execute_sql(query):
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )
    try:
        result = await conn.fetch(query)
        return [dict(record) for record in result]
    except Exception as e:
        return f"Error executing SQL: {str(e)}"
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main(query="SELECT * FROM customers;"))
