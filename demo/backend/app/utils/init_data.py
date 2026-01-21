import os
import json
from app.models import PromptTemplate, Tag, TemplateTag, Category, Product, ProductTag, PromptTip
from app import db

def init_categories(app):
    """Initialize default categories and products if not exist."""
    with app.app_context():
        if Category.query.first():
            return
            
        print("Initializing default categories and products...")
        
        # 插入分类数据
        categories_data = [
            {'category_key': 'chat', 'name': '对话', 'icon': '💬', 'sort_order': 1},
            {'category_key': 'coding', 'name': '编程', 'icon': '💻', 'sort_order': 2},
            {'category_key': 'image', 'name': '图像', 'icon': '🎨', 'sort_order': 3},
            {'category_key': 'knowledge', 'name': '效率与知识库', 'icon': '📚', 'sort_order': 4},
            {'category_key': 'agent', 'name': '智能体', 'icon': '🤖', 'sort_order': 5},
            {'category_key': 'google', 'name': 'google 全家桶', 'icon': '🍌', 'sort_order': 6},
        ]

        category_map = {}
        for cat_data in categories_data:
            cat = Category(**cat_data)
            db.session.add(cat)
            db.session.flush()
            category_map[cat_data['category_key']] = cat.id

        # 插入产品数据
        products_data = [
            # 对话类
            {'category_key': 'chat', 'name': 'Gemini', 'url': 'https://gemini.google.com/',
             'recommend_reason': '长文本。有全家桶，效果好。', 'price': 'Pro ¥140',
             'tags': ['长文本', '谷歌', '全家桶', '写长文', '逻辑']},
            {'category_key': 'chat', 'name': '豆包', 'url': 'https://www.doubao.com',
             'recommend_reason': '有语音。有全家桶，效果不错。', 'price': '免费',
             'tags': ['语音', '字节跳动', '全家桶', '日常', '手机端']},
            {'category_key': 'chat', 'name': 'Kimi', 'url': 'https://www.kimi.com',
             'recommend_reason': '长文本。', 'price': '免费',
             'tags': ['长文本', '月之暗面', '日常', '手机端']},
            {'category_key': 'chat', 'name': '通义千问', 'url': 'https://chat.qwen.ai/',
             'recommend_reason': '有全家桶，能对话有图片。效果勉勉强强。', 'price': '免费',
             'tags': ['全家桶', '对话', '图片', '阿里', 'qwen']},
            {'category_key': 'chat', 'name': 'Grok', 'url': 'https://x.com/i/grok',
             'recommend_reason': '特攻。我是当爬虫在用。', 'price': 'X 会员',
             'tags': ['特攻', '爬虫', 'X', 'Twitter']},

            # 编程类
            {'category_key': 'coding', 'name': 'Cursor', 'url': 'https://www.cursor.com/',
             'recommend_reason': '目前的行业标准。', 'price': 'Pro 版约 ¥140/月',
             'tags': ['IDE', '行业标准', '编程', '开发环境']},
            {'category_key': 'coding', 'name': 'Trae', 'url': 'https://www.trae.ai/',
             'recommend_reason': '字节出品，Cursor 的强力竞争者，不仅免费还非常好用。',
             'price': '首月 ¥21/月 后续 ¥70/月',
             'tags': ['IDE', '字节跳动', '免费', '编程', '开发环境']},
            {'category_key': 'coding', 'name': 'Claude Code', 'url': 'https://claude.ai/code',
             'recommend_reason': '命令行工具，建议配合国产模型 (Minimax/kimi k2) 的 API 使用。',
             'price': 'API 计费',
             'tags': ['Terminal', '命令行', 'Claude', 'Minimax', 'kimi']},

            # 图像类
            {'category_key': 'image', 'name': '即梦 (Jimeng)', 'url': 'https://jimeng.jianying.com/',
             'recommend_reason': '包含：文生图、文生视频。', 'price': '基础会员 ¥69/月',
             'tags': ['文生图', '文生视频', '剪映', '字节跳动']},
            {'category_key': 'image', 'name': 'Gemini (nano banana2)', 'url': 'https://gemini.google.com/',
             'recommend_reason': '含在 Gemini 订阅中，或通过 API 调用。', 'price': '约 ¥1/张',
             'tags': ['文生图', 'API', '谷歌', 'nano', '每日限额']},

            # 效率与知识库
            {'category_key': 'knowledge', 'name': 'NotebookLM', 'url': 'https://notebooklm.google.com/',
             'recommend_reason': '丢进去一堆 PDF，能生成播客、摘要、思维导图。', 'price': '免费',
             'tags': ['PDF', '播客', '摘要', '思维导图', '谷歌', '知识库']},
            {'category_key': 'knowledge', 'name': 'Ima', 'url': 'https://ima.qq.com/',
             'recommend_reason': '适合整理凌乱的想法。', 'price': '免费',
             'tags': ['知识库', '整理', '腾讯', '碎片想法']},
            {'category_key': 'knowledge', 'name': 'Youmind', 'url': 'https://youmind.com/zh-CN/',
             'recommend_reason': '类似 notebooklm。', 'price': '免费',
             'tags': ['知识库', '思维导图', '碎片信息', '整理']},
            {'category_key': 'knowledge', 'name': '秘塔 AI 搜索', 'url': 'https://metaso.cn/',
             'recommend_reason': '国内搜资料首选，无广告，直达信源。', 'price': '免费',
             'tags': ['搜索', '无广告', '国内', 'DeepResearch']},
            {'category_key': 'knowledge', 'name': 'Perplexity', 'url': 'https://www.perplexity.ai/',
             'recommend_reason': '国外搜资料首选。', 'price': '免费/Pro',
             'tags': ['搜索', '国外', 'DeepResearch', '问答']},
            {'category_key': 'knowledge', 'name': 'ithy', 'url': 'https://ithy.com/',
             'recommend_reason': '深度搜索工具。', 'price': '免费',
             'tags': ['搜索', '深度研究', '研究工具']},

            # 智能体
            {'category_key': 'agent', 'name': 'Coze (扣子)', 'url': 'https://www.coze.cn/',
             'recommend_reason': '配合飞书使用，搭建自己的工作流机器人。', 'price': '免费',
             'tags': ['工作流', '飞书', '机器人', '字节跳动', 'Agent']},
            {'category_key': 'agent', 'name': 'n8n', 'url': 'https://n8n.io/',
             'recommend_reason': '本地工作流自动化工具。', 'price': '免费/付费',
             'tags': ['工作流', '本地', '自动化', '开源']},
            {'category_key': 'agent', 'name': 'Manus', 'url': 'https://www.manus.ai/',
             'recommend_reason': '能够操控浏览器的智能体，帮你自动订票、填表。', 'price': '待定',
             'tags': ['浏览器操控', '自动化', '订票', '填表', 'Agent']},
            {'category_key': 'agent', 'name': 'AutoGLM', 'url': 'https://autoglm.zhipuai.cn/',
             'recommend_reason': '能够操控浏览器的智能体，帮你自动订票、填表。', 'price': '免费',
             'tags': ['浏览器操控', '自动化', '智谱AI', 'Agent']},

            #  谷歌全家桶
            {"category_key": "google",
          "name": "Gemini (nano banana2)",
          "url": "https://gemini.google.com/",
          "recommend_reason": "含在 Gemini 订阅中，或通过 API 调用。",
          "price": "约 ¥1/张",
          "tags": ["文生图", "API", "谷歌", "nano", "每日限额"]
        },
        {
          "name": "NotebookLM",
          "category_key": "google",
          "url": "https://notebooklm.google.com/",
          "recommend_reason": "丢进去一堆 PDF，能生成播客、摘要、思维导图。",
          "price": "免费",
          "tags": ["PDF", "播客", "摘要", "思维导图", "谷歌", "知识库"]
        },
        {
          "name": "stitch",
          "category_key": "google",
          "url": "https://stitch.withgoogle.com/",
          "recommend_reason": "原型",
          "price": "免费",
          "tags": ["原型", "产品", "API", "谷歌", "每日限额"]
        },
        {
          "name": "antigravity",
          "category_key": "google",
          "url": "https://antigravity.google/",
          "recommend_reason": "IDE",
          "price": "免费",
          "tags": ["开发", "编程", "API", "谷歌"]
        },
        {
          "name": "Gemini CLI",
          "category_key": "google",
          "url": "https://my.feishu.cn/wiki/GrVlw4opIioIyVkIFLWcdfoUn2e",
          "recommend_reason": "IDE",
          "price": "免费",
          "tags": ["开发", "编程", "API", "谷歌", "开源"]
        },
        {
          "name": "AI studio",
          "category_key": "google",
          "url": "https://aistudio.google.com/api-keys",
          "recommend_reason": "平台",
          "price": "免费",
          "tags": ["开发", "编程", "API", "谷歌", "开源"]
        }
        ]

        for i, prod_data in enumerate(products_data):
            product = Product(
                category_id=category_map[prod_data['category_key']],
                name=prod_data['name'],
                url=prod_data['url'],
                recommend_reason=prod_data['recommend_reason'],
                price=prod_data['price'],
                sort_order=i
            )
            db.session.add(product)
            db.session.flush()

            for tag_name in prod_data['tags']:
                tag = ProductTag(product_id=product.id, tag_name=tag_name)
                db.session.add(tag)
        
        db.session.commit()
        print("Default categories and products initialized.")

