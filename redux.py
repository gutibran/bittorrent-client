import argparse
from typing import BinaryIO, Tuple
from pathlib import Path

def parse_integer() -> Tuple[int, int]: 
    """Parse a bencoded integer."""
    pass

def read_bencoded_file(bencoded_file_path: str) -> Tuple[BinaryIO, int]:
    bencoded_file_path = Path(bencoded_file_path).resolve()
    bencoded_file_size = bencoded_file_path.stat().st_size 
    with open(bencoded_file_path, "rb") as bencoded_file:
        return (bencoded_file, bencoded_file_size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="viewtorrentfile",
        description="View the metadata of a bencoded torrent (metainfo) file.")
    parser.add_argument("-f", "--file-path", type=str, help="The path to the bencoded torrent (metainfo) file.")
    parser.add_argument("-c", "--chunk-size", type=int, help="The chunk size to read data from the file.")
    args = parser.parse_args()
    chunk_size = args.chunk_size
    bencoded_file, bencoded_file_size = read_bencoded_file(args.file_path)
    for i in range(bencoded_file_size):
        current_byte_index = bencoded_file.tell()
        currnet_byte 