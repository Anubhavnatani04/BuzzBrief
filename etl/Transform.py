import os
import re
import logging
from datetime import datetime
from simhash import Simhash
from datasketch import MinHash, LeanMinHash
from nltk.corpus import stopwords
import pickle

# Initialize NLP resources
stop_words = set(stopwords.words('english'))

def normalize_text(text):
    """Enhanced text normalization pipeline"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)      # Remove numbers
    tokens = text.split()
    return ' '.join([t for t in tokens if t not in stop_words and len(t) > 2])

def calculate_time_window(published_at):
    """Precise 4-hour window calculation with better timestamp handling"""
    try:
        if isinstance(published_at, (int, float)):
            # Handle Unix timestamps (both seconds and milliseconds)
            if published_at > 1e11:  # If in milliseconds
                published_at = published_at / 1000
            dt = datetime.fromtimestamp(published_at)
        elif isinstance(published_at, str):
            # Handle multiple date formats
            for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]:
                try:
                    dt = datetime.strptime(published_at, fmt)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"Unable to parse date string: {published_at}")
        else:
            raise ValueError(f"Unsupported date type: {type(published_at)}")
            
        # Calculate 4-hour window
        window_timestamp = dt.replace(minute=0, second=0, microsecond=0).timestamp()
        return window_timestamp // (4 * 3600) * (4 * 3600)
    except Exception as e:
        logging.error(f"Date processing error: {str(e)} for value: {published_at}")
        # Return current time window as fallback
        now = datetime.now()
        return now.replace(minute=0, second=0, microsecond=0).timestamp() // (4 * 3600) * (4 * 3600)

def generate_simhash(text):
    """Optimized SimHash generation with int64 range limit"""
    hash_value = Simhash(normalize_text(text)).value
    # Ensure the value fits in int64 range by taking modulo
    max_int64 = 9223372036854775807  # Maximum value for int8 in PostgreSQL
    return hash_value % max_int64

def generate_minhash(text, num_perm=128):
    """Efficient MinHash with shingle optimization; now returns serialized bytes"""
    minhash = MinHash(num_perm=num_perm)
    text = normalize_text(text)
    shingles = [text[i:i+5] for i in range(len(text)-4)]  # 5-char shingles
    for s in set(shingles):
        minhash.update(s.encode('utf-8'))
    lean_mh = LeanMinHash(minhash)
    return pickle.dumps(lean_mh)

def extract_entities(text):
    """Improved entity extraction using NLP patterns"""
    text = normalize_text(text)
    return list(set(
        re.findall(r'\b[A-Z][a-z]+\b(?=\s+[A-Z][a-z]+)', text) +  # Proper nouns
        re.findall(r'\b\w{7,}\b', text)  # Long words
    ))[:10]  # Limit to 10 entities

def transform_data(raw_articles):
    """Batch transformation with improved error handling"""
    import gc
    logging.info("🛠️ Transforming articles")
    
    transformed = []
    errors = 0
    
    for art in raw_articles:
        try:
            # Convert timestamp to datetime object immediately
            try:
                if isinstance(art.get('published_at'), (int, float)):
                    published_at = datetime.fromtimestamp(float(art.get('published_at')))
                elif isinstance(art.get('published_at'), str):
                    published_at = datetime.strptime(art.get('published_at'), "%Y-%m-%d")
                else:
                    published_at = datetime.now()
            except Exception:
                published_at = datetime.now()

            # Calculate time window as datetime
            time_window = datetime.fromtimestamp(
                calculate_time_window(published_at.timestamp())
            )

            content = (art.get('content') or '').strip()
            title = (art.get('title') or '').strip()
            
            # Enhanced description handling with multiple fallbacks
            description = (art.get('description') or '').strip()
            if not description:
                # Try getting first sentence from content
                sentences = content.split('.')
                if sentences and sentences[0].strip():
                    description = sentences[0].strip() + '.'
                # If no valid sentence, try using content excerpt
                if not description and content:
                    description = content[:150].strip() + '...'
                # If still no description, use title
                if not description and title:
                    description = title
                # Final fallback
                if not description:
                    description = "No description available."

            transformed.append({
                "source": art.get('source', 'unknown'),
                "image_url": art.get('image_url', ''),
                "headline": title,
                "content": content,
                "description": description,
                "published_at": published_at,  # Now a datetime object
                "url": art.get('url', ''),
                "time_window": time_window,    # Now a datetime object
                "title_hash": generate_simhash(title),
                "content_hash": generate_minhash(content),  # Renamed from content_minhash
                "entities": extract_entities(content),
                "is_kid_friendly": art.get('is_kid_friendly', False),
                "categories": art.get('categories', ['General'])
            })
        except Exception as e:
            logging.error(f"Error transforming article: {str(e)}")
            errors += 1
            continue
        finally:
            # Free memory for each article
            del art
            gc.collect()
    if errors > 0:
        logging.warning(f"Transform phase had {errors} errors")
        gc.collect()
    logging.info(f"✨ Transformed {len(transformed)} articles")
    return transformed