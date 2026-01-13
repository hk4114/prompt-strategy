from flask import Blueprint, jsonify
from app.models import Category

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('', methods=['GET'])
def get_categories():
    """获取所有分类及其产品"""
    categories = Category.query.order_by(Category.sort_order).all()
    return jsonify({
        'categories': [cat.to_dict() for cat in categories]
    })


@categories_bp.route('/<category_key>', methods=['GET'])
def get_category(category_key):
    """获取单个分类详情"""
    category = Category.query.filter_by(category_key=category_key).first_or_404()
    return jsonify(category.to_dict())
