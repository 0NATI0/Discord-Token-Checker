import requests
from time import time
from colorama import Fore
from datetime import datetime
from time import sleep
import threading
import json
import random
from pystyle import *
import os


author = "al1ce0."
join_for_more = "discord.gg/g3n"


config = json.load(open('./config.json', 'r', encoding='utf-8'))
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
xtrack = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InBsLVBMIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNC4wLjU3MzUuMTk5IFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMTQuMC41NzM1LjE5OSIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiIiwicmVmZXJyaW5nX2RvbWFpbiI6IiIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyMTk4MzksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9" # this was made by al1ce0. discord.gg/g3n
total, unlocked, locked = 0, 0, 0
time_start = None


class Log:
    def Success(text, highlighted):
        time_now = datetime.fromtimestamp(time()).strftime('%H:%M:%S')
        if not highlighted:
            print(Fore.LIGHTBLACK_EX + time_now + Fore.RESET + f" {Fore.LIGHTWHITE_EX}({Fore.GREEN}${Fore.LIGHTWHITE_EX}) " + text + Fore.RESET)
        else:
            print(Fore.LIGHTBLACK_EX + time_now + Fore.RESET + f" {Fore.LIGHTWHITE_EX}({Fore.GREEN}${Fore.LIGHTWHITE_EX}) " + text + Fore.LIGHTGREEN_EX + " " + highlighted + Fore.RESET)

    def Error(text, highlighted):
        time_now = datetime.fromtimestamp(time()).strftime('%H:%M:%S')
        if not highlighted:
            print(Fore.LIGHTBLACK_EX + time_now + Fore.RESET + f" {Fore.LIGHTWHITE_EX}({Fore.RED}!{Fore.LIGHTWHITE_EX}) " + text + Fore.RESET)
        else:
            print(Fore.LIGHTBLACK_EX + time_now + Fore.RESET + f" {Fore.LIGHTWHITE_EX}({Fore.RED}!{Fore.LIGHTWHITE_EX}) " + text + Fore.RED + " " + highlighted + Fore.RESET)



class Misc:
    def finger():
        headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'Referer': 'https://discord.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-GPC': '1',
                'User-Agent': useragent,
                'X-Track': xtrack,
        }
        proxies = {"http": f"http://{Misc.proxy()}"} if not config['proxyless'] else None
        fingerprint = requests.get('https://discord.com/api/v9/experiments', headers=headers, proxies=proxies).json()['fingerprint']
        return fingerprint

    def proxy():
        with open('./data/proxies.txt') as f:
            random_line = random.choice(f.readlines()).strip()
            return random_line

def thread_woker(delay):
    while True:
        with open('./data/tokens.txt', 'r') as file:
            lines = file.readlines()

        if lines:
            first_line = lines[0].strip()
            sleep(delay)
            Checker.check_token(first_line)

            with open('./data/tokens.txt', 'w') as file:
                    file.writelines(lines[1:])
        else:
            sleep(0.75)
            Checker.printresult()
            break


class Checker:

    def init():
        global time_start
        time_start = time()
        delay = config['delay']

        thread = threading.Thread(target=thread_woker, args=(delay,))
        thread.start()

    def check_token(token):
        global total, unlocked, locked, time_start

        newheaders = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': token, 'origin': 'https://discord.com',
            'referer': 'https://discord.com/@me',
            'Content-Type': 'application/json',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': useragent,
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-fingerprint': Misc.finger(),
            'x-super-properties': xtrack
            }


        proxies = {"http": f"http://{Misc.proxy()}"} if not config['proxyless'] else None
        r = requests.get("https://discord.com/api/v9/users/@me/affinities/users", headers=newheaders, proxies=proxies)
        if r.status_code == 200:
            Log.Success('Unlocked', token)
            total += 1
            unlocked += 1
            with open("./checked/unlocked.txt", "a") as f:
                f.write(f"{token}\n")
        else:
            Log.Error('Locked', token)
            total += 1
            locked += 1
            with open("./checked/locked.txt", "a") as f:
                f.write(f"{token}\n")

    def printresult():
        print("\n\n\n")
        print(Center.XCenter(f"                                        Total: {Fore.BLUE}{total}{Fore.LIGHTWHITE_EX} | Unlocked: {Fore.GREEN}{unlocked}{Fore.LIGHTWHITE_EX} | Locked: {Fore.RED}{locked}{Fore.LIGHTWHITE_EX} | {Fore.CYAN}{round(time() - time_start, 2)}s{Fore.RESET}"))


os.system('cls')
logo = """
                              ___
     ___.   ___.    /   ___. /   \ , __
   .'   ` .'   `   /  .'   `   _-' |'  `.
   |    | |    |  ,'  |    |    \  |    |
 /  `---|  `---| ,     `---| \___) /    |
    \___/  \___/       \___/

            made by al1ce0.
"""

Write.Print(Center.Center(logo), color=Colors.blue_to_purple, interval=0)
print("\n\n")
sleep(1)
Checker.init()
