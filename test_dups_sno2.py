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
seen = {}
duplicates_count = 0
for i, row in enumerate(all_values):
    if not row: continue
    sno = row[0]
    expert_id = row[1] if len(row) > 1 else ""
    if expert_id in seen:
        print(f"Duplicate Expert_ID {expert_id} found at row {i+1} and row {seen[expert_id]}")
        duplicates_count += 1
    else:
        if expert_id:
            seen[expert_id] = i+1
print(f"Total duplicates found by Expert_ID: {duplicates_count}")
