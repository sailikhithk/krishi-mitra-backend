import json
import random
import traceback
import openai
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from collection_models import HardSkillImprovementSuggestions, SoftSkillImprovementSuggestions, EmotionsSuggestions, HardSkillQuestions, SoftSkillQuestions, HrQuestions, CompanyRoleCustomQuestions


import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
print('Openai    Key================================', OPENAI_API_KEY)
print('Anthropic Key================================', ANTHROPIC_API_KEY)

openai.api_key = OPENAI_API_KEY
openai.timeout = 1800 # increase timeout to 20 minutes 
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

def gpt_bot_system(user_prompt, system_prompt):
    try:
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=1500,
                temperature=1,
                api_key=OPENAI_API_KEY,
            )
        processed_response = response['choices'][0]['message']['content'].split('\n')
        return processed_response
        
    except Exception as e:
        print("Error in GPT Bot System: ", e)
        traceback.print_exc()

# def claude_bot_system(user_prompt): # need to look into it 
#     try:
#         claude_prompt = f"{HUMAN_PROMPT} {user_prompt}{AI_PROMPT}"
#         response = anthropic_client.completions.create(
#             model="claude-2",
#             max_tokens_to_sample=1500,
#             prompt=claude_prompt
#         )
#         completed_text = response.completion if response else None

#     except Exception as e:
#         print("Error in Claude Bot System: ", e)

def generate_company_questions(company_details): # need to Fix
    pass

def generate_working_role_related_data(role_name):
    try:
        user_prompt = f"Generate list of 5 string of paragraph regarts about that responsibilities of {role_name} role, I only required list of string as a response not more that and dont append numbers at the start i need only strings"
        system_prompt = "You are a helpful assistant that provides information about various roles."
        print(f"Pulling about responsibilities of a {role_name}")
        responsibilities = gpt_bot_system(user_prompt, system_prompt)

        user_prompt = f"Generate list of 5 string of required top most skills for the {role_name} role, I only required list of string as a response not more that and dont append numbers at the start i need only strings"
        print(f"Pulling about responsibilities of a {role_name}")
        top_skills = gpt_bot_system(user_prompt, system_prompt)
        return responsibilities, top_skills
    
    except Exception as e:
        print("Error in Generate Working Role Related Data: ", e)
        return [], []


def generate_company_related_data(company_name):
    try:
        user_prompt = f"Generate list of 1 string of paragraph regarts about that {company_name} company, I only required list of string as a response not more that that"
        system_prompt = "You are a helpful assistant that provides information about company."
        print(f"Pulling about company data of {company_name}")
        about_company = gpt_bot_system(user_prompt, system_prompt)

        user_prompt = f"Generate list of 1 string of paragraph regarts latest news of {company_name} company, I only required list of string as a response not more that that"    
        print(f"Pulling about company news of {company_name}")
        latest_news = gpt_bot_system(user_prompt, system_prompt)

        user_prompt = f"Generate list of 5 strings of paragraphs regarts latest trends of Google company industry, I only required list of string as a response not more that that and dont append numbers at the start i need only strings"
        print(f"Pulling about company trends of {company_name}")
        industry_trends = gpt_bot_system(user_prompt, system_prompt)

        return about_company, latest_news, industry_trends
    except Exception as e:
        print("Error in Generate Company Related Data: ", e)
        return [], [], []

def generate_skill_questions(skill_name, type):
    try:
        model_mapping = {
            'hard_skill': HardSkillQuestions,
            'soft_skill': SoftSkillQuestions,
            'hr_skill': HrQuestions
        }
        model = model_mapping.get(type)
        if model and model.objects(name=skill_name):
            print(f"Questions for {skill_name} exists")
            return 

        print(f"Generating skill questions for {skill_name}")
        levels = ["Beginner", "Intermediate", "Expert"]
        final_dict = {}
        for level in levels:
            user_prompt = f"Generate 200 {skill_name} interview questions for {level} level as a list of strings where each string repreresponsesents a question."
            system_prompt = "You are a helpful assistant that generates technical interview questions."
            generated_questions = gpt_bot_system(user_prompt, system_prompt)
            new_generated_questions = []
            for item in generated_questions:
                temp_data = item.split(". ", 1)
                if  len(temp_data) > 1:
                    new_generated_questions.append(temp_data[1])

            final_dict[level] = new_generated_questions
        
        new_skill_suggestion = model(
            name=skill_name, 
            beginner=final_dict.get("Beginner", []),
            intermediate=final_dict.get("Intermediate", []),
            expert=final_dict.get("Expert", [])
        )
        new_skill_suggestion.save()        
    
    except Exception as e:
        print("Error in generate_skill_questions: ", e)
        traceback.print_exc()

