from flask import Blueprint, jsonify, request
from ..models import db, PromptTip

import json

tips_bp = Blueprint('tips', __name__)

# Initialize default tips
def init_default_tips():
    """Initialize default prompt tips"""
    if PromptTip.query.first() is not None:
        return

    default_tips = [
        {
            'title': '技巧一：清晰定义角色',
            'content': "在提示词中明确 AI 应该扮演的角色，这能帮助 AI 更好地理解任务。例如：'作为资深前端工程师'、'作为产品经理'等。",
            'sort_order': 1
        },
        {
            'title': '技巧二：提供具体背景',
            'content': '详细说明任务的背景信息，包括目标受众、使用场景、限制条件等。背景越清晰，AI 的输出越符合预期。',
            'sort_order': 2
        },
        {
            'title': '技巧三：明确输出格式',
            'content': '指定输出的格式要求，如 Markdown、JSON、表格等。也可以要求包含特定的章节结构或字数限制。',
            'sort_order': 3
        },
        {
            'title': '技巧四：提供示例',
            'content': '给出一个或多个示例，让 AI 理解你期望的输出风格和质量。示例是最好的老师。',
            'sort_order': 4
        },
        {
            'title': '技巧五：使用限制条件',
            'content': '明确指出不应该做什么，或者需要遵循的约束。例如："避免使用专业术语"、"输出在 100 字内"等。',
            'sort_order': 5
        }
    ]

    try:
        for tip_data in default_tips:
            tip = PromptTip(
                title=tip_data['title'],
                content=tip_data['content'],
                sort_order=tip_data['sort_order'],
                is_active=True
            )
            db.session.add(tip)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing default tips: {e}")


@tips_bp.route('', methods=['GET'])
def get_tips():
    """Get all active tips"""
    tips = PromptTip.query.filter_by(is_active=True).order_by(PromptTip.sort_order).all()

    if not tips:
        init_default_tips()
        tips = PromptTip.query.filter_by(is_active=True).order_by(PromptTip.sort_order).all()

    return jsonify({
        'tips': [tip.to_dict() for tip in tips]
    })


@tips_bp.route('', methods=['POST'])
def create_tip():
    """Create a new tip"""
    data = request.json

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400

    try:
        # Get max sort_order
        max_order = db.session.query(db.func.max(PromptTip.sort_order)).scalar() or 0

        tip = PromptTip(
            title=title,
            content=content,
            sort_order=max_order + 1,
            is_active=True
        )
        db.session.add(tip)
        db.session.commit()

        return jsonify({
            'message': 'Tip created successfully',
            'tip': tip.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@tips_bp.route('/<int:tip_id>', methods=['PUT'])
def update_tip(tip_id):
    """Update a tip"""
    tip = PromptTip.query.get(tip_id)

    if not tip:
        return jsonify({'error': 'Tip not found'}), 404

    data = request.json

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    tip.title = data.get('title', tip.title)
    tip.content = data.get('content', tip.content)
    tip.is_active = data.get('is_active', tip.is_active)

    try:
        db.session.commit()
        return jsonify({'message': 'Tip updated successfully', 'tip': tip.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@tips_bp.route('/reorder', methods=['POST'])
def reorder_tips():
    """Reorder tips"""
    data = request.json

    if not data or 'tips' not in data:
        return jsonify({'error': 'Tips order data required'}), 400

    tips_order = data['tips']

    try:
        for index, tip_id in enumerate(tips_order):
            tip = PromptTip.query.get(tip_id)
            if tip:
                tip.sort_order = index

        db.session.commit()
        return jsonify({'message': 'Tips reordered successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
