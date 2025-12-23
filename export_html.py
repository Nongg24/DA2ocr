"""
Export results as HTML for better viewing (curly braces FIXED!)
"""
from pathlib import Path
from datetime import datetime
import sys
import os

def create_html_report(output_folder:  str = "output"):
    """Create a single HTML file with all results"""
    
    # Get absolute path
    if not os.path.isabs(output_folder):
        output_path = Path(os.getcwd()) / output_folder
    else:
        output_path = Path(output_folder)
    
    if not output_path.exists():
        print(f"❌ Output folder not found: {output_path}")
        return None

    print(f"📁 Checking folder: {output_path}")

    txt_files = list(output_path.glob("*.txt"))
    if not txt_files:  
        print(f"❌ No .txt files found in {output_path}")
        print(f"\n📋 All files in folder:")
        for file in output_path.iterdir():
            print(f"   - {file.name}")
        return None

    print(f"📊 Found {len(txt_files)} result file(s):")
    for f in txt_files:
        print(f"   ✅ {f.name}")

    # HTML CSS braces are escaped below!
    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OCR Results Summary</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing:  border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background:  linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #667eea; 
            margin-bottom: 10px;
            font-size: 32px;
        }}
        .timestamp {{
            color: #666; 
            font-size: 14px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .stat-box {{
            background:  linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 36px;
            font-weight:  bold;
            margin-bottom: 5px;
        }}
        .stat-label {{ 
            font-size: 14px;
            opacity: 0.9;
        }}
        .result-card {{
            background: white;
            padding: 30px;
            margin-bottom: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }}
        .result-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        .result-title {{
            color: #667eea;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }}
        .section {{
            margin: 25px 0;
        }}
        .section-title {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: bold;
            margin-bottom: 15px;
            font-size: 16px;
        }}
        .content {{
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            white-space: pre-wrap;
            line-height: 1.8;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            max-height: 400px;
            overflow-y: auto;
            border-left: 4px solid #667eea;
        }}
        .url-list {{
            list-style: none;
            padding: 0;
        }}
        .url-list li {{
            padding: 15px;
            margin: 10px 0;
            background: #f0f0f0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
        }}
        .url-list li:hover {{
            background: #e0e0e0;
            transform: translateX(5px);
        }}
        .url-list a {{
            color: #667eea;
            text-decoration: none;
            word-break: break-all;
            font-size: 14px;
        }}
        .url-list a:hover {{ 
            text-decoration: underline;
        }}
        .footer {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-top: 20px;
            color: #666;
        }}
        .no-results {{
            color: #999;
            font-style: italic;
            padding: 20px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Báo Cáo Kết Quả OCR</h1>
            <div class="timestamp">⏰ Tạo lúc: {timestamp}</div>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{total}</div>
                    <div class="stat-label">Ảnh đã xử lý</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{total_chars}</div>
                    <div class="stat-label">Ký tự trích xuất</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{total_urls}</div>
                    <div class="stat-label">Liên kết tìm được</div>
                </div>
            </div>
        </div>
"""

    total_chars = 0
    total_urls = 0

    # Process each result file
    for txt_file in sorted(txt_files):
        print(f"\n   Processing: {txt_file.name}")
        try:
            with open(txt_file, 'r', encoding='utf-8-sig', errors='ignore') as f:
                content = f.read()

            filename = txt_file.stem
            lines = content.split('\n')
            ocr_text = ""
            keyword = ""
            urls = []

            current_section = None

            for line in lines:
                if '[1]' in line and 'VĂN BẢN' in line: 
                    current_section = 'ocr'
                    continue
                elif '[2]' in line and 'TỪ KHÓA' in line:
                    current_section = 'keyword'
                    continue
                elif '[3]' in line and 'KẾT QUẢ' in line:
                    current_section = 'urls'
                    continue
                elif line.startswith('---') or line.startswith('===') or 'Xử lý hoàn tất' in line or 'Thời gian' in line or 'KẾT QUẢ XỬ LÝ' in line:
                    continue

                # Collect content based on section
                if current_section == 'ocr' and line.strip():
                    ocr_text += line + '\n'
                elif current_section == 'keyword' and line.strip():
                    keyword += line + ' '
                elif current_section == 'urls' and line.strip():
                    if '.' in line and ('http' in line or line[0].isdigit()):
                        urls.append(line.strip())

            total_chars += len(ocr_text)
            total_urls += len(urls)

            print(f"      OCR text: {len(ocr_text)} chars")
            print(f"      Keyword: {len(keyword.strip())} chars")
            print(f"      URLs: {len(urls)} found")

            # Add to HTML
            html_content += f"""
        <div class="result-card">
            <div class="result-title">📄 {filename}</div>

            <div class="section">
                <div class="section-title">🔍 [1] VĂN BẢN GỐC (OCR)</div>
                <div class="content">{ocr_text.strip() if ocr_text.strip() else '<div class="no-results">Không có dữ liệu</div>'}</div>
            </div>

            <div class="section">
                <div class="section-title">🎯 [2] TỪ KHÓA TÌM KIẾM</div>
                <div class="content">{keyword.strip() if keyword.strip() else '<div class="no-results">Không có từ khóa</div>'}</div>
            </div>

            <div class="section">
                <div class="section-title">🔗 [3] KẾT QUẢ TÌM KIẾM</div>
"""

            if urls:
                html_content += '                <ul class="url-list">\n'
                for url_line in urls:
                    if '. ' in url_line:
                        parts = url_line.split('. ', 1)
                        if len(parts) == 2 and parts[0].isdigit():
                            num, url = parts
                            html_content += f'                    <li><strong>{num}.</strong> <a href="{url}" target="_blank">{url}</a></li>\n'
                        else:
                            html_content += f'                    <li>{url_line}</li>\n'
                    else:
                        html_content += f'                    <li>{url_line}</li>\n'
                html_content += '                </ul>\n'
            else:
                html_content += '                <div class="content"><div class="no-results">Không tìm thấy kết quả</div></div>\n'

            html_content += """            </div>
        </div>
"""
        except Exception as e:
            print(f"      ⚠️ Error:  {e}")
            import traceback
            traceback.print_exc()

    html_content += """        <div class="footer">
            <p>🤖 Generated by DA2_OCR Pipeline</p>
            <p>Powered by Tesseract OCR + Gemini AI + DuckDuckGo Search</p>
        </div>
    </div>
</body>
</html>"""

    html_file = output_path / "summary_report.html"
    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content.format(
                timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                total=len(txt_files),
                total_chars=total_chars,
                total_urls=total_urls
            ))

        print(f"\n✅ HTML report created successfully!")
        print(f"📁 Location: {html_file.absolute()}")
        print(f"📊 Stats:")
        print(f"   - Files:  {len(txt_files)}")
        print(f"   - Characters: {total_chars:,}")
        print(f"   - URLs: {total_urls}")

        return html_file

    except Exception as e: 
        print(f"\n❌ Error creating HTML file: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("="*60)
    print("🔄 Generating HTML Report")
    print("="*60)
    print(f"📂 Current working directory: {os.getcwd()}")

    result = create_html_report()

    if result:
        print(f"\n{'='*60}")
        print("🎉 Success!")
        print(f"{'='*60}")
        print(f"📂 File location: {result}")
        print(f"\n💡 To open in browser:")
        print(f"   Invoke-Item \"{result}\"")
        print(f"   or double-click the file in File Explorer")
    else:
        print(f"\n{'='*60}")
        print("❌ Failed to create report")
        print(f"{'='*60}")
        sys.exit(1)