import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Setup Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

SHEET_NAME = "Game On Player Ledger"

def log_transaction_to_sheet(telegram_handle, first_name, sportsbook_username, password, action, amount, method, status):
    try:
        sheet = client.open(SHEET_NAME).worksheet("Log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, telegram_handle, first_name, sportsbook_username, password, action, amount, method, status]
        sheet.append_row(row)
    except Exception as e:
        print("❌ Failed to log to sheet:", e)

def log_bonus_claim(user_id, username, first_name):
    try:
        sheet = client.open(SHEET_NAME).worksheet("Bonuses")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [timestamp, str(user_id), f"@{username}", first_name]
        sheet.append_row(row)
    except Exception as e:
        print("❌ Failed to log bonus:", e)

def get_bonus_percent():
    try:
        sheet = client.open(SHEET_NAME).worksheet("Settings")
        data = sheet.get_all_records()
        for row in data:
            if row.get("Setting") == "bonus_percent":
                return float(row.get("Value"))
    except Exception as e:
        print("❌ Failed to fetch bonus percent:", e)
    return 0  # default if not found
