from dotenv import load_dotenv
import os

from datetime import datetime

load_dotenv()

print(f"Gemini API key = {os.getenv('GEMINI_API_KEY')}")

# langchain으로 GEMINI 최신 AI 불러오기
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))

# Parser 만들기
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class InputInfo(BaseModel):
    name: str = Field(description="이름")
    birth_date: str = Field(description="출생일, YYYY-MM-DD")
    birth_time: str = Field(description="출생 시간, HH:MM")
    timezone: str = Field(description="출생 시간대, 예: Asia/Seoul")
    birth_place: str = Field(description="출생지")
    gender: str = Field(description="성별")
    calendar_type: str = Field(description="달력 종류, 양력 또는 음력")
    analysis_date: str = Field(description="분석 기준 날짜")

class StemBranch(BaseModel):
    stem: str
    branch: str

class WonGuk(BaseModel):
    year: StemBranch
    month: StemBranch
    day: StemBranch
    hour: StemBranch
    
from parser import chain
from report_utils import generate_markdown, print_json, save_markdown, save_json

if __name__ == "__main__":
    answer = chain.invoke({
        "name": "조요셉",
        "country": "대한민국",
        "city": "전주",
        "yyyymmdd_hhmm": "2003-01-24 06:20",
        "sex": "남성"
    })

    markdown_report = generate_markdown(answer)
    json_output = print_json(answer)

    # 1️⃣ 화면 출력
    print("========== (A) Markdown 리포트 ==========")
    print(markdown_report)

    print("========== (B) JSON ==========")
    print(json_output)

    # 2️⃣ 파일 저장
    save_markdown(markdown_report, "report.md")
    print("\n✅ Markdown 파일 'report.md' 저장 완료!")

    save_json(answer, "report.json")
    print("✅ JSON 파일 'report.json' 저장 완료!")