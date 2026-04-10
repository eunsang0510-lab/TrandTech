from collector.hacker_news import get_top_stories
from collector.github_trending import get_trending_repos
from analyzer.claude_analyzer import analyze_trends, generate_blog_post, generate_blog_post_en
from publisher.github_pages import push_post
from datetime import datetime

def run():
    """전체 파이프라인 실행"""
    print("=" * 50)
    print(f"🚀 기술 트렌드 블로그 자동화 시작")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    try:
        # 1. 데이터 수집
        stories = get_top_stories(limit=30)
        repos = get_trending_repos(limit=20)

        # 2. AI 분석
        analysis = analyze_trends(stories, repos)

        # 3. 한글 블로그 글 생성 및 포스팅
        post_kr = generate_blog_post(analysis, stories, repos)
        push_post(
            title=post_kr["title"],
            content=post_kr["content"],
            date=datetime.now().strftime("%Y-%m-%d")
        )

        # 4. 영어 블로그 글 생성 및 포스팅
        post_en = generate_blog_post_en(analysis, stories, repos)
        push_post(
            title=post_en["title"],
            content=post_en["content"],
            date=datetime.now().strftime("%Y-%m-%d")
        )

        print("=" * 50)
        print(f"🎉 전체 파이프라인 완료!")
        print(f"📝 한글 제목: {post_kr['title']}")
        print(f"📝 영어 제목: {post_en['title']}")
        print("=" * 50)

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        raise e

if __name__ == "__main__":
    run()