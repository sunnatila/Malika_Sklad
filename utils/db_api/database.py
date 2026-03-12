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

    async def add_battery(self, title, brand_id, model_name, watt, voltage, capacity, count):
        now = datetime.datetime.now().date()
        sql = """
        INSERT INTO batteries (title, brand_id, model_name, watt, voltage, capacity, count,
                               created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        RETURNING id
        """
        return await self.pool.fetchval(sql, title, brand_id, model_name, watt, voltage, capacity, count, now, now)

    async def get_all_batteries(self):
        sql = """
        SELECT b.id, b.title, b.model_name, b.watt, b.voltage, b.capacity, b.count,
               b.created_at, br.name as brand_name
        FROM batteries b
        LEFT JOIN brands br ON b.brand_id = br.id
        ORDER BY b.created_at DESC
        """
        return await self.pool.fetch(sql)

    async def get_battery_by_id(self, battery_id):
        sql = """
        SELECT b.id, b.title, b.model_name, b.watt, b.voltage, b.capacity, b.count,
               b.created_at, br.name as brand_name
        FROM batteries b
        LEFT JOIN brands br ON b.brand_id = br.id
        WHERE b.id = $1
        """
        return await self.pool.fetchrow(sql, battery_id)

    # ===================== CHARGER =====================

    async def add_charger(self, title, brand_id, watt, voltage, count):
        now = datetime.datetime.now().date()
        sql = """
        INSERT INTO chargers (title, brand_id, watt, voltage, count,
                              created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id
        """
        return await self.pool.fetchval(sql, title, brand_id, watt, voltage, count, now, now)

    async def get_all_chargers(self):
        sql = """
        SELECT c.id, c.title, c.watt, c.voltage, c.count,
               c.created_at, br.name as brand_name
        FROM chargers c
        LEFT JOIN brands br ON c.brand_id = br.id
        ORDER BY c.created_at DESC
        """
        return await self.pool.fetch(sql)

    async def get_charger_by_id(self, charger_id):
        sql = """
        SELECT c.id, c.title, c.watt, c.voltage, c.count,
               c.created_at, br.name as brand_name
        FROM chargers c
        LEFT JOIN brands br ON c.brand_id = br.id
        WHERE c.id = $1
        """
        return await self.pool.fetchrow(sql, charger_id)

    # ===================== DISPLAY =====================

    async def add_display(self, title, brand_id, hz, pin, count):
        now = datetime.datetime.now().date()
        sql = """
        INSERT INTO displays (title, brand_id, hz, pin, count,
                              created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id
        """
        return await self.pool.fetchval(sql, title, brand_id, hz, pin, count, now, now)

    async def get_all_displays(self):
        sql = """
        SELECT d.id, d.title, d.hz, d.pin, d.count,
               d.created_at, br.name as brand_name
        FROM displays d
        LEFT JOIN brands br ON d.brand_id = br.id
        ORDER BY d.created_at DESC
        """
        return await self.pool.fetch(sql)

    async def get_display_by_id(self, display_id):
        sql = """
        SELECT d.id, d.title, d.hz, d.pin, d.count,
               d.created_at, br.name as brand_name
        FROM displays d
        LEFT JOIN brands br ON d.brand_id = br.id
        WHERE d.id = $1
        """
        return await self.pool.fetchrow(sql, display_id)

    # ===================== UMUMIY (har 3 jadval uchun) =====================

    async def reduce_count(self, table, product_id, amount):
        now = datetime.datetime.now().date()
        sql = f"UPDATE {table} SET count = count - $2, updated_at = $3 WHERE id = $1 RETURNING count"
        return await self.pool.fetchval(sql, product_id, amount, now)

    async def increase_count(self, table, product_id, amount):
        now = datetime.datetime.now().date()
        sql = f"UPDATE {table} SET count = count + $2, updated_at = $3 WHERE id = $1 RETURNING count"
        return await self.pool.fetchval(sql, product_id, amount, now)

    async def delete_product(self, table, product_id):
        sql = f"DELETE FROM {table} WHERE id = $1"
        return await self.pool.execute(sql, product_id)

    # ===================== BRAND =====================

    async def get_or_create_brand(self, name):
        sql = "SELECT id FROM brands WHERE LOWER(name) = LOWER($1)"
        result = await self.pool.fetchval(sql, name)
        if result:
            return result
        sql = "INSERT INTO brands (name) VALUES ($1) RETURNING id"
        return await self.pool.fetchval(sql, name)