import chromadb
from google import genai

client = genai.Client(api_key="api_key")

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_local_rag")


def load_and_chunk(paths):
    chunks = []
    chunk_id = 1
    
    for p in paths:
        with open(p, "r", encoding="utf-8") as f:
            
            for para in f.read().split("\n\n"):
                if para.strip():
                    
                    chunks.append({"id": f"c_{chunk_id}", "text": para.strip(), "src": p})
                    chunk_id += 1
    
    return chunks



def build_vector_store(chunks):
    print("Будуємо базу знань локально...")

    for c in chunks:
        collection.add(
            ids=[c["id"]], 
            documents=[c["text"]], 
            metadatas=[{"source": c["src"]}]
        )
    print("База знань готова!\n")



def ask_rag(question):
    print(f"Запит: {question}")
    
    results = collection.query(query_texts=[question], n_results=2)
    context = "\n".join(results['documents'][0])
    
    print(f"Знайдений контекст у файлах:\n{context}\n")
    
    prompt = f"Контекст:\n{context}\n\nПитання: {question}\nВідповідай строго за контекстом. Якщо інфи немає, пиши 'Я не знайшов інформації в документах'."
    
    ans = client.models.generate_content(
        model="gemini-3.5-flash", 
        contents=prompt
    )
    
    print(f"Відповідь Gemini:\n{ans.text}")
    print("="*50)


file_paths = [r"docs\django.txt", r"docs\sql.txt", r"docs\streamlit.txt"]

my_chunks = load_and_chunk(file_paths)
build_vector_store(my_chunks)

ask_rag("Що таке Django?")
ask_rag("Як замінити мастило в машині?")