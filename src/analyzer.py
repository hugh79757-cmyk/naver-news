import os
import anthropic

def analyze_headlines(headlines):
    """뉴스 제목들을 클로드에게 보내서 요약 리포트를 받습니다."""
    print("🧠 [Analyzer] Claude 분석 시작...")
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ [Analyzer] API 키가 없습니다.")
        return "<p>API 키 오류: 분석을 수행할 수 없습니다.</p>"

    client = anthropic.Anthropic(api_key=api_key)
    news_text = "\n".join(headlines)
    
    prompt = f"""
    아래 뉴스 헤드라인들을 분석해서 블로거를 위한 '인사이트 리포트'를 작성해줘.
    결과는 오직 HTML 태그(div, h3, ul, li, p 등)로만 출력해. (html, body 태그 제외)
    
    [뉴스 데이터]
    {news_text}
    
    [작성 양식]
    <div class="report-section">
        <h3>🔥 오늘의 핫 이슈 3</h3>
        <ul>
            <li>
                <strong>이슈 1: (제목)</strong><br>
                (내용 요약 1문장)<br>
                <span class="tip">💡 블로그 키워드 추천: (키워드 2~3개)</span>
            </li>
            ... (이슈 2, 3 반복)
        </ul>
    </div>
    """

    try:
        message = client.messages.create(
            # [2026.01 최신] 세계 최고 성능 모델 적용 (Claude Opus 4.5)
            model="claude-opus-4-5-20251101", 
            max_tokens=2000,
            temperature=0.5,
            messages=[{"role": "user", "content": prompt}]
        )

        return message.content[0].text
    except Exception as e:
        print(f"❌ [Analyzer] 에러: {e}")
        return f"<p>AI 분석 중 오류 발생: {e}</p>"