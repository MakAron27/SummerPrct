from flask import Flask, jsonify, request

# Создаём приложение
app = Flask(__name__)

# Наша "база данных" в памяти (пока просто список словарей)
notes = []
next_id = 1  # Простой счётчик для ID

# ---------- 1. ГЛАВНАЯ СТРАНИЦА (для проверки) ----------
@app.route('/')
def hello():
    return "Сервер заметок работает! Используй /notes"

# ---------- 2. ПОЛУЧИТЬ ВСЕ ЗАМЕТКИ (GET) ----------
@app.route('/notes', methods=['GET'])
def get_notes():
    return jsonify(notes)  # Переводим список в JSON и отдаём

# ---------- 3. ПОЛУЧИТЬ ОДНУ ЗАМЕТКУ (GET) ----------
@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    # Ищем заметку по ID
    for note in notes:
        if note['id'] == note_id:
            return jsonify(note)
    return jsonify({"error": "Заметка не найдена"}), 404

# ---------- 4. СОЗДАТЬ ЗАМЕТКУ (POST) ----------
@app.route('/notes', methods=['POST'])
def create_note():
    global next_id
    data = request.get_json()  # Получаем JSON из запроса
    
    # Простая проверка
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Нужно передать title и content"}), 400
    
    new_note = {
        "id": next_id,
        "title": data['title'],
        "content": data['content']
    }
    notes.append(new_note)
    next_id += 1
    return jsonify(new_note), 201  # 201 = Created

# ---------- 5. УДАЛИТЬ ЗАМЕТКУ (DELETE) ----------
@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    global notes
    for i, note in enumerate(notes):
        if note['id'] == note_id:
            del notes[i]
            return jsonify({"message": "Заметка удалена"}), 200
    return jsonify({"error": "Заметка не найдена"}), 404

# ---------- 6. ОБНОВИТЬ ЗАМЕТКУ (PUT) ----------
@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json()
    for note in notes:
        if note['id'] == note_id:
            # Обновляем только то, что передали
            note['title'] = data.get('title', note['title'])
            note['content'] = data.get('content', note['content'])
            return jsonify(note)
    return jsonify({"error": "Заметка не найдена"}), 404

# ---------- ЗАПУСК ----------
if __name__ == '__main__':
    app.run(debug=True)  # debug=True - автоматом перезагружается при изменении кода