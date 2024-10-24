import pandas as pd
import json

# ฟังก์ชันสำหรับเขียนไฟล์ JSON จาก Excel
def excel_to_json(excel_file, sheet_name, output_file):
    # อ่านข้อมูลจากไฟล์ Excel
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # ตรวจสอบคอลัมน์ที่จำเป็นทั้งหมดมีอยู่
    required_columns = [
        'ID', 'Q_ID', 'Sen_JP', 'Sen_Kana', 'Sen_Romaji', 'GG_Translate', 'Sen_TH', 
        'Sen_Kana_Blank', 'Sen_Romaji_Blank', 'Choice_Kana1', 'Choice_Kana2', 'Choice_Kana3',
        'Choice_Romaji1', 'Choice_Romaji2', 'Choice_Romaji3', 'Ans_Kana', 'Ans_Romaji'
    ]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"คอลัมน์ไม่ครบ ควรมี: {', '.join(required_columns)}")
    
    # แปลงข้อมูลเป็น list ของ dictionary
    data = []
    for _, row in df.iterrows():
        question_data = {
            "ID": row['ID'],
            "Q_ID": row['Q_ID'],
            "Sentence": {
                "JP": row['Sen_JP'],
                "Kana": row['Sen_Kana'],
                "Romaji": row['Sen_Romaji'],
                "Translate": row['GG_Translate'],
                "TH": row['Sen_TH']
            },
            "Blank_Sentence": {
                "Kana": row['Sen_Kana_Blank'],
                "Romaji": row['Sen_Romaji_Blank']
            },
            "Choices": {
                "Kana": [row['Choice_Kana1'], row['Choice_Kana2'], row['Choice_Kana3']],
                "Romaji": [row['Choice_Romaji1'], row['Choice_Romaji2'], row['Choice_Romaji3']]
            },
            "Answer": {
                "Kana": row['Ans_Kana'],
                "Romaji": row['Ans_Romaji']
            }
        }
        data.append(question_data)
    
    # บันทึกข้อมูลเป็นไฟล์ JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"บันทึกไฟล์ JSON ลงใน: {output_file}")

# การใช้งานฟังก์ชัน
filename = 'unit3.xlsx'  # ชื่อไฟล์ Excel ที่จะอ่าน
sheet_name = 'Word_Choice'  # ชื่อแผ่นที่ต้องการอ่าน
output_file = f'{filename.split(".")[0]}_word_choice.json'  # ชื่อไฟล์ JSON ที่จะบันทึก

# เรียกใช้ฟังก์ชัน
excel_to_json(filename, sheet_name, output_file)
