from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length).decode('utf-8'))
        
        persona = data.get('persona', '')
        context = data.get('context', '')
        task = data.get('task', '')
        limit = data.get('limit', '')
        goal = data.get('goal', '')
        note = data.get('note', '这对我的职业生涯非常重要!')
        
        parts = []
        if persona:
            parts.append(f"## 角色\n作为 {persona}")
        if context:
            parts.append(f"## 背景\n{context}")
        if task:
            parts.append(f"## 任务\n{task}")
        if limit:
            parts.append(f"## 限制\n{limit}")
        if goal:
            parts.append(f"## 输出\n{goal}")
        if note:
            parts.append(f"---\n{note}")
            
        prompt = "\n\n".join(parts)
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"prompt": prompt, "logId": 1}, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
