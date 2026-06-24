import requests
import base64
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GH_TOKEN")
GITHUB_USERNAME = os.getenv("GH_USERNAME")
GITHUB_REPO = os.getenv("GH_PAGES_REPO")


def push_post(title: str, content: str, date: str = None, keywords: list = None, lang: str = "ko", weekly: bool = False) -> bool:
    """마크다운 파일을 GitHub Pages 레포에 push"""
    now = datetime.now()
    if not date:
        date = now.strftime("%Y-%m-%d")

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

    # YAML 깨짐 방지: 제목·설명의 큰따옴표/특수따옴표를 작은따옴표로 치환
    safe_title = title.replace('"', "'").replace('“', "'").replace('”', "'")

    # description: 첫 번째 일반 텍스트 단락 사용 (TOC/링크/헤딩 제외)
    description = ""
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("-") and not stripped.startswith("|") and not stripped.startswith(">"):
            description = stripped[:120].replace('"', "'").replace('“', "'").replace('”', "'").strip()
            break
    if not description:
        description = content[:120].replace("\n", " ").replace('"', "'").replace('“', "'").replace('”', "'").strip()

    # 같은 날 포스트 순서 구분을 위해 현재 시각 포함
    date_time = now.strftime("%Y-%m-%d %H:%M:%S +0900")

    # 카테고리: 위클리 / 언어별 구분
    if weekly:
        category = "weekly"
    elif lang == "en":
        category = "en"
    else:
        category = "ko"

    # 태그: 분석된 키워드 사용, 없으면 기본값
    if keywords:
        tag_list = keywords[:6]
    else:
        tag_list = ["AI", "Tech", "Trend"]
    tags_yaml = ", ".join(f'"{t}"' for t in tag_list)

    # Jekyll front matter
    file_content = f"""---
layout: post
title: "{safe_title}"
date: {date_time}
lang: {lang}
categories: [tech-trend, {category}]
tags: [{tags_yaml}]
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
    