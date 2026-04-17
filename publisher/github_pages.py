import requests
import base64
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GH_TOKEN")
GITHUB_USERNAME = os.getenv("GH_USERNAME")
GITHUB_REPO = os.getenv("GH_PAGES_REPO")


def push_post(title: str, content: str, date: str = None, keywords: list = None) -> bool:
    """마크다운 파일을 GitHub Pages 레포에 push"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    print(f"USERNAME: {GITHUB_USERNAME}")
    print(f"REPO: {GITHUB_REPO}")
    print(f"TOKEN 존재: {'Yes' if GITHUB_TOKEN else 'No'}")
    print(f"GitHub Pages 포스팅 중: {title}")

    # 한글 제거 후 영문 slug 생성
    slug = title.lower()
    slug = ''.join(c for c in slug if c.isascii())
    slug = slug.replace(" ", "-")
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    slug = slug.strip('-')[:50]

    if len(slug) < 5:
        slug = f"tech-trend-{date}"

    filename = f"_posts/{date}-{slug}.md"

    # description 생성
    description = content[:150].replace("\n", " ").replace('"', "'").strip()

    # Jekyll front matter
    file_content = f"""---
layout: post
title: "{title}"
date: {date}
categories: tech-trend
tags: [AI, 기술트렌드, 주식, 실리콘밸리]
description: "{description}"
---

{content}
"""

    encoded = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    # 기존 파일 SHA 확인
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{filename}"
    sha = None
    check = requests.get(url, headers=headers)
    if check.status_code == 200:
        sha = check.json().get("sha")

    data = {
        "message": f"Add post: {title}",
        "content": encoded,
        "branch": "main"
    }

    if sha:
        data["sha"] = sha

    print(f"API URL: {url}")
    response = requests.put(url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        print(f"✅ GitHub Pages 포스팅 완료!")
        print(f"   파일: {filename}")
        return True
    else:
        print(f"❌ 포스팅 실패: {response.status_code} - {response.text}")
        return False


if __name__ == "__main__":
    test_title = "AI Tech Trend Analysis 2026"
    test_content = """
## Today's Tech Trend

AI is changing everything.

## Key Trends

- **AI & LLMs** keep growing
- **Rust** popular in systems programming
- **React** ecosystem evolving

## Wrap Up

Check daily tech trend updates!
"""
    push_post(title=test_title, content=test_content)