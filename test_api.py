import requests
import json

# Адрес твоего сервера
BASE_URL = "http://127.0.0.1:5000"

print("="*40)
print("1. Проверяем, что сервер жив (GET /)")
response = requests.get(BASE_URL + "/")
print("Ответ:", response.text)

print("\n" + "="*40)
print("2. Смотрим список заметок (GET /notes)")
response = requests.get(BASE_URL + "/notes")
print("Список заметок:", response.json())

print("\n" + "="*40)
print("3. СОЗДАЁМ заметку (POST /notes)")
new_note = {
    "title": "Моя первая заметка",
    "content": "Я сделал это без Postman!"
}
response = requests.post(BASE_URL + "/notes", json=new_note)
print("Статус создания:", response.status_code)
print("Созданная заметка:", response.json())

print("\n" + "="*40)
print("4. Проверяем список снова (GET /notes)")
response = requests.get(BASE_URL + "/notes")
print("Теперь заметок:", len(response.json()))
print("Все заметки:", response.json())

print("\n" + "="*40)
print("5. Получаем конкретную заметку с ID=1 (GET /notes/1)")
response = requests.get(BASE_URL + "/notes/1")
print("Заметка №1:", response.json())