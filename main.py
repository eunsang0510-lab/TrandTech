from collector.hacker_news import get_top_stories
from collector.github_trending import get_trending_repos
from collector.silicon_valley_ads import get_silicon_valley_ads
from collector.news_scraper import get_tech_news
from analyzer.claude_analyzer import (
    analyze_trends,
    generate_blog_post,
    generate_blog_post_en,
    generate_stock_analysis,
    generate_silicon_valley_ads_section,
    generate_weekly_trend_report
)
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
        ads = get_silicon_valley_ads()
        news = get_tech_news()

        # 2. AI 분석
        analysis = analyze_trends(stories, repos)

        # 3. 주식 분석 생성
        stock_analysis = generate_stock_analysis(analysis)

        # 4. 실리콘밸리 광고판 분석 생성
        sv_ads_section = generate_silicon_valley_ads_section(analysis, ads)

        # 5. 한글 블로그 글 생성 및 포스팅
        post_kr = generate_blog_post(analysis, stories, repos)
        full_content_kr = (
            post_kr["content"] + "\n\n"
            + sv_ads_section + "\n\n"
            + stock_analysis
        )
        push_post(
            title=post_kr["title"],
            content=full_content_kr,
            date=datetime.now().strftime("%Y-%m-%d")
        )

        # 6. 영어 블로그 글 생성 및 포스팅
        post_en = generate_blog_post_en(analysis, stories, repos)
        full_content_en = (
            post_en["content"] + "\n\n"
            + sv_ads_section + "\n\n"
            + stock_analysis
        )
        push_post(
            title=post_en["title"],
            content=full_content_en,
            date=datetime.now().strftime("%Y-%m-%d")
        )

        # 7. 매주 월요일 주간 트렌드 리포트 발행
        if datetime.now().weekday() == 0:  # 0 = 월요일        
            print("📅 오늘은 월요일! 주간 트렌드 리포트 생성 중...")
            weekly_report = generate_weekly_trend_report(analysis, news, ads)
            push_post(
                title=weekly_report["title"],
                content=weekly_report["content"],
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