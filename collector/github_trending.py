import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_trending_repos(language="", since="daily", limit=20):
    """GitHub Trending 저장소 수집"""
    print("GitHub Trending 수집 중...")

    url = f"https://github.com/trending/{language}?since={since}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")

    repos = []
    repo_list = soup.select("article.Box-row")[:limit]

    for repo in repo_list:
        try:
            # 저장소 이름
            name_tag = repo.select_one("h2 a")
            name = name_tag.get_text(strip=True).replace("\n", "").replace(" ", "") if name_tag else ""

            # 설명
            desc_tag = repo.select_one("p")
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            # 언어
            lang_tag = repo.select_one("[itemprop='programmingLanguage']")
            language_name = lang_tag.get_text(strip=True) if lang_tag else "Unknown"

            # 스타 수
            star_tag = repo.select("a.Link--muted")
            stars = star_tag[0].get_text(strip=True).replace(",", "") if star_tag else "0"

            url_path = name_tag["href"] if name_tag else ""

            repos.append({
                "source": "github_trending",
                "title": f"{name} - {description}",
                "url": f"https://github.com{url_path}",
                "score": int(stars) if stars.isdigit() else 0,
                "language": language_name,
                "collected_at": datetime.now()
            })
        except Exception as e:
            print(f"저장소 수집 오류: {e}")
            continue

    print(f"✅ GitHub Trending {len(repos)}개 수집 완료!")
    return repos


if __name__ == "__main__":
    repos = get_trending_repos()
    for r in repos[:5]:
        print(f"[{r['language']}] {r['title']}")
        print(f"  ⭐ {r['score']} | {r['url']}\n")