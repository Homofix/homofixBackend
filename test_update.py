import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = 'google_sheets_credentials.json'
SPREADSHEET_ID = '1i3liZoLekd9_JGws8xMdwTWNwZCfxiHtOfD8x6Uu4Jw'

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID)
worksheet = sheet.worksheet("Experts")

try:
    cell = worksheet.find("924", in_column=1)
    print("Found cell row:", cell.row)
    formatted_row = ["924", "HE-877 (RAHUL704)", "Cleaning", "Bathroom Cleaning, Sofa Cleaning", "Delhi Ncr", "faridabad", "Ballabgarh HUb", "121101, 121003, 121004, 121002, 121007, 121001, 121006, 121005, 121010, 121008, 121009", "Hold", "Active", "-3131.99", "9599891607"]
    worksheet.update(values=[formatted_row], range_name=f"A{cell.row}")
    print("Update successful")
except Exception as e:
    print("Error during update:", repr(e))
