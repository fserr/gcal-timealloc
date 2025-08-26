import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
    # --- AUTH ---
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # --- GET CALENDARS ---
        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get("items", [])

        calendars_id_map = {}
        cal_selector_constructor = 0
        print("Calendars:")
        for cal in calendars:
            cal_selector_constructor += 1
            calendars_id_map[cal_selector_constructor] = cal["id"]
            print(f"{cal_selector_constructor}. {cal['summary']}")
        
        print("")
        
        # TODO: "Select calendar ..."
        calendar_selector = 1

        # --- GET UPCOMING EVENTS FROM SELECTED CALENDAR ---
        # Constructor for retrieving desired timespan
        now_utc = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        print(now_utc)

        # TODAY
        if calendar_selector == 1:
            time_min = now_utc
            time_max = now_utc
            return
        # THIS WEEK
        elif calendar_selector == 2:
            time_min = now_utc
            time_max = now_utc
            return
        # THIS MONTH
        elif calendar_selector == 3:
            time_min = now_utc
            time_max = now_utc
            return
        # THIS YEAR
        elif calendar_selector == 4:
            time_min = now_utc
            time_max = now_utc
            return
        # CUSTOM
        elif calendar_selector == 5:
            time_min = now_utc
            time_max = now_utc
            return
        
        else:
            print("Invalid option.")
            return
        
        time_min = now_utc
        time_max = now_utc
        
        events_result = (
            service.events()
            .list(
                calendarId=calendars_id_map[calendar_selector],
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return
        
        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()