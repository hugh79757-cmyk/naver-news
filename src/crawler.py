import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import time

load_dotenv()

def fetch_naver_ranking_news():
    """네이버 언론사별 랭킹 뉴스 수집 (2026년 1월 최신 버전)"""
    print("    🕷️  [Naver] 크롤링 시작...")
    url = "https://news.naver.com/main/ranking/popularDay.naver"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.naver.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 방법 1: 랭킹 뉴스 박스
        press_boxes = soup.select('.rankingnews_box')
        
        if not press_boxes:
            # 방법 2: 대체 셀렉터 시도
            print("    🔄 [Naver] 대체 셀렉터 시도...")
            press_boxes = soup.select('div.rankingnews_box_wrap div.rankingnews_box')
        
        if not press_boxes:
            print("    ⚠️  [Naver] 뉴스 박스를 찾을 수 없습니다.")
            print(f"    💡 HTML 일부: {soup.text[:200]}")
            return []
        
        news_list = []
        for box in press_boxes:
            # 언론사 이름
            press_name = box.select_one('.rankingnews_name')
            if not press_name:
                press_name = box.select_one('strong.rankingnews_name')
            if not press_name:
                continue
            press_name = press_name.get_text(strip=True)

            # 1위 뉴스
            first_news = box.select_one('.list_content li a')
            if not first_news:
                first_news = box.select_one('ul.rankingnews_list li a')
            
            if first_news:
                title = first_news.get_text(strip=True)
                news_list.append(f"[{press_name}] {title}")

        if news_list:
            # 제목 길이순 정렬 후 상위 20개
            news_list.sort(key=len, reverse=True)
            final_list = news_list[:20]
            print(f"    ✅ {len(final_list)}개 수집 완료")
            return final_list
        else:
            print("    ⚠️  [Naver] 뉴스를 추출할 수 없습니다.")
            return []

    except requests.RequestException as e:
        print(f"    ❌ [Naver] 요청 에러: {e}")
        return []
    except Exception as e:
        print(f"    ❌ [Naver] 파싱 에러: {e}")
        return []


def fetch_policy_api():
    """정책브리핑 RSS 방식으로 수집 (API 대신)"""
    print("    🏛️  [Policy] RSS 수집 중...")
    
    # API 대신 RSS 사용
    url = "https://www.korea.kr/rss/policy.xml"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, 'xml')
        
        items = soup.find_all('item')
        if not items:
            print("    ⚠️  [Policy] RSS 항목이 없습니다.")
            return []
        
        policy_list = []
        money_keywords = ["지원", "신청", "지급", "환급", "무료", "개시", "특가", "혜택", "보조금"]
        
        for item in items[:15]:  # 상위 15개
            title_tag = item.find('title')
            if not title_tag:
                continue
            title = title_tag.text.strip()
            
            # 키워드 필터링
            if any(k in title for k in money_keywords):
                policy_list.append(f"[정부정책] {title}")
                
        if policy_list:
            print(f"    ✅ {len(policy_list)}개 수집 완료")
            return policy_list
        else:
            print("    ⚠️  [Policy] 키워드 매칭 뉴스 없음")
            return []

    except requests.RequestException as e:
        print(f"    ❌ [Policy] RSS 에러: {e}")
        return []
    except Exception as e:
        print(f"    ❌ [Policy] 파싱 에러: {e}")
        return []


def fetch_daum_news():
    """다음 뉴스 랭킹 수집 (2026년 1월 최신 URL)"""
    print("    🕷️  [Daum] 크롤링 시작...")
    url = "https://news.daum.net/ranking/popular/"  # URL 끝에 / 추가
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9"
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 방법 1: 기존 셀렉터
        news_list = soup.select('.list_news2 .link_txt')
        
        if not news_list:
            # 방법 2: 대체 셀렉터
            print("    🔄 [Daum] 대체 셀렉터 시도...")
            news_list = soup.select('ul.list_news2 li a.link_txt')
        
        if not news_list:
            # 방법 3: 더 넓은 범위
            news_list = soup.select('div.rank_news a')
        
        if not news_list:
            print("    ⚠️  [Daum] 뉴스 리스트를 찾을 수 없습니다.")
            print(f"    💡 HTML 일부: {soup.text[:200]}")
            return []
        
        headlines = []
        for news in news_list[:15]:
            title = news.get_text(strip=True)
            if title and len(title) > 10:  # 너무 짧은 제목 제외
                headlines.append(f"[Daum] {title}")
        
        if headlines:
            print(f"    ✅ {len(headlines)}개 수집 완료")
            return headlines
        else:
            print("    ⚠️  [Daum] 유효한 뉴스가 없습니다.")
            return []
        
    except requests.RequestException as e:
        print(f"    ❌ [Daum] 요청 에러: {e}")
        return []
    except Exception as e:
        print(f"    ❌ [Daum] 파싱 에러: {e}")
        return []


# 추가: 네이버 메인 헤드라인 수집 (백업용)
def fetch_naver_main_headlines():
    """네이버 메인 페이지 헤드라인 수집 (백업용)"""
    print("    🕷️  [Naver Main] 크롤링 시작...")
    url = "https://news.naver.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 헤드라인 수집
        headlines = soup.select('.cjs_news_headlines .cjs_t')
        
        if not headlines:
            headlines = soup.select('.sh_text._sh_text_headline')
        
        news_list = []
        for h in headlines[:20]:
            title = h.get_text(strip=True)
            if title and len(title) > 15:
                news_list.append(f"[네이버메인] {title}")
        
        if news_list:
            print(f"    ✅ {len(news_list)}개 수집 완료")
        return news_list
        
    except Exception as e:
        print(f"    ❌ [Naver Main] 에러: {e}")
        return []
