import traceback
import random
import pandas as pd
from datetime import datetime

from flask_jwt_extended import create_access_token

from models import (Assignment, AssignmentUserMapping, QuestionBankMaster, UserMaster, Role, Branch, Department, Course, InstitutionMaster, AssignmentResults)

from collection_models import (CourseContent)
from utils import obj_to_list, obj_to_dict, document_to_dict, identify_list_differences
from database import session
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import desc,asc

from dotenv import load_dotenv
load_dotenv()


import random
class AssignmentService:
    def __init__(self):
        pass
    
    def get_users(self, course_id, institution_id, branch_name):
        try:
            users = session.query(AssignmentUserMapping).filter_by(course_id = course_id).all()
            course_users = [i.user_id for i in users]
            
            mode = "Student"
            users = session.query( 
                                    UserMaster.first_name,
                                    UserMaster.last_name,
                                    UserMaster.number_of_interviews,
                                    UserMaster.id,
                                    UserMaster.phone_number,
                                    UserMaster.address,
                                    UserMaster.email,
                                    UserMaster.created_date,
                                    UserMaster.is_active,
                                    Branch.name.label("branch_name"), 
                                    Department.name.label("department_name"),
                                    InstitutionMaster.institution_name.label("institution_name"), 
                                    Course.name.label("course_name")) \
                    .join(Role, UserMaster.role_id == Role.id) \
                    .join(Branch, UserMaster.branch_id == Branch.id) \
                    .join(Department, UserMaster.department_id == Department.id) \
                    .join(InstitutionMaster, UserMaster.institution_id == InstitutionMaster.id) \
                    .join(Course, UserMaster.course_id == Course.id) \
                    .filter(Role.name == mode)\
                    .filter(InstitutionMaster.id == institution_id)
            
            column_name = "created_date"
            users = users.filter(Branch.name == branch_name)
            
            
            # UN ASSINGED USERS:
            unassined_users = users.filter(UserMaster.id.notin_(course_users)).order_by(desc(getattr(UserMaster, column_name))).all()
            
            # ASSINGED USERS:
            assined_users = users.filter(UserMaster.id.in_(course_users)).order_by(desc(getattr(UserMaster, column_name))).all()
            
            unassined_users_data_list = [
                {
                    "id": user.id,
                    "name": f"{user.first_name} {user.last_name}",
                    "phone_number": user.phone_number,
                    "address": user.address,
                    "email": user.email,
                    "branch_name": user.branch_name,
                    "department_name": user.department_name,
                    "institution_name": user.institution_name,
                    "avg_score": 50,
                    "course_name": user.course_name,
                    "created_date": str(user.created_date),
                    "is_active": user.is_active,
                }
                for user in unassined_users
            ]
            
            assined_users_data_list = [
                {
                    "id": user.id,
                    "name": f"{user.first_name} {user.last_name}",
                    "phone_number": user.phone_number,
                    "address": user.address,
                    "email": user.email,
                    "branch_name": user.branch_name,
                    "department_name": user.department_name,
                    "institution_name": user.institution_name,
                    "avg_score": 50,
                    "course_name": user.course_name,
                    "created_date": str(user.created_date),
                    "is_active": user.is_active,
                }
                for user in assined_users
            ]
              
            return {
                "status": True, 
                "data":{ 
                "assined_users": assined_users_data_list,
                "unassined_users": unassined_users_data_list
                }
            }
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Assignment not found"}
    
    def get_random_questions(self, question_banks, num_questions):
        num_banks = len(question_banks)
        per_bank = num_questions // num_banks
        remainder = num_questions % num_banks

        result = []
        for bank_id, questions in question_banks.items():
            questions_from_bank = random.sample(questions, min(per_bank, len(questions)))
            for _ in  questions_from_bank:
                _["question_bank_id"] = bank_id
                _["question_bank_question_id"] = _["id"]
                result.append(_)

            # result.extend(random.sample(questions, min(per_bank, len(questions))))

        while remainder > 0:
            for bank_id, questions in random.sample(list(question_banks.items()), num_banks):
                if remainder > 0 and questions:
                    selected_question = random.choice(questions)
                    if selected_question not in result:
                        selected_question["question_bank_id"] = bank_id
                        selected_question["question_bank_question_id"] = selected_question["id"]
                        result.append(selected_question)
                        remainder -= 1
                if remainder == 0:
                    break

        return result

    def create_assignment(self, data, user_id):
        try:            
            assignment_name = data["name"]
            assignment_description = data["description"]
            question_bank_ids = data["question_bank_ids"]
            number_of_questions = data["number_of_questions"]
            question_banks_data = {}
            for question_bank_id in question_bank_ids:
                question_bank_obj = session.query(QuestionBankMaster).filter_by(id = question_bank_id).first()
                if question_bank_obj:
                    question_banks_data[str(question_bank_id)] = question_bank_obj.questions

            questions_in_assignment = self.get_random_questions(question_banks_data, number_of_questions)
            
            for i,question in enumerate(questions_in_assignment):
                questions_in_assignment[i]["id"] = i + 1
            
            new_assignment  = Assignment(
                name = assignment_name,
                description = assignment_description,
                questions = questions_in_assignment,
                created_by = user_id,
                updated_by = user_id
                )
            session.add(new_assignment)
            session.commit()
            return {"status": True, "message": "assignment created", "assignment_id": new_assignment.id}
                        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "assignment not created", "error": str(e)}
    
    def assign_assignment(self, data):
        try:
            assignment_id = data["assignment_id"]
            user_ids = data["user_ids"]
            current_user_ids = [mapping.user_id for mapping in session.query(AssignmentUserMapping).filter_by(assignment_id=assignment_id).all()]
            new_users, deleted_users, unchanged_users = identify_list_differences(current_user_ids, user_ids)

            for new_user in new_users:
                assignment_user_mapping = AssignmentUserMapping(assignment_id=assignment_id, user_id=new_user)
                session.add(assignment_user_mapping)
                session.commit()

            assignment_obj = session.query(Assignment).filter_by(id = assignment_id).first()
            assignment_obj.stage = 2
            session.commit()

            return {"status": True, "message": "Assignment assinged"}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Assignment not assigned"}

    def update_assignment(self, data):
        try:
            skills_required = data.get("skills_required", [])
            assignment_id = data["assignment_id"]
            max_time_min = data.get("max_time_min", 60)
            always_open_submission = data.get("always_open_submission", True)
            deadline = data.get("deadline", None)
            auto_reminders = data.get("auto_reminders", True)
            auto_assignment_notification = data.get("auto_assignment_notification", True)
            allows_late_submission = data.get("allows_late_submission", False)
            attempts_allowed = data.get("attempts_allowed", 1)
            
            assignment_obj = session.query(Assignment).filter_by(id = assignment_id).first()
            assignment_obj.skills_required = ','.join(skills_required)
            assignment_obj.max_time_min = max_time_min
            assignment_obj.always_open_submission = always_open_submission
            assignment_obj.deadline = deadline
            assignment_obj.auto_reminders = auto_reminders
            assignment_obj.auto_assignment_notification = auto_assignment_notification
            assignment_obj.allows_late_submission = allows_late_submission
            assignment_obj.number_of_reattempt = attempts_allowed
            assignment_obj.status = "Assignment Created"
            session.commit()
            return {"status": True, "message": "Assignment updated"}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
    
    def is_assignment_allowed(self, assignment_id, user_id):
        try:
            assignment_obj = session.query(Assignment).filter_by(id = assignment_id).first()
            if not assignment_obj:
                return {"status": False, "message": "Assignment not found"}
            
            always_open_submission = assignment_obj.always_open_submission
            deadline = assignment_obj.deadline
            current_time = datetime.now()
            
            if not always_open_submission:
                if current_time > deadline:
                    if not assignment_obj.allows_late_submission:
                        return {"status": False, "message": "Deadline reached for this assignment"}
                    
            attempts_completed = session.query(AssignmentResults).filter_by(assignment_id = assignment_id).filter_by(user_id = user_id).count()    
                        
            if attempts_completed + 1 > assignment_obj.attempts_allowed:
                return {"status": False, "message": "Maximum attempts reached for this assignment"}
            
            
            return {"status": True, "message": "Assignment can started"}
            
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False}
    
    def unassign_assignment(self, data):
        try:
            assignment_id = data["assignment_id"]
            user_ids = data["user_ids"]
            for user_id in user_ids:
                existing = session.query(AssignmentUserMapping).filter_by(assignment_id=assignment_id).filter_by(user_id=user_id).first()
                if existing:
                    session.delete(existing)
                    session.commit()
                
            return {"status": True, "message": "Assignment unassinged"}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Assignment not unassigned"}
    
    def get_assignment(self, assignment_id):
        try:
            assignment = session.query(Assignment).filter_by(id = assignment_id).first()
            return {"status": True, "data": obj_to_dict(assignment)}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
    
    def delete_assignment(self, assignment_id):
        try:
            assignment_obj = session.query(Assignment).filter_by(id = assignment_id).first()
            if not assignment_obj:
                return {"status": False, "message": "Assignment not found"}
            session.delete(assignment_obj)
            session.commit()
            return {"status": True, "message": "Assignment deleted"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
    
    def list_assignment(self, user_id, user_role_name, page_number=1, limit=10):
        try:
            if user_role_name == "teacher":
                total_records = session.query(Assignment).filter_by(created_by = user_id).count()
                
                if not total_records:
                    return {"status": True, "data": [], "metadata": {}}
 
                assignments = session.query(Assignment).filter_by(created_by = user_id).order_by(Assignment.id.desc())\
                    .limit(limit).offset((page_number - 1) * limit).all()
                
                processed_assignments_data = obj_to_list(assignments)
            else:
                current_time = datetime.now()
                total_records = session.query(AssignmentUserMapping).filter_by(user_id = user_id).count()
                if not total_records:
                    return {"status": True, "data": [], "metadata": {}}
 
                assignment_user_mapping_obj = session.query(AssignmentUserMapping).filter_by(user_id = user_id).order_by(AssignmentUserMapping.id.desc()).limit(limit).offset((page_number - 1) * limit).all()
                assignment_ids = [mapping.assignment_id for mapping in assignment_user_mapping_obj]
                assignments = session.query(Assignment).filter(Assignment.id.in_(assignment_ids)).all()
                assignments_data = obj_to_list(assignments)
                processed_assignments_data = []
                for assignment in assignments_data:
                    
                    assignment_result_obj = session.query(AssignmentResults).order_by(desc(AssignmentResults.id)).first()
                    if assignment_result_obj:
                        assignment["result_id"] = assignment_result_obj.id
                    else:
                        assignment["result_id"] = None
                    
                    always_open_submission = assignment.get("always_open_submission", True)
                    if always_open_submission:
                        assignment["is_locked"] = False
                    
                    else:
                        deadline = assignment.get("deadline")
                        # allows_late_submission = assignment.get("allows_late_submission", False)
                        if deadline:
                            assignment["is_locked"] = current_time < deadline
                        else:
                            assignment["is_locked"] = False
                    processed_assignments_data.append(assignment)
                                
            total_pages = (total_records + limit - 1) // limit
            metadata = {
                    "limit": limit,
                    "total_pages": total_pages,
                    "total_records": total_records,
                    "current_page": page_number,
                    "records_per_page": limit,
                    "next_page": f"/list?&page_number={page_number + 1}&limit={limit}" if page_number < total_pages else None,
                    "previous_page": f"/list?&page_number={page_number - 1}&limit={limit}" if page_number > 1 else None
                }
            
            return {
                "status": True, 
                "metadata": metadata,
                "data": processed_assignments_data
                }
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {
                "status": False, 
                "message": "error", 
                "error": str(e)}
    
    def evaluate_assignment(self, assignment_id, assignment_result_id):
        try:
            assignment_obj = session.query(Assignment).filter_by(id = assignment_id).first()
            if not assignment_obj:
                return {"status": False, "message": "Assignment not found"}

            assignment_result_obj = session.query(AssignmentResults).filter_by(id = assignment_result_id).first()
            if not assignment_result_obj:
                return {"status": False, "message": "Assignment result not found"}
            
            questions = assignment_obj.questions
            answers = assignment_result_obj.submitted_data
            
            questions_dict = {}
            for question in questions:
                questions_dict[question["id"]] = question
            
            print("questions_dict", questions_dict)
            print("questions", questions)
            print("answers", answers)

            
            total_marks = 0
            scored_marks = 0
            evaluated_answers = []
            for answer in answers:
                question_id = answer["question_id"]
                selected_options = set(answer["selected_options"])
                selected_answer = []

                question = questions_dict.get(question_id, {})
                correct_options = set(question.get("correctAnswer", []))
                
                all_options = question.get("options", [])
                for selected_option in selected_options:
                    try:
                        selected_answer.append(all_options[int(selected_option)-1])
                    except:
                        pass

                
                
                marks = int(question.get("marks", 0))
                total_marks += marks
                print("selected_options", selected_options)
                print("selected_answer", selected_answer)
                print("correct_options", correct_options)

                if set(selected_answer) == correct_options:
                    scored_marks += marks
                    answer["correct_answers"] = list(correct_options)
                    answer["is_correct"] = True
                    answer["marks"] = marks
                else:
                    answer["correct_answers"] = list(correct_options)
                    answer["is_correct"] = False
                    answer["marks"] = 0
                answer["all_options"] = all_options    
                evaluated_answers.append(answer)
            
            pass_mark = 0.6 * total_marks
            if scored_marks > pass_mark:
                is_qulified = True
            else:
                is_qulified = False
            
            print("is_qulified", is_qulified)
            print("assignment_result_obj.is_late", assignment_result_obj.is_late)
            print("evaluated_answers", evaluated_answers)
            print("scored_marks", scored_marks)
            
            assignment_result_obj.is_qualified = is_qulified
            assignment_result_obj.is_late = assignment_result_obj.is_late
            assignment_result_obj.evaluation_data = evaluated_answers
            assignment_result_obj.marks = scored_marks
            assignment_result_obj.status = "Evaluation completed"
            
            session.commit()

            assignment_obj.status = "Evaluation completed"
            session.commit()
            
            result = {
                "is_qulified": is_qulified,
                "marks": scored_marks,
                "total_marks": total_marks,
                "result_id": assignment_result_obj.id,
                "evaluated_answers": evaluated_answers
            }
            
            return {"status": True, "message": "Evaluation completed", "data": result}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
    
    
    def submit_assignment(self, data, user_id): 
        try:
            assignment_id = data["assignment_id"]
            
            older_attempts_count = session.query(AssignmentResults).filter_by(user_id = user_id, assignment_id = assignment_id).count()
            is_late = data["is_late"]
            answer = data["content"]
            submission = AssignmentResults(
                assignment_id = assignment_id, 
                user_id = user_id, 
                status = "Assignment Submitted",
                attempt_number = older_attempts_count,
                submitted_data = answer,
                is_late = is_late
                )
            session.add(submission)
            session.commit()
            
            assignment_result_id = submission.id
            return self.evaluate_assignment(assignment_id, assignment_result_id)
                        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
        
    def start_assignment(self, assignment_id, user_id):
        try:
            assignment_obj = session.query(Assignment).filter_by(id = assignment_id).first()
            if not assignment_obj:
                return {"status": False, "message": "Assignment not found"}
            
            current_time = datetime.now()
            
            if not assignment_obj.always_open_submission:
                if current_time > assignment_obj.deadline:
                    if not assignment_obj.allows_late_submission:
                        return {"status": True, "message": "Deadline reached for this assignment"}
                            
            attempts_completed = session.query(AssignmentResults).filter_by(assignment_id = assignment_id).filter_by(user_id = user_id).count()
            if attempts_completed + 1 > assignment_obj.attempts_allowed:
                return {"status": False, "message": "Maximum attempts reached for this assignment"} 
                      
            return {"status": True, "message": "Assignment can started"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
        
    def assignment_results(self, user_id, assignment_id, user_role_name, page_number=1, limit=10):
        try:
            if user_role_name == "teacher":
                results = session.query(AssignmentResults).filter_by(assignment_id = assignment_id).all()
            else:
                results = session.query(AssignmentResults).filter_by(assignment_id = assignment_id).filter_by(user_id = user_id).all()
        
            data_list = obj_to_list(results)
            
            if data_list:
                total_records = len(data_list)
                print("total_records", total_records)
                total_pages = (total_records + limit - 1) // limit
                start_index = (page_number - 1) * limit
                end_index = start_index + limit
                print("limit", limit)
                print("total_pages", total_pages)
                print("start_index", start_index)
                print("end_index", end_index)
                data_list = data_list[start_index:end_index]

                metadata = {
                    "limit": limit,
                    "total_pages": total_pages,
                    "total_records": total_records,
                    "current_page": page_number,
                    "records_per_page": limit,
                    "next_page": f"/results/{assignment_id}?page_number={page_number + 1}&limit={limit}" if page_number < total_pages else None,
                    "previous_page": f"/results/{assignment_id}?page_number={page_number - 1}&limit={limit}" if page_number > 1 else None
                }

                response = {
                    "status": True,
                    "metadata": metadata,
                    "data": data_list
                }

            return response
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"status": False, "message": "error", "error": str(e)}
        