def generate_jd_skill_questions(skill_name, count = 0):
    try:
        user_prompt = f"Generate 5 {skill_name} interview questions for Mid to export level as a list of strings where each string repreresponsesents a question."
        system_prompt = "You are a helpful assistant that generates technical interview questions."
        generated_questions = gpt_bot_system(user_prompt, system_prompt)
        new_generated_questions = []
        for _, question in enumerate(generated_questions):
            temp_data = question.split(". ", 1)
            if len(temp_data) > 1:
                new_generated_questions.append({
                "category": "jd_skill",
                "duration": 60,
                "id": count + 1,
                "question": question,
                "sub_category": skill_name,
                "tag": "technical",
                })
        return new_generated_questions
    except Exception as e:
        print("Error in generate_jd_skill_questions: ", e)
        traceback.print_exc()
        return []

def generate_cultural_skill_questions(skill_name, count=0):
    try:
        user_prompt = f"Generate 5 {skill_name} interview questions for Mid to export level as a list of strings where each string repreresponsesents a question."
        system_prompt = "You are a helpful assistant that generates cultural interview questions."
        generated_questions = gpt_bot_system(user_prompt, system_prompt)
        new_generated_questions = []
        for _, question in enumerate(generated_questions):
            temp_data = question.split(". ", 1)
            if len(temp_data) > 1:
                new_generated_questions.append({
                "category": "cultural_skill",
                "duration": 60,
                "id": count + 1,
                "question": question,
                "sub_category": skill_name,
                "tag": "technical",
                })
        return new_generated_questions
    except Exception as e:
        print("Error in generate_cultural_skill_questions: ", e)
        traceback.print_exc()
        return []

def generate_skill_improvement_suggestions(skill_name, type):
    try:
        print(f"Generating skill improvement suggestions for {skill_name}")
        model_mapping = {
            'hard_skill': HardSkillImprovementSuggestions,
            'soft_skill': SoftSkillImprovementSuggestions,
            'emotion': EmotionsSuggestions
        }
        model = model_mapping.get(type)
        if model and model.objects(name=skill_name):
            print(f"improvement suggestions for {skill_name} exists")
            return 
            
        user_prompt = f"Generate 5 {skill_name} improvement suggestions as a list of strings where each string represents a suggestions."
        system_prompt = "You are a helpful assistant that Suggest improvement suggestions for a given skill."
        generated_suggestions= gpt_bot_system(user_prompt, system_prompt)
        
        new_generated_suggestions = []
        for item in generated_suggestions:
            temp_data = item.split(". ", 1)
            if  len(temp_data) > 1:
                new_generated_suggestions.append(temp_data[1])

        new_skill_suggestion = model(name=skill_name, suggestions=new_generated_suggestions)
        new_skill_suggestion.save()        
        
    except Exception as e:
        print("Error in Generate Skill Improvement Suggestions: ", e)
        
