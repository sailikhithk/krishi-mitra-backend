from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from .google_auth import GoogleConnector
import io
import zipfile
import os
import json
from dotenv import load_dotenv
load_dotenv()

class GoogleCalendarManager(GoogleConnector):
    def __init__(self):
        self.service = super().create_calender_service()
        self.master_folder_id = os.environ.get("GOOGLE_PARENT_FOLDER_ID")

    def create_event(self, calendar_id, start_time, end_time, summary, description, attendees, reminders):
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'Your/Timezone',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Your/Timezone',
            },
            'attendees': [{'email': attendee} for attendee in attendees],
            'reminders': {
                'useDefault': False,
                'overrides': reminders,
            },
        }

        event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        event_id = event.get('id')
        print(f"Event created: {event.get('htmlLink')}")
        return event_id

    def update_event(self, calendar_id, event_id, start_time, end_time, summary, description, attendees, reminders):
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'Your/Timezone',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Your/Timezone',
            },
            'attendees': [{'email': attendee} for attendee in attendees],
            'reminders': {
                'useDefault': False,
                'overrides': reminders,
            },
        }

        updated_event = self.service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
        print(f"Event updated: {updated_event.get('htmlLink')}")


    def delete_event(self, calendar_id, event_id):
        try:
            self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            print(f"Event deleted: {event_id}")
        except Exception as error:
            print(f"An error occurred: {error}")