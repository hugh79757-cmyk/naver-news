import os
import time
import hashlib
import hmac
import base64
import requests

class NaverAPI:
    """네이버 광고 API + 검색 API로 키워드 데이터 조회"""
    
    def __init__(self):
        self.ad_client_id = os.environ.get("NAVER_AD_CLIENT_ID")
        self.ad_client_secret = os.environ.get("NAVER_AD_CLIENT_SECRET")
        self.ad_customer_id = os.environ.get("NAVER_AD_CUSTOMER_ID")
        self.search_client_id = os.environ.get("NAVER_CLIENT_ID")
        self.search_client_secret = os.environ.get("NAVER_CLIENT_SECRET")
    
    def _get_header(self, method, uri):
        """광고 API 헤더 생성"""
        timestamp = str(round(time.time() * 1000))
        sign = f"{timestamp}.{method}.{uri}"
        signature = hmac.new(
            self.ad_client_secret.encode(),
            sign.encode(),
            hashlib.sha256
        ).digest()
        signature_base64 = base64.b64encode(signature).decode()
        
        return {
            "X-API-KEY": self.ad_client_id,
            "X-Customer": self.ad_customer_id,
            "X-Timestamp": timestamp,
            "X-Signature": signature_base64,
        }
    
    def get_search_volume(self, keywords):
        """네이버 광고 API로 월간검색량 조회"""
        if not all([self.ad_client_id, self.ad_client_secret, self.ad_customer_id]):
            print("    ❌ [NaverAPI] 광고 API 키가 없습니다.")
            return {}
        
        BASE_URL = "https://api.naver.com"
        uri = "/keywordstool"
        method = "GET"
        results = {}
        
        for i in range(0, len(keywords), 5):
            batch = keywords[i:i+5]
            
            cleaned_batch = []
            for kw in batch:
                kw = kw.strip().replace(" ", "")
                if kw and len(kw) > 1:
                    cleaned_batch.append(kw)
            
            if not cleaned_batch:
                continue
            
            headers = self._get_header(method, uri)
            params = {
                "hintKeywords": ",".join(cleaned_batch),
                "showDetail": "1"
            }
            
            try:
                response = requests.get(BASE_URL + uri, headers=headers, params=params)
                
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
                    print(f"    ⚠️ [NaverAPI] 일부 키워드 조회 실패: {response.status_code}")
                    
            except Exception as e:
                print(f"    ⚠️ [NaverAPI] 요청 실패: {e}")
            
            time.sleep(0.2)
        
        return results
    
    def get_blog_count(self, keyword):
        """네이버 검색 API로 블로그 문서수 조회"""
        if not all([self.search_client_id, self.search_client_secret]):
            return 0
        
        headers = {
            "X-Naver-Client-Id": self.search_client_id,
            "X-Naver-Client-Secret": self.search_client_secret
        }
        params = {"query": keyword, "display": 1}
        
        try:
            response = requests.get(
                "https://openapi.naver.com/v1/search/blog.json",
                headers=headers,
                params=params
            )
            if response.status_code == 200:
                return response.json().get("total", 0)
            return 0
        except:
            return 0
    
    def analyze_keywords(self, keywords):
    """키워드 분석: 검색량, 문서수, 포화도 계산"""
    print(f"    📊 [NaverAPI] {len(keywords)}개 키워드 분석 시작...")
    
    print("    🔍 검색량 조회 중...")
    search_volumes = self.get_search_volume(keywords)
    print(f"    ✅ {len(search_volumes)}개 키워드 검색량 조회 완료")
    
    # 상위 200개로 확대
    sorted_keywords = sorted(search_volumes.items(), key=lambda x: x[1], reverse=True)[:200]
    
    print(f"    📝 블로그 문서수 조회 중... (상위 {len(sorted_keywords)}개)")
    results = []
    
    for keyword, volume in sorted_keywords:
        if volume == 0:
            continue
        
        blog_count = self.get_blog_count(keyword)
        time.sleep(0.05)
        
        saturation = round(blog_count / volume, 2) if volume > 0 else 999
        
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
