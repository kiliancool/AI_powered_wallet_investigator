from parser import (
    hex_to_int,
    to_decimal,
    raw_to_decimal,
    parse_timestamp
)


def format_transfer(transfer):
    raw_block_number = transfer.get("block_number")
    raw_unique_id = transfer.get("unique_id")
    raw_transaction_hash = transfer.get("transaction_hash")
    raw_from_address = transfer.get("from_address")
    raw_to_address = transfer.get("to_address")
    raw_value = transfer.get("value")

    raw_erc721_token_id = transfer.get("erc721_token_id")
    raw_erc1155_metadata = transfer.get("erc1155_metadata")

    raw_token_id = transfer.get("token_id")
    raw_asset = transfer.get("asset")
    raw_category = transfer.get("category")

    raw_contract_value = transfer.get("contract_value")
    raw_contract_address = transfer.get("contract_address")
    raw_contract_decimals = transfer.get("contract_decimals")

    raw_block_timestamp = transfer.get("block_timestamp")

    block_number = hex_to_int(raw_block_number)

    unique_id = raw_unique_id
    tx_hash = raw_transaction_hash

    from_address = raw_from_address
    to_address = raw_to_address

    value = to_decimal(raw_value)

    erc721_token_id = raw_erc721_token_id
    erc1155_metadata = raw_erc1155_metadata

    token_id = raw_token_id
    asset = raw_asset
    category = raw_category

    contract_decimals = hex_to_int(raw_contract_decimals)

    int_contract_value = hex_to_int(raw_contract_value)

    contract_value = raw_to_decimal(
        int_contract_value,
        contract_decimals
    )

    contract_address = raw_contract_address

    timestamp = parse_timestamp(raw_block_timestamp)

    if timestamp is not None:
        formatted_time = timestamp.strftime(
            "%d %B %Y, %I:%M:%S %p UTC"
        )
    else:
        formatted_time = None

    return {
        "Block Number": block_number,
        "unique_id": unique_id,
        "tx_hash": tx_hash,

        "from_address": from_address,
        "to_address": to_address,

        "value": value,

        "erc721_token_id": erc721_token_id,
        "erc1155_metadata": erc1155_metadata,

        "token_id": token_id,
        "asset": asset,
        "category": category,

        "contract_value": contract_value,
        "contract_address": contract_address,
        "contract_decimals": contract_decimals,

        "block_timestamp": formatted_time
    }


def format_transfers(parsed_transfers):
    formatted_transfers = []

    number_of_transactions = len(parsed_transfers)

    for transfer in parsed_transfers:
        transfer_data = format_transfer(transfer)

        transfer_data["Number of transactions"] = number_of_transactions

        formatted_transfers.append(transfer_data)

    return formatted_transfers
