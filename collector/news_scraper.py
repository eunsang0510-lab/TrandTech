import requests
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_tech_news() -> list:
    """기술 관련 최신 뉴스 수집"""
    print("기술 뉴스 수집 중...")

    news = []

    # Hacker News 알고리아 검색 API로 최근 7일 뉴스 수집
    search_terms = [
        "AI trend 2026",
        "tech layoffs 2026",
        "startup funding 2026",
        "silicon valley billboard",
        "big tech announcement"
    ]

    for term in search_terms:
        try:
            url = f"https://hn.algolia.com/api/v1/search?query={term}&tags=story&hitsPerPage=5&numericFilters=created_at_i>%d" % (
                int(datetime.now().timestamp()) - 7 * 24 * 60 * 60
            )
            response = requests.get(url, verify=False, timeout=10)
            data = response.json()

            for hit in data.get("hits", []):
                if hit.get("title"):
                    news.append({
                        "title": hit.get("title", ""),
                        "url": hit.get("url", ""),
                        "score": hit.get("points", 0),
                        "date": hit.get("created_at", "")
                    })
        except Exception as e:
            print(f"뉴스 수집 오류: {e}")
            continue

    print(f"✅ 기술 뉴스 {len(news)}개 수집 완료!")
    return news[:20]