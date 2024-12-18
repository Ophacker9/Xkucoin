import requests
import random
import time

from smart_airdrop_claimer import base

import headers
import get_info

def try_tap(cookie, molecule, proxies=None):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/gold/increase?lang=en_US"
    increment = random.randint(10, 20)  # Updated range: 10 to 20 taps
    form_data = {"increment": str(increment), "molecule": str(molecule)}
    base.log(f"{base.yellow}Sending {increment} taps...")

    try:
        response = requests.post(
            url=url,
            headers=headers(cookie=cookie),
            data=form_data,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()

        return data
    except:
        return None


def process_tap(cookie, molecule, proxies=None):
    while True:
        tap_data = try_tap(cookie=cookie, molecule=molecule, proxies=proxies)
        if tap_data and tap_data.get("success"):
            get_info(cookie=cookie, proxies=proxies)
            time.sleep(random.uniform(0.05, 0.1))  # Random delay: 10 to 20 taps per second
        else:
            msg = tap_data["msg"] if tap_data else "Unknown error"
            base.log(f"{base.white}Auto Tap: {base.red}{msg}")
            break
