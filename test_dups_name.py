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
    if expert_id:
        name = expert_id.split('(')[1].split(')')[0] if '(' in expert_id else expert_id
        if name in seen:
            print(f"Duplicate Name {name} found at row {i+1} (S.No {sno}) and row {seen[name]['row']} (S.No {seen[name]['sno']})")
            duplicates_count += 1
        else:
            seen[name] = {'row': i+1, 'sno': sno}
print(f"Total duplicates found by Name: {duplicates_count}")
