import asyncpg
import datetime
from typing import Optional
from data import config


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=config.HOST,
            port=config.PORT,
            user=config.USER,
            password=config.PASSWORD,
            database=config.NAME,
            min_size=2,
            max_size=10
        )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    # ===================== BATTERY =====================

    async def add_battery(self, title, category, count):
        now = datetime.date.today()
        sql = """
        INSERT INTO batteries (title, category, count, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """
        return await self.pool.fetchval(sql, title, category, count, now, now)

    async def get_all_batteries(self):
        sql = """
        SELECT id, title, category, count, created_at
        FROM batteries ORDER BY created_at DESC
        """
        return await self.pool.fetch(sql)

    async def get_battery_by_id(self, bid):
        sql = "SELECT id, title, category, count, created_at FROM batteries WHERE id = $1"
        return await self.pool.fetchrow(sql, bid)

    # ===================== CHARGER =====================

    async def add_charger(self, title, category, watt, voltage, count):
        now = datetime.date.today()
        sql = """
        INSERT INTO chargers (title, category, watt, voltage, count, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id
        """
        return await self.pool.fetchval(sql, title, category, watt, voltage, count, now, now)

    async def get_all_chargers(self):
        sql = "SELECT id, title, category, watt, voltage, count, created_at FROM chargers ORDER BY created_at DESC"
        return await self.pool.fetch(sql)

    async def get_charger_by_id(self, cid):
        sql = "SELECT id, title, category, watt, voltage, count, created_at FROM chargers WHERE id = $1"
        return await self.pool.fetchrow(sql, cid)

    # ===================== DISPLAY =====================

    async def add_display(self, title, hz, pin, count):
        now = datetime.date.today()
        sql = """
        INSERT INTO displays (title, hz, pin, count, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id
        """
        return await self.pool.fetchval(sql, title, hz, pin, count, now, now)

    async def get_all_displays(self):
        sql = "SELECT id, title, hz, pin, count, created_at FROM displays ORDER BY created_at DESC"
        return await self.pool.fetch(sql)

    async def get_display_by_id(self, did):
        sql = "SELECT id, title, hz, pin, count, created_at FROM displays WHERE id = $1"
        return await self.pool.fetchrow(sql, did)

    # ===================== UMUMIY =====================

    async def reduce_count(self, table, product_id, amount):
        now = datetime.date.today()
        sql = f"UPDATE {table} SET count = count - $2, updated_at = $3 WHERE id = $1 RETURNING count"
        return await self.pool.fetchval(sql, product_id, amount, now)

    async def increase_count(self, table, product_id, amount):
        now = datetime.date.today()
        sql = f"UPDATE {table} SET count = count + $2, updated_at = $3 WHERE id = $1 RETURNING count"
        return await self.pool.fetchval(sql, product_id, amount, now)

    async def delete_product(self, table, product_id):
        sql = f"DELETE FROM {table} WHERE id = $1"
        return await self.pool.execute(sql, product_id)
