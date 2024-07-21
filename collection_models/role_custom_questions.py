from mongoengine import Document, StringField, ListField, DateTimeField, IntField
from datetime import datetime

class CompanyRoleCustomQuestions(Document):
    meta = {'collection': 'company_role_custom_questions'}
    
    company = StringField(required=True)
    role_name = StringField(required=True)
    beginner = ListField(StringField())
    intermediate = ListField(StringField())
    export = ListField(StringField())
    institution_id = IntField(required=True)
    
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    # Override the save method to update the modified date
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(CompanyRoleCustomQuestions, self).save(*args, **kwargs)
