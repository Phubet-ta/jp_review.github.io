import pandas as pd
import random
import json

# ฟังก์ชันสำหรับสร้างแบบฝึกหัด
def generate_exercise(filename, sheet_name, num_questions, output_file):
    # อ่านข้อมูลจาก Excel
    df = pd.read_excel(filename, sheet_name=sheet_name)

    # ตรวจสอบว่าจำนวนคำเพียงพอไหม ถ้าไม่ให้หมุนคำที่มี
    total_words = len(df)
    if total_words < 5:
        raise ValueError("จำเป็นต้องมีคำอย่างน้อย 5 คำในข้อมูล")

    # การหมุนวนคำให้ใช้ทุกคำอย่างเท่าๆ กัน
    exercises = []
    all_indices = list(range(total_words))

    # คำนวณจำนวนชุดที่เราจะวนใช้
    repeat_count = (num_questions * 5) // total_words + 1

    # หมุนวนคำให้ครบตามจำนวนที่ต้องการ
    extended_indices = all_indices * repeat_count  # ขยายลิสต์โดยการวนซ้ำ
    current_pos = 0  # ตำแหน่งเริ่มต้นในการเลือกคำ

    for i in range(num_questions):
        question = []
        # เลือกคำ 5 คำในแต่ละข้อจาก extended_indices
        for idx in range(5):
            word_index = extended_indices[current_pos]
            question.append({
                "index": idx + 1,
                "jp": df.iloc[word_index]['JP'],
                "kana": df.iloc[word_index]['Hiragana'],
                "romaji": df.iloc[word_index]['Romaji'],
                "thai": df.iloc[word_index]['TH']
            })
            current_pos += 1  # ขยับตำแหน่งสำหรับคำถัดไป

        exercises.append({
            "exercise_number": i + 1,
            "pairs": question
        })

    # บันทึกเป็นไฟล์ JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(exercises, f, ensure_ascii=False, indent=4)

    print(f"บันทึกแบบฝึกหัดลงไฟล์: {output_file}")

# การใช้งานฟังก์ชัน
filename = 'unit5.xlsx'  # ชื่อไฟล์ Excel
sheet_name = 'word'  # ชื่อแผ่นที่ใช้
num_questions = 15  # จำนวนข้อที่ต้องการ
output_file = f'{filename.split(".")[0]}_word_match.json'  # ชื่อไฟล์ JSON ที่จะบันทึก

# สร้างแบบฝึกหัดและบันทึกลงไฟล์
generate_exercise(filename, sheet_name, num_questions, output_file)
