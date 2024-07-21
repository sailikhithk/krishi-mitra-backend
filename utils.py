# Cryptography
from cryptography.fernet import Fernet
import pandas as pd
import traceback

encrypt_key = "dHAphTsGijvUR6D0huM9bDqifYN3JPcI6WSLRkbj_EY="


def encrypt(data):
    data = data.encode()
    f = Fernet(encrypt_key)
    return f.encrypt(data).decode("utf-8")


def decrypt(data):
    data = data.encode()
    f = Fernet(encrypt_key)
    return f.decrypt(data).decode("utf-8")

def obj_to_list(data):
    list_dicts = []
    for obj in data:
        temp_dic = obj_to_dict(obj)
        temp_dic.pop("password_hash", None)
        list_dicts.append(temp_dic)        
    return list_dicts

def obj_to_dict(data):
    response = {}
    if data is None:
        return {}
    for c in data.__table__.columns:
        if c.name not in ["created_date", "updated_date", "password_modified_date", "last_login_date"]:
            response[c.name] = getattr(data, c.name)
        else:
            response[c.name] = str(getattr(data, c.name))
    return response

def document_to_dict(data):
    return data.to_mongo().to_dict() if data else {}

def document_to_list(data):
    return [row.to_mongo().to_dict() for row in data]

def query_to_dataframe(query_result):
    if not query_result:
        return pd.DataFrame()

    if isinstance(query_result[0], tuple):
        df = pd.DataFrame(query_result, columns=[col['name'] for col in query_result.column_descriptions])
    else:
        df = pd.DataFrame([record.__dict__ for record in query_result])
        df = df.drop(columns=['_sa_instance_state'])
    return df

        
def identify_list_differences(old_list, new_list):
    old_set = set(old_list)
    new_set = set(new_list)

    new_keys = new_set - old_set
    deleted_keys = old_set - new_set
    unchanged_keys = old_set & new_set

    return new_keys, deleted_keys, unchanged_keys


def download_sample_file(mode, sample_data = False): 
    try:
        mode = str(mode).strip().lower().replace(" ", "_")
        if mode == 'student':
            if sample_data:
                file_name = "students_sample_data.xlsx"
            else:
                file_name = "students.xlsx"
        elif mode == 'teacher':
            if sample_data:
                file_name = "teachers_sample_data.xlsx"
            else:
                file_name = "teachers.xlsx"
        elif mode == 'hard_skill':
            if sample_data:
                file_name = "hard_skills_sample_data.xlsx"
            else:
                file_name = "hard_skills.xlsx"
        elif mode == 'soft_skill':
            if sample_data:
                file_name = "soft_skills_sample_data.xlsx"
            else:
                file_name = "soft_skills.xlsx"
        elif mode == 'institution':
            if sample_data:
                file_name = "institution_config_sample_data.xlsx"
            else:
                file_name = "institution_config.xlsx"
        elif mode == 'company':
            if sample_data:
                file_name = "company_sample_data.xlsx"
            else:
                file_name = "company.xlsx"
        elif mode == 'question':
            if sample_data:
                file_name = "question_bank_sample_data.xlsx"
            else:
                file_name = "question_bank.xlsx"
        elif mode == 'interview_questions':
            if sample_data:
                file_name = "interview_questions_sample_data.xlsx"
            else:
                file_name = "interview_questions.xlsx"
        else:
            file_name = ""

        return file_name
    
    except Exception as e:
        traceback.print_exc()
        return ""