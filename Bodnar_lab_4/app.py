import streamlit as st
import google.generativeai as genai
import json


def get_info_gemini(promt, temp=0.7):
    
   
    API_KEY = "api-key"
    
    genai.configure(api_key=API_KEY)

    config = genai.GenerationConfig(temperature=temp)
    model = genai.GenerativeModel('gemini-3.5-flash', generation_config=config)

    response = model.generate_content(promt)
    return response.text


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Завдання 1", "Завдання 2", "Завдання 3", "Завдання 4", "Завдання 5", "Завдання 6"])

with tab1:
    st.title("Завдання 1")
    st.text('Використання просунутих технік Prompt Engineering')
    st.text("Аналіз тексту")    
    text_to_analyze = "Django ORM дозволяє взаємодіяти з базою даних, використовуючи об'єктно-орієнтований підхід замість написання сирих SQL-запитів. Це пришвидшує розробку, але може призводити до проблем з продуктивністю (наприклад, N+1 queries), якщо використовувати його неправильно."    
    
    with st.expander('Данні'):
        st.write(f"Текст: {text_to_analyze}")
        
    radio_select = st.radio('Виберіть:', ['Проаналізуй наведений текст та визнач його основні ідеї:', 'Ти Senior Python розробник. Проаналізуй текст:'])
    promt = f"{text_to_analyze} {radio_select}" 
        
        
    if st.button("Запит до ШІ", type='primary', use_container_width=True, key='1'):
        rezult = get_info_gemini(promt)
        
        st.info(f"Відповідь ШІ:\n{rezult}")
            
            
    
with tab2:
    st.title("Завдання 2")
    st.text('Декомпозиція складної задачі')
    
    if st.button("Запит до ШІ", type='primary', use_container_width=True, key='2'): 
        rez_gemini = get_info_gemini("Назви 1 ключове поняття з реляційних баз даних. Відповідь - лише 1 слово.")
        st.info(f"Етап 1 (Поняття): {rez_gemini}")
        fact = get_info_gemini(f"Напиши 1 ключовий факт про {rez_gemini}.")
        st.info(f"Етап 2 (Факт): {fact}")
        shos = get_info_gemini(f"Сформуй тестове запитання з 4 варіантами відповідей на основі цього факту: {fact}")
        st.info(f"Етап 3 (Запитання):\n{shos}")

with tab3:
    st.title("Завдання 3")
    st.text('Імітація ReAct')
    
    promt = """Проаналізуй текст: 'Додатки для трекінгу звичок допомагають формувати дисципліну. Однак, за даними деяких досліджень, користувачі часто втрачають мотивацію через 3 тижні.'
Визнач, які твердження є фактами, а які - висновками.
Спочатку сформуй план аналізу, потім виконай його та наприкінці подай результат з перевіркою."""
    
    with st.expander('Данні'):
        st.code(f"Промт: {promt}")
        
    if st.button("Запит до ШІ", type='primary', use_container_width=True, key='3'):
        rezult = get_info_gemini(promt)
        st.info(f"Відповідь ШІ: {rezult}")
    
    
with tab4:
    st.title("Завдання 4")
    st.text('Формування структурованого результату (JSON)')
    
    promt_json = """Поверни ТІЛЬКИ чистий JSON (без вступних слів, без пояснень і без тексту навколо) про архітектуру веб-додатка на Django.
Формат має бути точно таким:
{
    "topic": "Архітектура Django",
    "key_components": ["MVT pattern", "Django ORM", "Admin panel"],
    "database": "PostgreSQL",
    "conclusion": "Django дозволяє швидко будувати надійні бекенд-системи."
}"""

    with st.expander('Дані промпту'):
        st.code(promt_json)
        
    if st.button("Запит до ШІ (Отримати JSON)", type='primary', use_container_width=True, key='4'):
        raw_text = get_info_gemini(promt_json)
        
        clean_json_text = raw_text.replace("```json", "").replace("```", "").strip()
        
        st.subheader("1. Отриманий текст від Gemini:")
        st.code(clean_json_text, language='json')
        
        try:
            parsed_data = json.loads(clean_json_text)
            st.success("Успішно розпарсено засобами Python (json.loads)!")
            
            st.subheader("2. Структурований вивід у Streamlit:")
            st.write(f"**Тема:** {parsed_data.get('topic')}")
            st.write(f"**База даних:** {parsed_data.get('database')}")
            st.write("**Компоненти:**")
            for comp in parsed_data.get('key_components', []):
                st.write(f"- {comp}")
            st.write(f"**Висновок:** {parsed_data.get('conclusion')}")
        except Exception as e:
            st.error(f"Помилка парсингу JSON: {e}")    
    
with tab5:
    st.title("Завдання 5")
    st.text('Робота з великим контекстом (Chunking)')
    
    c1 = "Частина 1: Backend системи розробляється на Python з використанням Django. Основний фокус робиться на безпеці та швидкості розробки API."
    c2 = "Частина 2: Frontend реалізується як Single Page Application (SPA). Взаємодія з бекендом відбувається через REST API у форматі JSON."
    c3 = "Частина 3: База даних — PostgreSQL з реплікацією. Для кешування важких запитів та сесій використовується Redis."
    
    with st.expander('Переглянути вхідні Chunks'):
        st.write(f"**Chunk 1:** {c1}")
        st.write(f"**Chunk 2:** {c2}")
        st.write(f"**Chunk 3:** {c3}")
        
    if st.button("Виконати Chunking та Узагальнення", type='primary', use_container_width=True, key='5'):
        s1 = get_info_gemini(f"Зроби коротке узагальнення (1 речення): {c1}")
        s2 = get_info_gemini(f"Зроби коротке узагальнення (1 речення): {c2}")
        s3 = get_info_gemini(f"Зроби коротке узагальнення (1 речення): {c3}")
        
        st.subheader("1. Узагальнення окремих фрагментів:")
        st.write(f"- **Chunk 1:** {s1}")
        st.write(f"- **Chunk 2:** {s2}")
        st.write(f"- **Chunk 3:** {s3}")
        
        final_prompt = f"Сформуй підсумковий висновок про архітектуру на основі цих трьох тез:\n1. {s1}\n2. {s2}\n3. {s3}"
        final_sum = get_info_gemini(final_prompt)
        
        st.subheader("2. Фінальне загальне узагальнення (Збірка):")
        st.success(final_sum)


with tab6:
    st.title("Завдання 6")
    st.text('Дослідження параметрів генерації (Temperature)')
    
    temp_value = st.slider("Оберіть значення Temperature:", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    
    prompt_temp = "Придумай 1 унікальну та креативну фічу для додатку з трекінгу звичок."
    st.write(f"**Запит:** {prompt_temp}")
    
    if st.button("Згенерувати", type='primary', use_container_width=True, key='6'):
        res = get_info_gemini(prompt_temp, temp=temp_value)
        st.subheader(f"Відповідь Gemini (при Temperature = {temp_value}):")
        st.info(res)