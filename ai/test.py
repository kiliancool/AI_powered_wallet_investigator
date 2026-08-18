import os
import requests

from dotenv import load_dotenv

load_dotenv()

ALCHEMY_API_KEY = os.getenv("API_KEY")

def test_environment():
    print("Testing environment variables...")

    if not ALCHEMY_API_KEY:
        raise ValueError("ALCHEMY_API_KEY is missing")

    print("✓ Environment variables loaded")



def test_wallet_address():
    print("\nTesting wallet address validation...")

    wallet_address = "0x0000000000000000000000000000000000000000"

    if not wallet_address.startswith("0x"):
        raise ValueError("Invalid address prefix")

    if len(wallet_address) != 42:
        raise ValueError("Invalid Ethereum address length")

    try:
        int(wallet_address[2:], 16)
    except ValueError:
        raise ValueError("Address contains non-hex characters")

    print("✓ Wallet address validation passed")


def main():
    print("=== Blockchain Investigator Tests ===")

    test_environment()
    test_wallet_address()

    print("\n✓ All tests passed!")


if __name__ == "__main__":
    main()
