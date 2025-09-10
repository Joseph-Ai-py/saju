from dotenv import load_dotenv
import os
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))

class InputInfo(BaseModel): # 입력 정보
    name: str = Field(description="이름")
    birth_date: str = Field(description="출생일, YYYY-MM-DD")
    birth_time: str = Field(description="출생 시간, HH:MM")
    timezone: str = Field(description="출생 시간대, 예: Asia/Seoul")
    birth_place: str = Field(description="출생지")
    gender: str = Field(description="성별")
    calendar_type: str = Field(description="달력 종류, 양력 또는 음력")
    analysis_date: str = Field(description="분석 기준 날짜")

class StemBranch(BaseModel): # 천간과 지지
    stem: str = Field(description="천간")
    branch: str = Field(description="지지")

class WonGuk(BaseModel): # 사주 원국
    year: StemBranch = Field(description="연주")
    month: StemBranch = Field(description="월주")
    day: StemBranch = Field(description="일주")
    hour: StemBranch = Field(description="시주")

class HiddenStem(BaseModel): # 숨은 천간
    stem: str = Field(description="숨은 천간")
    weight: float = Field(description="가중치")

class ElementBalance(BaseModel): # 오행 균형
    raw: float = Field(description="원시 값")
    percent: float = Field(description="백분율")

class FiveElements(BaseModel): # 오행 분석
    wood: ElementBalance = Field(description="목")
    fire: ElementBalance = Field(description="화")
    earth: ElementBalance = Field(description="토")
    metal: ElementBalance = Field(description="금")
    water: ElementBalance = Field(description="수")
    yin_percent: float = Field(description="음의 비율")
    yang_percent: float = Field(description="양의 비율")
    balance_index: float = Field(description="균형 지수")
    dominant: Dict[str, Any] = Field(description="과다한 오행")
    deficient: Dict[str, Any] = Field(description="부족한 오행")

class TenGod(BaseModel): # 십신 분석
    raw: int = Field(description="원시 값")
    weighted: float = Field(description="가중치")
    percent: float = Field(description="백분율")

class SpecialPattern(BaseModel): # 특수 패턴
    pattern: str = Field(description="특수 패턴")
    branches: List[str] = Field(description="해당 지지들")
    meaning: str = Field(description="의미")

class YongShinCandidate(BaseModel): # 용신 후보
    element: str = Field(description="용신 후보 오행")
    score: float = Field(description="점수")
    reason: str = Field(description="선정 이유")

class CharacterTalents(BaseModel): # 성격 및 재능
    summary: str = Field(description="성격 및 재능 요약")
    evidence: List[str] = Field(description="근거들")

class CareerScore(BaseModel): # 직업군 점수
    career_group: str = Field(description="직업군")
    score: float = Field(description="점수")

class CalculationLog(BaseModel): # 계산 로그
    weights: Dict[str, float] = Field(description="계산에 사용된 가중치들")
    formulas: Dict[str, str] = Field(description="계산에 사용된 공식들")
    assumptions: str = Field(description="계산에 사용된 가정들")

class SaJuReport(BaseModel): # 사주 명리 분석 리포트
    markdown_report: str = Field(description="사람이 읽을 수 있는 Markdown 리포트 (2000자 이상)")
    input: InputInfo = Field(description="사용자 입력 정보")
    won_guk: WonGuk = Field(description="사주 원국")
    hidden_stems: Dict[str, List[HiddenStem]] = Field(description="각 지지별 숨은 천간들")
    five_elements: FiveElements = Field(description="오행 분석")
    ten_gods: Dict[str, TenGod] = Field(description="십신 분석")
    special_patterns: List[SpecialPattern] = Field(description="특수 패턴들")
    yong_shin_candidates: List[YongShinCandidate] = Field(description="용신 후보들")
    character_and_talents: CharacterTalents = Field(description="성격 및 재능 분석")
    career_scores: List[CareerScore] = Field(description="직업군 점수들")
    calculation_log: CalculationLog = Field(description="계산 로그")
    content: str = Field(description="JSON 내부에 저장되는 동일한 2000자 이상 서술형 해설")

parser = JsonOutputParser(pydantic_object=SaJuReport)

def load_template(file_path="template.md"):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

template = load_template('template.md')

prompt = PromptTemplate(
    template=template,
    input_variables=["name", "country", "city", "yyyymmdd_hhmm", "sex"],
    partial_variables={"today": datetime.today().date()},
)

prompt_partial = prompt.partial(format_instructions=parser.get_format_instructions())
chain = prompt_partial | llm | parser
