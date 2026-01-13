from flask import Blueprint, jsonify, request
from ..models import db, PromptTemplate, Tag, TemplateTag
import json

templates_bp = Blueprint('templates', __name__)

# Initialize default templates
def init_default_templates():
    """Initialize default prompt templates"""
    if PromptTemplate.query.first() is not None:
        return

    default_templates = [
        {
            'title': '翻译文章',
            'content': '''请尊重原意，保持原有格式不变，用简体中文重写内容。要求:
1. 英文人名以及专业术语保持不变
2. 代码片段维持原格式
3. 风格与科普读物相似
4. 适当解读：如果是普通人难懂的专业术语或因为文化差异导致的难以理解，做出更多的注释以更好的理解，注释部分用括号包裹并加粗''',
            'template_type': 'minimal_formula',
            'is_system': True,
            'tags': ['翻译', '中文', '专业术语']
        },
        {
            'title': '技术文档解释',
            'content': '''作为技术文档解释专家，请帮助理解以下技术文档：

## 背景
用户需要理解一份技术文档的核心概念和实现细节

## 任务
用通俗易懂的语言解释以下技术文档的关键点，包括：
1. 核心概念
2. 实现原理
3. 使用场景
4. 优缺点分析

## 要求
- 避免使用过于专业的术语，必要时请解释
- 提供具体的例子帮助理解
- 结构清晰，层次分明
- 适合初学者阅读''',
            'template_type': 'minimal_formula',
            'is_system': True,
            'tags': ['技术', '解释', '文档', '初学者']
        },
        {
            'title': '代码审查',
            'content': '''作为资深开发工程师，请审查以下代码：

## 角色
资深开发工程师，专注于代码质量和最佳实践

## 背景
需要审查一段代码，发现潜在问题并提出改进建议

## 任务
审查以下代码，从以下方面进行分析：
1. 代码规范性问题
2. 潜在的bug
3. 性能优化建议
4. 安全漏洞
5. 可维护性改进

## 要求
- 具体问题具体分析，不要泛泛而谈
- 提供具体的改进代码示例
- 解释每个问题的影响和修复方法
- 优先关注严重问题''',
            'template_type': 'complex_8step',
            'is_system': True,
            'tags': ['代码', '审查', '质量', '最佳实践']
        },
        {
            'title': '需求分析',
            'content': '''### 角色
作为产品经理和系统架构师

### 背景
当前面临 [需求不明确] 问题
需要分析用户需求并制定产品方案

### 任务
第一轮：理解用户的核心痛点和目标
第二轮：提出解决方案的框架和关键功能
第三轮：制定实施计划和优先级排序

### 要求
- 从用户价值角度思考
- 考虑技术可行性和商业可行性
- 提供具体的验收标准
- 识别潜在风险

### 格式
1. 请使用 Markdown 格式输出
2. 首先给出需求优先级排序
3. 然后分 '核心功能'、'次要功能'、'未来规划' 三个板块

### 范例
例如，你可以这样分析：'用户真正的需求是节省时间，而不是增加更多功能' ''',
            'template_type': 'complex_8step',
            'is_system': True,
            'tags': ['需求', '分析', '产品', '规划']
        }
    ]

    try:
        for template_data in default_templates:
            # Create template
            template = PromptTemplate(
                title=template_data['title'],
                content=template_data['content'],
                template_type=template_data['template_type'],
                is_system=template_data['is_system'],
                usage_count=0
            )
            db.session.add(template)
            db.session.flush()

            # Create tags
            for tag_name in template_data['tags']:
                # Check if tag exists
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()

                # Create template-tag association
                template_tag = TemplateTag(
                    template_id=template.id,
                    tag_id=tag.id
                )
                db.session.add(template_tag)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing default templates: {e}")


@templates_bp.route('', methods=['GET'])
def get_templates():
    """Get all templates with optional filtering"""
    template_type = request.args.get('type')
    search = request.args.get('search', '').strip()
    tag = request.args.get('tag', '').strip()

    query = PromptTemplate.query

    # Filter by type
    if template_type:
        query = query.filter_by(template_type=template_type)

    # Filter by tag
    if tag:
        query = query.join(TemplateTag).join(Tag).filter(Tag.name == tag)

    # Search in title and content
    if search:
        query = query.filter(
            db.or_(
                PromptTemplate.title.contains(search),
                PromptTemplate.content.contains(search)
            )
        )

    templates = query.order_by(PromptTemplate.usage_count.desc()).all()

    if not templates:
        init_default_templates()
        templates = query.order_by(PromptTemplate.usage_count.desc()).all()

    return jsonify({
        'templates': [template.to_dict() for template in templates]
    })


@templates_bp.route('', methods=['POST'])
def create_template():
    """Create a new template"""
    data = request.json

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title = data.get('title')
    content = data.get('content')
    template_type = data.get('template_type', 'minimal_formula')
    tag_names = data.get('tags', [])

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400

    try:
        template = PromptTemplate(
            title=title,
            content=content,
            template_type=template_type,
            is_system=False,
            usage_count=0
        )
        db.session.add(template)
        db.session.flush()

        # Add tags
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.flush()

            template_tag = TemplateTag(
                template_id=template.id,
                tag_id=tag.id
            )
            db.session.add(template_tag)

        db.session.commit()

        return jsonify({
            'message': 'Template created successfully',
            'template': template.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@templates_bp.route('/<int:template_id>', methods=['GET'])
def get_template(template_id):
    """Get a single template"""
    template = PromptTemplate.query.get(template_id)

    if not template:
        return jsonify({'error': 'Template not found'}), 404

    return jsonify(template.to_dict())


@templates_bp.route('/<int:template_id>/use', methods=['POST'])
def increment_usage(template_id):
    """Increment template usage count"""
    template = PromptTemplate.query.get(template_id)

    if not template:
        return jsonify({'error': 'Template not found'}), 404

    template.usage_count += 1
    db.session.commit()

    return jsonify({'message': 'Usage count updated'})


@templates_bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all tag names"""
    tags = Tag.query.all()
    return jsonify({
        'tags': [tag.name for tag in tags]
    })
