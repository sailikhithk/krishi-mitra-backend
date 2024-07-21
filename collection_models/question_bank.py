from mongoengine import Document, StringField, ListField, DictField, DateTimeField
from datetime import datetime

class CourseContent(Document):
    meta = {'collection': 'course_content'}
    
    name = StringField(required=True)
    description = StringField(required=True)
    course_code = StringField(required=True)
    content_data = DictField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    # Override the save method to update the modified date
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(CourseContent, self).save(*args, **kwargs)
    
