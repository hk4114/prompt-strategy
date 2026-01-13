from http.server import BaseHTTPRequestHandler
import json

CATEGORIES_DATA = {
    "categories": [
        {
            "id": "chat", "name": "对话", "icon": "💬",
            "products": [
                {"name": "Gemini", "url": "https://gemini.google.com/", "recommendReason": "长文本。有全家桶，效果好。", "price": "Pro ¥140", "tags": ["长文本", "谷歌", "全家桶", "写长文", "逻辑"]},
                {"name": "豆包", "url": "https://www.doubao.com", "recommendReason": "有语音。有全家桶，效果不错。", "price": "免费", "tags": ["语音", "字节跳动", "全家桶", "日常", "手机端"]},
                {"name": "Kimi", "url": "https://www.kimi.com", "recommendReason": "长文本。", "price": "免费", "tags": ["长文本", "月之暗面", "日常", "手机端"]},
                {"name": "通义千问", "url": "https://chat.qwen.ai/", "recommendReason": "有全家桶，能对话有图片。效果勉勉强强。", "price": "免费", "tags": ["全家桶", "对话", "图片", "阿里", "qwen"]},
                {"name": "Grok", "url": "https://x.com/i/grok", "recommendReason": "特攻。我是当爬虫在用。", "price": "X 会员", "tags": ["特攻", "爬虫", "X", "Twitter"]}
            ]
        },
        {
            "id": "coding", "name": "编程", "icon": "💻",
            "products": [
                {"name": "Cursor", "url": "https://www.cursor.com/", "recommendReason": "目前的行业标准。", "price": "Pro 版约 ¥140/月", "tags": ["IDE", "行业标准", "编程", "开发环境"]},
                {"name": "Trae", "url": "https://www.trae.ai/", "recommendReason": "字节出品，Cursor 的强力竞争者，不仅免费还非常好用。", "price": "首月 ¥21/月 后续 ¥70/月", "tags": ["IDE", "字节跳动", "免费", "编程", "开发环境"]},
                {"name": "Claude Code", "url": "https://claude.ai/code", "recommendReason": "命令行工具，建议配合国产模型 (Minimax/kimi k2) 的 API 使用。", "price": "API 计费", "tags": ["Terminal", "命令行", "Claude", "Minimax", "kimi"]}
            ]
        },
        {
            "id": "image", "name": "图像", "icon": "🎨",
            "products": [
                {"name": "即梦 (Jimeng)", "url": "https://jimeng.jianying.com/", "recommendReason": "包含：文生图、文生视频。", "price": "基础会员 ¥69/月", "tags": ["文生图", "文生视频", "剪映", "字节跳动"]},
                {"name": "Gemini (nano banana2)", "url": "https://gemini.google.com/", "recommendReason": "含在 Gemini 订阅中，或通过 API 调用。", "price": "约 ¥1/张", "tags": ["文生图", "API", "谷歌", "nano", "每日限额"]}
            ]
        },
        {
            "id": "knowledge", "name": "效率与知识库", "icon": "📚",
            "products": [
                {"name": "NotebookLM", "url": "https://notebooklm.google.com/", "recommendReason": "丢进去一堆 PDF，能生成播客、摘要、思维导图。", "price": "免费", "tags": ["PDF", "播客", "摘要", "思维导图", "谷歌", "知识库"]},
                {"name": "Ima", "url": "https://ima.qq.com/", "recommendReason": "适合整理凌乱的想法。", "price": "免费", "tags": ["知识库", "整理", "腾讯", "碎片想法"]},
                {"name": "Youmind", "url": "https://youmind.com/zh-CN/", "recommendReason": "类似 notebooklm。", "price": "免费", "tags": ["知识库", "思维导图", "碎片信息", "整理"]},
                {"name": "秘塔 AI 搜索", "url": "https://metaso.cn/", "recommendReason": "国内搜资料首选，无广告，直达信源。", "price": "免费", "tags": ["搜索", "无广告", "国内", "DeepResearch"]},
                {"name": "Perplexity", "url": "https://www.perplexity.ai/", "recommendReason": "国外搜资料首选。", "price": "免费/Pro", "tags": ["搜索", "国外", "DeepResearch", "问答"]},
                {"name": "ithy", "url": "https://ithy.com/", "recommendReason": "深度搜索工具。", "price": "免费", "tags": ["搜索", "深度研究", "研究工具"]}
            ]
        },
        {
            "id": "agent", "name": "智能体", "icon": "🤖",
            "products": [
                {"name": "Coze (扣子)", "url": "https://www.coze.cn/", "recommendReason": "配合飞书使用，搭建自己的工作流机器人。", "price": "免费", "tags": ["工作流", "飞书", "机器人", "字节跳动", "Agent"]},
                {"name": "n8n", "url": "https://n8n.io/", "recommendReason": "本地工作流自动化工具。", "price": "免费/付费", "tags": ["工作流", "本地", "自动化", "开源"]},
                {"name": "Manus", "url": "https://www.manus.ai/", "recommendReason": "能够操控浏览器的智能体，帮你自动订票、填表。", "price": "待定", "tags": ["浏览器操控", "自动化", "订票", "填表", "Agent"]},
                {"name": "AutoGLM", "url": "https://autoglm.zhipuai.cn/", "recommendReason": "能够操控浏览器的智能体，帮你自动订票、填表。", "price": "免费", "tags": ["浏览器操控", "自动化", "智谱AI", "Agent"]}
            ]
        },
        {
            "id": "google", "name": "谷歌全家桶", "icon": "🍌",
            "products": [
                {"category_key": "google", "name": "Gemini (nano banana2)", "url": "https://gemini.google.com/", "recommendReason": "含在 Gemini 订阅中，或通过 API 调用。", "price": "约 ¥1/张", "tags": ["文生图", "API", "谷歌", "nano", "每日限额"]},
                {"name": "NotebookLM", "category_key": "google", "url": "https://notebooklm.google.com/", "recommendReason": "丢进去一堆 PDF，能生成播客、摘要、思维导图。", "price": "免费", "tags": ["PDF", "播客", "摘要", "思维导图", "谷歌", "知识库"]},
                {"name": "stitch", "category_key": "google", "url": "https://stitch.withgoogle.com/", "recommendReason": "原型", "price": "免费", "tags": ["原型", "产品", "API", "谷歌", "每日限额"]},
                {"name": "antigravity", "category_key": "google", "url": "https://antigravity.google/", "recommendReason": "IDE", "price": "免费", "tags": ["开发", "编程", "API", "谷歌"]},
                {"name": "Gemini CLI", "category_key": "google", "url": "https://my.feishu.cn/wiki/GrVlw4opIioIyVkIFLWcdfoUn2e", "recommendReason": "IDE", "price": "免费", "tags": ["开发", "编程", "API", "谷歌", "开源"]},
                {"name": "AI studio", "category_key": "google", "url": "https://aistudio.google.com/api-keys", "recommendReason": "平台", "price": "免费", "tags": ["开发", "编程", "API", "谷歌", "开源"]}
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
