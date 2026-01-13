from flask import Blueprint, jsonify, request
from ..models import db, PromptUsageLog, ReviewRecord
from datetime import datetime
import json

prompts_bp = Blueprint('prompts', __name__)


@prompts_bp.route('/generate', methods=['POST'])
def generate_prompt():
    """Generate and save a prompt"""
    data = request.json

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    prompt_type = data.get('prompt_type')
    generated_prompt = data.get('generated_prompt')
    form_data = data.get('form_data', {})

    if not prompt_type or not generated_prompt:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        usage_log = PromptUsageLog(
            prompt_type=prompt_type,
            generated_prompt=generated_prompt,
            form_data=json.dumps(form_data) if form_data else None
        )
        db.session.add(usage_log)
        db.session.commit()

        return jsonify({
            'message': 'Prompt generated successfully',
            'usage_log_id': usage_log.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@prompts_bp.route('/review', methods=['POST'])
def save_review():
    """Save review record after copying prompt"""
    data = request.json

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    usage_log_id = data.get('usage_log_id')
    expected_effect = data.get('expected_effect', '')
    evaluation_method = data.get('evaluation_method', '')
    error_handling = data.get('error_handling', '')
    adjustment_notes = data.get('adjustment_notes', '')
    prompt_reasoning = data.get('prompt_reasoning', '')

    try:
        # Check if review already exists for this usage log
        existing_review = ReviewRecord.query.filter_by(usage_log_id=usage_log_id).first()

        if existing_review:
            # Update existing review
            existing_review.expected_effect = expected_effect
            existing_review.evaluation_method = evaluation_method
            existing_review.error_handling = error_handling
            existing_review.adjustment_notes = adjustment_notes
            existing_review.prompt_reasoning = prompt_reasoning
        else:
            # Create new review
            review = ReviewRecord(
                usage_log_id=usage_log_id,
                expected_effect=expected_effect,
                evaluation_method=evaluation_method,
                error_handling=error_handling,
                adjustment_notes=adjustment_notes,
                prompt_reasoning=prompt_reasoning
            )
            db.session.add(review)

        db.session.commit()

        return jsonify({'message': 'Review saved successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@prompts_bp.route('/review/<int:usage_log_id>', methods=['GET'])
def get_review(usage_log_id):
    """Get review record by usage log ID"""
    review = ReviewRecord.query.filter_by(usage_log_id=usage_log_id).first()

    if not review:
        return jsonify({'error': 'Review not found'}), 404

    return jsonify(review.to_dict())
