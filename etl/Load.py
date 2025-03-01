import asyncio
import asyncpg
import logging
import pickle
from datasketch import MinHash

# Adjust the connection string as per your Supabase / PostgreSQL configuration
DB_DSN = "postgresql://user:password@localhost:5432/database"

async def load_data(articles):
    logging.info("Starting data load")
    pool = await asyncpg.create_pool(dsn=DB_DSN)
    async with pool.acquire() as conn:
        for article in articles:
            try:
                duplicate = await check_duplicate(conn, article)
                if not duplicate:
                    await insert_article(conn, article)
                else:
                    logging.info("Duplicate article skipped: %s", article["headline"])
            except Exception as e:
                logging.error("Error processing article '%s': %s", article["headline"], str(e))
    await pool.close()
    logging.info("Data load completed")

async def check_duplicate(conn, article):
    """
    Check for duplicates using:
    a) Matching time_window and title_hash from hash_index table.
    b) MinHash similarity for content (threshold 0.7).
    c) Entity overlap (at least 3 common entities).
    """
    query = """
    SELECT content_minhash, entities FROM hash_index 
    WHERE time_window = $1 AND title_hash = $2;
    """
    rows = await conn.fetch(query, article["time_window"], article["title_hash"])
    if not rows:
        return False
    for row in rows:
        stored_minhash = pickle.loads(row["content_minhash"])
        similarity = article["content_minhash"].jaccard(stored_minhash)
        if similarity >= 0.7:
            # Check entity overlap; assume stored entities and current entities are lists of strings.
            overlap = set(article["entities"]).intersection(set(row["entities"]))
            if len(overlap) >= 3:
                return True
    return False

async def insert_article(conn, article):
    """
    Insert the unique article into the articles table,
    then update the hash_index table with its fingerprints.
    """
    minhash_bytes = pickle.dumps(article["content_minhash"])
    insert_article_query = """
    INSERT INTO articles (published_at, source, headline, content, time_window, title_hash, entities)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    RETURNING id;
    """
    article_id = await conn.fetchval(
        insert_article_query,
        article["published_at"],
        article["source"],
        article["headline"],
        article["content"],
        article["time_window"],
        article["title_hash"],
        article["entities"]
    )
    
    insert_hash_query = """
    INSERT INTO hash_index (article_id, time_window, title_hash, content_minhash, entities)
    VALUES ($1, $2, $3, $4, $5);
    """
    await conn.execute(
        insert_hash_query,
        article_id,
        article["time_window"],
        article["title_hash"],
        minhash_bytes,
        article["entities"]
    )