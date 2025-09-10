import json

def generate_markdown(data):
    user_info = data['input']
    name = user_info['name']
    birth_date = user_info['birth_date']
    birth_time = user_info['birth_time']
    birth_place = user_info['birth_place']
    gender = user_info['gender'].strip()
    calendar_type = user_info['calendar_type']
    analysis_date = user_info['analysis_date']

    md = f"""# {name}님의 사주 명리 분석 리포트

## 1️⃣ 기본 정보
- 이름: {name}
- 성별: {gender}
- 출생일시: {calendar_type} {birth_date} {birth_time} ({birth_place})
- 분석 기준일: {analysis_date}

## 2️⃣ 사주 원국
- 연주: {data['won_guk']['year']['stem']} {data['won_guk']['year']['branch']}
- 월주: {data['won_guk']['month']['stem']} {data['won_guk']['month']['branch']}
- 일주: {data['won_guk']['day']['stem']} {data['won_guk']['day']['branch']}
- 시주: {data['won_guk']['hour']['stem']} {data['won_guk']['hour']['branch']}

## 3️⃣ 분석 내용
{data['content']}

---
"""
    return md

def print_json(data):
    return json.dumps(data, ensure_ascii=False, indent=2)

def save_markdown(md, filename="report.md"):
    with open(filename, "w", encoding="utf-8") as f_md:
        f_md.write(md)

def save_json(data, filename="report.json"):
    with open(filename, "w", encoding="utf-8") as f_json:
        json.dump(data, f_json, ensure_ascii=False, indent=4)
