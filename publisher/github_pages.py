import requests
import base64
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GH_TOKEN")
GITHUB_USERNAME = os.getenv("GH_USERNAME")
GITHUB_REPO = os.getenv("GH_PAGES_REPO")

def push_post(title: str, content: str, date: str = None) -> bool:
    """마크다운 파일을 GitHub Pages 레포에 push"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # 디버깅용 출력
    print(f"USERNAME: {GITHUB_USERNAME}")
    print(f"REPO: {GITHUB_REPO}")
    print(f"TOKEN 존재: {'Yes' if GITHUB_TOKEN else 'No'}")

    print(f"GitHub Pages 포스팅 중: {title}")

    slug = title.lower().replace(" ", "-")[:50]
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    filename = f"_posts/{date}-{slug}.md"

    file_content = f"""---
layout: post
title: "{title}"
date: {date}
categories: tech trends
---

{content}
"""

    encoded = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "message": f"Add post: {title}",
        "content": encoded,
        "branch": "main"
    }

    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{filename}"
    print(f"API URL: {url}")
    
    response = requests.put(url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        print(f"✅ GitHub Pages 포스팅 완료!")
        print(f"   파일: {filename}")
        return True
    else:
        print(f"❌ 포스팅 실패: {response.status_code} - {response.text}")
        return False