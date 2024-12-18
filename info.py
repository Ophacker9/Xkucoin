import requests

from smart_airdrop_claimer import base

import headers

def get_info(cookie, proxies=None):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/summary?lang=en_US"

    try:
        response = requests.get(
            url=url,
            headers=headers(cookie=cookie),
            proxies=proxies,
            timeout=20,
        )
        response.raise_for_status()  # Will raise HTTPError for bad responses (4xx, 5xx)
        data = response.json()

        # Check if data structure is as expected and exists
        if data.get("data"):
            available_amount = data["data"].get("availableAmount", "N/A")
            feed_preview = data["data"].get("feedPreview", {})
            molecule = feed_preview.get("molecule", "N/A")

            # Log balance if available
            base.log(f"{base.green}Balance: {base.white}{available_amount:,}")

            return molecule
        else:
            base.log(f"{base.red}Error: No 'data' in response.")
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