def generate_company_based_questions(level, role, company, role_name=None):
    if role_name == "Screening":
        result = CompanyRoleCustomQuestions.object(company=company, role_name = role).first()
        questions
        if result: 
            if level.lower() == 'beginner':
                questions = result.beginner
            elif level.lower() == 'intermediate':
                questions = result.intermediate
            elif level.lower()  in ['expert', 'export']:
                questions = result.export
                if not questions:
                    questions = result.expert
        if questions:
            # adding technical questions
            technical_questions = questions.get("technical", [])
            
            if technical_questions:
                selected_indices = random.sample(range(2, len(questions) - 2), 5)
            else:
                selected_indices = []
            final_list = []
            for i in selected_indices:
                count = count + 1
                final_list.append({
                        "id": count,
                        "tag": "technical",
                        "question": technical_questions[i],
                        "duration": 60,
                        "category": role,
                        "sub_category": None
                    }
                )    
            
            # adding behavioral questions
            behavioral_questions = questions.get("behavioral", [])
            
            if behavioral_questions:
                selected_indices = random.sample(range(2, len(questions) - 2), 5)
            else:
                selected_indices = []
            final_list = []
            for i in selected_indices:
                count = count + 1
                final_list.append({
                        "id": count,
                        "tag": "behavioral",
                        "question": behavioral_questions[i],
                        "duration": 60,
                        "category": role,
                        "sub_category": None
                    }
                )
            
            # adding hr questions
            hr_questions = questions.get("hr", [])
            
            if hr_questions:
                selected_indices = random.sample(range(2, len(questions) - 2), 5)
            else:
                selected_indices = []
            final_list = []
            for i in selected_indices:
                count = count + 1
                final_list.append({
                        "id": count,
                        "tag": "hr",
                        "question": hr_questions[i],
                        "duration": 60,
                        "category": role,
                        "sub_category": None
                    }
                )
            return final_list

    technical_prompt = f"Generate 5 Technical interview questions for a role of {role} for {level} level in {company} as a list of strings where each string represents a question."
    print("technical_prompt", technical_prompt)
    
    behavioral_prompt = f"Generate 3 Behavioral interview questions for {level} level in {company} as a list of strings where each string represents a question."
    print("behavioral_prompt", behavioral_prompt)
    
    company_prompt = f"Generate 3 {company} Company information related interview questions for {level} level as a list of strings where each string represents a question."
    print("company_prompt", company_prompt)
    
    
    prompts = {
        "technical": technical_prompt, 
        "behavioral": behavioral_prompt, 
        "hr": company_prompt
    }
    
    final_list = []
    count = 0
    for key, prompt in prompts.items():
        try:
            # Attempt to use OpenAI API
            print("Preparing questions using open AI")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates interview questions."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1500,
                temperature=1,
                api_key=OPENAI_API_KEY,
            )
            print("Open AI questions completed")

            generated_questions = response['choices'][0]['message']['content'].split('\n')

            new_generated_questions = []
            for item in generated_questions:
                temp_data = item.split(". ", 1)
                if len(temp_data) > 1:
                    new_generated_questions.append(temp_data[1])

            for i in new_generated_questions:
                count = count + 1
                final_list.append({
                    "id": count,
                    "tag": key,
                    "question": i,
                    "duration": 180,
                    "category": role,
                    "sub_category": None
                })
            
            return final_list
        
        except Exception as e:
            print(f"OpenAI Error occurred for {key} questions: {e}, so using Claude AI")
            claude_prompt = f"{HUMAN_PROMPT} {prompt}{AI_PROMPT}"
            response = anthropic_client.completions.create(
                model="claude-2",
                max_tokens_to_sample=1500,
                prompt=claude_prompt
            )
            completed_text = response.completion if response else None

            if completed_text:
                # Processing the narrative-style response
                lines = completed_text.split("\n")
                for line in lines:
                    if line.strip() and line.strip().isdigit() == False and "Here are" not in line:
                        # Check for quoted question format
                        if '"' in line:
                            question_text = line.strip().split('"')[1]
                        else:
                            question_text = line.strip()
                        
                        count += 1
                        final_list.append({
                            "id": count,
                            "tag": key,
                            "question": question_text,
                            "duration": 60,
                            "category": role,
                            "sub_category": None
                        })
                        print(f"Generated {key} question {count}: {question_text}")
            return final_list

def extract_required_techical_skills(jd_text, interview_type):
    try:
        jd_text = str(jd_text).strip().lower()
        jd_text = jd_text.replace("\n", " ")
        jd_text = jd_text.replace("\r", " ")
        jd_text = jd_text.replace("\t", " ")
        jd_text = jd_text.replace("\xa0", " ")
        jd_text = jd_text.replace("\u200b", " ")

        if interview_type == "jd_interview":
            user_prompt = f"Generate 1 string of comma seperated required skills for provided job description: {jd_text}, dont provide any additional text."
        else:
            user_prompt = f"Analyze the provided for the following job description along with company name and role: {jd_text}. Using external data sources where necessary, identify the most relevant cultural fit categories that are likely to be significant for this role and company. Consider variations in cultural expectations based on industry standards, the specific job role, and known aspects of the company's corporate culture. Provide a focused list of cultural fit categories that align closely with the expected environment and responsibilities. Generate 1 string of comma seperated required cultural fit categories, dont provide any additional text."
        
        system_prompt = "You are a helpful assistant that generates required skills for a job based on a job description."
        required_skills = gpt_bot_system(user_prompt, system_prompt)
        return required_skills 

    except Exception as e:
        print("Error in Extract Required Technical Skills: ", e)
        return []          




        




# Harnath Need to work
# def generate_js_based_questions(jd_text, role, company):
#     try:

#         jd_text = str(jd_text).strip().lower()
#         jd_text = jd_text.replace("\n", " ")
#         jd_text = jd_text.replace("\r", " ")
#         jd_text = jd_text.replace("\t", " ")
#         jd_text = jd_text.replace("\xa0", " ")
#         jd_text = jd_text.replace("\u200b", " ")

#         jd_prompt = f"Generate 10 Technical interview questions for a role of {role} for {level} level in {company} as a list of strings where each string represents a question."