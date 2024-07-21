import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

class GoogleConnector:
    def __init__(self):
        self.credentials_dict = {
            "type": os.environ.get("GOOGLE_TYPE"),
            "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
            "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDgyOHf3Cmz7Wl3\n+MHHjfC3JETvENd8NBBKPNmTM0t7gf+/msPeqHqIpGN8p3PmU8wuXxjZNPtiQtNp\nEHC5FT5BAL1B5ibYZt7M7vjg6muojRASfTQ7u88P1GfdivBT0diyUghZzkldSxpD\nZwSpiwSW5n1QP6tFUWtw+sKXQ64FB4vj7fN86W8welUGRiRKPnYPTRIjlJDuQuC3\nKwEujTqAX6BQUiMLhCrURw9lfPcioOnyIeKmkYAN37MDUef4yXmFn8IjFdqJ9qBQ\n9SHfqxnl0j3yyeXr4TnAf3btCfGr3mE5tpvFziwIdWEcRrX5UGlRE5+l03PsyDLI\nSNK9D+wXAgMBAAECgf9w1GSMeXZ1WjYWgkbCY/zv8MSpO0rujTOgD+smeBjrZdV5\n17V5jhfzfpBxgZwrgOR8Yj+Wx4FnUSPNGPN7863L8xMMgPn+paQwOcOzIffoIuZu\nYWpWkW7eA0AfdB4t9KdQ2txWN7WbnpcQPiWY9K7ZD9jW7x6JLNVBYJ1MUCyJWM9T\nXF1om+SdzjCxFRZhrsKDX8yhdGUVNIsLZKbYimiZKuwZAdVQ/lE+tScElMzDNDCC\nIlHJfQ4hzZUoPa+fi7/cGDfO2PV5MwFn20NscfB9cM2KfXvuHL54oyX+9h5KyHGB\nq2KdUDi+O9i8jZxTopVMKrSWgDzhvSuOgrcA8PUCgYEA+nLzBaYDlkGAmwgJnPrU\nOL4/ZrUBcZEH/TGauksBB74pt6xX7TAB38g8s1uXUZh3OhxIr4jCwXsm31nzAgjK\nJclSpv/TXspJQgUDgEaZVjLakXLO6kAWPQcM09XBkhtNJVnbKiCOX7/vGzJ50cBZ\ngs5cTp339OtGLu0/a0ibo0sCgYEA5cRQNwPGXfaMii9/tTP7Y8ZTxVItd/Fzan63\nuvUYJIlHzDiJyaIUdGig+fh/aRabVsJHHVvy6yhrst6EEQpuJho/AW7VYDblMUNA\n+6+QiwzbMwLiB8h88ZnPCWy6sruYu8u1zrbIl2CFGSXEOx+SeRKnX3cCsQuD52An\nvhaCTuUCgYBmn09hUyNJIFH4NJTr1AO9tIb6KNUMmebyIq9KAo3LhGpHrsDgmblK\n3xuwSql4b8b68rf95UYYTcQh5ROkE8HxNcs+Trlnr+/Qs4k5uLQAFBpnWunaJqR2\nITtqWb5VhgZYdbdOTcTJCzaIqGguQGjtJm3AcQ43N2istd40sa3EfQKBgQCcnbQP\nzALrCaPCjZ3/Ze91kzqGxf04RNznOnkCdw592RWXnvJM/q3yq18PBNPUThSUjtjq\nqkJrCKJgykw7UWDDmCBaWbIYY1LWwYEKDiH4pkrD+rMXmxGPncgCJJseOcFiQPks\nbmtMw/31pkicBGlTHeP4rqanB7JhhKmSaMVqAQKBgQD2WoM2Hp3LIZb03Ra+f298\n/SScQK72RN0ysSqafsaEnkKxmIsSBxe7+weiTk/mW1Zn27DQ6vswm3Ilut/bmk/w\nWbq0XFhjZxHUAKu6aDgyZqBswLofyS20PdRbdhbWEGtmw9j4dWQYWcOWgu+C8M9e\nGzsLNU2si5N3HKxqM8b4Lw==\n-----END PRIVATE KEY-----\n",
            "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "auth_uri": os.environ.get("GOOGLE_AUTH_URI"),
            "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.environ.get("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_X509_CERT_URL")
        }
        
    def _connect_to_google_by_file(self, credentials_path):
        creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=self.scope)
        service = build('drive', 'v3', credentials=creds)
        return service

    def _connect_to_google_by_dict(self, scope, service_name):
        creds = service_account.Credentials.from_service_account_info(
            self.credentials_dict, 
            scopes=scope,
            subject= 'admin-workspace@munsow.com'
            )
        service = build(service_name, 'v3', credentials=creds)
        return service
    
    def create_drive_service(self):
        scope = ['https://www.googleapis.com/auth/drive']
        service = self._connect_to_google_by_dict(scope, "drive")
        return service
    
    def create_calender_service(self):
        scope = ['https://www.googleapis.com/auth/calendar']
        service = self._connect_to_google_by_dict(scope, "calendar")
        return service
    
        