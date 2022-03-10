import json
from datetime import datetime
import re

from bet_formater import get_bet
from google_sheets_export import register_bet


def _contains_bet_command(string):
    if isinstance(string, str) and \
            string.find("\U0001F3C6") > -1 and string.find("\U000023F0") > -1 and string.find("\U000026BD") > -1:
        return True
    else:
        return False


def _extract_bet_command(string):
    index_end_bet = string.find("\U0001FA99")
    result = ""

    if index_end_bet > -1:
        string_formatted = string[0:index_end_bet]
        string_formatted = re.sub("\\s{2,}", ";", string_formatted)
        string_formatted = re.sub("\n", "", string_formatted)
        string_formatted = re.sub("\U00002705{2,}", "", string_formatted)
        string_formatted = re.sub("\U0001F3C6", "", string_formatted)
        string_formatted = re.sub("\U000023F0", "", string_formatted)
        string_formatted = re.sub("\U000026BD", "", string_formatted)
        string_formatted = re.sub("\U00002716", "", string_formatted)
        string_formatted = string_formatted[:-1]
        string_array = string_formatted.split(";")
        string_array_formatted = []

        for index, value in enumerate(string_array):

            if index == len(string_array) - 1:
                string_array_formatted.append(value[2:-1])
            elif index == 1:
                order_array = value.split(".")
                order_array_formatted = []

                for i in order_array:
                    i_formatted = re.sub('[^A-Za-z0-9]+', '', i)

                    if len(i_formatted) == 1:
                        order_array_formatted.append("0" + i)
                    else:
                        order_array_formatted.append(i)

                order_string = ".".join(order_array_formatted)
                order_result_index = order_string.find("\U00002705")
                order_result = str(order_result_index)

                if order_result_index > -1:
                    order_result = order_string[order_result_index - 2:order_result_index]

                string_array_formatted.append(re.sub("\U00002705", "", order_string))
                string_array_formatted.append(order_result)
            else:
                string_array_formatted.append(value.strip())

        result = ";".join(
            [string_array_formatted[1], string_array_formatted[2], string_array_formatted[3], string_array_formatted[0]]
        )

    return result


def export_telegram_chat_bet(file_path):
    chat_file = open(file_path)
    chat_dict = json.load(chat_file)
    chat_list_text = []

    for data in chat_dict:
        date = datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%S")
        date_formatted = date.strftime("%d-%m-%Y %H:%M")

        for text in data["text"]:
            if _contains_bet_command(text):
                chat_list_text.append(date_formatted + ";" + _extract_bet_command(text))

    chat_file.close()
    return chat_list_text


# bet_list = export_telegram_chat_bet(open("/Users/rebeca.diniz/Downloads/result.json"))
#
# for bet in bet_list:
#     result = get_bet(bet)
#
#     if result["success"]:
#         register_bet(
#             result["bet"]["time"],
#             result["bet"]["order"],
#             result["bet"]["order_result"],
#             result["bet"]["bet_type"],
#             result["bet"]["championship"]
#         )
#     else:
#         print("deu ruim")
