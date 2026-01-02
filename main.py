import os
from dotenv import load_dotenv
from src import crawler, analyzer, builder

# .env 파일에서 환경변수 로드 (로컬 실행용)
load_dotenv()

def main():
    print("🚀 뉴스 봇 가동 시작...")
    
    # 1. 뉴스 수집
    headlines = crawler.fetch_naver_ranking_news()
    if not headlines:
        print("❌ 뉴스 수집 실패로 종료합니다.")
        return

    # 2. AI 분석
    ai_report = analyzer.analyze_headlines(headlines)
    
    # 3. 웹사이트 생성
    builder.build_html_file(ai_report)
    
    print("🎉 모든 작업이 완료되었습니다.")

if __name__ == "__main__":
    main()