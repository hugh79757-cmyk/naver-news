import os
from datetime import datetime

def build_html_file(ai_content):
    """
    템플릿에 AI 키워드 분석 결과를 삽입해서 최종 HTML을 생성합니다.
    """
    print("    🔨 [Builder] HTML 생성 중...")
    
    # 1. 템플릿 읽기
    template_path = "templates/layout.html"
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"    ❌ [Builder] 템플릿 파일을 찾을 수 없습니다: {template_path}")
        print("    💡 'templates/layout.html' 파일이 있는지 확인하세요.")
        return

    # 2. 플레이스홀더 치환
    now_str = datetime.now().strftime("%Y년 %m월 %d일 %H시 %M분")
    final_html = template.replace("{{content}}", ai_content)
    final_html = final_html.replace("{{date}}", now_str)
    
    # 3. 출력 폴더 생성
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 4. 파일 저장
    output_path = os.path.join(output_dir, "index.html")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"    ✅ [Builder] 생성 완료: {output_path}")
    except Exception as e:
        print(f"    ❌ [Builder] 파일 저장 실패: {e}")
