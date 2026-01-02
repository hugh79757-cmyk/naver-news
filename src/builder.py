import os
import re
from datetime import datetime
import shutil

def build_html_file(ai_content):
    """
    1. AI 분석 결과에서 상위 3개 키워드 추출
    2. 파일명에 날짜 + 키워드 포함
    3. 아카이브 시스템 구축
    """
    print("    🔨 [Builder] HTML 생성 중...")
    
    # 타임스탬프
    now = datetime.now()
    now_str = now.strftime("%Y년 %m월 %d일 %H시 %M분")
    date_prefix = now.strftime("%Y-%m-%d_%H-%M")
    
    # 1. AI 분석 결과에서 상위 3개 이슈 제목 추출
    top_keywords = extract_top_keywords(ai_content, count=3)
    
    # 2. 파일명 생성 (날짜 + 키워드)
    if top_keywords:
        keywords_str = "_".join(top_keywords)
        archive_filename = f"{date_prefix}_{keywords_str}.html"
    else:
        archive_filename = f"{date_prefix}_분석결과.html"
    
    print(f"    📝 [Builder] 파일명: {archive_filename}")
    
    # 3. 기존 index.html을 archive로 백업
    output_path = "output/index.html"
    archive_dir = "output/archive"
    os.makedirs(archive_dir, exist_ok=True)
    
    if os.path.exists(output_path):
        archive_path = os.path.join(archive_dir, archive_filename)
        shutil.copy(output_path, archive_path)
        print(f"    📦 [Builder] 백업 완료: {archive_filename}")
    
    # 4. 과거 목록 HTML 생성
    archive_list_html = generate_archive_list(archive_dir)
    
    # 5. 템플릿 읽기
    template_path = "templates/layout.html"
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"    ❌ 템플릿 파일 없음: {template_path}")
        return

    # 6. 플레이스홀더 치환
    final_html = template.replace("{{date}}", now_str)
    final_html = final_html.replace("{{content}}", ai_content)
    final_html = final_html.replace("{{archive_list}}", archive_list_html)
    
    # 7. 저장
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    archive_count = len([f for f in os.listdir(archive_dir) if f.endswith('.html')])
    print(f"    ✅ [Builder] 생성 완료: output/index.html")
    print(f"    📚 [Builder] 총 {archive_count}개 아카이브 보관 중")


def extract_top_keywords(ai_content, count=3):
    """
    AI 분석 결과에서 상위 N개 이슈 제목을 추출하여 파일명에 사용
    """
    keywords = []
    
    # 정규식으로 "1. [이슈명: ...]" 패턴 추출
    pattern = r'\d+\.\s*\[([^\]]+)\]'
    matches = re.findall(pattern, ai_content)
    
    for match in matches[:count]:
        # 제목 정리: 특수문자 제거, 공백을 대시로
        cleaned = re.sub(r'[^\w\s가-힣]', '', match)  # 특수문자 제거
        cleaned = cleaned.strip()
        cleaned = re.sub(r'\s+', '', cleaned)  # 공백 제거
        
        # 너무 길면 앞 10글자만
        if len(cleaned) > 10:
            cleaned = cleaned[:10]
        
        if cleaned:
            keywords.append(cleaned)
    
    return keywords


def generate_archive_list(archive_dir):
    """
    archive 폴더의 파일 목록을 보기 좋게 HTML로 생성
    파일명에서 날짜와 키워드를 추출하여 표시
    """
    files = sorted(
        [f for f in os.listdir(archive_dir) if f.endswith('.html')],
        reverse=True  # 최신순
    )
    
    if not files:
        return '<div class="archive-section"><p>📭 아직 과거 분석 결과가 없습니다.</p></div>'
    
    html = '<div class="archive-section">'
    html += '<h3>📚 과거 분석 결과 아카이브</h3>'
    html += '<p class="archive-info">총 <strong>{}</strong>개의 분석 결과가 저장되어 있습니다.</p>'.format(len(files))
    html += '<ul class="archive-list">'
    
    for filename in files[:30]:  # 최근 30개만 표시
        # 파일명 파싱: 2026-01-02_18-24_종각역사고_나나강도_곽튜브다이어트.html
        parts = filename.replace('.html', '').split('_')
        
        if len(parts) >= 2:
            date_part = parts[0]  # 2026-01-02
            time_part = parts[1]  # 18-24
            keywords_part = '_'.join(parts[2:]) if len(parts) > 2 else "분석결과"
            
            # 날짜 포맷팅
            try:
                date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H-%M")
                display_date = date_obj.strftime("%Y년 %m월 %d일 %H:%M")
            except:
                display_date = f"{date_part} {time_part}"
            
            # 키워드 표시 (언더스코어를 쉼표로)
            keywords_display = keywords_part.replace('_', ' · ')
            
            # HTML 생성
            html += f'''
            <li>
                <a href="archive/{filename}" target="_blank">
                    <span class="archive-date">📅 {display_date}</span>
                    <span class="archive-keywords">🔑 {keywords_display}</span>
                </a>
            </li>
            '''
        else:
            # 파싱 실패 시 파일명 그대로 표시
            html += f'<li><a href="archive/{filename}" target="_blank">📄 {filename}</a></li>'
    
    html += '</ul></div>'
    return html
