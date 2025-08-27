from datetime import datetime, time, timezone, timedelta, date
import calendar
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_duration_seconds(event) -> float:
    """
    Calculates and formats the duration of a timed Google Calendar event.
    Args:
        event: A single event resource dictionary from the API.
    Returns:
        A formatted string like "X hours and Y min", or None for all-day events.
    """
    # We only process events with specific start and end times ('dateTime')
    if 'dateTime' not in event['start'] or 'dateTime' not in event['end']:
        return 0 # This is an all-day event

    # Parse the ISO 8601 timestamps into datetime objects
    start_time = datetime.fromisoformat(event['start']['dateTime'])
    end_time = datetime.fromisoformat(event['end']['dateTime'])

    # The difference is a timedelta object
    duration = end_time - start_time

    # Calculate total hours and remaining minutes
    total_seconds = duration.total_seconds()
    return total_seconds
    
    
def get_formatted_duration(total_seconds):
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)

    # Apply the specific formatting rules
    if hours > 0 and minutes > 0:
        return f"{hours} hours and {minutes} min"
    elif hours > 0:
        return f"{hours} hours"
    elif minutes > 0:
        return f"{minutes} min"
    else:
        return "0 min" # For events with no duration


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
        
        
        calendar_selector = 6       # TODO: "Select calendar: "

        # --- GET UPCOMING EVENTS FROM SELECTED CALENDAR ---
        # Constructor for retrieving desired timespan
        today_utc = datetime.now(timezone.utc).date()
        
        print("Timespans: ")
        print("1. Current day")
        print("2. Current week")
        print("3. Current month")
        print("4. Current year")
        print("5. Custom")
        
        timespan_selector = 4       # TODO: "Select timespan (YYYY/MM/DD): "
        
        # TODAY
        if timespan_selector == 1:
            time_min = datetime.combine(today_utc, time.min, tzinfo=timezone.utc).isoformat()
            time_max = datetime.combine(today_utc, time.max, tzinfo=timezone.utc).isoformat()
        # THIS WEEK
        elif timespan_selector == 2:
            # First day of week = monday
            week_start_utc = today_utc - timedelta(days=today_utc.weekday())
            week_end_utc = week_start_utc + timedelta(days=6)
            time_min = datetime.combine(week_start_utc, time.min, tzinfo=timezone.utc).isoformat()
            time_max = datetime.combine(week_end_utc, time.max, tzinfo=timezone.utc).isoformat()
        # THIS MONTH
        elif timespan_selector == 3:
            month_start_utc = today_utc.replace(day=1)
            _, month_end_utc_num = calendar.monthrange(today_utc.year, today_utc.month)
            month_end_utc = today_utc.replace(day=month_end_utc_num)
            time_min = datetime.combine(month_start_utc, time.min, tzinfo=timezone.utc).isoformat()
            time_max = datetime.combine(month_end_utc, time.max, tzinfo=timezone.utc).isoformat()
        # THIS YEAR
        elif timespan_selector == 4:
            year_start_utc = date(today_utc.year, 1, 1)
            year_end_utc = date(today_utc.year, 12, 31)
            time_min = datetime.combine(year_start_utc, time.min, tzinfo=timezone.utc).isoformat()
            time_max = datetime.combine(year_end_utc, time.max, tzinfo=timezone.utc).isoformat()
        # CUSTOM
        elif timespan_selector == 5:
            time_min = datetime.combine(today_utc, time.min, tzinfo=timezone.utc).isoformat()
            time_max = datetime.combine(today_utc, time.max, tzinfo=timezone.utc).isoformat()
        else:
            print("Invalid option.")
            return
        
        
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
            print("No events found.")
            return
        
        # TODO: Print total duration
        total_seconds = 0.0
        for event in events:
            total_seconds = total_seconds + get_duration_seconds(event)
        print(get_formatted_duration(total_seconds))

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()