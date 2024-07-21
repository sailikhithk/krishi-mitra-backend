from mongoengine import Document, StringField, ListField, DateTimeField
from datetime import datetime

class HardSkillImprovementSuggestions(Document):
    meta = {'collection': 'hard_skill_improvement_suggestions'}
    
    name = StringField(required=True)
    suggestions = ListField(StringField())

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    # Override the save method to update the modified date
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(HardSkillImprovementSuggestions, self).save(*args, **kwargs)
