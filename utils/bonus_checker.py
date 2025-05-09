import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

SHEET_NAME = "Game On Player Ledger"

def has_claimed_bonus(user_id):
    try:
        sheet = client.open(SHEET_NAME).worksheet("Bonuses")
        all_rows = sheet.get_all_values()
        for row in all_rows[1:]:
            if str(user_id) == row[1]:  # user_id is in column B (index 1)
                return True
        return False
    except Exception as e:
        print("❌ Failed to check bonus claim:", e)
        return False
