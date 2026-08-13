import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

TIMEOUT = 10

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def get_user_input():
    wallet_address = input("\nEnter a wallet address: ").strip()
    return wallet_address


def get_wallet_transfers(api_key, wallet_address):
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

    incoming_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "alchemy_getAssetTransfers",
        "params": [incoming_params]
    }

    outgoing_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "alchemy_getAssetTransfers",
        "params": [outgoing_params]
    }

    incoming_response = requests.post(
        url=url,
        timeout=TIMEOUT,
        headers=HEADERS,
        json=incoming_payload
    )

    outgoing_response = requests.post(
        url=url,
        timeout=TIMEOUT,
        headers=HEADERS,
        json=outgoing_payload
    )

    incoming_response.raise_for_status()
    outgoing_response.raise_for_status()

    incoming_data = incoming_response.json()
    outgoing_data = outgoing_response.json()

    if "error" in incoming_data:
        raise RuntimeError(incoming_data["error"])

    if "error" in outgoing_data:
        raise RuntimeError(outgoing_data["error"])

    return {
        "incoming": incoming_data,
        "outgoing": outgoing_data
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

    response = requests.post(
        url=url,
        timeout=TIMEOUT,
        headers=HEADERS,
        json=payload
    )

    response.raise_for_status()

    data = response.json()

    return data
