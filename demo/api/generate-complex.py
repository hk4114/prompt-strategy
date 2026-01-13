from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length).decode('utf-8'))
        prompt = f"""### 角色
作为 {data.get('role', '')} 专家

### 背景
当前面临 {data.get('background', '')} 问题
交代背景与受众：明确 AI 应扮演的角色、任务发生的场景以及目标群体

### 任务
{data.get('task', '')}

### 要求
{data.get('requirements', '')}

### 格式
{data.get('format', '')}

### 范例
{data.get('example', '')}"""
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
