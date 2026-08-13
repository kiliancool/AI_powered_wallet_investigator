from api import (
    API_KEY,
    get_user_input,
    get_wallet_transfers
)

from transfer_parser import parse_transfers
from formatter import format_transfers


def main():
    wallet_address = get_user_input()

    wallet_data = get_wallet_transfers(
        API_KEY,
        wallet_address
    )

    all_formatted_transfers = []

    for direction, response in wallet_data.items():

        transfers = response.get("result", {}).get("transfers", [])

        parsed_transfers = parse_transfers(transfers)

        formatted_transfers = format_transfers(
            parsed_transfers
        )

        for transfer in formatted_transfers:
            transfer["direction"] = direction

        all_formatted_transfers.extend(
            formatted_transfers
        )

    print("\nWallet transfers:\n")

    for transfer in all_formatted_transfers:
        print(transfer)


if __name__ == "__main__":
    main()
