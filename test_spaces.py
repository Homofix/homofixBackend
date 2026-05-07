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
for i, row in enumerate(all_values):
    if not row: continue
    sno = row[0]
    if sno != sno.strip():
        print(f"Row {i+1} has spaces in S.No: '{sno}'")
