import os
from datetime import datetime
import shutil

def build_keyword_report(keyword_results, related_data=None):
    """키워드 분석 결과를 HTML 테이블로 변환"""
    
    if not keyword_results:
        return "<p>분석된 키워드가 없습니다.</p>"
    
    # 상위 50개만 선택 (포화도 0.5 이하 우선)
    top_keywords = [r for r in keyword_results if r["saturation"] <= 0.5][:50]
    
    # 50개 안 되면 나머지에서 채움
    if len(top_keywords) < 50:
        remaining = [r for r in keyword_results if r not in top_keywords]
        top_keywords += remaining[:50 - len(top_keywords)]
    
    html = """
    <div class="keyword-report">
        <h3>📊 상위노출 가능 키워드 TOP 50</h3>
        <p class="update-info">포화도 = 블로그문서수 ÷ 월간검색량 (낮을수록 상위노출 쉬움)</p>
        
        <table class="keyword-table">
            <thead>
                <tr>
                    <th>순위</th>
                    <th>키워드</th>
                    <th>월간검색량</th>
                    <th>블로그문서수</th>
                    <th>포화도</th>
                    <th>상위노출</th>
                    <th>분석</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for idx, item in enumerate(top_keywords, 1):
        keyword = item['keyword']
        naver_url = f"https://search.naver.com/search.naver?query={keyword}"
        html += f"""
                <tr>
                    <td>{idx}</td>
                    <td><strong>{keyword}</strong></td>
                    <td>{item['monthly_search']:,}</td>
                    <td>{item['blog_count']:,}</td>
                    <td>{item['saturation']}</td>
                    <td>{item['possibility']}</td>
                    <td><a href="{naver_url}" target="_blank" class="analyze-btn">🔍</a></td>
                </tr>
        """
    
    html += """
            </tbody>
        </table>
    </div>
    """
    
    # 상위 20개 연관검색어 섹션
    if related_data:
        html += """
    <div class="related-keywords">
        <h3>🔗 상위 20개 키워드 연관검색어</h3>
        <p class="update-info">네이버 자동완성 기반 연관검색어입니다.</p>
        
        <div class="related-grid">
    """
        for item in related_data:
            keyword = item['keyword']
            related = item['related']
            naver_url = f"https://search.naver.com/search.naver?query={keyword}"
            
            html += f"""
            <div class="related-card">
                <div class="related-header">
                    <strong>{keyword}</strong>
                    <a href="{naver_url}" target="_blank" class="analyze-btn">🔍</a>
                </div>
                <ul class="related-list">
            """
            for rel_kw in related:
                rel_url = f"https://search.naver.com/search.naver?query={rel_kw}"
                html += f'<li><a href="{rel_url}" target="_blank">{rel_kw}</a></li>'
            
            if not related:
                html += '<li class="no-data">연관검색어 없음</li>'
            
            html += """
                </ul>
            </div>
            """
        
        html += """
        </div>
    </div>
    """
    
    return html


def build_html_file(ai_content, keyword_results=None):
    """
    HTML 파일 생성 및 아카이브
    """
    print("    🔨 [Builder] HTML 생성 중...")
    
    now = datetime.now()
    now_str = now.strftime("%Y년 %m월 %d일 %H시 %M분")
    date_prefix = now.strftime("%Y-%m-%d_%H-%M")
    
    # 상위 3개 키워드 추출 (파일명용)
    if keyword_results and len(keyword_results) > 0:
        top_keywords = [item['keyword'][:10].replace(' ', '') for item in keyword_results[:3]]
        keywords_str = "_".join(top_keywords)
        archive_filename = f"{date_prefix}_{keywords_str}.html"
    else:
        archive_filename = f"{date_prefix}_분석결과.html"
    
    print(f"    📝 [Builder] 파일명: {archive_filename}")
    
    # 기존 index.html을 archive로 백업
    output_path = "output/index.html"
    archive_dir = "output/archive"
    os.makedirs(archive_dir, exist_ok=True)
    
    if os.path.exists(output_path):
        archive_path = os.path.join(archive_dir, archive_filename)
        shutil.copy(output_path, archive_path)
        print(f"    📦 [Builder] 백업 완료: {archive_filename}")
    
    # 과거 목록 HTML 생성
    archive_list_html = generate_archive_list(archive_dir)
    
    # 템플릿 읽기
    template_path = "templates/layout.html"
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"    ❌ 템플릿 파일 없음: {template_path}")
        return

    # 플레이스홀더 치환
    final_html = template.replace("{{date}}", now_str)
    final_html = final_html.replace("{{content}}", ai_content)
    final_html = final_html.replace("{{archive_list}}", archive_list_html)
    
    # 저장
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    archive_count = len([f for f in os.listdir(archive_dir) if f.endswith('.html')])
    print(f"    ✅ [Builder] 생성 완료: output/index.html")
    print(f"    📚 [Builder] 총 {archive_count}개 아카이브 보관 중")


def generate_archive_list(archive_dir):
    """
    archive 폴더의 파일 목록을 HTML로 생성
    """
    files = sorted(
        [f for f in os.listdir(archive_dir) if f.endswith('.html')],
        reverse=True
    )
    
    if not files:
        return '<div class="archive-section"><p>📭 아직 과거 분석 결과가 없습니다.</p></div>'
    
    html = '<div class="archive-section">'
    html += '<h3>📚 과거 분석 결과 아카이브</h3>'
    html += '<p class="archive-info">총 <strong>{}</strong>개의 분석 결과가 저장되어 있습니다.</p>'.format(len(files))
    html += '<ul class="archive-list">'
    
    for filename in files[:30]:
        parts = filename.replace('.html', '').split('_')
        
        if len(parts) >= 2:
            date_part = parts[0]
            time_part = parts[1]
            keywords_part = '_'.join(parts[2:]) if len(parts) > 2 else "분석결과"
            
            try:
                date_obj = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H-%M")
                display_date = date_obj.strftime("%Y년 %m월 %d일 %H:%M")
            except:
                display_date = f"{date_part} {time_part}"
            
            keywords_display = keywords_part.replace('_', ' · ')
            
            html += f'''
            <li>
                <a href="archive/{filename}" target="_blank">
                    <span class="archive-date">📅 {display_date}</span>
                    <span class="archive-keywords">🔑 {keywords_display}</span>
                </a>
            </li>
            '''
        else:
            html += f'<li><a href="archive/{filename}" target="_blank">📄 {filename}</a></li>'
    
    html += '</ul></div>'
    return html
