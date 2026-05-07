import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = 'google_sheets_credentials.json'
SPREADSHEET_ID = '1i3liZoLekd9_JGws8xMdwTWNwZCfxiHtOfD8x6Uu4Jw'

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID)
worksheet = sheet.worksheet("Experts")

try:
    cell = worksheet.find("NON_EXISTENT_ID", in_column=1)
    print("Result:", type(cell))
except Exception as e:
    print("Exception:", type(e), e)
