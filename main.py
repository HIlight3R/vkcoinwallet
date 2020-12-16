import cmd
from datetime import datetime

from colorama import Fore, Style
from terminaltables import AsciiTable
from vkcoinapi import *

from config import login


class WalletShell(cmd.Cmd):
    # Console settings
    prompt = Fore.YELLOW + '==> ' + Fore.RESET
    ruler = '-'
    intro = Style.BRIGHT + Fore.LIGHTBLUE_EX + 'Welcome to your personal VK Coin wallet!' + Fore.RESET + Style.RESET_ALL

    def __init__(self):
        """Class exemplar initialisation"""
        super().__init__()  # Parent class initialisation
        self.config = login()  # Configuration variable
        # VKCoinAPI class exemplar initialisation
        self.coin = VKCoin(key=self.config['key'], merchantId=self.config['uid'], token=self.config['token'])

    def do_get_payment_url(self, arg) -> None:
        """get_payment_url amount [free]
        amount (float) - total sum
        free (bool) - allow user to change amount>"""

        args = parse(arg)
        amount = int(float(args[0]) * 1000)
        free = to_bool(get(args, 1))  # Allow user to change amount

        result = self.coin.getPaymentURL(amount=amount, free=free)
        print(result)

    def do_get_balance(self, arg) -> None:
        """get_balance [*ids]
        *ids (1 or more ints) - IDs of users to get balance (if not defined returns current user balance)"""

        user_ids = parse(arg)

        result = self.coin.getBalance(user_ids=user_ids)

        data = [[Style.BRIGHT + 'ID' + Style.RESET_ALL, Style.BRIGHT + 'Balance' + Style.RESET_ALL]]

        for key, value in result['response'].items():
            data.append([f'ID {key}', f'{str(value / 1000)} VKC'])

        table = AsciiTable(data)
        table.justify_columns[0] = 'center'
        table.justify_columns[1] = 'center'

        print(table.table)

    def do_get_transactions(self, arg) -> None:
        """get_transactions [type]
        type (int) - type of interpretation; if type = 1 then it returns last 1000 transactions from payment links, if
            type = 2 (default) then it returns last 100 transactions"""

        args = parse(arg)
        result = self.coin.getTransactions(type=args[0]) if args else self.coin.getTransactions()

        data = [[Style.BRIGHT + 'Date and time' + Style.RESET_ALL, Style.BRIGHT + 'To ID & from ID' + Style.RESET_ALL,
                 Style.BRIGHT + 'Amount' + Style.RESET_ALL]]

        for item in result['response']:
            data.append([datetime.fromtimestamp(item['created_at']).strftime('%d.%m.%Y %H:%M:%S'),
                         f"ID {item['from_id']} => ID {item['to_id']}", f"{int(item['amount']) / 1000} VKC"])

        table = AsciiTable(data)
        table.justify_columns[0] = 'center'
        table.justify_columns[1] = 'center'
        table.justify_columns[2] = 'center'

        print(table.table)

    def do_send_payment(self, arg):
        """send_payment to amount
            to (int) - ID of receiver
            amount (float) - total sum"""

        args = parse(arg)

        to = int(args[0])
        amount = int(float(args[1]) * 1000)

        result = self.coin.sendPayment(to=to, amount=amount)
        answer = result.get('response')
        if answer:
            print(Fore.GREEN + 'Successful payment!' + Fore.RESET)
        else:
            print(Fore.RED + 'Something went wrong! Try again...' + Fore.RESET)

    def do_exit(self, *args) -> None:
        """Closes program"""
        input('Press ENTER to exit...')
        exit(0)

    def do_quit(self, *args) -> None:
        """Same as exit"""
        self.do_exit()


def parse(arg) -> tuple:
    return tuple(arg.split())


def get(t: tuple, n: int):
    try:
        return t[n]
    except IndexError:
        return None


def to_bool(exp: str) -> bool:
    if exp is None or exp in ('-', 'n', 'N', 'no', 'No', 'NO', 'off', 'Off', 'OFF', 'false', 'False', 'FALSE'):
        return False
    elif exp is not None and exp in ('+', 'y', 'Y', 'yes', 'Yes', 'YES', 'on', 'On', 'ON', 'true', 'True', 'TRUE'):
        return True


if __name__ == '__main__':
    try:
        WalletShell().cmdloop()
    except KeyboardInterrupt:
        WalletShell().do_exit()
