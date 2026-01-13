from flask import Blueprint, jsonify
from app.models import PromptTip

tips_bp = Blueprint('tips', __name__)


@tips_bp.route('', methods=['GET'])
def get_tips():
    """获取所有启用的提示词技巧"""
    tips = PromptTip.query.filter_by(is_active=True).order_by(PromptTip.sort_order).all()
    return jsonify({
        'tips': [tip.to_dict() for tip in tips]
    })
