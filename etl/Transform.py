import re
import logging
from datetime import datetime
from simhash import Simhash
from datasketch import MinHash
import nltk

# Ensure that NLTK stopwords are downloaded
try:
    from nltk.corpus import stopwords
except LookupError:
    nltk.download('stopwords')
    from nltk.corpus import stopwords

def normalize_text(text):
    """
    Lowercase, remove special characters, and filter stopwords.
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    stop_words = set(stopwords.words('english'))
    filtered = [word for word in tokens if word not in stop_words]
    return " ".join(filtered)

def calculate_time_window(published_at):
    """
    Calculate a 4-hour window for a given ISO datetime string.
    """
    dt = datetime.fromisoformat(published_at)
    hour_block = (dt.hour // 4) * 4
    window_start = dt.replace(hour=hour_block, minute=0, second=0, microsecond=0)
    return window_start.isoformat()

def generate_simhash(text):
    """
    Generate a 64-bit SimHash value for normalized text.
    """
    return Simhash(text).value

def generate_minhash(text, num_perm=128):
    """
    Create a MinHash signature using 128 permutations.
    """
    minhash = MinHash(num_perm=num_perm)
    shingles = text.split()
    for shingle in shingles:
        minhash.update(shingle.encode('utf8'))
    return minhash

def extract_entities(text):
    """
    Dummy entity extraction; replace with a proper NLP-based implementation.
    """
    words = set(text.split())
    # For demonstration, consider words longer than 5 characters as entities
    entities = [word for word in words if len(word) > 5]
    return entities

def transform_data(raw_articles):
    logging.info("Starting data transformation")
    transformed_articles = []
    for article in raw_articles:
        normalized_headline = normalize_text(article["headline"])
        normalized_content = normalize_text(article["content"])
        time_window = calculate_time_window(article["published_at"])
        title_hash = generate_simhash(normalized_headline)
        content_minhash = generate_minhash(normalized_content)
        entities = extract_entities(article["content"])

        transformed_articles.append({
            "published_at": article["published_at"],
            "source": article["source"],
            "headline": article["headline"],
            "content": article["content"],
            "time_window": time_window,
            "title_hash": title_hash,
            "content_minhash": content_minhash,
            "entities": entities,
        })
    logging.info("Data transformation completed")
    return transformed_articles