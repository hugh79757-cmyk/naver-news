import os
from datetime import datetime

def build_html_file(ai_content):
    """템플릿에 AI 분석 결과를 삽입"""
    print("    🔨 [Builder] HTML 생성 중...")
    
    # ⭐ 이 경로가 맞는지 확인
    template_path = "templates/layout.html"
    
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"    ❌ 템플릿 파일을 찾을 수 없습니다: {template_path}")
        return

    # 플레이스홀더 치환
    now_str = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
    final_html = template.replace("{{content}}", ai_content)
    final_html = final_html.replace("{{date}}", now_str)
    
    # 저장
    os.makedirs("output", exist_ok=True)
    output_path = "output/index.html"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print(f"    ✅ [Builder] 생성 완료: {output_path}")
