import traceback
import base64
import os
import copy
import random
import json
import uuid
import pandas as pd
import threading
from datetime import datetime

from flask_jwt_extended import create_access_token

from models import (EntityMaster, EntityMapping)

from collection_models import (CourseContent)
from utils import obj_to_list, obj_to_dict, document_to_dict, identify_list_differences
from database import session
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import desc,asc
from ai_generator import generate_skill_questions
from dotenv import load_dotenv
load_dotenv()


import random
class AdminService:
    def __init__(self):
        pass

    def create_entity(self, data):
        try:
            entity_name = data.get("entity_name", "")

            if not entity_name:
                return {"status": False, "message": "Entity name is required"}
            
            
            entity_obj = session.query(EntityMaster).filter_by(name = entity_name).first()
            if entity_obj:
                return {"status": False, "message": "Entity already exists"}
            else:
                entity_obj = EntityMaster(name = entity_name)

                session.add(entity_obj)
                session.commit()
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": f"entity creation failed, error: {e}"}
 
    def create_entity_mapping(self, data):
        try:
            entity_id = data.get("entity_id", "")
            entity_mapping_value = data.get("entity_mapping_value", "")
            if not entity_id:
                return {"status": False, "message": "Entity id is required"}
            
            if not entity_mapping_value:
                return {"status": False, "message": "Entity mapping value is required"}
            
            entity_mapping_obj = session.query(EntityMapping).filter_by(entity_id = entity_id).filter_by(name = entity_mapping_value).first()
            if entity_mapping_obj:
                return {"status": False, "message": "Entity mapping already exists"}
            else:
                entity_mapping_obj = EntityMapping(
                    entity_id = entity_id,
                    name = entity_mapping_value
                    )
                session.add(entity_mapping_obj)
                session.commit()
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": f"Entity mapping creation failed, error: {e}"}
    
    def get_entity_list(self):
        try:
            entities = session.query(EntityMaster).all()
            return {"status": True, "entities": obj_to_list(entities)}
        
        except Exception as e:
            traceback.print_exc()
            return {"status": False, "message": f"Entity list not found, error: {e}"}
            
    def get_entity_mapping(self, entity_name):
        try:
            if not entity_name:
                return {"status": False, "message": "Entity name is required"}
            
            entity_master_obj = session.query(EntityMaster).filter_by(name = entity_name).first()
            if not entity_master_obj:
                return {"status": False, "message": "Entity name not found"}
            
            entity_mapping = session.query(EntityMapping).filter_by(entity_id = entity_master_obj.id).all()
            return {"status": True, "entity_mapping": obj_to_list(entity_mapping)}
        
        except Exception as e:
            traceback.print_exc()
            return {"status": False, "message": f"Entity mapping not found, error: {e}"}
    
        
    
    def activate_entity(self, entity_id):
        try:
            if not entity_id:
                return {"status": False, "message": "Entity id is required"}
            
            entity_obj = session.query(EntityMaster).filter_by(id = entity_id).first()
            if entity_obj:
                entity_obj.is_active = True
                session.commit()
                return {"status": True, "message": "Entity activated"}
            else:
                return {"status": False, "message": "Entity not found"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": f"Entity activation failed, error: {e}"}
        
    def deactivate_entity(self, entity_id):
        try:
            if not entity_id:
                return {"status": False, "message": "Entity id is required"}
            
            entity_obj = session.query(EntityMaster).filter_by(id = entity_id).first()
            if entity_obj:
                entity_obj.is_active = False
                session.commit()
                return {"status": True, "message": "Entity deactivated"}
            else:
                return {"status": False, "message": "Entity not found"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": f"Entity deactivation failed, error: {e}"}
        
    def activate_entity_mapping(self, entity_mapping_id):
        try:
            if not entity_mapping_id:
                return {"status": False, "message": "Entity mapping id is required"}
            
            entity_mapping_obj = session.query(EntityMapping).filter_by(id = entity_mapping_id).first()
            if entity_mapping_obj:
                entity_mapping_obj.is_active = True
                session.commit()
                return {"status": True, "message": "Entity mapping activated"}
            else:
                return {"status": False, "message": "Entity mapping not found"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": f"Entity mapping activation failed, error: {e}"}
        
    def deactivate_entity_mapping(self, entity_mapping_id):
        try:
            if not entity_mapping_id:
                return {"status": False, "message": "Entity mapping id is required"}
            
            entity_mapping_obj = session.query(EntityMapping).filter_by(id = entity_mapping_id).first()
            if entity_mapping_obj:
                entity_mapping_obj.is_active = False
                session.commit()
                return {"status": True, "message": "Entity mapping deactivated"}
            else:
                return {"status": False, "message": "Entity mapping not found"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": f"Entity mapping deactivation failed, error: {e}"}
        

    def generate_skill_questions(self, data):
        try:
            skill_name = data.get("skill_name")
            skill_type = data.get("skill_type")
            
            skill_models = ['hard_skill','soft_skill','hr_skill']

            
            if not skill_name:
                return {"status": False, "message": "Skill name is required"}
            
            if not skill_type:
                return {"status": False, "message": "Skill type is required"}

            
            if skill_type not in skill_models:
                return {"status": False, "message": "Invalid skill type"}
            
            thread = threading.Thread(
            target=generate_skill_questions, 
            args=(skill_name, skill_type,)
            )
            thread.start()
            return {"status": True, "message": "Skill questions are beeing generated"}

        except Exception as e:
            traceback.print_exc()
            return {"error": str(e)}
        

                

