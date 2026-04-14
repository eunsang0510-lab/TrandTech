import requests
import base64
import os
from datetime import datetime
from dotenv import load_dotenv
from publisher.image_generator import generate_og_image

load_dotenv()

GITHUB_TOKEN = os.getenv("GH_TOKEN")
GITHUB_USERNAME = os.getenv("GH_USERNAME")
GITHUB_REPO = os.getenv("GH_PAGES_REPO")


def push_image(image_path: str, date: str) -> bool:
    """이미지를 GitHub Pages 레포에 업로드"""
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    filename = f"assets/images/og-{date}.png"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "message": f"Add OG image: {date}",
        "content": encoded,
        "branch": "main"
    }

    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{filename}"
    response = requests.put(url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        print(f"✅ OG 이미지 업로드 완료: {filename}")
        return True
    else:
        print(f"❌ 이미지 업로드 실패: {response.status_code}")
        return False


def push_post(title: str, content: str, date: str = None, keywords: list = None) -> bool:
    """마크다운 파일을 GitHub Pages 레포에 push"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    print(f"USERNAME: {GITHUB_USERNAME}")
    print(f"REPO: {GITHUB_REPO}")
    print(f"TOKEN 존재: {'Yes' if GITHUB_TOKEN else 'No'}")
    print(f"GitHub Pages 포스팅 중: {title}")

    # OG 이미지 생성 및 업로드
    og_image_path = generate_og_image(
        title=title,
        date=date.replace("-", "."),
        keywords=keywords or []
    )
    push_image(og_image_path, date)
    og_image_url = f"/assets/images/og-{date}.png"

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
og_image: "{og_image_url}"
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


if __name__ == "__main__":
    test_title = "AI와 클라우드의 융합: 2026년 기술 트렌드"
    test_content = """
## 오늘의 기술 트렌드

AI가 모든 것을 바꾸고 있습니다.

## 주요 트렌드

- **AI & LLMs** 계속 성장 중
- **Rust** 시스템 프로그래밍에서 인기
- **React** 생태계 계속 진화

## 마무리

매일 업데이트되는 기술 트렌드를 확인하세요!
"""
    push_post(
        title=test_title,
        content=test_content,
        keywords=["AI", "클라우드", "머신러닝"]
    )