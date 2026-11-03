from openai import OpenAI

client = OpenAI(api_key="api-key")

def send_request(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,

        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Помилка: {e}"

print("=== ЗАВДАННЯ 1: 5 ТИПІВ ЗАПИТІВ ===")
print("\n1. Пояснення:")
print(send_request([{"role": "user", "content": "Коротко поясни, що таке ORM у Django."}]))

print("\n2. Генерація:")
print(send_request([{"role": "user", "content": "Напиши 2 речення про переваги Python."}]))

print("\n3. Переклад:")
print(send_request([{"role": "user", "content": "Переклади українською: 'MySQL is a relational database management system.'"}]))

print("\n4. Узагальнення:")
print(send_request([{"role": "user", "content": "Узагальни до 1 тези: 'Django — це високорівневий Python веб-фреймворк, який заохочує швидку розробку і чистий, прагматичний дизайн. Він бере на себе багато клопоту веб-розробки.'"}]))

print("\n5. Список:")
print(send_request([{"role": "user", "content": "Напиши список з 3 популярних баз даних для веб-проєктів."}]))


print("\n=== ЗАВДАННЯ 2: ZERO-SHOT ТА FEW-SHOT ===")
print("\nZero-shot:")
print(send_request([{"role": "user", "content": "Напиши SQL запит для вибірки всіх користувачів."}]))

print("\nFew-shot:")
print(send_request([{"role": "user", "content": "Приклад 1: Вибрати імена -> SELECT name FROM users;\nПриклад 2: Вибрати email -> SELECT email FROM users;\nЗавдання: Напиши SQL запит для вибірки всіх користувачів."}]))


print("\n=== ЗАВДАННЯ 3: УДОСКОНАЛЕННЯ ПРОМПТУ ===")
print("\nПочатковий:")
print(send_request([{"role": "user", "content": "Розкажи про бази даних."}]))

print("\nВдосконалений:")
print(send_request([{"role": "user", "content": "Ти Senior розробник. Поясни студенту 3 курсу, навіщо потрібна реляційна база даних у трекері звичок. Відповідь дай списком, до 40 слів."}]))


print("\n=== ЗАВДАННЯ 4: СИСТЕМНІ РОЛІ ===")
task_prompt = "Що таке міграції в базі даних?"

print("\nРоль: Викладач")
print(send_request([
    {"role": "system", "content": "Ти викладач університету."},
    {"role": "user", "content": task_prompt}
]))

print("\nРоль: Програміст")
print(send_request([
    {"role": "system", "content": "Ти практикуючий backend-програміст."},
    {"role": "user", "content": task_prompt}
]))

print("\nРоль: Науковець")
print(send_request([
    {"role": "system", "content": "Ти дослідник комп'ютерних наук."},
    {"role": "user", "content": task_prompt}
]))