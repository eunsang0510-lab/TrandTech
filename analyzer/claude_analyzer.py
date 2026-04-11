from groq import Groq
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_trends(stories: list, repos: list) -> dict:
    """수집한 데이터를 Groq로 분석"""
    print("Groq AI 트렌드 분석 중...")

    hn_text = "\n".join([f"- {s['title']} (score: {s['score']})" for s in stories[:20]])
    gh_text = "\n".join([f"- {r['title']} (stars: {r['score']})" for r in repos[:20]])

    prompt = f"""
오늘 수집한 기술 트렌드 데이터입니다.

[Hacker News 상위 글]
{hn_text}

[GitHub Trending 저장소]
{gh_text}

위 데이터를 분석해서 아래 JSON 형식으로만 응답해주세요. 다른 텍스트 없이 JSON만 출력하세요.

{{
  "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],
  "summary": "오늘 기술 트렌드 전체 요약 (2~3문장)",
  "hot_topics": ["주목할 토픽1", "주목할 토픽2", "주목할 토픽3"]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7
    )

    text = response.choices[0].message.content.strip()

    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    result = json.loads(text)
    print(f"✅ 트렌드 분석 완료! 키워드: {result['keywords']}")
    return result


def generate_blog_post(analysis: dict, stories: list, repos: list) -> dict:
    """한글 블로그 글 생성"""
    print("블로그 글 생성 중...")

    keywords = ", ".join(analysis["keywords"])
    hot_topics = "\n".join([f"- {t}" for t in analysis["hot_topics"]])
    hn_text = "\n".join([f"- [{s['score']}점] {s['title']}" for s in stories[:10]])
    gh_text = "\n".join([f"- ⭐{r['score']} {r['title']}" for r in repos[:10]])

    prompt = f"""
당신은 IT 기술 트렌드 블로그 작가입니다.
아래 데이터를 바탕으로 한국어 블로그 글을 작성해주세요.

[오늘의 키워드]
{keywords}

[주목할 토픽]
{hot_topics}

[Hacker News 인기글]
{hn_text}

[GitHub Trending]
{gh_text}

[작성 조건]
- 제목은 클릭하고 싶은 매력적인 한국어 제목
- 분량은 1500자 이상
- 구성: 도입부 → 주요 트렌드 분석 → 각 토픽 상세 설명 → 마무리
- IT 기획자/개발자가 읽기 좋은 인사이트 포함
- HTML 태그 없이 일반 텍스트로 작성
- 맨 첫 줄에 제목만 출력하고 두 번째 줄부터 본문 시작
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000,
        temperature=0.8
    )

    content = response.choices[0].message.content.strip()
    lines = content.strip().split("\n")
    title = lines[0].strip()
    body = "\n".join(lines[1:]).strip()

    print(f"✅ 블로그 글 생성 완료! 제목: {title}")
    return {"title": title, "content": body}


def generate_blog_post_en(analysis: dict, stories: list, repos: list) -> dict:
    """영어 블로그 글 생성"""
    print("영어 블로그 글 생성 중...")

    keywords = ", ".join(analysis["keywords"])
    hot_topics = "\n".join([f"- {t}" for t in analysis["hot_topics"]])
    hn_text = "\n".join([f"- [{s['score']} pts] {s['title']}" for s in stories[:10]])
    gh_text = "\n".join([f"- ⭐{r['score']} {r['title']}" for r in repos[:10]])

    prompt = f"""
You are a tech trend blog writer for developers.
Write an English blog post based on the data below.

[Today's Keywords]
{keywords}

[Hot Topics]
{hot_topics}

[Hacker News Top Posts]
{hn_text}

[GitHub Trending]
{gh_text}

[Requirements]
- Attractive title that developers want to click
- At least 800 words
- Structure: Intro → Key Trends → Detailed Topics → Wrap-up
- Include actionable insights for developers and tech PMs
- Use markdown formatting
- First line is the title only, body starts from second line
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000,
        temperature=0.8
    )

    content = response.choices[0].message.content.strip()
    lines = content.strip().split("\n")
    title = lines[0].strip()
    body = "\n".join(lines[1:]).strip()

    print(f"✅ 영어 블로그 글 생성 완료! 제목: {title}")
    return {"title": title, "content": body}

def generate_stock_analysis(analysis: dict) -> str:
    """기술 트렌드 기반 주식 분석 생성"""
    print("주식 분석 생성 중...")

    keywords = ", ".join(analysis["keywords"])
    hot_topics = "\n".join([f"- {t}" for t in analysis["hot_topics"]])

    prompt = f"""
당신은 기술 트렌드 기반 주식 분석가입니다.
오늘의 기술 트렌드를 바탕으로 유망 주식을 분석해주세요.

[오늘의 기술 트렌드 키워드]
{keywords}

[주목할 토픽]
{hot_topics}

아래 형식으로 작성해주세요.

## 📈 오늘의 Tech Trend 기반 유망 주식 분석

### 🇺🇸 미국 주식 TOP 10

| 종목명 | 티커 | 선정 이유 | 주목 포인트 |
|---|---|---|---|
| (종목명) | (티커) | (트렌드 연관성 한 줄) | (주목할 점 한 줄) |
... 10개 작성

### 🇰🇷 한국 주식 TOP 10

| 종목명 | 티커 | 선정 이유 | 주목 포인트 |
|---|---|---|---|
| (종목명) | (티커) | (트렌드 연관성 한 줄) | (주목할 점 한 줄) |
... 10개 작성

### ⚠️ 투자 유의사항
본 포스팅은 투자 참고용 정보이며 투자 권유가 아닙니다. 
투자 결정은 본인 책임이며, 투자 전 반드시 전문가와 상담하시기 바랍니다.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000,
        temperature=0.7
    )

    result = response.choices[0].message.content.strip()
    print("✅ 주식 분석 생성 완료!")
    return result