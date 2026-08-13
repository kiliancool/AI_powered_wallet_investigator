def parse_transfer(transfer):
    raw_contract = transfer.get("rawContract") or {}
    raw_metadata = transfer.get("metadata") or {}

    return {
        "block_number": transfer.get("blockNum"),
        "unique_id": transfer.get("uniqueId"),
        "transaction_hash": transfer.get("hash"),

        "from_address": transfer.get("from"),
        "to_address": transfer.get("to"),

        "value": transfer.get("value"),

        "erc721_token_id": transfer.get("erc721TokenId"),
        "erc1155_metadata": transfer.get("erc1155Metadata"),

        "token_id": transfer.get("tokenId"),
        "asset": transfer.get("asset"),
        "category": transfer.get("category"),

        "contract_value": raw_contract.get("value"),
        "contract_address": raw_contract.get("address"),
        "contract_decimals": raw_contract.get("decimal"),

        "block_timestamp": raw_metadata.get("blockTimestamp")
    }


def parse_transfers(wallet_transfers):
    parsed_transfers = []

    for transfer in wallet_transfers:
        parsed_transfer = parse_transfer(transfer)
        parsed_transfers.append(parsed_transfer)

    return parsed_transfers
