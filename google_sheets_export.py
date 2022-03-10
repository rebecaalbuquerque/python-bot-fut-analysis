import gspread
from oauth2client.service_account import ServiceAccountCredentials

from bet_formater import get_bet


class BetRegisterMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BetRegister(metaclass=BetRegisterMeta):

    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open('Bot')
        self.sheet_instance = sheet.get_worksheet(0)
        self.write_request_per_minute = 40

    def add_bet(self, time, order, order_result, bet_type, championship):
        self.sheet_instance.insert_row([time, order, order_result, bet_type, championship], 2)

    def add_bet_list(self, bet_list):
        for bet in bet_list:
            result = get_bet(bet)

            if result["success"]:
                BetRegister().add_bet(
                    result["bet"]["time"],
                    result["bet"]["order"],
                    result["bet"]["order_result"],
                    result["bet"]["bet_type"],
                    result["bet"]["championship"]
                )
            else:
                print(result["message"])


def register_bet(time, order, order_result, bet_type, championship):
    # Setting up google sheet
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Bot')
    sheet_instance = sheet.get_worksheet(0)

    sheet_instance.insert_row([time, order, order_result, bet_type, championship], 2)
