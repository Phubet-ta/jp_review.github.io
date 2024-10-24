import pandas as pd
import json

# ฟังก์ชันสำหรับเขียนไฟล์ JSON จาก Excel
def excel_to_json(excel_file, sheet_name, output_file):
    # อ่านข้อมูลจากไฟล์ Excel
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # ตรวจสอบคอลัมน์ที่จำเป็นทั้งหมดมีอยู่
    required_columns = [
        'Page_ID', 'Q_ID', 'Qustion_JP', 'Qustion_Kana', 'Qusetion_Romaji', 'Qustion_TH', 
        'Answer_JP', 'Answer_Kana', 'Answer_Romaji', 'Answer_TH'
    ]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"คอลัมน์ไม่ครบ ควรมี: {', '.join(required_columns)}")
    
    # แปลงข้อมูลเป็น list ของ dictionary
    data = []
    for _, row in df.iterrows():
        question_data = {
            "Page_ID": row['Page_ID'],
            "Q_ID": row['Q_ID'],
            "Question": {
                "JP": row['Qustion_JP'],
                "Kana": row['Qustion_Kana'],
                "Romaji": row['Qusetion_Romaji'],
                "TH": row['Qustion_TH']
            },
            "Answer": {
                "JP": row['Answer_JP'],
                "Kana": row['Answer_Kana'],
                "Romaji": row['Answer_Romaji'],
                "TH": row['Answer_TH']
            }
        }
        data.append(question_data)
    
    # บันทึกข้อมูลเป็นไฟล์ JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"บันทึกไฟล์ JSON ลงใน: {output_file}")

# การใช้งานฟังก์ชัน
filename = 'unit3.xlsx'  # ชื่อไฟล์ Excel
sheet_name = 'QA＿match'  # ชื่อแผ่นที่ต้องการอ่าน
output_file = f'{filename.split(".")[0]}_qa_match.json'  # ชื่อไฟล์ JSON ที่จะบันทึก

excel_to_json(filename, sheet_name, output_file)
