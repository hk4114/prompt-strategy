import json
from flask import Blueprint, jsonify, request
from app import db
from app.models import PromptUsageLog, ReviewRecord

prompts_bp = Blueprint('prompts', __name__)


@prompts_bp.route('/generate', methods=['POST'])
def generate_prompt():
    """生成提示词并记录日志"""
    data = request.get_json()
    
    prompt_type = data.get('promptType', 'minimal_formula')
    form_data = data.get('formData', {})
    
    # 根据类型生成提示词
    if prompt_type == 'minimal_formula':
        generated = generate_minimal_formula(form_data)
    elif prompt_type == 'complex_8step':
        generated = generate_complex_prompt(form_data)
    else:
        generated = form_data.get('content', '')
    
    # 记录使用日志
    log = PromptUsageLog(
        prompt_type=prompt_type,
        generated_prompt=generated,
        form_data=json.dumps(form_data, ensure_ascii=False)
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'logId': log.id,
        'prompt': generated
    })


def generate_minimal_formula(form_data):
    """生成最小公式提示词"""
    persona = form_data.get('persona', '')
    context = form_data.get('context', '')
    task = form_data.get('task', '')
    limit = form_data.get('limit', '')
    goal = form_data.get('goal', '')
    note = form_data.get('note', '这对我的职业生涯非常重要!')
    
    prompt = f"""## 角色
作为 {persona}

## 背景  
{context}

## 任务  
{task}

## 限制  
{limit}

## 输出  
1. 以 Markdown 形式输出
2. 输出结果必须包含参考资料
3. {goal}

---
{note}"""
    
    return prompt


def generate_complex_prompt(form_data):
    """生成复杂任务8步法提示词"""
    role = form_data.get('role', '')
    background = form_data.get('background', '')
    task = form_data.get('task', '')
    requirements = form_data.get('requirements', '')
    format_spec = form_data.get('format', '')
    example = form_data.get('example', '')
    
    prompt = f"""### 角色
作为 {role} 专家

### 背景
{background}

### 任务 
{task}

### 要求
{requirements}

### 格式
{format_spec}

### 范例
{example}"""
    
    return prompt


@prompts_bp.route('/review', methods=['POST'])
def save_review():
    """保存复盘记录"""
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
    
    return jsonify({
        'success': True,
        'id': review.id
    })


@prompts_bp.route('/logs', methods=['GET'])
def get_logs():
    """获取使用日志列表"""
    logs = PromptUsageLog.query.order_by(PromptUsageLog.created_at.desc()).limit(50).all()
    return jsonify({
        'logs': [log.to_dict() for log in logs]
    })
