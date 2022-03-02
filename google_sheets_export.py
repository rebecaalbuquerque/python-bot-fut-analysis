import gspread
from oauth2client.service_account import ServiceAccountCredentials


def register_bet(time, order, order_result, bet_type, championship):
    # Setting up google sheet
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Bot')
    sheet_instance = sheet.get_worksheet(0)

    sheet_instance.insert_row([time, order, order_result, bet_type, championship], 2)
