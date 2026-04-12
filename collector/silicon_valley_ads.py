import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_silicon_valley_ads() -> list:
    """실리콘밸리 광고판 관련 최신 뉴스 수집"""
    print("실리콘밸리 광고판 뉴스 수집 중...")

    ads = []

    # Hacker News에서 실리콘밸리 광고 관련 검색
    search_terms = [
        "billboard silicon valley",
        "highway 101 advertisement tech",
        "san francisco billboard startup"
    ]

    for term in search_terms:
        try:
            url = f"https://hn.algolia.com/api/v1/search?query={term}&tags=story&hitsPerPage=5"
            response = requests.get(url, verify=False, timeout=10)
            data = response.json()

            for hit in data.get("hits", []):
                if hit.get("url"):
                    ads.append({
                        "title": hit.get("title", ""),
                        "url": hit.get("url", ""),
                        "score": hit.get("points", 0),
                        "source": "hackernews_search"
                    })
        except Exception as e:
            print(f"수집 오류: {e}")
            continue

    print(f"✅ 실리콘밸리 광고 관련 뉴스 {len(ads)}개 수집 완료!")
    return ads[:10]


if __name__ == "__main__":
    ads = get_silicon_valley_ads()
    for ad in ads:
        print(f"- {ad['title']}")
        print(f"  {ad['url']}\n")