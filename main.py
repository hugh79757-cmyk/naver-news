import os
from dotenv import load_dotenv
from src import crawler, analyzer, builder

# .env 파일에서 환경변수 로드 (로컬 실행용)
load_dotenv()

def main():
    print("🚀 뉴스 봇 가동 시작...")
    
    all_headlines = []

    # 1. 네이버 뉴스 수집 (실패해도 계속 진행)
    naver_news = crawler.fetch_naver_ranking_news()
    if naver_news:
        all_headlines.extend(naver_news)
    else:
        print("⚠️ 네이버 뉴스 수집 실패 (건너뜀)")

    # 2. 정책브리핑 수집 (독립 실행)
    policy_news = crawler.fetch_policy_api()
    if policy_news:
        all_headlines.extend(policy_news)
    else:
        print("⚠️ 정책브리핑 수집 실패 (건너뜀)")

    # 3. 데이터가 하나라도 있으면 분석 시작
    if not all_headlines:
        print("❌ 수집된 뉴스가 전혀 없습니다. 종료합니다.")
        return

    print(f"📊 총 {len(all_headlines)}개의 헤드라인을 분석합니다.")
    
    # ... (이후 분석 및 빌드 코드는 그대로)

        # ... (네이버 수집 코드 아래에 추가)
    
    # 3. 다음 뉴스 수집 (New!)
    daum_news = crawler.fetch_daum_news()
    if daum_news:
        all_headlines.extend(daum_news)
    else:
        print("⚠️ 다음 뉴스 수집 실패 (건너뜀)")