def init_tips(app):
    """Initialize default tips if not exist."""
    with app.app_context():
        if PromptTip.query.first():
            return
            
        print("Initializing default tips...")
        tips_data = [
            {'title': '技巧一', 'content': '点击复制按钮，生成结果中添加文案', 'sort_order': 1},
            {'title': '技巧二', 'content': '作为参考常驻页面，支持缩放', 'sort_order': 2},
        ]
        for tip_data in tips_data:
            tip = PromptTip(**tip_data)
            db.session.add(tip)
        
        db.session.commit()
        print("Default tips initialized.")

def init_default_templates(app):
    """Initialize default templates if database is empty."""
    with app.app_context():
        # Check if templates exist
        if PromptTemplate.query.first():
            print("Templates already exist. Skipping initialization.")
            return

        print("Initializing default templates from JSON...")
        
        # Path to templates_export_2026-01-14.json
        # app/utils/init_data.py -> app/utils -> app -> backend -> demo -> project root
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        file_path = os.path.join(base_dir, 'templates_export_2026-01-14.json')
        
        # Check if file exists, if not try looking in project root relative to current working directory
        if not os.path.exists(file_path):
             # Fallback: try absolute path provided by user
             file_path = '/Users/kanehua/project/prompt-strategy/templates_export_2026-01-14.json'
        
        if not os.path.exists(file_path):
            print(f"Error: Default templates file not found at {file_path}")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                templates = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON file: {e}")
            return
        except Exception as e:
            print(f"Error: Failed to read file: {e}")
            return
            
        if not isinstance(templates, list):
            print("Error: JSON root must be an array")
            return

        success_count = 0
        warning_count = 0

        for t in templates:
            # Validate required fields
            if 'title' not in t or 'content' not in t:
                print(f"Warning: Skipping invalid template: {t.get('title', 'Unknown')}")
                warning_count += 1
                continue
                
            template = PromptTemplate(
                title=t['title'],
                content=t['content'],
                template_type=t.get('templateType', 'custom'),
                is_system=t.get('isSystem', False)
            )
            db.session.add(template)
            db.session.flush()
            
            # Process tags
            if 'tags' in t and isinstance(t['tags'], list):
                for tag_name in t['tags']:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                        db.session.flush()
                    
                    template_tag = TemplateTag(template_id=template.id, tag_id=tag.id)
                    db.session.add(template_tag)
            
            success_count += 1
            
        try:
            db.session.commit()
            print(f"Successfully initialized {success_count} default templates.")
            if warning_count > 0:
                print(f"Skipped {warning_count} invalid templates.")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to initialize default templates: {e}")
