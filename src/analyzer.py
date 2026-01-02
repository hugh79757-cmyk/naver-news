import os
import anthropic

def analyze_headlines(headlines):
    """
    뉴스 헤드라인을 분석해서 SEO 최적화된 키워드를 추출합니다.
    Claude AI는 글쓰기 가이드가 아닌, 키워드 분석 전문가 역할을 합니다.
    """
    print("🧠 [Analyzer] SEO 키워드 분석 시작...")
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ [Analyzer] API 키가 없습니다.")
        return "<p>API 키 오류: 분석을 수행할 수 없습니다.</p>"

    client = anthropic.Anthropic(api_key=api_key)
    news_text = "\n".join(headlines)
    
    # ⭐ 핵심: 키워드 분석 전문 프롬프트
    prompt = f"""
당신은 네이버 블로그 상위 노출 전문가이자 SEO 키워드 분석가입니다.
아래 뉴스 헤드라인들을 분석해서 **블로거가 당장 쓸 수 있는 고수익 키워드**를 추출하세요.

---
[오늘의 뉴스 데이터]
{news_text}

---
[당신의 임무]
1. 뉴스를 분석해서 상위 5개 이슈 선정
2. 각 이슈별로 "돈 되는 키워드" 추출:
   - 메인 키워드 (검색량 높음)
   - 롱테일 키워드 (경쟁 낮음, 블로거가 노릴 키워드)
   - 질문형 키워드 (사람들이 실제로 검색하는 쿼리)
3. 클릭율 높은 제목 키워드 조합 제안

---
[출력 형식 - 반드시 HTML 형식으로]

<div class="keyword-report">
    <h3>🔥 오늘의 블로그 키워드 TOP 5</h3>
    
    <div class="keyword-item">
        <h4>1. [이슈명: 한 줄로 핵심 요약]</h4>
        
        <div class="keyword-section">
            <p><strong>📌 메인 키워드</strong></p>
            <ul>
                <li><span class="keyword">"키워드1"</span> 
                    <span class="badge">예상검색량: 일 5만</span>
                    <span class="badge red">경쟁: 상</span>
                    <span class="tip">→ 제목에 반드시 포함</span>
                </li>
                <li><span class="keyword">"키워드2"</span> 
                    <span class="badge">예상검색량: 일 2만</span>
                    <span class="badge orange">경쟁: 중</span>
                </li>
            </ul>
        </div>
        
        <div class="keyword-section">
            <p><strong>🎯 롱테일 키워드 (노리기 쉬움)</strong></p>
            <ul>
                <li><span class="keyword">"구체적인 롱테일 키워드1"</span> 
                    <span class="badge green">경쟁: 하</span>
                    <span class="tip">→ 초보 블로거 추천</span>
                </li>
                <li><span class="keyword">"구체적인 롱테일 키워드2"</span> 
                    <span class="badge green">경쟁: 하</span>
                </li>
                <li><span class="keyword">"구체적인 롱테일 키워드3"</span> 
                    <span class="badge green">경쟁: 하</span>
                </li>
            </ul>
        </div>
        
        <div class="keyword-section">
            <p><strong>❓ 실제 검색 쿼리 (질문형)</strong></p>
            <ul>
                <li>"OOO은 왜?"</li>
                <li>"OOO 방법은?"</li>
                <li>"OOO 총정리"</li>
                <li>"OOO 얼마나?"</li>
            </ul>
            <p class="small-tip">💡 이 질문들을 제목이나 소제목으로 사용하면 상위 노출 확률 UP</p>
        </div>
        
        <div class="keyword-section">
            <p><strong>✨ 추천 제목 조합 (CTR 높은 순)</strong></p>
            <ol>
                <li><strong>"[메인키워드] + [롱테일]"</strong> 
                    <span class="ctr">예상 CTR 8%</span>
                    <br><span class="example">예: "윤석열 사우나 설치 비용 총정리"</span>
                </li>
                <li><strong>"[질문형] + [메인키워드]"</strong> 
                    <span class="ctr">예상 CTR 6%</span>
                    <br><span class="example">예: "대통령실 사우나 왜 문제될까?"</span>
                </li>
                <li><strong>"[숫자] + [메인키워드] + [리스트]"</strong> 
                    <span class="ctr">예상 CTR 7%</span>
                    <br><span class="example">예: "집무실 논란 총정리 5가지"</span>
                </li>
            </ol>
        </div>
        
        <div class="meta-info">
            <p>
                <span class="tag">⏰ 작성권장: 24시간 이내</span>
                <span class="tag">💰 수익성: 상</span>
                <span class="tag">🎯 난이도: 중</span>
                <span class="tag">📊 예상유입: 1만~2만</span>
            </p>
        </div>
    </div>
    
    <hr>
    
    <!-- 이슈 2~5도 동일 형식 반복 -->
    
</div>

<div class="bonus-section">
    <h3>💎 보너스: 틈새 키워드 (경쟁 거의 없음)</h3>
    <ul>
        <li><span class="keyword">"초틈새 키워드1"</span> - 검색량 적지만 상위노출 100%</li>
        <li><span class="keyword">"초틈새 키워드2"</span> - 지역 특화 키워드</li>
        <li><span class="keyword">"초틈새 키워드3"</span> - 전문가 타겟 키워드</li>
    </ul>
</div>

---
**중요 지침:**
- 검색량/경쟁도는 당신의 전문가적 판단으로 예측
- 실제 사람들이 검색할 법한 "자연스러운" 키워드만 추출
- 너무 전문적이거나 어려운 용어는 제외
- 숫자는 구체적으로 (예: "많음" ❌, "일 5만" ✅)
- 롱테일 키워드는 최소 3단어 이상 조합
"""

    try:
        message = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=4000,
            temperature=0.6,  # 창의성과 정확성 균형
            messages=[{"role": "user", "content": prompt}]
        )

        result = message.content[0].text
        print("✅ [Analyzer] SEO 키워드 분석 완료")
        return result
        
    except Exception as e:
        print(f"❌ [Analyzer] 에러: {e}")
        return f"<p>AI 분석 중 오류 발생: {e}</p>"


# 추가 함수: 키워드 품질 검증 (선택)
def validate_keywords(ai_response):
    """
    Claude가 생성한 키워드의 품질을 간단히 검증합니다.
    - 너무 짧은 키워드 필터링
    - 중복 제거
    - 특수문자 정리
    """
    # TODO: 필요시 구현
    pass
