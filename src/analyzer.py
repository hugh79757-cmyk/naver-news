import anthropic
import time

def extract_keywords(headlines):
    """Claude AI로 뉴스 헤드라인에서 블로그 키워드 추출"""
    print("🧠 [Analyzer] 키워드 추출 시작...")
    
    client = anthropic.Anthropic()
    
    headlines_text = "\n".join([f"- {h}" for h in headlines])
    
    prompt = f"""다음 뉴스 헤드라인들을 분석하여 블로그 키워드를 추출해주세요.

뉴스 헤드라인:
{headlines_text}

요구사항:
1. 각 헤드라인에서 블로그 검색에 적합한 키워드 2-3개 추출
2. 띄어쓰기 없이 붙여서 작성 (예: "삼성전자주가", "비트코인전망")
3. 너무 일반적인 단어 제외 (뉴스, 오늘, 발표 등)
4. 검색량이 있을 것 같은 구체적인 키워드 선정
5. 키워드만 쉼표로 구분하여 나열 (설명 없이)

응답 형식:
키워드1, 키워드2, 키워드3, ...
"""
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            result = response.content[0].text
            keywords = [kw.strip().replace(" ", "") for kw in result.split(",")]
            keywords = [kw for kw in keywords if len(kw) >= 2]
            keywords = list(dict.fromkeys(keywords))
            
            print(f"✅ [Analyzer] {len(keywords)}개 키워드 추출 완료")
            return keywords
            
        except anthropic.APIError as e:
            if "overloaded" in str(e).lower() or "529" in str(e):
                wait_time = (attempt + 1) * 30  # 30초, 60초, 90초
                print(f"⏳ [Analyzer] API 과부하, {wait_time}초 후 재시도... ({attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                print(f"❌ [Analyzer] 에러: {e}")
                return []
    
    print("❌ [Analyzer] 최대 재시도 횟수 초과")
    return []


# 함수 별칭 (main.py 호환성)
analyze_headlines = extract_keywords
