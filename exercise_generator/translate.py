import pandas as pd
import json

# ฟังก์ชันสำหรับเขียนไฟล์ JSON จาก Excel
def excel_to_json_v2(excel_file, sheet_name, output_file):
    # อ่านข้อมูลจากไฟล์ Excel
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # ตรวจสอบคอลัมน์ที่จำเป็นทั้งหมดมีอยู่
    required_columns = [
        'Sen_JP', 'Sen_Romaji', 'Sen_JP_split', 'Sen_TH', 'Sen_TH_split'
    ]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"คอลัมน์ไม่ครบ ควรมี: {', '.join(required_columns)}")
    
    # แปลงข้อมูลเป็น list ของ dictionary
    data = []
    for _, row in df.iterrows():
        question_data = {
            "Sentence": {
                "JP": row['Sen_JP'],
                "Romaji": row['Sen_Romaji'],
                "JP_split": row['Sen_JP_split'].split(','),  # แยกคำ
                "TH": row['Sen_TH'],
                "TH_split": row['Sen_TH_split'].split(',')  # แยกคำ
            }
        }
        data.append(question_data)
    
    # บันทึกข้อมูลเป็นไฟล์ JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"บันทึกไฟล์ JSON ลงใน: {output_file}")

# การใช้งานฟังก์ชัน
filename = 'unit3.xlsx'  # ชื่อไฟล์ Excel ที่จะอ่าน
sheet_name = 'Translate'  # ชื่อแผ่นที่ต้องการอ่าน
output_file = f'{filename.split(".")[0]}_translate.json'  # ชื่อไฟล์ JSON ที่จะบันทึก

# เรียกใช้ฟังก์ชัน
excel_to_json_v2(filename, sheet_name, output_file)
