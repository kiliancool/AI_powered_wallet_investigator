"""
Decyphra
AI-powered blockchain wallet investigation prototype.

Current stage:
TRL 3 — Experimental proof of concept.

This implementation demonstrates the feasibility of combining
blockchain activity data, structured parsing, and an AI reasoning
layer to produce human-readable wallet investigations.
"""



import json
from api import (
    API_KEY,
    get_user_input,
    get_wallet_transfers
)

from transfer_parser import parse_transfers
from formatter import format_transfers
from ai.engine import conversation, cli_loop, clean_text



def welcome_message():
    print("------------------------------------")
    print("Welcome to Decyphra ⛓️  Intelligence")
    print("------------------------------------\n")
welcome_message() 



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

    print("\nGathering onchain intelligence..\n")

    print("Decyphra is here to help you decipher onchain intelligence. What do you need?\n")


    if wallet_address:
        conversation.append({"role":"user",
                            "content": clean_text(
        "WALLET INVESTIGATION EVIDENCE\n\n"
        +
        json.dumps(all_formatted_transfers, indent=2, default=str)
    )
    })


# receives structured wallet evidence and generates
# natural-language investigative analysis.


if __name__ == "__main__":
    main()
    cli_loop()

