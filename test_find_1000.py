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
# Find an S.No >= 1000
for i, row in enumerate(all_values):
    if row and row[0].replace(',', '').isdigit() and int(row[0].replace(',', '')) >= 1000:
        val = row[0]
        print(f"Row {i+1} has S.No: '{val}'")
        # Let's see if find() can find it with and without comma
        cell1 = worksheet.find(val, in_column=1)
        clean_val = val.replace(',', '')
        cell2 = worksheet.find(clean_val, in_column=1)
        print(f"find('{val}'):", cell1)
        print(f"find('{clean_val}'):", cell2)
        break
