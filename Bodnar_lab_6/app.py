import streamlit as st
import chromadb
from google import genai
import time


st.set_page_config("Prompt Engineering, RAG та Fine-tuning")
st.header("Лабораторна робота №6")



API_KEY = "API-KEY"
client = genai.Client(api_key=API_KEY)

chroma_client = chromadb.Client()


categorys = (
    "Категорія: програмування. Опис: написання коду, змінні, цикли, функції, об'єктно-орієнтоване програмування, Python, Django.",
    "Категорія: штучний інтелект. Опис: машинне навчання, нейронні мережі, глибоке навчання, комп'ютерний зір, LLM.",
    "Категорія: бази даних. Опис: SQL, таблиці, первинні та зовнішні ключі, індекси, транзакції, PostgreSQL, MySQL.",
    "Категорія: комп'ютерні мережі. Опис: IP-адреси, маршрутизація, протоколи TCP/IP, HTTP, DNS, комутатори."
)


@st.cache_resource
def init_chroma():
    c_client = chromadb.Client()
    # Створюємо або беремо існуючу колекцію
    col = c_client.get_or_create_collection(name="categories_rag")
    
    # Якщо в колекції ще немає документів — додаємо їх у вигляді СПИСКУ list()
    if col.count() == 0:
        col.add(
            ids=["cat_1", "cat_2", "cat_3", "cat_4"],
            documents=list(categorys) # Обов'язково конвертуємо кортеж у list!
        )
    return col

collection = init_chroma()



promts = [
    ("Цикли for та while використовуються для багаторазового виконання блоку коду.", "програмування"),
    ("Первинний ключ (Primary Key) унікально ідентифікує кожен запис у таблиці.", "бази даних"),
    ("Протокол TCP забезпечує надійну доставку пакетів між вузлами.", "комп'ютерні мережі"),
    ("Згорткові нейронні мережі ефективно розпізнають об'єкти на зображеннях.", "штучний інтелект"),
    ("Індекси прискорюють пошук даних, але сповільнюють операції вставки.", "бази даних")
    ]


with st.expander("Катигорії"):
    for index, cat in enumerate(categorys):
        st.write(index+1, cat)
    
    
with st.expander("Дані"):
    for index, promt in enumerate(promts):
        st.write(index+1, promt)
        
        
def safe_generate(prompt):
    for attempt in range(5):
        try:
            res = client.models.generate_content(
                model="gemini-3.5-flash", 
                contents=prompt
            )
            return res.text.strip().lower()
        
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                time.sleep(5)
            else:
                raise e
    return "помилка сервера"
        
        
        
def classify_prompt(text):
    full_promt = f"""Визнач категорію наведеного тексту.
Можливі категорії: програмування, штучний інтелект, бази даних, комп'ютерні мережі.
Поверни ЛИШЕ назву категорії маленькими літерами без крапки.
Текст: {text}"""
    return safe_generate(full_promt)


def classify_rag(text):
    results = collection.query(query_texts=[text], n_results=1)
    context = results["documents"][0][0]
    
    full_promt = f"""На основі наведеного довідника визнач категорію тексту. Поверни ЛИШЕ назву категорії маленькими літерами.
Довідник: {context}
Текст: {text}"""
    return safe_generate(full_promt)


def classify_finetuning(text):
    full_promt = f"""Класифікуй текст за прикладами. Поверни ЛИШЕ назву категорії.

Текст: Python є мовою програмування високого рівня.
Категорія: програмування

Текст: Нейронна мережа складається з набору взаємопов'язаних нейронів.
Категорія: штучний інтелект

Текст: Реляційна база даних зберігає інформацію у вигляді таблиць.
Категорія: бази даних

Текст: Маршрутизатор передає пакети даних між різними мережами.
Категорія: комп'ютерні мережі

Текст: {text}
Категорія:"""
    return safe_generate(full_promt) 
    
        
        
        
st.header('ЗАПУСК ЕКСПЕРИМЕНТУ')
if st.button("ЗАПУСК", type="primary", use_container_width=True):
    
    rez_table = []
    score_prompt, score_rag, score_ft = 0, 0, 0
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total = len(promts)
    
    for i, (text, expected) in enumerate(promts, 1):
        
        status_text.text(f"Обробка прикладу {i} з {total}...")
        
        res_p = classify_prompt(text)
        time.sleep(1.5)
        res_r = classify_rag(text)
        time.sleep(1.5)
        res_f = classify_finetuning(text)
        time.sleep(1.5)

        if expected in res_p: 
            score_prompt += 1
        if expected in res_r: 
            score_rag += 1
        if expected in res_f: 
            score_ft += 1
            
        rez_table.append({
                "№": i,
                "Текст": text,
                "Очікувано": expected,
                "Prompt": res_p,
                "RAG": res_r,
                "Fine-tuning (Few-shot)": res_f
            })
    
    status_text.success("Готово!")  
    st.table(rez_table)
    
    st.write(f"Точність: Prompt = {score_prompt/5*100}%, RAG = {score_rag/5*100}%, Fine-tuning = {score_ft/5*100}%")