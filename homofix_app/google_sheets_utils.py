import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
import os
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

# Define the scope
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Path to the credentials file
CREDS_FILE = os.path.join(settings.BASE_DIR, 'google_sheets_credentials.json')

# Spreadsheet IDs (Using the ones provided in the URL)
# https://docs.google.com/spreadsheets/d/1WGJjRWxYN5oRqv2XXwhOEioKSka8vIwUuiXJREitAZQ/edit?gid=0#gid=0
# https://docs.google.com/spreadsheets/d/1UwskHVXLjzKzlXslKIG3eTPTG6sO1zaFjWn1_pSpLbs/edit?gid=1056621026#gid=1056621026
# It seems there are two links provided. I will assume the first one is the main one or try both if specific tabs are missing?
# The user provided one main link and another one right after without a space.
# 1. 1WGJjRWxYN5oRqv2XXwhOEioKSka8vIwUuiXJREitAZQ
# 2. 1UwskHVXLjzKzlXslKIG3eTPTG6sO1zaFjWn1_pSpLbs
# I will use the first one as default, but logic might be needed if they are split. 
# Looking at the prompt: "this is my google sheet - [link1] [link2]" 
# It's possible different tabs are in different sheets.
# However, usually "Customers", "Bookings" etc are in one CRM-like sheet. 
# I'll default to the first one defined as SPREADSHEET_ID.

SPREADSHEET_ID = '1i3liZoLekd9_JGws8xMdwTWNwZCfxiHtOfD8x6Uu4Jw'

def get_gspread_client():
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        logger.error(f"Error authenticating with Google Sheets: {e}")
        return None

def format_date(value):
    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value

def append_to_sheet(tab_name, row_data):
    """
    Appends a row of data to the specified tab in Google Sheets.
    
    Args:
        tab_name (str): The name of the worksheet/tab.
        row_data (list): A list of values to append as a row.
    """
    client = get_gspread_client()
    if not client:
        return

    try:
        sheet = client.open_by_key(SPREADSHEET_ID)
        try:
            worksheet = sheet.worksheet(tab_name)
        except gspread.exceptions.WorksheetNotFound:
            # Fallback: check the second sheet ID if not found in first
            # The user pasted two URLs concatenated.
            # 2nd ID: 1UwskHVXLjzKzlXslKIG3eTPTG6sO1zaFjWn1_pSpLbs
            try:
                sheet = client.open_by_key('1UwskHVXLjzKzlXslKIG3eTPTG6sO1zaFjWn1_pSpLbs')
                worksheet = sheet.worksheet(tab_name)
            except Exception as e:
                 logger.error(f"Worksheet '{tab_name}' not found in either spreadsheet: {e}")
                 return

        # Format data (handle dates, None, etc.)
        formatted_row = [str(item) if item is not None else "" for item in row_data]
        
        worksheet.append_row(formatted_row)
        logger.info(f"Successfully appended row to {tab_name}")
        
    except Exception as e:
        logger.error(f"Error appending to Google Sheet '{tab_name}': {e}")

def update_or_append_row(tab_name, search_col_idx, search_value, row_data):
    """
    Updates a row if the search_value is found in search_col_idx, else appends.
    
    Args:
        tab_name (str): Name of the tab.
        search_col_idx (int): 1-based column index to search in (e.g., 1 for Column A).
        search_value (str/int): The value to search for (e.g., Customer ID).
        row_data (list): The new data to write.
    """
    client = get_gspread_client()
    if not client:
        return

    try:
        sheet = client.open_by_key(SPREADSHEET_ID)
        try:
            worksheet = sheet.worksheet(tab_name)
        except gspread.exceptions.WorksheetNotFound:
             # Fallback 
            try:
                sheet = client.open_by_key('1UwskHVXLjzKzlXslKIG3eTPTG6sO1zaFjWn1_pSpLbs')
                worksheet = sheet.worksheet(tab_name)
            except Exception as e:
                 logger.error(f"Worksheet '{tab_name}' not found: {e}")
                 return

        formatted_row = [str(item) if item is not None else "" for item in row_data]
        search_value_str = str(search_value)

        try:
            # unique search in the specified column
            cell = worksheet.find(search_value_str, in_column=search_col_idx)
            
            if cell:
                # For 'All Bookings' tab, preserve 'Assigned Expert' on reassignment
                if tab_name == "All Bookings":
                    old_row = worksheet.row_values(cell.row)
                    # index 2 is Assigned Expert, index 22 is Reassigned Expert
                    if len(old_row) > 2 and old_row[2].strip():
                        old_expert = old_row[2].strip()
                        new_expert = str(row_data[2]).strip() if len(row_data) > 2 else ""
                        
                        if old_expert and new_expert and old_expert != new_expert:
                            row_data[2] = old_expert
                            if len(row_data) > 22:
                                row_data[22] = new_expert
                        elif old_expert == new_expert:
                            # Preserve any existing reassigned expert if re-saved
                            if len(old_row) > 22 and old_row[22].strip():
                                if len(row_data) > 22:
                                    row_data[22] = old_row[22].strip()

                formatted_row = [str(item) if item is not None else "" for item in row_data]
                worksheet.update(values=[formatted_row], range_name=f"A{cell.row}")
                logger.info(f"Successfully updated row {cell.row} in {tab_name}")
            else:
                worksheet.append_row(formatted_row)
                logger.info(f"Value {search_value} not found, appended new row to {tab_name}")

        except Exception as e:
             # If find fails or other error, try append?
             # find raises generic exception? No, usually returns None or raises CellNotFound (in older versions). 
             # In newer gspread, find returns None if not found? 
             # Actually, creating a fallback to append is safer.
             logger.warning(f"Error updating row in {tab_name}, falling back to append: {e}")
             worksheet.append_row(formatted_row)

    except Exception as e:
        logger.error(f"Error processing Google Sheet '{tab_name}': {e}")
