import asyncpg
from transformers import pipeline
from nltk.tokenize import sent_tokenize
import nltk
import asyncio
nltk.download('punkt')
nltk.data.path.append(r"C:\Users\surya\AppData\Roaming\nltk_data")
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
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    return " ".join(summaries)
