from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length).decode('utf-8'))
        prompt = f"""## 角色
作为 {data.get('persona', '')}

## 背景
{data.get('context', '')}

## 任务
{data.get('task', '')}

## 限制
{data.get('limit', '')}

## 输出
1. 以 Markdown 形式输出
2. 输出结果必须包含参考资料
3. 输出风格犀利、凝练、有力
4. 展示至少两种备选方案及其淘汰理由

---
{data.get('note', '这对我的职业生涯非常重要!')}"""
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
