import traceback
import uuid
import pandas as pd
from datetime import datetime

from flask_jwt_extended import create_access_token

from models import (TrainingCourse, TrainingCourseUserMapping, UserMaster, Role, Branch, Department, Course, InstitutionMaster)

from collection_models import (CourseContent)
from utils import obj_to_list, obj_to_dict, document_to_dict, identify_list_differences
from database import session
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import desc,asc
from sqlalchemy.orm.attributes import flag_modified

from dotenv import load_dotenv
load_dotenv()

class CourseService:
    def __init__(self):
        pass

    def create_course(self, data, user_id):
        try:
            name = data["name"]
            description = data["description"]
            unique_code = str(uuid.uuid4())
            course = TrainingCourse(
                name=name, 
                description=description, 
                unique_code=unique_code,
                created_by = user_id,
                updated_by = user_id,
                stage = 1
                )
            session.add(course)
            session.commit()
            return {"course_id": course.id, "unique_code": course.unique_code, "status": True, "message": "Course created"}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Course not created"}

    def get_list_course(self, user_id):
        try:
            courses = session.query(TrainingCourse).filter_by(created_by = user_id).all()
            return {"status": True, "courses": obj_to_list(courses)}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Courses not found"}
        
    def get_course(self, course_id, user_id):
        try:
            course_obj = session.query(TrainingCourse).filter_by(id=course_id).first()
            if not course_obj:
                return {"status": False, "message": "Course not found"}
            response1 = obj_to_dict(course_obj)

            course_document = CourseContent.objects(course_code=course_obj.unique_code).first()
            response2 = document_to_dict(course_document)
            response2.pop("created_at", None)
            response2.pop("updated_at", None)
            response2.pop("_id", None)
            response2.pop("course_code", None)

            content_data = response2.get("content_data", [])
            response = {**response1, **response2}
            track_obj = session.query(TrainingCourseUserMapping).filter_by(course_id=course_id).filter_by(user_id=user_id).first()
            current_track = {}
            if track_obj:
                current_track = track_obj.track
            
            if not current_track:
                current_track = {}

            for topic_index, topic in enumerate(content_data):
                full_topic_completed_list = []
                sub_topic_list = topic.get("subtopics", [])
                for sub_topic_index, sub_topic in enumerate(sub_topic_list):
                    sub_topic_name = sub_topic.get("name", "")
                    current_track_sub_topic_names = current_track.get(topic["name"], [])
                    if sub_topic_name in current_track_sub_topic_names:
                        sub_topic["completed"] = True
                        full_topic_completed_list.append(True)
                    else:
                        sub_topic["completed"] = False
                        full_topic_completed_list.append(False)
                    sub_topic_list[sub_topic_index] = sub_topic
                if False in full_topic_completed_list:
                    topic["completed"] = False
                elif not full_topic_completed_list:
                    topic["completed"] = False
                else:
                    topic["completed"] = True
                content_data[topic_index] = topic

            response["content_data"] = content_data        
            
            if track_obj:
                response['track'] = track_obj.track
            else:
                response['track'] = {}
            progress = self.course_progress(course_id, user_id)
            
            return {"status": True, "data": response, "progress": progress}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Course not found"}

    def list_course(self, user_id, role):
        try:
            if role.strip().lower() == 'teacher':
                courses = session.query(
                    TrainingCourse.id.label('course_id'),
                    TrainingCourse.name.label('course_name'),
                    ).filter(TrainingCourse.created_by == user_id).all()
                
            else:
                courses = session.query(
                    TrainingCourse.id.label('course_id'),
                    TrainingCourse.name.label('course_name'),
                )\
                .join(TrainingCourseUserMapping, TrainingCourseUserMapping.course_id == TrainingCourse.id)\
                .filter(TrainingCourseUserMapping.user_id == user_id)\
                .all()
            data_list = [
                    {
                        "course_id": course.course_id,
                        "course_name": course.course_name
                    } for course in courses
                ]
            return {"status": True, "courses": data_list}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Courses not found"}

    def course_progress(self, course_id, user_id):
        try:
            track_obj = session.query(TrainingCourseUserMapping).filter_by(course_id=course_id).filter_by(user_id=user_id).first()
            if not track_obj:
                return 0
            track_data = track_obj.track
            course_obj = session.query(TrainingCourse).filter_by(id = course_id).first()
            course_document = CourseContent.objects(course_code=course_obj.unique_code).first()
            course_document = document_to_dict(course_document)
            content_data = course_document.get("content_data", [])
            full_content_data_points = 0
            for topic in content_data:
                subtopics_len = len(topic.get("subtopics", []))
                full_content_data_points = full_content_data_points + subtopics_len
            
            completed_content_data_points = 0
            for topic in track_data:
                completed_content_data_points = completed_content_data_points + len(track_data[topic])
            
            if full_content_data_points:
                return round((completed_content_data_points / full_content_data_points) * 100, 2)
            return 0
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return 0

    def assign_course(self, data):
        try:
            course_id = data["course_id"]
            user_ids = data["user_ids"]
            current_user_ids = [mapping.user_id for mapping in session.query(TrainingCourseUserMapping).filter_by(course_id=course_id).all()]
            new_users, deleted_users, unchanged_users = identify_list_differences(current_user_ids, user_ids)

            for new_user in new_users:
                course_user_mapping = TrainingCourseUserMapping(course_id=course_id, user_id=new_user)
                session.add(course_user_mapping)
                session.commit()

            # session.query(TrainingCourseUserMapping).filter_by(course_id = course_id).filter(TrainingCourseUserMapping.user_id.in_(deleted_users)).delete(synchronize_session=False)
            # session.commit()
            
            course_obj = session.query(TrainingCourse).filter_by(id = course_id).first()
            course_obj.stage = 2
            session.commit()

            return {"status": True, "message": "Course assinged"}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Course not assigned"}

    def unassign_course(self, data):
        try:
            course_id = data["course_id"]
            user_ids = data["user_ids"]
            for user_id in user_ids:
                existing = session.query(TrainingCourseUserMapping).filter_by(course_id=course_id).filter_by(user_id=user_id).first()
                if existing:
                    session.delete(existing)
                    session.commit()
                
            return {"status": True, "message": "Course unassinged"}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Course not unassigned"}

    def get_users(self, course_id, institution_id, branch_name):
        try:
            users = session.query(TrainingCourseUserMapping).filter_by(course_id = course_id).all()
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
            return {"error": str(e), "status": False, "message": "Course not found"}
        
    def create_content(self, data):
        try:
            course_id = data["course_id"]
            content = data["content"]
            course_obj = session.query(TrainingCourse).filter_by(id=course_id).first()
            if not course_obj:
                return {"status": False, "message": "Course not found"}
            
            unique_code = course_obj.unique_code
            course_content = CourseContent.objects(course_code=unique_code).first()
            if not course_content:
                course_content = CourseContent(
                    name = course_obj.name,
                    description = course_obj.description,
                    course_code=unique_code,
                    content_data = content
                )
                course_content.save()
            return {"status": True, "message": "Course content updated"}
        
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Course content not updated"}

    def delete_course(self, course_id, user_id):
        try:
            course_obj = session.query(TrainingCourse).filter_by(id = course_id).first()
            if not course_obj:
                return {"status": False, "message": "Course not found"}
            if course_obj.created_by != user_id:
                return {"status": False, "message": "User has no permission to delete this course"}
            session.delete(course_obj)
            session.commit()
            return {"status": True, "message": "Course deleted"}
            
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Course not unassigned"}
        
    def update_task(self, data, user_id):
        try:
            course_id = data["course_id"]
            requested_sub_topic = data["sub_topic"]
            requested_topic = data["topic"]
            subtopic_check = data.get("check", True)
            
            course_user_mapping_obj = session.query(TrainingCourseUserMapping).filter_by(course_id = course_id).filter_by(user_id = user_id).first()
            if not course_user_mapping_obj:
                return {"status": False, "message": "Course not found"}

            current_track = course_user_mapping_obj.track
            
            if not current_track:
                current_track = {}
                current_track[requested_topic] = []
            elif requested_topic not in current_track:
                current_track[requested_topic] = []
            
            # print("subtopic_check", subtopic_check)
            # print("qqqqq", current_track[requested_topic])
            if subtopic_check:
                # print(111111)
                if requested_sub_topic not in current_track[requested_topic]:
                    # print(22222)
                    current_track[requested_topic].append(requested_sub_topic)
                    # print(3333333)
            else:
                if requested_sub_topic in current_track[requested_topic]:
                    current_track[requested_topic] = [num1 for num1 in current_track[requested_topic] if num1 != requested_sub_topic]
            
            # print("current_track", current_track)
            course_user_mapping_obj.track = current_track
            flag_modified(course_user_mapping_obj, "track")
            session.commit()
            session.refresh(course_user_mapping_obj)
            # print("after commit current_track", current_track)

            progress = self.course_progress(course_id, user_id)
            
            return {"status": True, "message": "Course updated", "progress": progress}
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return {"error": str(e), "status": False, "message": "Course not updated"}