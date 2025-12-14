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

async def mark_as_read(greetingid):
    db_config = config.db_config

    conn = await aiomysql.connect(**db_config)
    async with conn.cursor() as cur:
        await cur.execute("UPDATE greetings SET read = true WHERE greetingid = %s", greetingid)
        await conn.commit()

    conn.close()

async def delete_row(greetingid):
    db_config = config.db_config

    conn = await aiomysql.connect(**db_config)
    async with conn.cursor() as cur:
        await cur.execute("DELETE FROM gretings WHERE greetingid = %s", greetingid)
        await conn.commit()

    conn.close()

async def select_unreaded(index):
    db_config = config.db_config

    conn = await aiomysql.connect(**db_config)
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM greetings LIMIT 1 OFFSET %s", index)
        result = await cur.fetchall()
        await conn.commit()
    conn.close()
    return result


