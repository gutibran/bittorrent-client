import sys
from pathlib import Path
from typing import BinaryIO, Tuple

"""Rewrite and refactor this shit tommorow."""

def parse_integer(bencoded_file: BinaryIO, byte_index: int) -> tuple[int, int]:
    """Parse a bencoded integer."""
    bencoded_integer = ""
    current_byte = bencoded_file.read(1)
    current_character = current_byte.decode("utf-8")
    while current_character.isdigit() and current_character != "e":
        current_byte = bencoded_file.read(1)
        byte_index += 1
        current_character = current_byte.decode("utf-8")
        bencoded_integer += current_character
    return (int(bencoded_integer), byte_index)


def parse_dictionary(bencoded_file: BinaryIO, byte_index: int) -> Tuple[dict, int]:
    """Parse a bencoded dictionary."""
    bencoded_dict = {}
    current_byte = bencoded_file.read(1)
    byte_index += 1

    while current_byte.decode("utf-8") != "e":
        try:
            character = current_byte.decode("utf-8")
        except UnicodeDecodeError:
            character = current_byte.hex()

        # Parse the key
        if character.isdigit():
            parsed_key, byte_index = parse_string(bencoded_file, byte_index)
        else:
            raise ValueError("Invalid key format in dictionary")

        # Parse the value based on the next character
        current_byte = bencoded_file.read(1)
        byte_index += 1
        try:
            value_character = current_byte.decode("utf-8")
        except UnicodeDecodeError:
            value_character = current_byte.hex()

        if value_character == "i":
            # Parse an integer
            parsed_value, byte_index = parse_integer(bencoded_file, byte_index)
        elif value_character == "d":
            # Parse a nested dictionary
            parsed_value, byte_index = parse_dictionary(bencoded_file, byte_index)
        elif value_character == "l":
            # Parse a nested list
            parsed_value, byte_index = parse_list(bencoded_file, byte_index)
        elif value_character.isdigit():
            # Parse a string
            parsed_value, byte_index = parse_string(bencoded_file, byte_index)
        else:
            raise ValueError(f"Invalid value format in dictionary: {value_character}")

        # Add the key-value pair to the dictionary
        bencoded_dict[parsed_key] = parsed_value

        # Read the next character (either a key or 'e' to close the dictionary)
        current_byte = bencoded_file.read(1)
        byte_index += 1

    return (bencoded_dict, byte_index)


def parse_list(bencoded_file: BinaryIO, byte_index: int) -> Tuple[list, int]:
    """Parse a bencoded list."""
    bencoded_list = []
    current_byte = bencoded_file.read(1)
    byte_index += 1

    while current_byte.decode("utf-8") != "e":
        try:
            current_character = current_byte.decode("utf-8")
        except UnicodeDecodeError:
            current_character = current_byte.hex()

        if current_character == "i":
            # Parse an integer
            parsed_integer, byte_index = parse_integer(bencoded_file, byte_index)
            bencoded_list.append(parsed_integer)
        elif current_character == "d":
            # Parse a dictionary
            parsed_dict, byte_index = parse_dictionary(bencoded_file, byte_index)
            bencoded_list.append(parsed_dict)
        elif current_character == "l":
            # Parse a nested list
            parsed_nested_list, byte_index = parse_list(bencoded_file, byte_index)
            bencoded_list.append(parsed_nested_list)
        elif current_character.isdigit():
            # Parse a string
            parsed_string, byte_index = parse_string(bencoded_file, byte_index)
            bencoded_list.append(parsed_string)

        # Read the next character
        current_byte = bencoded_file.read(1)
        byte_index += 1  # Add this line to update byte_index inside the loop

    return (bencoded_list, byte_index)

    return (bencoded_list, byte_index)


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
    # the current character is : at this point
    return (int(bencoded_string_length), byte_index)


def parse_string_characters(
    bencoded_file: BinaryIO, byte_index: int, string_length: int
) -> tuple[str, int]:
    """Concatenate characters to form a string of n characters."""
    bencoded_string = ""
    for _ in range(string_length):
        current_byte = bencoded_file.read(1)
        byte_index += 1
        current_character = current_byte.decode("utf-8")
        bencoded_string += current_character
    return (bencoded_string, byte_index)


def parse_string(bencoded_file: BinaryIO, byte_index: int) -> Tuple[str, str, int]:
    """Parse a single bencoded string. Returns the index of the end of the string."""
    bencoded_string_key_length, byte_index = parse_string_length(
        bencoded_file, byte_index
    )
    bencoded_string_key, byte_index = parse_string_characters(
        bencoded_file, byte_index, bencoded_string_key_length
    )
    bencoded_string_value_length, byte_index = parse_string_length(
        bencoded_file, byte_index
    )
    bencoded_string_value, byte_index = parse_string_characters(
        bencoded_file, byte_index, bencoded_string_value_length
    )
    return (bencoded_string_key, bencoded_string_value, byte_index)


def parse_bencoded_file(bencoded_file: str):
    """Parse a bencoded file."""
    bencoded_file_path = Path(bencoded_file).resolve()
    bencoded_file_size = bencoded_file_path.stat().st_size
    with open(bencoded_file_path, "rb") as bencoded_file:
        current_byte_index = bencoded_file.tell()
        current_byte = bencoded_file.read(1)
        parsed_bencoded_data = {}
        while current_byte_index != bencoded_file_size:
            try:
                character = current_byte.decode("utf-8")
            except UnicodeDecodeError:
                character = current_byte.hex()

            # parse teh bencode file
            pass
