import os
import anthropic

def analyze_headlines(headlines):
    """
    뉴스 헤드라인에서 키워드 후보를 대량 추출합니다.
    """
    print("🧠 [Analyzer] 키워드 추출 시작...")
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ [Analyzer] API 키가 없습니다.")
        return []

    client = anthropic.Anthropic(api_key=api_key)
    news_text = "\n".join(headlines)
    
    prompt = f"""
아래 뉴스 헤드라인들을 분석해서 블로그 키워드 후보를 추출하세요.

[뉴스 헤드라인]
{news_text}

[추출 규칙]
1. 각 뉴스에서 사람들이 검색할 만한 키워드를 최대한 많이 추출
2. 키워드 형태:
   - 메인 키워드 (2~3단어): 예) "전기차보조금", "삼성갤럭시"
   - 롱테일 키워드 (3~5단어): 예) "2025전기차보조금신청방법"
   - 질문형 키워드: 예) "전기차보조금얼마"
   - 연관 키워드: 뉴스와 관련된 파생 키워드도 포함
3. 반드시 50개 이상 키워드 추출 (목표: 60~80개)
4. 너무 일반적인 키워드는 제외 (예: "뉴스", "오늘", "발표")
5. 실제 사람들이 네이버에서 검색할 법한 자연스러운 키워드만
6. **모든 키워드는 띄어쓰기 없이 붙여서 작성** (예: "전기차 보조금" ❌ → "전기차보조금" ✅)

[출력 형식]
키워드만 한 줄에 하나씩 출력하세요. 번호나 설명 없이 키워드만.
띄어쓰기 없이 붙여서 출력하세요.
반드시 50개 이상 출력하세요.
"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )

        result = message.content[0].text
        
        # 키워드 파싱 + 띄어쓰기 강제 제거 (후처리)
        keywords = [
            line.strip().replace(" ", "") 
            for line in result.strip().split("\n") 
            if line.strip()
        ]
        
        print(f"✅ [Analyzer] {len(keywords)}개 키워드 추출 완료")
        return keywords
        
    except Exception as e:
        print(f"❌ [Analyzer] 에러: {e}")
        return []
