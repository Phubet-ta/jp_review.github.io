from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import json
import random
import builtins

app = Flask(__name__)

# Custom filter to convert integer to character
@app.template_filter('int_to_char')
def int_to_char(value):
    return builtins.chr(value)  # Use builtins.chr to ensure chr is recognized

@app.route('/')
def select_lesson():
    return render_template('select-lesson.html')

def load_exercises(unit, lesson):
    file_path = f'exercise_data/unit{unit}_{lesson}.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Route สำหรับเลือกและแสดงแบบฝึกหัดตามหมายเลข
@app.route('/word_match/<int:unit>/<int:exercise_number>', methods=['GET', 'POST'])
def word_match(unit, exercise_number):
    exercises = load_exercises(unit, "word_match")
    exercise = next((ex for ex in exercises if ex['exercise_number'] == exercise_number), None)
    if not exercise:
        return f"Exercise {exercise_number} not found.", 404

    pairs = exercise['pairs']
    kana_words = [pair['kana'] for pair in pairs] 
    romaji_words = [pair['romaji'] for pair in pairs]
    thai_words = [pair['thai'] for pair in pairs]
    
    random.seed(exercise_number+555) # Use exercise_number as seed for consistent shuffling
    shuffled_thai_words = random.sample(thai_words, len(thai_words))

    answers = []
    score = 0
    if request.method == 'POST':
        answers = []
        score = 0  # Initialize score here
        for i in range(len(kana_words)):
            selected_answer = request.form.get(f'answer_{i+1}')
            correct_answer = pairs[i]['thai']  # Get the correct Thai word from pairs

            if selected_answer == correct_answer:
                score += 1
                answers.append(f"{i+1}. {kana_words[i]} - {selected_answer} (ถูกต้อง)")
            else:
                answers.append(f"{i+1}. {kana_words[i]} - {selected_answer} (ไม่ถูกต้อง)")

    return render_template('word_match.html',
                           exercise_number=exercise_number,
                           kana_words=kana_words,
                           romaji_words=romaji_words,
                           thai_words=thai_words,
                           shuffled_thai_words=shuffled_thai_words,
                           pairs=pairs,
                           answers=answers,
                           score=score,
                           unit=unit,
                           total_exercises=len(exercises))
               
if __name__ == '__main__':
    app.run(debug=True)

'''word_match(3, 1)'''