from mongoengine import Document, StringField, ListField, DateTimeField, IntField
from datetime import datetime

class CulturalSkillCustomQuestions(Document):
    meta = {'collection': 'cultural_custom_questions'}
    
    name = StringField(required=True)
    questions = ListField(StringField())
    
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    # Override the save method to update the modified date
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(CulturalSkillCustomQuestions, self).save(*args, **kwargs)