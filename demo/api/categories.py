from http.server import BaseHTTPRequestHandler
import json

CATEGORIES_DATA = {
    "categories": [
        {
            "id": "chat", "name": "对话", "icon": "💬",
            "products": [
                {"name": "Gemini", "url": "https://gemini.google.com/", "recommendReason": "长文本。有全家桶，效果好。", "price": "Pro ¥140", "tags": ["长文本", "谷歌", "全家桶"]},
                {"name": "豆包", "url": "https://www.doubao.com", "recommendReason": "有语音。有全家桶，效果不错。", "price": "免费", "tags": ["语音", "字节跳动", "全家桶"]},
                {"name": "Kimi", "url": "https://www.kimi.com", "recommendReason": "长文本。", "price": "免费", "tags": ["长文本", "月之暗面"]},
                {"name": "通义千问", "url": "https://chat.qwen.ai/", "recommendReason": "有全家桶，能对话有图片。", "price": "免费", "tags": ["全家桶", "阿里"]},
                {"name": "Grok", "url": "https://x.com/i/grok", "recommendReason": "特攻。我是当爬虫在用。", "price": "X 会员", "tags": ["特攻", "X"]}
            ]
        },
        {
            "id": "coding", "name": "编程", "icon": "💻",
            "products": [
                {"name": "Cursor", "url": "https://www.cursor.com/", "recommendReason": "目前的行业标准。", "price": "Pro ¥140/月", "tags": ["IDE", "行业标准"]},
                {"name": "Trae", "url": "https://www.trae.ai/", "recommendReason": "字节出品，Cursor 的强力竞争者。", "price": "¥70/月", "tags": ["IDE", "字节跳动"]},
                {"name": "Claude Code", "url": "https://claude.ai/code", "recommendReason": "命令行工具。", "price": "API 计费", "tags": ["Terminal", "Claude"]}
            ]
        },
        {
            "id": "image", "name": "图像", "icon": "🎨",
            "products": [
                {"name": "即梦", "url": "https://jimeng.jianying.com/", "recommendReason": "文生图、文生视频。", "price": "¥69/月", "tags": ["文生图", "文生视频"]},
                {"name": "Gemini", "url": "https://gemini.google.com/", "recommendReason": "通过 API 调用。", "price": "约 ¥1/张", "tags": ["文生图", "API"]}
            ]
        },
        {
            "id": "knowledge", "name": "效率与知识库", "icon": "📚",
            "products": [
                {"name": "NotebookLM", "url": "https://notebooklm.google.com/", "recommendReason": "PDF 生成播客、摘要。", "price": "免费", "tags": ["PDF", "播客"]},
                {"name": "秘塔 AI 搜索", "url": "https://metaso.cn/", "recommendReason": "国内搜资料首选。", "price": "免费", "tags": ["搜索", "国内"]},
                {"name": "Perplexity", "url": "https://www.perplexity.ai/", "recommendReason": "国外搜资料首选。", "price": "免费/Pro", "tags": ["搜索", "国外"]}
            ]
        },
        {
            "id": "agent", "name": "智能体", "icon": "🤖",
            "products": [
                {"name": "Coze", "url": "https://www.coze.cn/", "recommendReason": "搭建工作流机器人。", "price": "免费", "tags": ["工作流", "飞书"]},
                {"name": "n8n", "url": "https://n8n.io/", "recommendReason": "本地工作流自动化。", "price": "免费/付费", "tags": ["工作流", "开源"]},
                {"name": "Manus", "url": "https://www.manus.ai/", "recommendReason": "操控浏览器智能体。", "price": "待定", "tags": ["浏览器", "自动化"]}
            ]
        }
    ]
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(CATEGORIES_DATA, ensure_ascii=False).encode('utf-8'))
