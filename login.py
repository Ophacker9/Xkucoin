import requests
import urllib.parse

from smart_airdrop_claimer import base

import headers

def parse_and_decode_params(data):
    # Parse the query string into a dictionary
    params = dict(urllib.parse.parse_qsl(data))

    # Return the decoded values with other params
    return {
        "decoded_user": params.get("user", ""),
        "decoded_start_param": params.get("start_param", ""),
        "hash": params.get("hash", ""),
        "auth_date": params.get("auth_date", ""),
        "chat_type": params.get("chat_type", ""),
        "chat_instance": params.get("chat_instance", ""),
    }


def get_cookie(data, proxies=None):
    url = "https://www.kucoin.com/_api/xkucoin/platform-telebot/game/login?lang=en_US"
    decoded_data = parse_and_decode_params(data)
    payload = {
        "inviterUserId": "5914982564",  # This seems static; verify if it needs to be dynamic
        "extInfo": {
            "hash": decoded_data["hash"],
            "auth_date": decoded_data["auth_date"],
            "via": "miniApp",
            "user": decoded_data["decoded_user"],
            "chat_type": decoded_data["chat_type"],
            "chat_instance": decoded_data["chat_instance"],
            "start_param": decoded_data["decoded_start_param"],
        },
    }

    try:
        session = requests.Session()
        response = session.post(
            url=url,
            headers=headers(),  # Ensuring the headers() function is called correctly
            json=payload,  # Ensure JSON format is the correct one for the API
            proxies=proxies,
            timeout=20,
        )

        # Check if response is successful and contains cookies
        if response.status_code == 200:
            cookie = "; ".join(
                [f"{cookie.name}={cookie.value}" for cookie in session.cookies]
            )
            return cookie
        else:
            base.log(f"Failed to retrieve cookie, status code: {response.status_code}")
            return None

    except Exception as e:
        base.log(f"Error in get_cookie: {e}")
        return None
