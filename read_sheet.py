import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

CREDS_FILE = 'google_sheets_credentials.json'
SPREADSHEET_ID = '1i3liZoLekd9_JGws8xMdwTWNwZCfxiHtOfD8x6Uu4Jw'

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID)
try:
    worksheet = sheet.worksheet("Experts")
    headers = worksheet.row_values(1)
    print("Headers:", headers)
    
    # print first data row to see what is in column 1
    row2 = worksheet.row_values(2)
    print("Row 2:", row2)
    
except Exception as e:
    print(e)
    
