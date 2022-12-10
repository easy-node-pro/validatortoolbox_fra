import subprocess
import os
import dotenv
import shutil
from os import environ
from colorama import Fore, Back, Style
from subprocess import PIPE, run
from toolbox.library import print_stars, print_stars_reset, return_txt, load_var_file, disk_partitions, converted_unit, free_space_check, all_sys_info
from toolbox.toolbox import menu_error, menu_ubuntu_updates, menu_reboot_server, finish_node
from config import easy_env_fra

def docker_check():
    status = subprocess.call(["docker"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if status == 0:
        print("* Docker is available and working properly.")
        print("* Menu coming soon!")
        print_stars()
        return 0
    else:
        print("* Docker is not available or is not working properly.")
        print("* Install docker on this server and give the user access to continue.")
        print_stars()
        raise SystemExit(0)

def menu_findora() -> None:
    # menuTopperFull()
    for x in return_txt(easy_env_fra.findora_menu):
        x = x.strip()
        try:
            x = eval(x)
        except SyntaxError:
            pass
        if x:
            print(x)

def refresh_stats() -> None:
    print_stars()
    print(f'* Coming soon!')
    print_stars()
    input("* Press ENTER to continue.")

def check_balance_menu() -> None:
    print_stars()
    print(f'* Coming soon!')
    print_stars()
    input("* Press ENTER to continue.")

def operating_system_updates() -> None:
    print_stars()
    print(f'* Coming soon!')
    print_stars()
    input("* Press ENTER to continue.")

def server_disk_check() -> None:
    print_starsReset()
    print("* Here are all of your mount points: ")
    for part in disk_partitions():
        print(part)
    print_stars()
    total, used, free = shutil.disk_usage(easy_env_fra.our_disk_mount)
    total = str(converted_unit(total))
    used = str(converted_unit(used))
    print("Disk: " + str(easy_env_fra.our_disk_mount) + "\n" + free_space_check(easy_env_fra.our_disk_mount) + " Free\n" + used + " Used\n" + total + " Total")
    print_stars()
    input("* Disk check complete, press ENTER to return to the main menu. ")

def coming_soon() -> None:
    print_stars()
    print(f'* Coming soon!')
    print_stars()
    input("* Press ENTER to continue.")

def menu_topper() -> None:
    Load1, Load5, Load15 = os.getloadavg()
    # get sign pct
    # get balances
    # get other validator data
    os.system("clear")
    print_stars()
    print(f'{Style.RESET_ALL}* {Fore.GREEN}validator-toolbox for Findora FRA Validators by Easy Node   v{easy_env_fra.easy_version}{Style.RESET_ALL}   https://easynode.pro *')
    print_stars()
    print(f'* Server Hostname & IP:             {easy_env_fra.server_host_name}{Style.RESET_ALL} - {Fore.YELLOW}{easy_env_fra.our_external_ip}{Style.RESET_ALL}')
    print(f'* Current disk space free: {Fore.CYAN}{free_space_check(easy_env_fra.our_disk_mount): >6}{Style.RESET_ALL}\n')
    print_stars()
    print(f"* CPU Load Averages: {round(Load1, 2)} over 1 min, {round(Load5, 2)} over 5 min, {round(Load15, 2)} over 15 min")
    print_stars()
    return
    
def run_findora_menu() -> None:
    menu_options = {
        1: refresh_stats,
        2: check_balance_menu,
        3: coming_soon,
        4: coming_soon,
        5: coming_soon,
        6: coming_soon,
        7: coming_soon,
        8: coming_soon,
        9: coming_soon,
        10: coming_soon,
        11: coming_soon,
        12: coming_soon,
        13: server_disk_check,
        14: coming_soon,
        15: all_sys_info,
        999: menu_reboot_server,
    }
    while True:
        os.system("clear")
        menu_topper()
        menu_findora()
        try:
            option = int(input("* Enter your option: "))
        except ValueError:
            menu_error()
            menu_findora()
        if option == 0:
            return finish_node()
        os.system("clear")
        menu_options[option]()