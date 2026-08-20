import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

TIMEOUT = 10

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def _post_with_retries(url, json_payload, max_attempts=3, backoff=1):
    """Simple requests.post wrapper with retry/backoff."""
    attempt = 0
    while attempt < max_attempts:
        try:
            resp = requests.post(url=url, timeout=TIMEOUT, headers=HEADERS, json=json_payload)
            resp.raise_for_status()
            return resp
        except requests.RequestException as e:
            attempt += 1
            if attempt >= max_attempts:
                raise
            sleep_time = backoff * (2 ** (attempt - 1))
            time.sleep(sleep_time)


def get_user_input():
    wallet_address = input("\nEnter a wallet address: ").strip()
    return wallet_address


def _fetch_asset_transfers(url, params, max_pages=5, max_transfers=500):
    """Fetch asset transfers using Alchemy's alchemy_getAssetTransfers JSON-RPC.

    Handles pagination via `pageKey` in the result. Returns a dict with:
      - transfers: accumulated list
      - pages_fetched: number of pages fetched
      - partial: True if results were truncated by max_pages/max_transfers
    """
    transfers = []
    page_key = None
    pages = 0

    while True:
        pages += 1
        request_params = dict(params)
        if page_key:
            request_params["pageKey"] = page_key

        payload = {
            "jsonrpc": "2.0",
            "id": pages,
            "method": "alchemy_getAssetTransfers",
            "params": [request_params]
        }

        resp = _post_with_retries(url, payload)
        data = resp.json()

        # Basic validation
        result = data.get("result") or {}
        page_transfers = result.get("transfers", [])

        transfers.extend(page_transfers)

        page_key = result.get("pageKey")

        # Stop conditions
        if not page_key:
            break
        if pages >= max_pages:
            break
        if len(transfers) >= max_transfers:
            break

    partial = False
    if page_key or len(transfers) >= max_transfers or pages >= max_pages:
        partial = True

    return {
        "transfers": transfers,
        "pages_fetched": pages,
        "partial": partial
    }


def get_wallet_transfers(api_key, wallet_address, max_pages=5, max_transfers=500):
    if not api_key:
        raise ValueError("API_KEY is missing from the environment.")

    url = f"https://eth-mainnet.g.alchemy.com/v2/{api_key}"

    base_params = {
        "fromBlock": "0x0",
        "toBlock": "latest",
        "excludeZeroValue": True,
        "withMetadata": True,
        "category": [
            "external",
            "erc20",
            "erc721",
            "erc1155"
        ]
    }

    incoming_params = {
        **base_params,
        "toAddress": wallet_address
    }

    outgoing_params = {
        **base_params,
        "fromAddress": wallet_address
    }

    incoming_result = _fetch_asset_transfers(url, incoming_params, max_pages=max_pages, max_transfers=max_transfers)
    outgoing_result = _fetch_asset_transfers(url, outgoing_params, max_pages=max_pages, max_transfers=max_transfers)

    # Wrap results to match previous return shape but include metadata about pagination
    return {
        "incoming": {"result": {"transfers": incoming_result["transfers"]}, "meta": {"pages_fetched": incoming_result["pages_fetched"], "partial": incoming_result["partial"]}},
        "outgoing": {"result": {"transfers": outgoing_result["transfers"]}, "meta": {"pages_fetched": outgoing_result["pages_fetched"], "partial": outgoing_result["partial"]}}
    }


def get_balance(api_key, wallet_address):
    if not api_key:
        raise ValueError("API_KEY is missing from the environment.")

    url = f"https://api.g.alchemy.com/data/v1/{api_key}/assets/tokens/by-address"

    payload = {
        "addresses": [
            {
                "address": wallet_address,
                "networks": ["eth-mainnet"]
            }
        ],
        "withMetadata": True,
        "withPrices": True,
        "includeNativeTokens": True,
        "includeErc20Tokens": True
    }

    response = _post_with_retries(url, payload)

    data = response.json()

    return data
