from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

TEMPLATES = [
    {"id": 1, "title": "翻译文章", "content": "请尊重原意，保持原有格式不变，用简体中文重写内容。要求:\n1. 英文人名以及专业术语保持不变\n2. 代码片段维持原格式\n3. 风格与科普读物相似\n4. 适当解读专业术语", "templateType": "custom", "isSystem": True, "usageCount": 0, "tags": ["翻译", "文章"]}
]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        keyword = query.get('keyword', [''])[0]
        templates = [t for t in TEMPLATES if not keyword or keyword.lower() in t['title'].lower() or keyword.lower() in t['content'].lower()]
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"templates": templates}, ensure_ascii=False).encode('utf-8'))

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length).decode('utf-8'))
        new = {"id": len(TEMPLATES) + 1, "title": data.get('title', ''), "content": data.get('content', ''), "templateType": "custom", "isSystem": False, "usageCount": 0, "tags": data.get('tags', [])}
        TEMPLATES.append(new)
        self.send_response(201)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(new, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
