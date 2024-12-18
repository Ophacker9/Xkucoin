import requests
import random
import time
import fake_useragent
from smart_airdrop_claimer import base
from core.headers import headers

# Initialize fake user-agent generator
ua = fake_useragent.UserAgent()

def get_random_user_agent():
    """Get a random user-agent"""
    return ua.random

def get_info(cookie, proxies=None):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/summary?lang=en_US"

    try:
        # Randomize the user-agent to avoid detection
        random_ua = get_random_user_agent()

        # Headers with randomized User-Agent and other anti-ban headers
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.kucoin.com",
            "Referer": "https://www.kucoin.com/",
            "User-Agent": random_ua,
            "Cookie": cookie,
            "Accept-Language": random.choice(["en-US", "en-GB", "fr-FR", "es-ES"])  # Rotate language too
        }

        # Add some randomized delay to mimic human behavior
        delay = random.uniform(2, 5)  # Random sleep between 2 and 5 seconds to avoid rapid requests
        time.sleep(delay)

        response = requests.get(
            url=url,
            headers=headers,
            timeout=20,
        )

        # Checking if the response is successful
        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                available_amount = data["data"].get("availableAmount", "N/A")
                feed_preview = data["data"].get("feedPreview", {})
                molecule = feed_preview.get("molecule", "N/A")

                # Log balance
                base.log(f"{base.green}Balance: {base.white}{available_amount:,}")
                return molecule
            else:
                base.log(f"{base.red}Error: No 'data' in response.")
                return None
        else:
            base.log(f"{base.red}Failed to retrieve data, status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        base.log(f"{base.red}Request error: {str(e)}")
        return None
    except ValueError as e:
        base.log(f"{base.red}JSON decode error: {str(e)}")
        return None
    except Exception as e:
        base.log(f"{base.red}Unexpected error: {str(e)}")
        return None