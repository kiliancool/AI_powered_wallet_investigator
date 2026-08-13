from decimal import Decimal
from datetime import datetime, timezone


WEI_PER_ETH = Decimal("1000000000000000000")


def hex_to_int(value):
    if value is None:
        return None

    if not isinstance(value, str):
        raise TypeError("hex_to_int() expects a string")

    if not value.startswith(("0x", "0X")):
        raise ValueError(f"Not a hexadecimal value: {value}")

    return int(value, 16)


def to_decimal(value):
    if value is None:
        return None

    return Decimal(str(value))


def wei_to_eth(value):
    if value is None:
        return None

    return Decimal(value) / WEI_PER_ETH


def hex_wei_to_eth(value):
    if value is None:
        return None

    wei_value = hex_to_int(value)

    return wei_to_eth(wei_value)


def raw_to_decimal(value, decimals):
    if value is None or decimals is None:
        return None

    return Decimal(value) / (Decimal(10) ** decimals)


def hex_raw_to_decimal(value, decimals):
    if value is None or decimals is None:
        return None

    raw_value = hex_to_int(value)

    return raw_to_decimal(raw_value, decimals)


def unix_to_datetime(value):
    if value is None:
        return None

    return datetime.fromtimestamp(
        value,
        timezone.utc
    )


def iso_to_datetime(value):
    if value is None:
        return None

    if value.endswith("Z"):
        value = value[:-1] + "+00:00"

    return datetime.fromisoformat(value)


def parse_timestamp(value):
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return unix_to_datetime(value)

    if isinstance(value, str):

        if value.startswith(("0x", "0X")):
            timestamp = hex_to_int(value)
            return unix_to_datetime(timestamp)

        return iso_to_datetime(value)

    raise TypeError(
        f"Unsupported timestamp type: {type(value).__name__}"
    )
