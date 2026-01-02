import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

def fetch_naver_ranking_news():
    """
    [네이버] 각 언론사별 랭킹 1위 뉴스만 수집합니다.
    """
    print("🕷️ [Naver] 언론사별 1위 뉴스 수집 중...")
    url = "https://news.naver.com/main/ranking/popularDay.naver"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 언론사별 박스들
        press_boxes = soup.select('.rankingnews_box')
        
        news_list = []
        for box in press_boxes:
            # 1. 언론사 이름
            press_name = box.select_one('.rankingnews_name')
            if press_name:
                press_name = press_name.get_text(strip=True)
            else:
                continue

            # 2. 1위 뉴스 (첫 번째 링크)
            first_news = box.select_one('.list_content > li > a')
            if first_news:
                title = first_news.get_text(strip=True)
                # 출처 표기: [조선일보] 기사제목
                news_list.append(f"[{press_name}] {title}")

        # 너무 많으면 비용 나가니까 20개만 (제목 긴 순서로 정렬해서 알찬 것만)
        news_list.sort(key=len, reverse=True)
        final_list = news_list[:20]
        
        print(f"✅ 네이버 뉴스 {len(final_list)}개 수집 완료")
        return final_list

    except Exception as e:
        print(f"❌ [Naver] 수집 에러: {e}")
        return []

def fetch_policy_api():
    """ 
    [정책브리핑] 공공데이터 API로 정부 정책 뉴스 수집 
    """
    print("🏛️ [Policy] 정책브리핑 API 요청 중...")
    
    api_key = os.environ.get("DATA_GO_KR_KEY")
    if not api_key:
        print("⚠️ 공공데이터 API 키가 없습니다. (.env 확인)")
        return []

    url = "http://apis.data.go.kr/1371000/policyNewsService/getPolicyNewsList"
    params = {
        "serviceKey": api_key,
        "numOfRows": 10,
        "pageNo": 1
    }
    
    try:
        res = requests.get(url, params=params)
        soup = BeautifulSoup(res.content, 'xml') # XML 파싱
        
        items = soup.find_all('item')
        policy_list = []
        
        # 돈 되는 키워드 필터링
        money_keywords = ["지원", "신청", "지급", "환급", "무료", "개시", "특가"]
        
        for item in items:
            title = item.find('title').text
            # 키워드가 있거나, 없으면 그냥 다 가져오기 (정책은 다 좋으니까)
            if any(k in title for k in money_keywords):
                policy_list.append(f"[정부정책] {title}")
            else:
                # 키워드 없어도 최근 3개는 무조건 포함
                if len(policy_list) < 3:
                    policy_list.append(f"[정부정책] {title}")
                    
        print(f"✅ 정책 뉴스 {len(policy_list)}개 수집 완료")
        return policy_list

    except Exception as e:
        print(f"❌ [Policy] API 에러: {e}")
        return []
