import asyncio
import asyncpg
import logging
import ssl
from datasketch import LeanMinHash
from dotenv import load_dotenv
import os
from datetime import datetime
import pickle
import time

load_dotenv()
DB_URL = os.getenv("DB_URL")

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

class DeduplicationEngine:
    def __init__(self):
        self.pool = None
        self.dupe_count = 0
        self.total_processed = 0
        self.retry_attempts = 3
        self.retry_delay = 1
        self.timeout = 60
        self.article_timeout = 15
        self.cleanup_timeout = 60
        self.category_cache = {}
        self.semaphore = asyncio.Semaphore(3)

    async def connect_with_retry(self):
        for attempt in range(self.retry_attempts):
            try:
                if not DB_URL:
                    raise ValueError("Database URL not configured")
                self.pool = await asyncpg.create_pool(
                    dsn=DB_URL,
                    ssl=ssl_context,
                    command_timeout=20,
                    min_size=1,
                    max_size=3,
                    timeout=10,
                    max_inactive_connection_lifetime=10,
                    statement_cache_size=0,
                )
                async with self.pool.acquire() as conn:
                    await conn.fetchval('SELECT 1')
                logging.info("Database connection established successfully")
                return True
            except Exception as e:
                logging.error(f"DB connection attempt {attempt+1} failed: {e}")
                if attempt < self.retry_attempts - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))
                else:
                    raise ConnectionError("Failed to connect to database")

    async def __aenter__(self):
        await self.connect_with_retry()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.pool:
            try:
                await asyncio.wait_for(self.pool.close(), timeout=5)
                logging.info("Pool closed gracefully")
            except (asyncio.TimeoutError, asyncpg.InterfaceError):
                self.pool.terminate()
                logging.warning("Forced termination")
            finally:
                rate = (self.dupe_count / max(1, self.total_processed)) * 100
                logging.info(f"🔄 Duplicate rate: {rate:.1f}%")

    async def preload_categories(self, conn):
        records = await conn.fetch("SELECT id, name FROM categories")
        self.category_cache = {r["name"]: r["id"] for r in records}

    async def get_category_ids(self, conn, categories):
        ids = []
        for category in categories:
            if category not in self.category_cache:
                cat_id = await conn.fetchval("""
                    INSERT INTO categories (name)
                    VALUES ($1)
                    ON CONFLICT (name) DO UPDATE SET name = $1
                    RETURNING id
                """, category)
                self.category_cache[category] = cat_id
            ids.append(self.category_cache[category])
        return ids

    async def is_duplicate(self, conn, article):
        th = article['title_hash']
        tw = article['time_window']
        fingerprint = f"{int(tw.timestamp())}-{th}"

        exists = await conn.fetchval(
            "SELECT 1 FROM hash_index WHERE fingerprint = $1", fingerprint)
        if not exists:
            return False

        stored = await conn.fetch("""
            SELECT content_hash, entities 
            FROM articles 
            WHERE time_window = $1 AND title_hash = $2
            AND published_at >= ($3::timestamp - INTERVAL '24 hours')
        """, tw, th, article['published_at'])

        current_mh = pickle.loads(article['content_hash'])
        for row in stored:
            stored_mh = pickle.loads(row['content_hash'])
            if current_mh.jaccard(stored_mh) >= 0.7 and len(
                set(article['entities']).intersection(row['entities'])
            ) >= 2:
                return True
        return False

    async def insert_article(self, conn, article):
        categories = article.get('categories', ['General'])
        if isinstance(categories, str):
            categories = [categories]

        category_ids = await self.get_category_ids(conn, categories)
        try: 
            art_id = await conn.fetchval("""
                INSERT INTO articles (
                    headline, content, description, source, url, 
                    published_at, time_window, title_hash, 
                    content_hash, entities, image_url, is_kid_friendly
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                RETURNING id
            """,
            article['headline'], article['content'], article['description'],
            article['source'], article['url'], article['published_at'],
            article['time_window'], article['title_hash'],
            article['content_hash'], article['entities'],
            article.get('image_url', ''), article.get('is_kid_friendly', False))
        except asyncpg.exceptions.UniqueViolationError:
            return None

        for cat_id in category_ids:
            await conn.execute("""
                INSERT INTO article_category (article_id, category_id)
                VALUES ($1, $2) ON CONFLICT DO NOTHING
            """, art_id, cat_id)

        await conn.execute("""
            INSERT INTO hash_index (fingerprint, article_ids)
            VALUES ($1, ARRAY[$2::UUID])
            ON CONFLICT (fingerprint)
            DO UPDATE SET article_ids = array_append(
                array_remove(hash_index.article_ids, $2::UUID), $2::UUID)
        """, f"{int(article['time_window'].timestamp())}-{article['title_hash']}", art_id)

        return art_id

    async def process_article(self, article):
        async with self.semaphore:
            self.total_processed += 1
            try:
                async with self.pool.acquire() as conn:
                    async with conn.transaction():
                        if await asyncio.wait_for(self.is_duplicate(conn, article), timeout=self.article_timeout):
                            self.dupe_count += 1
                            return
                        await asyncio.wait_for(self.insert_article(conn, article), timeout=self.article_timeout)
            except asyncio.TimeoutError:
                logging.warning(f"Timeout processing article: {article.get('headline', 'Unknown')}")
            except Exception as e:
                logging.warning(f"Error processing article: {article.get('headline', 'Unknown')} - {e}")

    async def load_articles(self, articles):
        start = time.perf_counter()
        async with self.pool.acquire() as conn:
            await self.preload_categories(conn)

        tasks = [self.process_article(art) for art in articles]
        await asyncio.gather(*tasks)
        logging.info(f"⏱ Load time: {time.perf_counter() - start:.2f} seconds")
        return self.total_processed - self.dupe_count > 0

async def load_data(articles):
    logging.info("📤 Starting database load")
    try:
        async with DeduplicationEngine() as engine:
            success = await engine.load_articles(articles)
        logging.info("✅ Database load completed")
        return success
    except Exception as e:
        logging.error(f"Database load failed: {e}")
        return False
