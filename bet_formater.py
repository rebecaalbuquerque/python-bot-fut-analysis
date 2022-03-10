import re

ADD_REGEX = "(?:(?:(?:(0[1-9]|1[0-9]|2[0-8])[\/\-\.](0[1-9]|1[0-2])|(29|30)[\/\-\.](0[13-9]|1[0-2])|(31)[\/\-\.](0[13578]|1[02]))[\/\-\.]([1-2][0-9]{3}))|(?:(29)[\/\-\.](02)[\/\-\.]([1-2][0-9](?:0[48]|[2468][048]|[13579][26])|(?:0[48]|[2468][048]|[13579][26])00)))(?: ((?:[0-1][0-9])|(?:2[0-3])):([0-5][0-9]))?;([0-9]{1,2}.[0-9]{1,2}.[0-9]{1,2});(-?[0-9]{1,2});(.+?);(\\b[^\\d\\W]+\\b$)"


def get_bet(message):
    match = re.search(ADD_REGEX, message)

    if match:
        command = match.string[match.span()[0]:match.span()[1]]
        bet = command.split(";")

        time = bet[0]
        order_array = bet[1].split(".")
        order_result = bet[2]
        bet_type = bet[3]
        championship = bet[4]
        order = ""

        for index, value in enumerate(order_array):
            if value == order_result:
                order += "["
                order += value
                order += "]"
            else:
                order += value

            if index < len(order_array) - 1:
                order += "."

        result = "\U00002705" if int(order_result) > -1 else "\U0000274C"

        response = """
            Você salvou a seguinte aposta:

            \U0001F3C6 {}
            \U000026BD {}
            \U000023F0 {}

            {}
            """.format(championship, bet_type, order, result)

        return {
            "success": True,
            "bet": {
                "time": time,
                "order": order,
                "order_result": order_result,
                "bet_type": bet_type,
                "championship": championship
            },
            "message": response
        }

    else:
        return {
            "success": False,
            "bet": [],
            "message": "Não foi possível identificar a aposta {}".format(message)
        }
