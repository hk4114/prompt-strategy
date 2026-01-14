import os
import json
from app.models import PromptTemplate, Tag, TemplateTag
from app import db

def init_default_templates(app):
    """Initialize default templates if database is empty."""
    with app.app_context():
        # Check if templates exist
        if PromptTemplate.query.first():
            print("Templates already exist. Skipping initialization.")
            return

        print("Initializing default templates from JSON...")
        
        # Path to templates_export_2026-01-14.json
        # app/utils/init_data.py -> app/utils -> app -> backend -> demo -> project root
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        file_path = os.path.join(base_dir, 'templates_export_2026-01-14.json')
        
        # Check if file exists, if not try looking in project root relative to current working directory
        if not os.path.exists(file_path):
             # Fallback: try absolute path provided by user
             file_path = '/Users/kanehua/project/prompt-strategy/templates_export_2026-01-14.json'
        
        if not os.path.exists(file_path):
            print(f"Error: Default templates file not found at {file_path}")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                templates = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON file: {e}")
            return
        except Exception as e:
            print(f"Error: Failed to read file: {e}")
            return
            
        if not isinstance(templates, list):
            print("Error: JSON root must be an array")
            return

        success_count = 0
        warning_count = 0

        for t in templates:
            # Validate required fields
            if 'title' not in t or 'content' not in t:
                print(f"Warning: Skipping invalid template: {t.get('title', 'Unknown')}")
                warning_count += 1
                continue
                
            template = PromptTemplate(
                title=t['title'],
                content=t['content'],
                template_type=t.get('templateType', 'custom'),
                is_system=t.get('isSystem', False)
            )
            db.session.add(template)
            db.session.flush()
            
            # Process tags
            if 'tags' in t and isinstance(t['tags'], list):
                for tag_name in t['tags']:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        db.session.add(tag)
                        db.session.flush()
                    
                    template_tag = TemplateTag(template_id=template.id, tag_id=tag.id)
                    db.session.add(template_tag)
            
            success_count += 1
            
        try:
            db.session.commit()
            print(f"Successfully initialized {success_count} default templates.")
            if warning_count > 0:
                print(f"Skipped {warning_count} invalid templates.")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to initialize default templates: {e}")
