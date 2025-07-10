import os
import chromadb
from chromadb.config import Settings

DATA_DIR = 'data/health_data/'
VECTORSTORE_DIR = 'data/vectorstore/'

os.makedirs(VECTORSTORE_DIR, exist_ok=True)

# Read documents
documents = []
for fname in os.listdir(DATA_DIR):
    with open(os.path.join(DATA_DIR, fname), 'r', encoding='utf-8') as f:
        documents.append(f.read())

# Initialize ChromaDB
client = chromadb.Client(Settings(persist_directory=VECTORSTORE_DIR))
collection = client.get_or_create_collection('health_knowledge')

# Add documents to vectorstore
for i, doc in enumerate(documents):
    collection.add(documents=[doc], ids=[f'doc_{i}'])

print('Vectorstore initialized with health and skincare data.') 