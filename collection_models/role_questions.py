from mongoengine import Document, StringField, ListField, DateTimeField
from datetime import datetime

class CompanyRoleQuestions(Document):
    meta = {'collection': 'company_role_questions'}
    
    company = StringField(required=True)
    name = StringField(required=True)
    beginner = ListField(StringField())
    intermediate = ListField(StringField())
    expert = ListField(StringField())
    export = ListField(StringField())
    
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    # Override the save method to update the modified date
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(CompanyRoleQuestions, self).save(*args, **kwargs)
