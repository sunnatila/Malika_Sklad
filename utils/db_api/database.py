import asyncpg
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

    # ===================== PRODUCT METHODS =====================

    async def add_product(self, title, product_type, category_id, brand_id,
                          model_name, watt, voltage, capacity, count):
        """Yangi mahsulot qo'shish"""
        sql = """
        INSERT INTO products (title, product_type, category_id, brand_id,
                              model_name, watt, voltage, capacity, count,
                              created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW(), NOW())
        RETURNING id
        """
        return await self.pool.fetchval(
            sql, title, product_type, category_id, brand_id,
            model_name, watt, voltage, capacity, count
        )

    async def get_products_by_type(self, product_type):
        """Mahsulotlarni turi bo'yicha olish"""
        sql = """
        SELECT p.id, p.title, p.product_type, p.model_name, p.watt,
               p.voltage, p.capacity, p.count, 
               c.name as category_name, b.name as brand_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN brands b ON p.brand_id = b.id
        WHERE p.product_type = $1
        ORDER BY p.created_at DESC
        """
        return await self.pool.fetch(sql, product_type)

    async def get_product_by_id(self, product_id):
        """Mahsulotni ID bo'yicha olish"""
        sql = """
        SELECT p.id, p.title, p.product_type, p.model_name, p.watt,
               p.voltage, p.capacity, p.count,
               c.name as category_name, b.name as brand_name,
               p.created_at
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN brands b ON p.brand_id = b.id
        WHERE p.id = $1
        """
        return await self.pool.fetchrow(sql, product_id)

    async def reduce_product_count(self, product_id, amount):
        """Mahsulot sonini kamaytirish (chiqarish)"""
        sql = """
        UPDATE products 
        SET count = count - $2, updated_at = NOW()
        WHERE id = $1
        RETURNING count
        """
        return await self.pool.fetchval(sql, product_id, amount)

    async def increase_product_count(self, product_id, amount):
        """Mahsulot sonini ko'paytirish (qo'shish)"""
        sql = """
        UPDATE products 
        SET count = count + $2, updated_at = NOW()
        WHERE id = $1
        RETURNING count
        """
        return await self.pool.fetchval(sql, product_id, amount)

    async def delete_product(self, product_id):
        """Mahsulotni o'chirish"""
        sql = "DELETE FROM products WHERE id = $1"
        return await self.pool.execute(sql, product_id)

    # ===================== CATEGORY METHODS =====================

    async def get_or_create_category(self, name):
        """Kategoriyani olish yoki yaratish"""
        sql = "SELECT id FROM categories WHERE LOWER(name) = LOWER($1)"
        result = await self.pool.fetchval(sql, name)
        if result:
            return result
        sql = "INSERT INTO categories (name) VALUES ($1) RETURNING id"
        return await self.pool.fetchval(sql, name)

    # ===================== BRAND METHODS =====================

    async def get_or_create_brand(self, name):
        """Brendni olish yoki yaratish"""
        sql = "SELECT id FROM brands WHERE LOWER(name) = LOWER($1)"
        result = await self.pool.fetchval(sql, name)
        if result:
            return result
        sql = "INSERT INTO brands (name) VALUES ($1) RETURNING id"
        return await self.pool.fetchval(sql, name)

    async def get_brands(self):
        """Barcha brendlarni olish"""
        sql = "SELECT id, name FROM brands ORDER BY name"
        return await self.pool.fetch(sql)