import os
import time
import hashlib
import hmac
import base64
import requests

class NaverAPI:
    """네이버 광고 API + 검색 API로 키워드 데이터 조회"""
    
    def __init__(self):
        # 광고 API (검색량 조회)
        self.ad_client_id = os.environ.get("NAVER_AD_CLIENT_ID")
        self.ad_client_secret = os.environ.get("NAVER_AD_CLIENT_SECRET")
        self.ad_customer_id = os.environ.get("NAVER_AD_CUSTOMER_ID")
        
        # 검색 API (문서수 조회)
        self.search_client_id = os.environ.get("NAVER_CLIENT_ID")
        self.search_client_secret = os.environ.get("NAVER_CLIENT_SECRET")
    
    def _generate_signature(self, timestamp, method, uri):
        """광고 API 서명 생성"""
        message = f"{timestamp}.{method}.{uri}"
        signature = hmac.new(
            self.ad_client_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode('utf-8')
    
    def get_search_volume(self, keywords):
        """
        네이버 광고 API로 월간검색량 조회
        keywords: 키워드 리스트 (최대 100개)
        """
        if not all([self.ad_client_id, self.ad_client_secret, self.ad_customer_id]):
            print("    ❌ [NaverAPI] 광고 API 키가 없습니다.")
            return {}
        
        uri = "/keywordstool"
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        signature = self._generate_signature(timestamp, method, uri)
        
        headers = {
            "X-Timestamp": timestamp,
            "X-API-KEY": self.ad_client_id,
            "X-Customer": self.ad_customer_id,
            "X-Signature": signature
        }
        
        results = {}
        for i in range(0, len(keywords), 100):
            batch = keywords[i:i+100]
            params = {
                "hintKeywords": ",".join(batch),
                "showDetail": "1"
            }
            
            try:
                response = requests.get(
                    "https://api.naver.com" + uri,
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get("keywordList", []):
                        keyword = item.get("relKeyword", "")
                        pc_volume = item.get("monthlyPcQcCnt", 0)
                        mobile_volume = item.get("monthlyMobileQcCnt", 0)
                        
                        if isinstance(pc_volume, str):
                            pc_volume = 10
                        if isinstance(mobile_volume, str):
                            mobile_volume = 10
                            
                        results[keyword] = pc_volume + mobile_volume
                else:
                    print(f"    ❌ [NaverAPI] 광고 API 에러: {response.status_code}")
                    print(f"    ❌ [NaverAPI] 응답 내용: {response.text}")


                    
            except Exception as e:
                print(f"    ❌ [NaverAPI] 광고 API 요청 실패: {e}")
            
            time.sleep(0.1)
        
        return results
    
    def get_blog_count(self, keyword):
        """네이버 검색 API로 블로그 문서수 조회"""
        if not all([self.search_client_id, self.search_client_secret]):
            return 0
        
        headers = {
            "X-Naver-Client-Id": self.search_client_id,
            "X-Naver-Client-Secret": self.search_client_secret
        }
        
        params = {
            "query": keyword,
            "display": 1
        }
        
        try:
            response = requests.get(
                "https://openapi.naver.com/v1/search/blog.json",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("total", 0)
            else:
                return 0
                
        except Exception as e:
            return 0
    
    def analyze_keywords(self, keywords):
        """
        키워드 리스트를 분석해서 검색량, 문서수, 포화도 계산
        """
        print(f"    📊 [NaverAPI] {len(keywords)}개 키워드 분석 시작...")
        
        # 1. 검색량 조회
        print("    🔍 검색량 조회 중...")
        search_volumes = self.get_search_volume(keywords)
        
        # 2. 문서수 조회
        print("    📝 블로그 문서수 조회 중...")
        results = []
        
        for keyword in keywords:
            volume = search_volumes.get(keyword, 0)
            
            if volume == 0:
                continue
            
            blog_count = self.get_blog_count(keyword)
            time.sleep(0.1)
            
            if volume > 0:
                saturation = round(blog_count / volume, 2)
            else:
                saturation = 999
            
            if saturation <= 0.3:
                possibility = "🟢 매우높음"
            elif saturation <= 0.5:
                possibility = "🟡 높음"
            elif saturation <= 1.0:
                possibility = "🟠 보통"
            else:
                possibility = "🔴 낮음"
            
            results.append({
                "keyword": keyword,
                "monthly_search": volume,
                "blog_count": blog_count,
                "saturation": saturation,
                "possibility": possibility
            })
        
        results.sort(key=lambda x: x["saturation"])
        
        print(f"    ✅ {len(results)}개 키워드 분석 완료")
        return results
