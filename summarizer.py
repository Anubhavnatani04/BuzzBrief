import asyncpg
from transformers import pipeline
from nltk.tokenize import sent_tokenize
import nltk
import asyncio
nltk.download('punkt')

# --- Setup ---
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)

# --- Utils ---
def chunk_text(text, max_tokens=800):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) <= max_tokens:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def summarize_long_article(text):
    chunks = chunk_text(text, max_tokens=800)  # Stay under 1024
    summaries = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        result = summarizer(chunk, max_length=200, min_length=100, do_sample=False)
        if result and isinstance(result, list) and "summary_text" in result[0]:
            summary = result[0]['summary_text']
            summaries.append(summary)
    return " ".join(summaries)