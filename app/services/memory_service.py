import chromadb
import uuid


client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="dino_memories")

def remember(text):
    if not text:
        return
        
    collection.add(
        documents=[text],          
        ids=[str(uuid.uuid4())],  
        metadatas=[{"type": "chat_history"}] 
    )
    print(f"[Memory] Stored: {text}")

def recall(query_text, n_results=2):
    if not query_text:
        return ""
        
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    if results['documents']:
        memories = results['documents'][0]
        return "\n".join([f"- {m}" for m in memories])
    
    return "No relevant memories."