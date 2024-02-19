import sys
from pathlib import Path
from typing import BinaryIO, Tuple

def parse_integer(bencoded_file: BinaryIO, byte_index: int) -> Tuple[int, int]:
    bencoded_integer = ""
    current_byte = bencoded_file.read(1)
    current_character = current_byte.decode("utf-8")
    while current_character.isdigit() and current_character != "e":
        current_byte = bencoded_file.read(1)
        byte_index += 1
        current_character = current_byte.decode("utf-8")
        bencoded_integer += current_character
    return int(bencoded_integer), byte_index

def parse_dictionary(bencoded_file: BinaryIO, byte_index: int) -> Tuple[dict, int]:
    bencoded_dict = {}
    current_byte = bencoded_file.read(1)
    byte_index += 1

    while current_byte.decode("utf-8") != "e":
        try:
            character = current_byte.decode("utf-8")
        except UnicodeDecodeError:
            character = current_byte.hex()

        if character.isdigit():
            print("ok")
            parsed_key, byte_index = parse_string(bencoded_file, byte_index)
        else:
            raise ValueError("Invalid key format in dictionary")

        current_byte = bencoded_file.read(1)
        byte_index += 1
        try:
            value_character = current_byte.decode("utf-8")
        except UnicodeDecodeError:
            value_character = current_byte.hex()

        if value_character in ('i', 'd', 'l') or value_character.isdigit():
            # Use a dispatch dictionary to call the appropriate parsing function
            dispatch = {'i': parse_integer, 'd': parse_dictionary, 'l': parse_list, '0': parse_string}
            parsed_value, byte_index = dispatch[value_character](bencoded_file, byte_index)
        else:
            raise ValueError(f"Invalid value format in dictionary: {value_character}")

        bencoded_dict[parsed_key] = parsed_value

        current_byte = bencoded_file.read(1)
        byte_index += 1

    return bencoded_dict, byte_index

def parse_list(bencoded_file: BinaryIO, byte_index: int) -> Tuple[list, int]:
    bencoded_list = []
    current_byte = bencoded_file.read(1)
    byte_index += 1

    while current_byte.decode("utf-8") != "e":
        try:
            current_character = current_byte.decode("utf-8")
        except UnicodeDecodeError:
            current_character = current_byte.hex()

        if current_character in ('i', 'd', 'l') or current_character.isdigit():
            # Use a dispatch dictionary to call the appropriate parsing function
            dispatch = {'i': parse_integer, 'd': parse_dictionary, 'l': parse_list, '0': parse_string}
            parsed_item, byte_index = dispatch[current_character](bencoded_file, byte_index)
            bencoded_list.append(parsed_item)
        else:
            raise ValueError(f"Invalid character in list: {current_character}")

        current_byte = bencoded_file.read(1)
        byte_index += 1

    return bencoded_list, byte_index

def parse_string_length(bencoded_file: BinaryIO, byte_index: int) -> tuple[int, int]:
    """Find the length of a bencoded string."""
    bencoded_string_length = ""
    current_byte = bencoded_file.read(1)
    byte_index += 1
    current_character = current_byte.decode("utf-8")
    while current_character.isdigit() and current_character != ":":
        bencoded_string_length += current_character
        current_byte = bencoded_file.read(1)
        byte_index += 1
        current_character = current_byte.decode("utf-8")
        print(current_character)

    if not bencoded_string_length.isdigit():
        raise ValueError("Invalid bencoded string length")

    # the current character is ':' at this point
    return (int(bencoded_string_length), byte_index)


def parse_string(bencoded_file: BinaryIO, byte_index: int) -> Tuple[str, int]:
    bencoded_string_length, byte_index = parse_string_length(bencoded_file, byte_index)
    print(bencoded_string_length)
    bencoded_string = bencoded_file.read(bencoded_string_length).decode("utf-8")
    byte_index += bencoded_string_length
    return bencoded_string, byte_index

def parse_bencoded_file(bencoded_file: str):
    bencoded_file_path = Path(bencoded_file).resolve()
    bencoded_file_size = bencoded_file_path.stat().st_size

    with open(bencoded_file_path, "rb") as bencoded_file:
        current_byte_index = bencoded_file.tell()
        current_byte = bencoded_file.read(1)
        parsed_bencoded_data = []

        while current_byte_index != bencoded_file_size:
            try:
                character = current_byte.decode("utf-8")
            except UnicodeDecodeError:
                character = current_byte.hex()

            print(character)

            if character in ('i', 'd', 'l') or character.isdigit():
                dispatch = {'i': parse_integer, 'd': parse_dictionary, 'l': parse_list, '0': parse_string}
                parsed_data, current_byte_index = dispatch[character](bencoded_file, current_byte_index)
                parsed_bencoded_data.append(parsed_data)
                print(parsed_bencoded_data)
            else:
                raise ValueError(f"Unexpected character: {character}")

            current_byte = bencoded_file.read(1)

    return parsed_bencoded_data

torrent_file_path = "debian-12.5.0-amd64-netinst.iso.torrent"
print(parse_bencoded_file(torrent_file_path))