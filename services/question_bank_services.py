import traceback
import base64
import os
import copy
import random
import json
import uuid
import pandas as pd
from datetime import datetime

from flask_jwt_extended import create_access_token

from models import (QuestionBankMaster, InstitutionMaster)

from collection_models import (CourseContent)
from utils import obj_to_list, obj_to_dict, document_to_dict, identify_list_differences
from database import session
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import desc,asc

from dotenv import load_dotenv
load_dotenv()

class QuestionBankService:
    def __init__(self):
        pass

    def process_request(self, data, user_id):
        try:
            mode = data.get("mode")
            mode = str(mode).lower().strip().replace(" ", "_")
            
            
            if mode == "file":
                blob = data.get("base64")
                if not blob:
                    return {"status": False, "message": "invalid request file"}
                
                file_data = base64.b64decode(blob)
                file_data_name = f"questions_{user_id}.xlsx" 

                with open(file_data_name, 'wb') as file:
                    file.write(file_data)

                data_df = pd.read_excel(file_data_name, engine='openpyxl')
                list_of_dicts = []
                for index, row in data_df.iterrows():
                    correct_answer = [option.strip() for option in row['Correct Options'].split(',')]
                    
                    list_of_dicts.append({
                        "question": row['Question'],
                        "answerType": row['Answer Type'].lower(),
                        "marks": str(row['Marks']),
                        "correctAnswer": correct_answer,
                        "options": [row['Option1'], row['Option2'], row['Option3'], row['Option4']],
                        "numberOfOptions": str(len([row['Option1'], row['Option2'], row['Option3'], row['Option4']]))
                    })
                
                try:
                    os.remove(file_data_name)
                except OSError as e:
                    print(f"Error: {file_data_name} : {e.strerror}")
                
                return {"status": True, "data":list_of_dicts}
                                
            elif mode == "ai_generate":
                pass
            else:
                return {"status": False, "message": "invalid mode"}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
    
    def create_question_bank(self, data, user_id):
        try:
            question_bank_name = data["name"]
            question_bank_obj = session.query(QuestionBankMaster).filter_by(name = question_bank_name).first()
            if question_bank_obj:
                return {"status": False, "message": "Question bank already exists"}
            
            for i,question in enumerate(data["questions"]):
                question["id"] = i + 1
                data["questions"][i] = question
                       
            question_bank_obj = QuestionBankMaster(
                name = question_bank_name,
                questions = data["questions"],
                status = "Created",
                created_by = user_id,
                updated_by = user_id
                )
            session.add(question_bank_obj)
            session.commit()
            return {"status": True, "message": "Question bank created"}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
        

    def get_question_bank(self, question_bank_id):
        try:
            question_bank_obj = session.query(QuestionBankMaster).filter_by(id = question_bank_id).first()
            if question_bank_obj:
                return {"status": True, "data": obj_to_dict(question_bank_obj)}
            else:
                return {"status": False, "message": "Question bank not found"}
            
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}

    def list_question_bank(self, user_id):
        try:
            question_bank_obj = session.query(QuestionBankMaster).filter_by(created_by = user_id).all()
            if question_bank_obj:
                return {"status": True, "data": obj_to_list(question_bank_obj)}
            else:
                return {"status": False, "message": "Question bank not found"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}

    def delete_question_bank(self, question_bank_id):
        try:
            question_bank_obj = session.query(QuestionBankMaster).filter_by(id = question_bank_id).first()
            if question_bank_obj:
                session.delete(question_bank_obj)
                session.commit()
                return {"status": True, "message": "Question bank deleted"}
            else:
                return {"status": False, "message": "Question bank not found"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}