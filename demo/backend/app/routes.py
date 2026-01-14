from flask import Blueprint, jsonify, request
from app import db
from app.models import (
    Category, Product, ProductTag, PromptTemplate, Tag, TemplateTag,
    PromptUsageLog, ReviewRecord, PromptTip
)
import json

api_bp = Blueprint('api', __name__)


# ==================== 首页相关接口 ====================

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取所有分类和产品"""
    categories = Category.query.order_by(Category.sort_order).all()
    return jsonify({
        'categories': [c.to_dict() for c in categories]
    })


# ==================== 提示词模板接口 ====================

@api_bp.route('/templates', methods=['GET'])
def get_templates():
    """获取提示词模板列表"""
    keyword = request.args.get('keyword', '')
    template_type = request.args.get('type', '')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    query = PromptTemplate.query

    if keyword:
        query = query.filter(
            db.or_(
                PromptTemplate.title.contains(keyword),
                PromptTemplate.content.contains(keyword)
            )
        )

    if template_type:
        query = query.filter(PromptTemplate.template_type == template_type)

    pagination = query.order_by(PromptTemplate.usage_count.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    return jsonify({
        'templates': [t.to_dict() for t in pagination.items],
        'total': pagination.total,
        'page': page,
        'page_size': page_size
    })


@api_bp.route('/templates', methods=['POST'])
def create_template():
    """创建提示词模板"""
    data = request.get_json()

    template = PromptTemplate(
        title=data['title'],
        content=data['content'],
        template_type=data.get('templateType', 'custom'),
        is_system=data.get('isSystem', False)
    )
    db.session.add(template)
    db.session.flush()

    # 处理标签
    tags = data.get('tags', [])
    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
            db.session.flush()

        template_tag = TemplateTag(template_id=template.id, tag_id=tag.id)
        db.session.add(template_tag)

    db.session.commit()
    return jsonify(template.to_dict()), 201


@api_bp.route('/templates/<int:template_id>', methods=['DELETE'])
def delete_template(template_id):
    """删除提示词模板"""
    template = PromptTemplate.query.get_or_404(template_id)
    db.session.delete(template)
    db.session.commit()
    return jsonify({'message': '删除成功'})


@api_bp.route('/templates/<int:template_id>', methods=['PUT'])
def update_template(template_id):
    """更新提示词模板"""
    template = PromptTemplate.query.get_or_404(template_id)
    data = request.get_json()

    if 'title' in data:
        template.title = data['title']
    if 'content' in data:
        template.content = data['content']
    if 'templateType' in data:
        template.template_type = data['templateType']
    
    # 处理标签更新
    if 'tags' in data:
        # 清除旧标签关联
        TemplateTag.query.filter_by(template_id=template.id).delete()
        
        tags = data['tags']
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.flush()
            
            template_tag = TemplateTag(template_id=template.id, tag_id=tag.id)
            db.session.add(template_tag)

    db.session.commit()
    return jsonify(template.to_dict())


@api_bp.route('/templates/<int:template_id>/copy', methods=['POST'])
def copy_template(template_id):
    """复制模板（增加使用次数）"""
    template = PromptTemplate.query.get_or_404(template_id)
    template.usage_count += 1
    db.session.commit()
    return jsonify({'message': '复制成功', 'content': template.content})


# ==================== 提示词生成接口 ====================

@api_bp.route('/prompt/generate/minimal', methods=['POST'])
def generate_minimal_prompt():
    """生成最小公式提示词"""
    data = request.get_json()

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

    # 保存使用日志
    log = PromptUsageLog(
        prompt_type='minimal_formula',
        generated_prompt=prompt,
        form_data=json.dumps(data, ensure_ascii=False)
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        'prompt': prompt,
        'logId': log.id
    })


@api_bp.route('/prompt/generate/complex', methods=['POST'])
def generate_complex_prompt():
    """生成复杂提示词（8步法）"""
    data = request.get_json()

    role = data.get('role', '')
    background = data.get('background', '')
    task = data.get('task', '')
    requirements = data.get('requirements', '')
    format_spec = data.get('format', '')
    example = data.get('example', '')

    prompt = f"""### 角色
作为 {role} 专家

### 背景
当前面临 {background} 问题
交代背景与受众：明确 AI 应扮演的角色、任务发生的场景以及目标群体

### 任务
{task}

### 要求
{requirements}

### 格式
{format_spec}

### 范例
{example}"""

    # 保存使用日志
    log = PromptUsageLog(
        prompt_type='complex_8step',
        generated_prompt=prompt,
        form_data=json.dumps(data, ensure_ascii=False)
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        'prompt': prompt,
        'logId': log.id
    })


# ==================== 复盘记录接口 ====================

@api_bp.route('/review', methods=['POST'])
def create_review():
    """创建复盘记录"""
    data = request.get_json()

    review = ReviewRecord(
        usage_log_id=data.get('usageLogId'),
        expected_effect=data.get('expectedEffect'),
        evaluation_method=data.get('evaluationMethod'),
        error_handling=data.get('errorHandling'),
        adjustment_notes=data.get('adjustmentNotes'),
        prompt_reasoning=data.get('promptReasoning')
    )
    db.session.add(review)
    db.session.commit()

    return jsonify(review.to_dict()), 201


# ==================== 提示词技巧接口 ====================

@api_bp.route('/tips', methods=['GET'])
def get_tips():
    """获取提示词技巧"""
    tips = PromptTip.query.filter_by(is_active=True).order_by(PromptTip.sort_order).all()
    return jsonify({
        'tips': [t.to_dict() for t in tips]
    })


# ==================== 健康检查 ====================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'ok'})
