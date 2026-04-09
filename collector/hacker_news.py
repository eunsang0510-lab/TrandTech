import requests
import urllib3
from datetime import datetime

# SSL 경고 메시지 숨기기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_top_stories(limit=30):
    """Hacker News 상위 스토리 수집"""
    print("Hacker News 수집 중...")

    # 상위 스토리 ID 목록 가져오기
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(url, verify=False)
    story_ids = response.json()[:limit]

    stories = []
    for story_id in story_ids:
        try:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story = requests.get(story_url, verify=False).json()

            if story.get("type") == "story" and story.get("url"):
                stories.append({
                    "source": "hackernews",
                    "title": story.get("title", ""),
                    "url": story.get("url", ""),
                    "score": story.get("score", 0),
                    "collected_at": datetime.now()
                })
        except Exception as e:
            print(f"스토리 수집 오류: {e}")
            continue

    print(f"✅ Hacker News {len(stories)}개 수집 완료!")
    return stories


if __name__ == "__main__":
    stories = get_top_stories()
    for s in stories[:5]:
        print(f"[{s['score']}] {s['title']}")
        print(f"  {s['url']}\n")