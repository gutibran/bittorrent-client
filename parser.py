import argparse
import pathlib
import sys
import json

class Parser:
    def __init__(self, input_file_path=None):
        self.input_file = None
        self.input_file_length_in_bytes = 0
        self.parsed_output = None

        if input_file_path:
            with open(input_file_path, "rb") as input_file:
                self.input_file = input_file.read()
                self.input_file_length_in_bytes = len(self.input_file)
    

    def parse_string(self, index):
        """Parse a bencoded string."""
        integer_string = ""
        current_byte = self.input_file[index]
        while chr(current_byte) != ":":
            integer_string += chr(current_byte)
            index += 1
            current_byte = self.input_file[index]
        index += 1
        integer_string = int(integer_string)
        iterator = 0
        string = ""
        while iterator < integer_string:
            string += chr(self.input_file[index])
            index += 1
            iterator += 1
        return (string, index)
    

    def parse_integer(self, index):
        """Parse bencoded integer."""
        integer_string = ""
        current_byte = self.input_file[index]
        while chr(current_byte) != "e":
            integer_string += chr(current_byte)
            index += 1
            current_byte = self.input_file[index]
        return (int(integer_string), index + 1)
    

    def parse_list(self, index, list_=[]):
        parsed_list = []
        current_byte = self.input_file[index]
        while chr(current_byte) != "e" or index < self.input_file_length_in_bytes:
            if chr(current_byte).isnumeric():
                parsed_string, index = self.parse_string(index)
                parsed_list.append(parsed_string)
            elif chr(current_byte) == "i":
                parsed_integer, index = self.parse_integer(index + 1)
                parsed_list.append(parsed_integer)
            elif chr(current_byte) == "l":
                parsed_list, index = self.parse_list(index + 1)
                parsed_list.append(parsed_list)
            elif chr(current_byte) == "d":
                parsed_dictionary, index = self.parse_dictionary()
                parsed_list.append(parsed_dictionary)
        return (parsed_list, index + 1)


    def parse_dictionary(self, index):
        pass


    def parse(self):
        """Parse a bencoded file"""
        metainfo = {}
        index = 0
        while index < self.input_file_length_in_bytes:
            current_byte = self.input_file[index]
            if chr(current_byte).isnumeric():
                parsed_string, index = self.parse_string(index)
            elif chr(current_byte) == "i":
                parsed_integer, index = self.parse_integer(index + 1)
            elif chr(current_byte) == "l":
                print("detected list")
                parsed_list, index = self.parse_list(index + 1)
            elif chr(current_byte) == "d":
                parsed_dictionary, index = self.parse_dictionary()
        return metainfo
    

def main():
    parser = Parser("./list.torrent")
    parsed_file = parser.parse()
    print(parsed_file)

if __name__ == "__main__":
    main()