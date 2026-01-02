import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import time

load_dotenv()

def fetch_naver_ranking_news():
    """네이버 언론사별 랭킹 1위 뉴스 수집"""
    print("    🕷️  [Naver] 크롤링 시작...")
    url = "https://news.naver.com/main/ranking/popularDay.naver"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.naver.com/",
        "Accept-Language": "ko-KR,ko;q=0.9"
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        press_boxes = soup.select('.rankingnews_box')
        if not press_boxes:
            print("    ⚠️  [Naver] 뉴스 박스를 찾을 수 없습니다.")
            return []
        
        news_list = []
        for box in press_boxes:
            press_name = box.select_one('.rankingnews_name')
            if not press_name:
                continue
            press_name = press_name.get_text(strip=True)

            first_news = box.select_one('.list_content > li > a')
            if first_news:
                title = first_news.get_text(strip=True)
                news_list.append(f"[{press_name}] {title}")

        # 제목 길이순 정렬 후 상위 20개
        news_list.sort(key=len, reverse=True)
        final_list = news_list[:20]
        
        return final_list

    except requests.RequestException as e:
        print(f"    ❌ [Naver] 요청 에러: {e}")
        return []
    except Exception as e:
        print(f"    ❌ [Naver] 파싱 에러: {e}")
        return []


def fetch_policy_api():
    """정책브리핑 API 뉴스 수집"""
    print("    🏛️  [Policy] API 요청 중...")
    
    api_key = os.environ.get("DATA_GO_KR_KEY")
    if not api_key:
        print("    ⚠️  [Policy] API 키가 설정되지 않았습니다.")
        return []

    url = "http://apis.data.go.kr/1371000/policyNewsService/getPolicyNewsList"
    params = {
        "serviceKey": api_key,
        "numOfRows": 10,
        "pageNo": 1
    }
    
    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, 'xml')
        
        items = soup.find_all('item')
        if not items:
            print("    ⚠️  [Policy] 뉴스 항목이 없습니다.")
            return []
        
        policy_list = []
        money_keywords = ["지원", "신청", "지급", "환급", "무료", "개시", "특가", "혜택"]
        
        for item in items:
            title_tag = item.find('title')
            if not title_tag:
                continue
            title = title_tag.text
            
            # 키워드 필터링 또는 상위 3개 무조건 포함
            if any(k in title for k in money_keywords) or len(policy_list) < 3:
                policy_list.append(f"[정부정책] {title}")
                
        return policy_list

    except requests.RequestException as e:
        print(f"    ❌ [Policy] API 에러: {e}")
        return []
    except Exception as e:
        print(f"    ❌ [Policy] 파싱 에러: {e}")
        return []


def fetch_daum_news():
    """다음 뉴스 랭킹 수집"""
    print("    🕷️  [Daum] 크롤링 시작...")
    url = "https://news.daum.net/ranking/popular"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        news_list = soup.select('.list_news2 .link_txt')
        if not news_list:
            print("    ⚠️  [Daum] 뉴스 리스트를 찾을 수 없습니다.")
            return []
        
        headlines = []
        for news in news_list[:15]:
            title = news.get_text(strip=True)
            if title:
                headlines.append(f"[Daum] {title}")
                
        return headlines
        
    except requests.RequestException as e:
        print(f"    ❌ [Daum] 요청 에러: {e}")
        return []
    except Exception as e:
        print(f"    ❌ [Daum] 파싱 에러: {e}")
        return []
