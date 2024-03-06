import argparse
import json
import base64
from typing import Tuple, List, Union
from pathlib import Path


def read_bencoded_file(bencoded_file_path: str) -> Tuple[bytes, int]:
    """Open up and read a bencoded file. Return the data."""
    bencoded_file_path = Path(bencoded_file_path).resolve()
    with open(bencoded_file_path, "rb") as bencoded_file:
        return bencoded_file.read(), bencoded_file_path.stat().st_size


def parse_integer(data: bytes, start_index: int) -> Tuple[int, int]:
    """Parse a bencoded integer. Return a tuple containing the parsed integer and the current byte position (index)."""
    end_index = start_index + 1
    while data[end_index] != ord("e"):
        end_index += 1
    integer_value = int(data[start_index + 1 : end_index])
    return integer_value, end_index + 1


def parse_string(data: bytes, start_index: int) -> Tuple[bytes, int]:
    """Parse a bencoded string. Return a tuple containing the parsed string and the current byte position (index)."""
    colon_index = data.find(b":", start_index)
    length = int(data[start_index:colon_index].decode("utf-8"))
    string_value = data[colon_index + 1 : colon_index + 1 + length]
    return string_value, colon_index + 1 + length


def parse_list(
    data: bytes, start_index: int
) -> Tuple[List[Union[int, str, list, dict]], int]:
    """Parse a bencoded list. Return a tuple containing the parsed list and the current byte position (index)."""
    result_list = []
    index = start_index + 1
    while data[index] != ord("e"):
        value, index = parse_bencoded(data, index)
        result_list.append(value)
    return result_list, index + 1


def parse_dictionary(data: bytes, start_index: int) -> Tuple[dict, int]:
    result_dict = {}
    index = start_index + 1
    while data[index] != ord("e"):
        key, index = parse_string(data, index)
        value, index = parse_bencoded(data, index)

        # Decode the key assuming it's utf-8 encoded
        key_str = key.decode("utf-8")

        # Special handling for "pieces" key
        if key_str == "pieces" and isinstance(value, bytes):
            result_dict[key_str] = base64.b64encode(value).decode("utf-8")
        else:
            result_dict[key_str] = value

    return result_dict, index + 1


def parse_bencoded(
    data: bytes, start_index: int
) -> Tuple[Union[int, str, list, dict], int]:
    """Parse a bencoded data. Return a tuple containing the parsed data and the current byte position (index)."""
    if data[start_index] == ord("i"):
        return parse_integer(data, start_index)
    elif data[start_index] == ord("l"):
        return parse_list(data, start_index)
    elif data[start_index] == ord("d"):
        return parse_dictionary(data, start_index)
    elif data[start_index : start_index + 1].isdigit():
        return parse_string(data, start_index)


def convert_bytes_to_strings(data):
    if isinstance(data, bytes):
        return data.decode("utf-8")
    elif isinstance(data, list):
        return [convert_bytes_to_strings(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_bytes_to_strings(value) for key, value in data.items()}
    else:
        return data


def write_json(output_file_path: str, parsed_bencoded_data: dict) -> bool:
    try:
        output_file_path = Path(output_file_path).resolve()

        with open(output_file_path, "w") as json_file:
            json.dump(parsed_bencoded_data, json_file, indent=4, sort_keys=True)
        return True
    except Exception as e:
        print(f"Error writing JSON file: {e}")
        return False
