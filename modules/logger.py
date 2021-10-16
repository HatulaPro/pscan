from colorama import Fore, Style
import time


class Logger:
    output_file = None

    @staticmethod
    def set_output_file(file_name):
        if file_name:
            Logger.output_file = open(file_name, 'w')

    @staticmethod
    def time_now():
        return time.strftime("%H:%M:%S", time.localtime())

    @staticmethod
    def message(text):
        if Logger.output_file:
            Logger.output_file.write(text + '\n')

        text = text.replace('\n', '\n' + (' ' * 18))
        print(
            f"{Fore.MAGENTA}{Style.BRIGHT}{Logger.time_now()} {Fore.BLUE} MESSAGE{Style.RESET_ALL} {text}")

    @staticmethod
    def info(text):
        if Logger.output_file:
            Logger.output_file.write(text + '\n')

        text = text.replace('\n', '\n' + (' ' * 18))
        print(
            f"{Fore.MAGENTA}{Style.BRIGHT}{Logger.time_now()} {Fore.GREEN}    INFO{Style.RESET_ALL} {text}")

    @staticmethod
    def warning(text):
        if Logger.output_file:
            Logger.output_file.write(text + '\n')

        text = text.replace('\n', '\n' + (' ' * 18))
        print(
            f"{Fore.MAGENTA}{Style.BRIGHT}{Logger.time_now()} {Fore.YELLOW} WARNING{Style.RESET_ALL} {text}")

    @staticmethod
    def error(text):
        if Logger.output_file:
            Logger.output_file.write(text + '\n')

        text = text.replace('\n', '\n' + (' ' * 18))
        print(
            f"{Fore.MAGENTA}{Style.BRIGHT}{Logger.time_now()} {Fore.RED}   ERROR{Style.RESET_ALL} {text}")
