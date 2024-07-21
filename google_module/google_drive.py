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

class GoogleDriveManager(GoogleConnector):
    def __init__(self):
        super().__init__()
        self.service = super().create_drive_service()
        self.master_folder_id = os.environ.get("GOOGLE_PARENT_FOLDER_ID")

    def get_folders_in_drive(self):
        results = self.service.files().list().execute()
        print("results", results)
        
    def get_folders_in_folder(self, folder_id):
        results = self.service.files().list(
            q=f"'{folder_id}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'",
            fields="nextPageToken, files(id, name)").execute()
        folders = results.get('files', [])
        return folders

    def get_files_in_folder(self, folder_id):
        results = self.service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name)").execute()
        files = results.get('files', [])
        return [file['name'] for file in files]

    def folder_exists_by_id(self, folder_id):
        try:
            folder = self.service.files().get(fileId=folder_id).execute()
            return not folder == None
        except:
            return False

    def folder_exists_by_name(self, folder_name, parent_folder_id = None):
        try:
            print("Parent folder id to check", parent_folder_id)
            
            if not parent_folder_id:
                parent_folder_id = self.master_folder_id
            
            list_of_folders = self.get_folders_in_folder(parent_folder_id)
            print(f"list of folders in parent folder {parent_folder_id}", list_of_folders)
            print("Checking folder_name", folder_name)
            
            for folder in list_of_folders:
                
                if folder.get('name') == folder_name:
                    return folder
            return {}
        except:
            return {}
        
    def create_folder(self, folder_name, parent_folder_id=None):
        if not parent_folder_id:
            parent_folder_id = self.master_folder_id
        
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        folder = self.service.files().create(body=file_metadata, fields='id').execute()
        print("New Folder data:", folder)
        return folder.get('id')

    def delete_folder(self, folder_id):
        self.service.files().delete(fileId=folder_id).execute()

    def rename_folder(self, folder_id, new_name):
        file_metadata = {
            'name': new_name
        }
        self.service.files().update(fileId=folder_id, body=file_metadata).execute()

    def move_folder(self, folder_id, new_parent_folder_id):
        file_metadata = {
            'parents': [new_parent_folder_id]
        }
        self.service.files().update(fileId=folder_id, body=file_metadata).execute()

    def copy_folder(self, folder_id, new_parent_folder_id):
        copied_folder = self.service.files().copy(fileId=folder_id, body={'parents': [new_parent_folder_id]}).execute()
        return copied_folder.get('id')

    def zip_and_download_folder(self, folder_id, zip_filename):
        file_list = self.service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="files(id, name)").execute()
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in file_list.get('files', []):
                file_id = file['id']
                request = self.service.files().get_media(fileId=file_id)
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    if status:
                        print(f"Download {int(status.progress() * 100)}%.")
                    print("Download Complete.")
                    zipf.writestr(file['name'], fh.getvalue())

    def create_file(self, file_name, folder_id, file_data):
            # media = io.BytesIO(file_data)
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
            file = self.service.files().create(
                body=file_metadata,
                media_body=file_data,
                fields='id'
            ).execute()
            return file

    def delete_file(self, file_id):
        self.service.files().delete(fileId=file_id).execute()

    def rename_file(self, file_id, new_name):
        file_metadata = {
            'name': new_name
        }
        self.service.files().update(fileId=file_id, body=file_metadata).execute()

    def download_file(self, file_id, file_path):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print(f"Download {int(status.progress() * 100)}%.")
        print("Download Complete.")

    def move_file(self, file_id, new_parent_folder_id):
        file_metadata = {
            'parents': [new_parent_folder_id]
        }
        self.service.files().update(fileId=file_id, body=file_metadata).execute()