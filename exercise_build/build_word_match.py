from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# ฟังก์ชันดึงข้อมูลจากไฟล์ JSON
def load_exercises(unit):
    file_path = f'exercise_data/unit{unit}_word_match.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


# Route สำหรับเลือกและแสดงแบบฝึกหัดตามหมายเลข
@app.route('/word_match/<int:unit>/<int:exercise_number>', methods=['GET', 'POST'])
def word_match(unit, exercise_number):
    # ดึงข้อมูลคำศัพท์ทั้งหมดจากไฟล์ JSON
    exercises = load_exercises(unit)

    # หาข้อที่มีหมายเลขตรงกับ exercise_number
    exercise = next((ex for ex in exercises if ex['exercise_number'] == exercise_number), None)
    
    if not exercise:
        return f"Exercise {exercise_number} not found.", 404
    
    pairs = exercise['pairs']
    kana_words = [pair['kana'] for pair in pairs]  # ฝั่งคำญี่ปุ่น
    romaji_words = [pair['romaji'] for pair in pairs] # ฝั่งโรมาจิ
    thai_words = [pair['thai'] for pair in pairs]  # ฝั่งคำแปลไทย

    if request.method == 'POST':
        # รับคำตอบจากผู้ใช้
        answers = request.form.getlist('answer')
        # แสดงผลคำตอบหรือทำการตรวจสอบ
        return render_template('word_match.html', kana_words=kana_words, thai_words=thai_words, answers=answers, exercise_number=exercise_number)

    return render_template('word_match.html', kana_words=kana_words, thai_words=thai_words, answers=None, exercise_number=exercise_number)

if __name__ == '__main__':
    app.run(debug=True)
