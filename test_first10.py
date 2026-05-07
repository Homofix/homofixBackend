import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = 'google_sheets_credentials.json'
SPREADSHEET_ID = '1i3liZoLekd9_JGws8xMdwTWNwZCfxiHtOfD8x6Uu4Jw'

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID)
worksheet = sheet.worksheet("Experts")

all_values = worksheet.get_all_values()
for i in range(min(10, len(all_values))):
    print(f"Row {i+1}: S.No: {all_values[i][0]} | Expert_ID: {all_values[i][1] if len(all_values[i]) > 1 else ''}")
