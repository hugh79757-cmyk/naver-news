import os
from datetime import datetime

def build_html_file(ai_content):
    """템플릿을 읽어서 AI 내용을 채워넣고 최종 HTML을 만듭니다."""
    print("🔨 [Builder] HTML 생성 중...")
    
    # 1. 템플릿 읽기
    try:
        with open("templates/layout.html", "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print("❌ [Builder] 템플릿 파일을 찾을 수 없습니다.")
        return

    # 2. 내용 치환 (Injection)
    now_str = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
    final_html = template.replace("{{content}}", ai_content)
    final_html = final_html.replace("{{date}}", now_str)
    
    # 3. 파일 저장
    os.makedirs("output", exist_ok=True)
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(final_html)
        
    print("✅ [Builder] 'output/index.html' 생성 완료!")