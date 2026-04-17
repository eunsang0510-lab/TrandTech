import anthropic
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_trends(stories: list, repos: list) -> dict:
    """수집한 데이터를 Claude로 분석"""
    print("Claude AI 트렌드 분석 중...")

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

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = message.content[0].text.strip()

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
- 맨 첫 줄에 제목만 출력하고 두 번째 줄부터 본문 시작
- 본문 시작 전 아래 형식으로 목차 추가
  ## 목차
  - [섹션1](#섹션1)
  - [섹션2](#섹션2)
  ...
- 구성: 도입부 → 주요 트렌드 분석 → 각 토픽 상세 설명 → 마무리
- 각 섹션은 ## 헤딩으로 구분
- IT 기획자/개발자가 읽기 좋은 인사이트 포함
- HTML 태그 없이 마크다운으로 작성
"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    content = message.content[0].text.strip()
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

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    content = message.content[0].text.strip()
    lines = content.strip().split("\n")
    title = lines[0].strip()
    body = "\n".join(lines[1:]).strip()

    print(f"✅ 영어 블로그 글 생성 완료! 제목: {title}")
    return {"title": title, "content": body}

def generate_stock_analysis(analysis: dict, region: str = "미국") -> str:
    """기술 트렌드 기반 주식 분석 생성"""
    print("주식 분석 생성 중...")

    keywords = ", ".join(analysis["keywords"])
    hot_topics = "\n".join([f"- {t}" for t in analysis["hot_topics"]])

    # 지역별 증시 정보
    region_market = {
        "미국": {"market": "나스닥/NYSE", "currency": "USD", "flag": "🇺🇸"},
        "한국": {"market": "코스피/코스닥", "currency": "KRW", "flag": "🇰🇷"},
        "유럽": {"market": "유로스톡스/FTSE", "currency": "EUR", "flag": "🇪🇺"},
        "중국": {"market": "상하이/선전", "currency": "CNY", "flag": "🇨🇳"},
        "인도": {"market": "BSE/NSE", "currency": "INR", "flag": "🇮🇳"},
    }

    info = region_market.get(region, region_market["미국"])

    prompt = f"""
당신은 기술 트렌드 기반 글로벌 주식 분석가입니다.
오늘은 {info['flag']} {region} 관점에서 유망 주식을 분석해주세요.

[오늘의 기술 트렌드 키워드]
{keywords}

[주목할 토픽]
{hot_topics}

[주의사항]
- 반도체 관련주만 추천하지 말고 전력, 전선, 데이터센터, ESS, 배터리, 냉각시스템 등 다양한 섹터 고려
- 특정 산업에 편중되지 않고 골고루 선정

아래 형식으로 작성해주세요.

## 📈 오늘의 Tech Trend 기반 유망 주식 분석

### {info['flag']} {region} 주식 TOP 10 ({info['market']})

| 종목명 | 티커 | 섹터 | 선정 이유 | 주목 포인트 |
|---|---|---|---|---|
| (종목명) | (티커) | (섹터) | (트렌드 연관성 한 줄) | (주목할 점 한 줄) |

> 섹터 다양성 확보: 반도체, 전력/전선, 데이터센터, ESS/배터리, 소프트웨어 등 골고루 선정

### 🇰🇷 한국 주식 TOP 10 (코스피/코스닥)

| 종목명 | 티커 | 섹터 | 선정 이유 | 주목 포인트 |
|---|---|---|---|---|
| (종목명) | (티커) | (섹터) | (트렌드 연관성 한 줄) | (주목할 점 한 줄) |

> 섹터 다양성 확보: 반도체, 전력/전선, 데이터센터, ESS/배터리, 소프트웨어 등 골고루 선정

### 🚀 유망 스타트업 TOP 10

| 스타트업명 | 국가 | 분야 | 주목 이유 |
|---|---|---|---|
| (스타트업명) | (국가) | (분야) | (주목할 이유 한 줄) |

### ⚠️ 투자 유의사항
본 포스팅은 투자 참고용 정보이며 투자 권유가 아닙니다.
투자 결정은 본인 책임이며, 투자 전 반드시 전문가와 상담하시기 바랍니다.
"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    result = message.content[0].text.strip()
    print("✅ 주식 분석 생성 완료!")
    return result


def generate_silicon_valley_ads_section(analysis: dict, ads: list) -> str:
    """실리콘밸리 광고판 분석 섹션 생성"""
    print("실리콘밸리 광고판 분석 생성 중...")

    keywords = ", ".join(analysis["keywords"])
    ads_text = "\n".join([f"- {a['title']} ({a['url']})" for a in ads[:10]])

    prompt = f"""
당신은 실리콘밸리 기술 트렌드 분석가입니다.
오늘의 기술 트렌드와 실리콘밸리 광고판 관련 뉴스를 바탕으로 분석 섹션을 작성해주세요.

[오늘의 기술 트렌드 키워드]
{keywords}

[실리콘밸리 광고판 관련 뉴스]
{ads_text if ads_text else "최근 수집된 광고판 뉴스가 없습니다. 일반적인 실리콘밸리 광고 트렌드를 분석해주세요."}

아래 형식으로 작성해주세요.

## 🗽 실리콘밸리 광고판으로 보는 Tech Trend

실리콘밸리 101번 고속도로 광고판은 IT 업계의 바로미터입니다.
어떤 기업이 광고판을 샀느냐를 보면 지금 어떤 기술이 핫한지 알 수 있어요.

### 📋 이번 주 주목할 광고판 트렌드
(광고판에 등장한 기업/기술 분석 3~5개)

### 💡 광고판이 말해주는 투자 인사이트
(광고판 트렌드에서 읽을 수 있는 투자/기술 인사이트)

### 🔮 다음에 광고판에 등장할 기술은?
(예측 2~3가지)
"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    result = message.content[0].text.strip()
    print("✅ 실리콘밸리 광고판 분석 생성 완료!")
    return result


def generate_weekly_trend_report(analysis: dict, news: list, ads: list) -> dict:
    """주간 트렌드 변화 분석 특별 포스팅 생성"""
    print("주간 트렌드 변화 분석 생성 중...")

    keywords = ", ".join(analysis["keywords"])
    news_text = "\n".join([f"- {n['title']}" for n in news[:15]])
    ads_text = "\n".join([f"- {a['title']}" for a in ads[:10]])

    prompt = f"""
당신은 실리콘밸리 기술 트렌드 전문 분석가입니다.
이번 주 수집된 뉴스와 실리콘밸리 광고판 데이터를 바탕으로
트렌드 변화를 분석하는 특별 주간 리포트를 작성해주세요.

[이번 주 기술 키워드]
{keywords}

[이번 주 주요 뉴스]
{news_text}

[실리콘밸리 광고판 관련 뉴스]
{ads_text if ads_text else "광고판 관련 뉴스 없음. 일반적인 실리콘밸리 트렌드 기반으로 분석해주세요."}

아래 형식으로 작성해주세요.

## 📊 이번 주 Tech Trend 변화 리포트

### 🔥 변화하고 있다 — 이미 바뀌기 시작한 트렌드
(구체적인 근거와 함께 2~3가지)

### ⏳ 아직 변하지 않았다 — 여전히 유효한 트렌드
(구체적인 근거와 함께 2~3가지)

### 🔮 변할 것 같다 — 다음 주 주목할 변화 신호
(구체적인 근거와 함께 2~3가지)

### 💡 실리콘밸리 광고판이 말해주는 것
(광고판 트렌드와 연결한 인사이트)

### 📌 이번 주 핵심 요약
(3줄 요약)
"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    content = message.content[0].text.strip()
    lines = content.strip().split("\n")

    # 제목 생성
    today = datetime.now().strftime("%Y년 %m월 %d일")
    title = f"[주간 리포트] {today} Tech Trend 변화 분석"

    print(f"✅ 주간 트렌드 리포트 생성 완료!")
    return {"title": title, "content": content}


def generate_blog_post_by_region(analysis: dict, stories: list, repos: list, region: str) -> dict:
    """지역별 블로그 글 생성"""
    print(f"{region} 지역 블로그 글 생성 중...")

    region_info = {
        "미국": {
            "ko": "미국",
            "en": "US",
            "focus": "실리콘밸리, 빅테크, 나스닥, 미국 스타트업 생태계 중심으로",
            "emoji": "🇺🇸"
        },
        "한국": {
            "ko": "한국",
            "en": "Korea",
            "focus": "한국 IT 기업, 코스피/코스닥, K-스타트업, 삼성/네이버/카카오 등 중심으로",
            "emoji": "🇰🇷"
        },
        "유럽": {
            "ko": "유럽",
            "en": "Europe",
            "focus": "유럽 테크 생태계, EU AI 규제, 독일/영국/프랑스 스타트업 중심으로",
            "emoji": "🇪🇺"
        },
        "중국": {
            "ko": "중국",
            "en": "China",
            "focus": "중국 빅테크, 알리바바/텐센트/화웨이, 중국 AI 발전 현황 중심으로",
            "emoji": "🇨🇳"
        },
        "인도": {
            "ko": "인도",
            "en": "India",
            "focus": "인도 IT 아웃소싱, 벵갈루루 스타트업, 인도 디지털 전환 중심으로",
            "emoji": "🇮🇳"
        }
    }

    info = region_info.get(region, region_info["미국"])
    keywords = ", ".join(analysis["keywords"])
    hot_topics = "\n".join([f"- {t}" for t in analysis["hot_topics"]])
    hn_text = "\n".join([f"- [{s['score']}점] {s['title']}" for s in stories[:10]])
    gh_text = "\n".join([f"- ⭐{r['score']} {r['title']}" for r in repos[:10]])

    prompt = f"""
당신은 글로벌 IT 기술 트렌드 블로그 작가입니다.
오늘은 {info['emoji']} {region} 관점에서 기술 트렌드를 분석하는 글을 작성해주세요.

[오늘의 키워드]
{keywords}

[주목할 토픽]
{hot_topics}

[Hacker News 인기글]
{hn_text}

[GitHub Trending]
{gh_text}

[작성 조건]
- 제목은 반드시 "{info['emoji']} [{region} Tech Trend]" 로 시작하는 매력적인 한국어 제목
- {info['focus']} 분석해주세요
- 분량은 1500자 이상
- 맨 첫 줄에 제목만 출력하고 두 번째 줄부터 본문 시작
- 본문 시작 전 아래 형식으로 목차 추가
  ## 목차
  - [섹션1](#섹션1)
  - [섹션2](#섹션2)
- 구성: 도입부 → {region} 기술 트렌드 분석 → 주목할 기업/기술 → 마무리
- 각 섹션은 ## 헤딩으로 구분
- IT 기획자/개발자가 읽기 좋은 인사이트 포함
- HTML 태그 없이 마크다운으로 작성
"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    content = message.content[0].text.strip()
    lines = content.strip().split("\n")
    title = lines[0].strip()
    body = "\n".join(lines[1:]).strip()

    print(f"✅ {region} 블로그 글 생성 완료! 제목: {title}")
    return {"title": title, "content": body}