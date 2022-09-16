import base64
import binascii
from string import ascii_letters, digits
from typing import Tuple

from .util_binary import decode_integer, encode_integer, bin_header, STYPE

BYTE_DELIMIT = ord(b":")
B64CONTENT = set((ascii_letters + digits + "+/=").encode("ascii"))


def parse_byteseq(data: bytes) -> Tuple[int, bytes]:
    bytes_consumed = 1
    try:
        end_delimit = data[bytes_consumed:].index(BYTE_DELIMIT)
    except ValueError as why:
        raise ValueError("Binary Sequence didn't contain ending ':'") from why
    b64_content = data[bytes_consumed : bytes_consumed + end_delimit]
    bytes_consumed += end_delimit + 1
    if not all(c in B64CONTENT for c in b64_content):
        raise ValueError("Binary Sequence contained disallowed character")
    try:
        binary_content = base64.standard_b64decode(b64_content)
    except binascii.Error as why:
        raise ValueError("Binary Sequence failed to decode") from why
    return bytes_consumed, binary_content


def ser_byteseq(byteseq: bytes) -> str:
    return f":{base64.standard_b64encode(byteseq).decode('ascii')}:"


def bin_parse_byteseq(data: bytearray) -> Tuple[int, bytes]:
    cursor = 1  # header
    bytes_consumed, length = decode_integer(data[cursor:])
    cursor += bytes_consumed
    end = cursor + length
    return end, bytes(data[cursor:end])


def bin_ser_byteseq(value: bytes, parameters: bool) -> bytearray:
    data = bin_header(STYPE.BYTESEQ, parameters=parameters)
    data += encode_integer(len(value))
    data += value
    return data
