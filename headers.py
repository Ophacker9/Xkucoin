def headers(cookie=None):
    try:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.kucoin.com",
            "Referer": "https://www.kucoin.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

        if cookie:
            headers["Cookie"] = cookie

        return headers
    except Exception as e:
        raise ValueError(f"Error creating headers: {e}")
