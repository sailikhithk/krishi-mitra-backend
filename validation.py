PROCESS_QUESTION_BANK_REQUEST = {
    "type": "object",
    "properties": {
        "mode": {"type": "string"},
        "base64": {"type": "string"},
        "text": {"type": "string"}
    },
    "required": ["mode"]
}

CREATE_QUESTION_BANK_SCHEME = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "questions": {"type": "array"}
    },
    "required": ["name", "description", "questions"] 
}

CREATE_ASSIGNMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "question_bank_ids": {"type": "array"},
        "number_of_questions": {"type": "integer"}
    },
    "required": ["name", "description", "question_bank_ids", "number_of_questions"] 
}

ASSIGN_ASSIGNMENT_SCHEMA  = {
    "type": "object",
    "properties": {
        "assignment_id": {"type": "integer"},
        "user_ids": {
            "type": "array",
            "items": {
                "type": "integer"
            }
        }
    },
    "required": ["assignment_id", "user_ids"]
}

UNASSIGN_ASSIGNMENT_SCHEMA  = {
    "type": "object",
    "properties": {
        "assignment_id": {"type": "integer"},
        "user_ids": {
            "type": "array",
            "items": {
                "type": "integer"
            }
        }
    },
    "required": ["assignment_id", "user_ids"]
}

SUBMIT_ASSIGNMENT_SCHEMA  = {
    "type": "object",
    "properties": {
        "assignment_id": {"type": ["integer", "string"]},
        "is_late": {"type": "boolean"},
        "content": {"type": "array"}
    },
    "required": ["assignment_id", "is_late", "content"]
}

UPDATE_ASSIGNMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "assignment_id": {"type": "integer"},
        "skills_required" : {"type": "array",
            "items": {
                "type": "string"
            }
        },
        "max_time_min": {"type": "integer"},
        "always_open_submission": {"type": "boolean"},
        "deadline": {"type": ["string", "null"] },
        "allows_late_submission": {"type": ["boolean", "null"] },
        "attempts_allowed": {"type": "integer"},
        "auto_reminders": {"type": "boolean"},
    },
    "required": ["assignment_id", "skills_required", "max_time_min", "always_open_submission", "attempts_allowed", "auto_reminders"]
}

CREATE_COURSE_SCHEMA  = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"}
    },
    "required": ["name", "description"]
}

ASSIGN_COURSE_SCHEMA  = {
    "type": "object",
    "properties": {
        "course_id": {"type": "integer"},
        "user_ids": {
            "type": "array",
            "items": {
                "type": "integer"
            }
        }
    },
    "required": ["course_id", "user_ids"]
}

UNASSIGN_COURSE_SCHEMA  = {
    "type": "object",
    "properties": {
        "course_id": {"type": "integer"},
        "user_ids": {
            "type": "array",
            "items": {
                "type": "integer"
            }
        }
    },
    "required": ["course_id", "user_ids"]
}

CREATE_COURSE_CONTENT_SCHEMA = {
    "type": "object",
    "properties": {
        "course_id": {"type": "integer"},
        "content": {"type": "array"},
    },
    "required": ["course_id", "content"]
}

UPDATE_TRACK_COURSE_CONTENT_SCHEMA = {
    "type": "object",
    "properties": {
        "course_id": {"type": "integer"},
        "topic": {"type": "string"},
        "sub_topic": {"type": "string"},
                },
    "required": ["course_id", "topic", "sub_topic"]    
},
    
GENERATE_SCREENING_LINK_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "max_capacity": {"type": "integer"},
        "description": {"type": "string"},
        "activation_date": {"type": "string"},
        "expiry_date": {"type": "string"},
    },
    "required": ["name", "max_capacity", "activation_date", "expiry_date"]
}

INSTITUTION_CONFIGURATION_SCHEMA = {
    "type": "object",
    "properties": {
        "mode": {"type": "string"},
        "base64": {"type": "string"}
    },
    "required": ["mode", "base64"]
}

INSTITUTION_REGISTER_SCHEMA = {
    "type": "object",
    "properties": {
        "institution_name": {"type": "string"},
        "contact_name": {"type": "string"},
        "email": {"type": "string"},
        "phone_number": {"type": "string"},
        "country_id": {"type": "integer"},
        "city": {"type": "string"},
        "desiganation": {"type": "string"},
        "number_of_students": {"type": "integer"},
        "number_of_departments": {"type": "integer"},
        "domains": {"type": "string"},
        "preference_days": {"type": "string"},
        "preference_time": {"type": "string"},
        "password": {"type": "string"},
        "registration_number": {"type": "string"}
    },
    "required": ["institution_name", "contact_name", "email", "phone_number", "country_id", "city", "desiganation", "number_of_students", "number_of_departments", "domains", "preference_days", "preference_time", "password", "registration_number"]
}

