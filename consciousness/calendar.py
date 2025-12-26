import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_upcoming_events():
    creds = None
    # Token file stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                return "❌ Error: 'credentials.json' not found. Please place it in the lab folder."
            
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print(f"📅 [CALENDAR] Fetching events for {now}...")
    
    try:
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=3, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return "No upcoming events found."
        
        agenda = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            agenda.append(f"- {start}: {event['summary']}")
        
        return "\n".join(agenda)
    except Exception as e:
        return f"Error retrieving events: {str(e)}"

if __name__ == "__main__":
    print(get_upcoming_events())
