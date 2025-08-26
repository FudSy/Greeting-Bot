import asyncio
import aiomysql
import config

async def insert_user(userid, user_name, user_greeting):
    db_config = config.db_config

    conn = await aiomysql.connect(**db_config)
    async with conn.cursor() as cur:
        await cur.execute("INSERT INTO greetings (userid, user_name, user_greeting) VALUES (%s, %s, %s)", (userid, user_name, user_greeting))
        await conn.commit()

    conn.close()