INSTITUTION_UPDATE_SCHEMA = {
    "type": "object",
    "properties": {
        "institution_name": {"type": "string"},
        "contact_name": {"type": "string"},
        "email": {"type": "string"},
        "phone_number": {"type": "string"},
        "country_id": {"type": "integer"},
        "city": {"type": "string"},
        "desiganation": {"type": "string"},
        "number_of_students": {"type": "integer"},
        "number_of_departments": {"type": "integer"},
        "domains": {"type": "string"},
        "preference_days": {"type": "string"},
        "preference_time": {"type": "string"},
        "password": {"type": "string"},
        "registration_number": {"type": "string"}
    }
}

INSTITUTION_UPDATE_PASSWORD_SCHEMA = {
    "type": "object",
    "properties": {
        "new_password": {"type": "string"},
    },
    "required": ["new_password"]
}

USER_RESET_PASSWORD_SCHEMA = {
    "type": "object",
    "properties": {
        "new_password": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["new_password", "user_id"]
}

USER_UPDATE_PASSWORD_SCHEMA = {
    "type": "object",
    "properties": {
        "new_password": {"type": "string"},
    },
    "required": ["new_password"]
}

LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
        "role": {"type": "string"}
    },
    "required": ["email", "password"]
}

RESET_PASSWORD_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "new_password": {"type": "string"},
    },
    "required": ["email", "new_password"]
}


USER_REGISTER_SCHEMA = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "phone_number": {"type": "string"},
        "branch_id": {"type": "integer"},
        "department_id": {"type": "integer"},
        "institution_id": {"type": "integer"},
        "address": {"type": "string"},        
        "course_id": {"type": "integer"},
        "password": {"type": "string"},
        "role_id": {"type": "integer"},
    },
    "required": ["first_name", "last_name", "email", "phone_number", "branch_id", "department_id", "institution_id", "course_id", "password"]
}
    
SCREENING_USER_REGISTER_SCHEMA = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "phone_number": {"type": "string"},
        "branch_name": {"type": "string"},
        "department_name": {"type": "string"},
        "address": {"type": "string"},        
        "course_name": {"type": "string"},
        "password": {"type": "string"},
        "unique_code": {"type": "string"},
    },
    "required": ["first_name", "last_name", "email", "phone_number", "branch_name", "department_name", "course_name", "password", "unique_code"]
}

STUDENT_CREATED_BY_ADMIN_SCHEMA = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "phone_number": {"type": "string"},
        "branch_id": {"type": "integer"},
        "department_id": {"type": "integer"},
        "address": {"type": "string"},        
        "course_id": {"type": "integer"},
        "password": {"type": "string"},
        "student_id": {"type": "string"},
    },
    "required": ["first_name", "last_name", "email", "phone_number", "branch_id", "department_id", "address", "course_id", "password", "student_id"]
}

TEACHER_CREATED_BY_ADMIN_SCHEMA = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "phone_number": {"type": "string"},
        "email": {"type": "string"},
        "branch_id": {"type": "integer"},
        "department_id": {"type": "integer"},
        "institution_id": {"type": "integer"},
        "address": {"type": "string"},
        "password": {"type": "string"},
        
    }
}

USER_UPDATE_SCHEMA = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "phone_number": {"type": "string"},
        "branch_id": {"type": "integer"},
        "department_id": {"type": "integer"},
        "institution_id": {"type": "integer"},
        "address": {"type": "string"},
        
        "course": {"type": "integer"},
        "password": {"type": "string"},
        "role_id": {"type": "string"},
    }
}

ANALYSIS_MODE_SCHEMA = {
    "type": "string",
    "enum": ["behavioral_analysis", "ks_analysis", "practical_thinking_analysis", "emotion_sensing", "hard_skill_vs_soft_skills"]
}

UPLOAD_USER_ROLE_SCHEMA = {
    "type": "string",
    "enum": ["student", "teacher"]
}

ALLOWED_EXTENSIONS = {'xlsx'}


USER_REGISTER_INTERVIEW_SCHEMA = {
    "type": "object",
    "properties": {
        "interview_type": {"type": "string"},
        "specifications": {"type": "object"}
    },
    "required": ["interview_type", "specifications"]
}

PROCESS_JD_SCHEMA = {
    "type": "object",
    "properties": {
        "mode": {"type": "string"},
        "company_name": {"type": "string"},
        "company_role": {"type": "string"},
        "interview_type": {"type": "string"},
        
        "file": {"type": "string"},
        "text": {"type": "string"},
    },
    "required": ["mode", "company_name", "company_role", "interview_type"]
}
