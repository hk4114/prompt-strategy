from datetime import datetime
from app import db


class Category(db.Model):
    """产品分类表"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_key = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(10))
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.category_key,
            'name': self.name,
            'icon': self.icon,
            'products': [p.to_dict() for p in self.products.order_by(Product.sort_order)]
        }


class Product(db.Model):
    """产品表"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    recommend_reason = db.Column(db.Text)
    price = db.Column(db.String(100))
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    tags = db.relationship('ProductTag', backref='product', lazy='dynamic')
    
    def to_dict(self):
        return {
            'name': self.name,
            'url': self.url,
            'recommendReason': self.recommend_reason,
            'price': self.price,
            'tags': [t.tag_name for t in self.tags]
        }


class ProductTag(db.Model):
    """产品标签表"""
    __tablename__ = 'product_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    tag_name = db.Column(db.String(50), nullable=False)


class PromptTemplate(db.Model):
    """提示词模板表"""
    __tablename__ = 'prompt_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    template_type = db.Column(db.String(50), nullable=False)
    is_system = db.Column(db.Boolean, default=False)
    usage_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    tags = db.relationship('TemplateTag', backref='template', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'templateType': self.template_type,
            'isSystem': self.is_system,
            'usageCount': self.usage_count,
            'tags': [t.tag.name for t in self.tags if t.tag],
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }


class Tag(db.Model):
    """标签表"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TemplateTag(db.Model):
    """模板标签关联表"""
    __tablename__ = 'template_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('prompt_templates.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    
    tag = db.relationship('Tag')


class PromptUsageLog(db.Model):
    """提示词使用日志表"""
    __tablename__ = 'prompt_usage_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    prompt_type = db.Column(db.String(50), nullable=False)
    generated_prompt = db.Column(db.Text, nullable=False)
    form_data = db.Column(db.Text)  # JSON 字符串
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'promptType': self.prompt_type,
            'generatedPrompt': self.generated_prompt,
            'formData': self.form_data,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }


class ReviewRecord(db.Model):
    """复盘记录表"""
    __tablename__ = 'review_records'
    
    id = db.Column(db.Integer, primary_key=True)
    usage_log_id = db.Column(db.Integer, db.ForeignKey('prompt_usage_logs.id'))
    expected_effect = db.Column(db.Text)
    evaluation_method = db.Column(db.Text)
    error_handling = db.Column(db.Text)
    adjustment_notes = db.Column(db.Text)
    prompt_reasoning = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'usageLogId': self.usage_log_id,
            'expectedEffect': self.expected_effect,
            'evaluationMethod': self.evaluation_method,
            'errorHandling': self.error_handling,
            'adjustmentNotes': self.adjustment_notes,
            'promptReasoning': self.prompt_reasoning,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }


class PromptTip(db.Model):
    """提示词技巧表"""
    __tablename__ = 'prompt_tips'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'sortOrder': self.sort_order,
            'isActive': self.is_active
        }
