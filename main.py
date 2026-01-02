import os
from dotenv import load_dotenv
from src import crawler, analyzer, builder
from src.naver_api import NaverAPI

load_dotenv()

def main():
    print("=" * 60)
    print("🚀 블로그 키워드 분석 봇 시작")
    print("=" * 60)
    
    all_headlines = []

    # 1. 네이버 뉴스 수집
    print("\n[1/8] 네이버 랭킹 뉴스 수집 중...")
    naver_news = crawler.fetch_naver_ranking_news()
    if naver_news:
        all_headlines.extend(naver_news)
        print(f"    ✅ {len(naver_news)}개 수집 완료")
    else:
        print("    ⚠️  수집 실패")

    # 2. 네이버 메인 (백업)
    if not naver_news:
        print("\n[2/8] 네이버 메인 헤드라인 수집 중 (백업)...")
        naver_main = crawler.fetch_naver_main_headlines()
        if naver_main:
            all_headlines.extend(naver_main)

    # 3. 정책브리핑 수집
    print("\n[3/8] 정책브리핑 수집 중...")
    policy_news = crawler.fetch_policy_api()
    if policy_news:
        all_headlines.extend(policy_news)

    # 4. 다음 뉴스 수집
    print("\n[4/8] 다음 뉴스 수집 중...")
    daum_news = crawler.fetch_daum_news()
    if daum_news:
        all_headlines.extend(daum_news)

    # 5. 데이터 검증
    print("\n[5/8] 데이터 검증 중...")
    if not all_headlines:
        print("    ❌ 수집된 뉴스가 없습니다.")
        print("\n💡 해결 방법:")
        print("   1. 인터넷 연결 확인")
        print("   2. 뉴스 사이트 접속 가능 여부 확인")
        print("   3. 나중에 다시 시도")
        return
    
    print(f"    ✅ 총 {len(all_headlines)}개 헤드라인 수집 완료")
    
    # 중복 제거
    all_headlines = list(set(all_headlines))
    print(f"    🔄 중복 제거 후: {len(all_headlines)}개")

    # 6. Claude AI 키워드 추출
    print("\n[6/8] Claude AI 키워드 추출 중...")
    print("    ⏳ AI 분석 중... (약 10-20초 소요)")
    
    keywords = analyzer.analyze_headlines(all_headlines)
    
    if not keywords:
        print("    ❌ 키워드 추출 실패")
        return
    
    print(f"    ✅ {len(keywords)}개 키워드 추출 완료!")

    # 7. 네이버 API로 키워드 분석
    print("\n[7/8] 네이버 API 키워드 분석 중...")
    naver_api = NaverAPI()
    keyword_results = naver_api.analyze_keywords(keywords)
    
    if not keyword_results:
        print("    ❌ 키워드 분석 실패")
        return

    # 8. HTML 파일 생성
    print("\n[8/8] HTML 리포트 생성 중...")
    keyword_report = builder.build_keyword_report(keyword_results)
    builder.build_html_file(keyword_report, keyword_results)
    
    print("\n" + "=" * 60)
    print("✨ 모든 작업 완료!")
    print("📂 결과 파일: output/index.html")
    print("=" * 60)

if __name__ == "__main__":
    main()
