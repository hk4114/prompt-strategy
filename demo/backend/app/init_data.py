"""初始化数据"""
from app import db
from app.models import Category, Product, ProductTag, PromptTemplate, PromptTip, Tag


def init_data():
    """初始化数据库数据"""
    # 检查是否已有数据
    if Category.query.first():
        return
    
    # 初始化分类和产品数据
    categories_data = [
        {
            "category_key": "chat",
            "name": "对话",
            "icon": "💬",
            "sort_order": 1,
            "products": [
                {
                    "name": "Gemini",
                    "url": "https://gemini.google.com/",
                    "recommend_reason": "长文本。有全家桶，效果好。",
                    "price": "Pro ¥140",
                    "tags": ["长文本", "谷歌", "全家桶", "写长文", "逻辑"]
                },
                {
                    "name": "豆包",
                    "url": "https://www.doubao.com",
                    "recommend_reason": "有语音。有全家桶，效果不错。",
                    "price": "免费",
                    "tags": ["语音", "字节跳动", "全家桶", "日常", "手机端"]
                },
                {
                    "name": "Kimi",
                    "url": "https://www.kimi.com",
                    "recommend_reason": "长文本。",
                    "price": "免费",
                    "tags": ["长文本", "月之暗面", "日常", "手机端"]
                },
                {
                    "name": "通义千问",
                    "url": "https://chat.qwen.ai/",
                    "recommend_reason": "有全家桶，能对话有图片。效果勉勉强强。",
                    "price": "免费",
                    "tags": ["全家桶", "对话", "图片", "阿里", "qwen"]
                },
                {
                    "name": "Grok",
                    "url": "https://x.com/i/grok",
                    "recommend_reason": "特攻。我是当爬虫在用。",
                    "price": "X 会员",
                    "tags": ["特攻", "爬虫", "X", "Twitter"]
                }
            ]
        },
        {
            "category_key": "coding",
            "name": "编程",
            "icon": "💻",
            "sort_order": 2,
            "products": [
                {
                    "name": "Cursor",
                    "url": "https://www.cursor.com/",
                    "recommend_reason": "目前的行业标准。",
                    "price": "Pro 版约 ¥140/月",
                    "tags": ["IDE", "行业标准", "编程", "开发环境"]
                },
                {
                    "name": "Trae",
                    "url": "https://www.trae.ai/",
                    "recommend_reason": "字节出品，Cursor 的强力竞争者，不仅免费还非常好用。",
                    "price": "首月 ¥21/月 后续 ¥70/月",
                    "tags": ["IDE", "字节跳动", "免费", "编程", "开发环境"]
                },
                {
                    "name": "Claude Code",
                    "url": "https://claude.ai/code",
                    "recommend_reason": "命令行工具，建议配合国产模型 (Minimax/kimi k2) 的 API 使用。",
                    "price": "API 计费",
                    "tags": ["Terminal", "命令行", "Claude", "Minimax", "kimi"]
                }
            ]
        },
        {
            "category_key": "image",
            "name": "图像",
            "icon": "🎨",
            "sort_order": 3,
            "products": [
                {
                    "name": "即梦 (Jimeng)",
                    "url": "https://jimeng.jianying.com/",
                    "recommend_reason": "包含：文生图、文生视频。",
                    "price": "基础会员 ¥69/月",
                    "tags": ["文生图", "文生视频", "剪映", "字节跳动"]
                },
                {
                    "name": "Gemini (nano banana2)",
                    "url": "https://gemini.google.com/",
                    "recommend_reason": "含在 Gemini 订阅中，或通过 API 调用。",
                    "price": "约 ¥1/张",
                    "tags": ["文生图", "API", "谷歌", "nano", "每日限额"]
                }
            ]
        },
        {
            "category_key": "knowledge",
            "name": "效率与知识库",
            "icon": "📚",
            "sort_order": 4,
            "products": [
                {
                    "name": "NotebookLM",
                    "url": "https://notebooklm.google.com/",
                    "recommend_reason": "丢进去一堆 PDF，能生成播客、摘要、思维导图。",
                    "price": "免费",
                    "tags": ["PDF", "播客", "摘要", "思维导图", "谷歌", "知识库"]
                },
                {
                    "name": "Ima",
                    "url": "https://ima.qq.com/",
                    "recommend_reason": "适合整理凌乱的想法。",
                    "price": "免费",
                    "tags": ["知识库", "整理", "腾讯", "碎片想法"]
                },
                {
                    "name": "Youmind",
                    "url": "https://youmind.com/zh-CN/",
                    "recommend_reason": "类似 notebooklm。",
                    "price": "免费",
                    "tags": ["知识库", "思维导图", "碎片信息", "整理"]
                },
                {
                    "name": "秘塔 AI 搜索",
                    "url": "https://metaso.cn/",
                    "recommend_reason": "国内搜资料首选，无广告，直达信源。",
                    "price": "免费",
                    "tags": ["搜索", "无广告", "国内", "DeepResearch"]
                },
                {
                    "name": "Perplexity",
                    "url": "https://www.perplexity.ai/",
                    "recommend_reason": "国外搜资料首选。",
                    "price": "免费/Pro",
                    "tags": ["搜索", "国外", "DeepResearch", "问答"]
                },
                {
                    "name": "ithy",
                    "url": "https://ithy.com/",
                    "recommend_reason": "深度搜索工具。",
                    "price": "免费",
                    "tags": ["搜索", "深度研究", "研究工具"]
                }
            ]
        },
        {
            "category_key": "agent",
            "name": "智能体",
            "icon": "🤖",
            "sort_order": 5,
            "products": [
                {
                    "name": "Coze (扣子)",
                    "url": "https://www.coze.cn/",
                    "recommend_reason": "配合飞书使用，搭建自己的工作流机器人。",
                    "price": "免费",
                    "tags": ["工作流", "飞书", "机器人", "字节跳动", "Agent"]
                },
                {
                    "name": "n8n",
                    "url": "https://n8n.io/",
                    "recommend_reason": "本地工作流自动化工具。",
                    "price": "免费/付费",
                    "tags": ["工作流", "本地", "自动化", "开源"]
                },
                {
                    "name": "Manus",
                    "url": "https://www.manus.ai/",
                    "recommend_reason": "能够操控浏览器的智能体，帮你自动订票、填表。",
                    "price": "待定",
                    "tags": ["浏览器操控", "自动化", "订票", "填表", "Agent"]
                },
                {
                    "name": "AutoGLM",
                    "url": "https://autoglm.zhipuai.cn/",
                    "recommend_reason": "能够操控浏览器的智能体，帮你自动订票、填表。",
                    "price": "免费",
                    "tags": ["浏览器操控", "自动化", "智谱AI", "Agent"]
                }
            ]
        }
    ]
    
    # 插入分类和产品
    for cat_data in categories_data:
        products_data = cat_data.pop('products')
        category = Category(**cat_data)
        db.session.add(category)
        db.session.flush()
        
        for idx, prod_data in enumerate(products_data):
            tags = prod_data.pop('tags')
            product = Product(
                category_id=category.id,
                sort_order=idx,
                **prod_data
            )
            db.session.add(product)
            db.session.flush()
            
            for tag_name in tags:
                tag = ProductTag(product_id=product.id, tag_name=tag_name)
                db.session.add(tag)
    
    # 初始化提示词模板
    templates = [
        {
            "title": "翻译文章",
            "content": """请尊重原意，保持原有格式不变，用简体中文重写内容。要求:
1. 英文人名以及专业术语保持不变
2. 代码片段维持原格式
3. 风格与科普读物相似
4. 适当解读：如果是普通人难懂的专业术语或因为文化差异导致的难以理解，做出更多的注释以更好的理解，注释部分用括号包裹并加粗""",
            "template_type": "custom",
            "is_system": True
        },
        {
            "title": "代码审查",
            "content": """作为高级代码审查专家，请审查以下代码并提供反馈：

## 审查要点
1. 代码质量和可读性
2. 潜在的bug或安全漏洞
3. 性能优化建议
4. 最佳实践建议

请按以下格式输出：
- 🟢 优点：...
- 🟡 建议改进：...
- 🔴 必须修复：...""",
            "template_type": "custom",
            "is_system": True
        },
        {
            "title": "需求分析",
            "content": """作为产品经理和需求分析专家，请帮我分析以下需求：

## 你需要输出
1. 用户故事（User Story）
2. 功能点拆解
3. 优先级排序（P0/P1/P2）
4. 可能的风险和边界情况
5. 技术实现建议""",
            "template_type": "custom",
            "is_system": True
        }
    ]
    
    for tmpl_data in templates:
        template = PromptTemplate(**tmpl_data)
        db.session.add(template)
    
    # 初始化提示词技巧
    tips = [
        {
            "title": "角色设定技巧",
            "content": "在提示词开头明确AI的角色，例如：'作为一名资深产品经理...'，这能帮助AI更好地理解你的期望。",
            "sort_order": 1
        },
        {
            "title": "提供具体示例",
            "content": "给AI提供一个你期望输出的示例，比抽象描述更有效。例如：'输出格式参考：标题-内容-建议'。",
            "sort_order": 2
        },
        {
            "title": "分步骤要求",
            "content": "复杂任务分步进行：'第一步：...，第二步：...'，可以帮助AI更有条理地完成任务。",
            "sort_order": 3
        },
        {
            "title": "设定边界条件",
            "content": "明确限制条件：'字数控制在500字以内'、'只使用中文回答'，避免输出不符合预期。",
            "sort_order": 4
        }
    ]
    
    for tip_data in tips:
        tip = PromptTip(**tip_data)
        db.session.add(tip)
    
    db.session.commit()
    print("初始化数据完成！")
