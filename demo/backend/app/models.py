from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

try:
    from . import db
except ImportError:
    # Fallback during import conflicts
    db = SQLAlchemy()


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_key = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(10))
    sort_order = db.Column(db.Integer, default=0, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    products = db.relationship('Product', backref='category', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'category_key': self.category_key,
            'name': self.name,
            'icon': self.icon,
            'sort_order': self.sort_order,
            'products': [product.to_dict() for product in self.products]
        }


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    url = db.Column(db.String(500), nullable=False)
    recommend_reason = db.Column(db.Text)
    price = db.Column(db.String(100))
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tags = db.relationship('ProductTag', backref='product', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'recommend_reason': self.recommend_reason,
            'price': self.price,
            'sort_order': self.sort_order,
            'tags': [tag.tag_name for tag in self.tags]
        }


class ProductTag(db.Model):
    __tablename__ = 'product_tags'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    tag_name = db.Column(db.String(50), nullable=False, index=True)


class PromptTemplate(db.Model):
    __tablename__ = 'prompt_templates'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    template_type = db.Column(db.String(50), nullable=False, index=True)
    is_system = db.Column(db.Boolean, default=False)
    usage_count = db.Column(db.Integer, default=0, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tags = db.relationship('TemplateTag', backref='template', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'template_type': self.template_type,
            'is_system': self.is_system,
            'usage_count': self.usage_count,
            'tags': [tag.tag.to_dict() for tag in self.tags]
        }


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class TemplateTag(db.Model):
    __tablename__ = 'template_tags'

    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('prompt_templates.id'), nullable=False, index=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False, index=True)

    tag = db.relationship('Tag', backref='template_tags', lazy=True)

    __table_args__ = (db.UniqueConstraint('template_id', 'tag_id', name='uk_template_tag'),)


class PromptUsageLog(db.Model):
    __tablename__ = 'prompt_usage_logs'

    id = db.Column(db.Integer, primary_key=True)
    prompt_type = db.Column(db.String(50), nullable=False, index=True)
    generated_prompt = db.Column(db.Text, nullable=False)
    form_data = db.Column(db.Text)  # JSON string in SQLite
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    review = db.relationship('ReviewRecord', backref='usage_log', cascade='all, delete-orphan', lazy=True, uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'prompt_type': self.prompt_type,
            'generated_prompt': self.generated_prompt,
            'form_data': json.loads(self.form_data) if self.form_data else None,
            'created_at': self.created_at.isoformat()
        }


class ReviewRecord(db.Model):
    __tablename__ = 'review_records'

    id = db.Column(db.Integer, primary_key=True)
    usage_log_id = db.Column(db.Integer, db.ForeignKey('prompt_usage_logs.id'), index=True)
    expected_effect = db.Column(db.Text)
    evaluation_method = db.Column(db.Text)
    error_handling = db.Column(db.Text)
    adjustment_notes = db.Column(db.Text)
    prompt_reasoning = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'usage_log_id': self.usage_log_id,
            'expected_effect': self.expected_effect,
            'evaluation_method': self.evaluation_method,
            'error_handling': self.error_handling,
            'adjustment_notes': self.adjustment_notes,
            'prompt_reasoning': self.prompt_reasoning,
            'created_at': self.created_at.isoformat()
        }


class PromptTip(db.Model):
    __tablename__ = 'prompt_tips'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, default=0, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'sort_order': self.sort_order,
            'is_active': self.is_active
        }
