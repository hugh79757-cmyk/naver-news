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
    """HTML 파일 생성 및 아카이브"""
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
    
    # 저장
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    # 아카이브 페이지 생성
    archive_html = generate_archive_page(archive_dir)
    archive_page_path = "output/archive.html"
    with open(archive_page_path, "w", encoding="utf-8") as f:
        f.write(archive_html)
    
    archive_count = len([f for f in os.listdir(archive_dir) if f.endswith('.html')])
    print(f"    ✅ [Builder] 생성 완료: output/index.html")
    print(f"    📚 [Builder] 총 {archive_count}개 아카이브 보관 중")


def generate_archive_page(archive_dir):
    """별도 아카이브 페이지 생성"""
    files = sorted(
        [f for f in os.listdir(archive_dir) if f.endswith('.html')],
        reverse=True
    )
    
    html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>과거 분석 결과 - 블로그 키워드 인사이트</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --dancheong-blue: #1e3a8a;
            --dancheong-gold: #f59e0b;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --border-color: #e5e7eb;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Noto Sans KR', sans-serif;
            background: linear-gradient(180deg, #f0f4ff 0%, #f8fafc 100%);
            min-height: 100vh;
            color: var(--text-primary);
            line-height: 1.7;
        }
        .header {
            background: linear-gradient(135deg, var(--dancheong-blue) 0%, #1e40af 100%);
            padding: 2rem;
            text-align: center;
            color: white;
        }
        .header h1 { font-size: 1.5rem; margin-bottom: 0.5rem; }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }
        .back-btn {
            display: inline-block;
            padding: 10px 20px;
            background: var(--dancheong-blue);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            margin-bottom: 1.5rem;
        }
        .back-btn:hover { background: #1e40af; }
        .archive-list { list-style: none; }
        .archive-list li {
            background: white;
            margin-bottom: 10px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            transition: all 0.2s;
        }
        .archive-list li:hover {
            border-color: var(--dancheong-blue);
            box-shadow: 0 2px 8px rgba(30, 58, 138, 0.15);
        }
        .archive-list a {
            display: flex;
            justify-content: space-between;
            padding: 14px 18px;
            color: var(--text-primary);
            text-decoration: none;
        }
        .archive-date { color: var(--text-secondary); font-size: 0.9rem; }
        .archive-keywords { color: var(--dancheong-blue); font-size: 0.9rem; }
        .count-info {
            background: #fffbeb;
            border: 1px solid var(--dancheong-gold);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            text-align: center;
        }
    </style>
</head>
<body>
    <header class="header">
        <h1>📚 과거 분석 결과 아카이브</h1>
        <p>이전에 분석된 키워드 리포트 목록</p>
    </header>
    <div class="container">
        <a href="index.html" class="back-btn">← 메인으로 돌아가기</a>
        <div class="count-info">
            <strong>"""
    
    html += str(len(files))
    html += """</strong>개의 분석 결과가 저장되어 있습니다.
        </div>
        <ul class="archive-list">
"""
    
    for filename in files:
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
    
    html += """
        </ul>
    </div>
</body>
</html>"""
    
    return html
