# TimeAlloc
**TimeAlloc** is a command-line tool that connects to your Google Calendar account to calculate the total time spent in events for a selected calendar and timeframe. You can run it interactively or use command-line arguments for quick calculations.

## Overview

* **Secure Google Account Authentication:** Uses OAuth 2.0 to securely access your calendar data.
* **Multiple Calendar Support:** Automatically lists all your available Google Calendars for you to choose from.
* **Flexible Timespan Options:** Calculate event durations for today, this week, this month, or this year.
* **Custom Date Ranges:** Specify a custom start and end date for your calculation.
* **Dual Mode Operation:** Use the script in an interactive mode or directly with command-line arguments for faster use and scripting.

## Requirements

Ensure you have Python 3 installed on your system. The following Python packages are required (and provided by the requirments.txt file):

* `google-api-python-client`
* `google-auth-httplib2`
* `google-auth-oauthlib`

## Setup Instructions

### 1. Clone the Repository
First, clone this repository to your local machine:
```zsh
git clone https://github.com/fserr/gcal-timealloc.git
cd gcal-timealloc
```

### 2. Set Up Google API Credentials
This tool requires API credentials to access the Google Calendar API.

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project.
3.  From the navigation menu, go to **APIs & Services > Library** and enable the **Google Calendar API**.
4.  Go to **APIs & Services > Credentials**.
5.  Click **Create Credentials > OAuth client ID**.
6.  Select **Desktop app** as the application type.
7.  Click **Create**, then click **Download JSON** to download your credentials.
8.  **Rename the downloaded file to `credentials.json`** and place it in the root directory of this project.

### 3. Install Dependencies
Install the required Python packages using `pip`:
```zsh
pip install -r requirements.txt
```

### 4. Make the Script Executable
Give the script execution permissions:
```zsh
chmod +x timealloc
```

### 5. (Optional) Add to Your PATH
For easy access from any directory, you can add the script to your system's PATH.
```zsh
# Add this line to your ~/.bashrc, ~/.zshrc, or other shell configuration file
export PATH="/path/to/gcal-timealloc:$PATH"

# Then, reload your shell configuration
source ~/.zshrc
# OR
source ~/.bashrc
```

After this, you can run the tool by simply typing timealloc.

## How to Use

### First Run: Authentication
The first time you run the script, a browser window will open asking you to log in to your Google account and grant permission for the application to read your calendar data. After you approve, a `token.json` file will be created in the `~/.config/timealloc` directory (which will be created if not existent). This file stores your authentication tokens so you won't have to log in every time.

### Interactive Mode
To use the script interactively, run it without any arguments:
```bash
timealloc
```

You will be prompted to select a calendar and a timespan from a menu.

### Command-Line Arguments
- `-d`, `--day`: Get the total duration for the current day.
  - Example: `./timealloc -d`

- `-w`, `--week`: Get the total duration for the current week.
  - Example: `./timealloc -w`

- `-m`, `--month`: Get the total duration for the current month.
  - Example: `./timealloc -m`

- `-y`, `--year`: Get the total duration for the current year.
  - Example: `./timealloc -y`

- `--start` & `--end`: Specify a custom date range directly.
  - Example: `./timealloc --start='2025-01-01' --end='2025-01-31'`

- `--id`: Select the desired calendar by its ID.
  - Example: `./timealloc --id='1234@group.calendar.google.com'`

```
