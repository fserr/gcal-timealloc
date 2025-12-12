## TimeAlloc
**TimeAlloc** is a command-line utility written in Python that calculates the total duration of events in a Google Calendar within a specified timeframe. It ignores all-day events and supports both interactive and argument-based execution.

## Dependencies
The script requires Python 3 and the Google API client libraries.
```zsh
pip install -r requirements.txt
```
Dependencies listed in requirements.txt:
* `google-api-python-client`
* `google-auth-httplib2`
* `google-auth-oauthlib`

The script has been tested with Python 3.12.11.

## Setup
To use the tool, you must obtain OAuth 2.0 credentials from Google.
1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the Google Calendar API.
3. Create OAuth client ID credentials (application type: Desktop app).
4. Download the JSON file, rename it to credentials.json, and place it in the project root.

## Usage
Make the script executable:
```zsh
chmod +x timealloc
```

#### Authentication
On the first run, the script will open a browser window to authenticate with your Google account. It creates a `~/.config/timealloc/token.json` file to store the session tokens for future executions.

#### Interactive Mode
Run without arguments to select a calendar and timeframe via a menu.

#### CLI Mode
You can pass arguments to skip the interactive menu.

Timeframes:
* `-d`, `--day`: Current day.
* `-w`, `--week`: Current week.
* `-m`, `--month`: Current month.
* `-y`, `--year`: Current year.
* `--start`, `--end`: Custom range (format: YYYY-MM-DD).

Calendar Selection:
* `--id <ID>`: Select calendar by ID.
* `-n`, `--name <NAME>`: Select calendar by summary name.
* `--get-ids`: List available calendars and their IDs.

### Examples
Calculate total time for the current week:
```zsh
./timealloc -w
```

Calculate time for a specific date range on a specific calendar:
```zsh
./timealloc --name "Work" --start "2023-01-01" --end "2023-01-31"
```

List all calendar IDs:
```zsh
./timealloc --get-ids
```
