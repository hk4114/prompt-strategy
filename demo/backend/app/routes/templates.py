from flask import Blueprint, jsonify, request
from app import db
from app.models import PromptTemplate, Tag, TemplateTag

templates_bp = Blueprint('templates', __name__)


@templates_bp.route('', methods=['GET'])
def get_templates():
    """获取模板列表，支持搜索和类型筛选"""
    keyword = request.args.get('keyword', '')
    template_type = request.args.get('type', '')
    
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
    
    templates = query.order_by(PromptTemplate.usage_count.desc()).all()
    return jsonify({
        'templates': [t.to_dict() for t in templates]
    })


@templates_bp.route('/<int:template_id>', methods=['GET'])
def get_template(template_id):
    """获取单个模板详情"""
    template = PromptTemplate.query.get_or_404(template_id)
    return jsonify(template.to_dict())


@templates_bp.route('', methods=['POST'])
def create_template():
    """创建新模板"""
    data = request.get_json()
    
    template = PromptTemplate(
        title=data['title'],
        content=data['content'],
        template_type=data.get('templateType', 'custom'),
        is_system=False
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


@templates_bp.route('/<int:template_id>/copy', methods=['POST'])
def copy_template(template_id):
    """复制模板（增加使用次数）"""
    template = PromptTemplate.query.get_or_404(template_id)
    template.usage_count += 1
    db.session.commit()
    return jsonify({
        'success': True,
        'content': template.content
    })
