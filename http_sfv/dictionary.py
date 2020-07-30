from collections import UserDict

from .item import Item, InnerList, itemise, AllItemType
from .list import parse_item_or_inner_list
from .types import JsonType
from .util import (
    StructuredFieldValue,
    discard_http_ows,
    ser_key,
    parse_key,
)


class Dictionary(UserDict, StructuredFieldValue):
    def parse_content(self, data: bytes) -> int:
        bytes_consumed = 0
        while True:
            offset, this_key = parse_key(data[bytes_consumed:])
            bytes_consumed += offset
            if data[bytes_consumed : bytes_consumed + 1] == b"=":
                bytes_consumed += 1  # consume the "="
                offset, member = parse_item_or_inner_list(data[bytes_consumed:])
                bytes_consumed += offset
            else:
                member = Item()
                member.value = True
                bytes_consumed += member.params.parse(data[bytes_consumed:])
            self[this_key] = member
            bytes_consumed += discard_http_ows(data[bytes_consumed:])
            if not data[bytes_consumed:]:
                return bytes_consumed
            if data[bytes_consumed : bytes_consumed + 1] != b",":
                raise ValueError("Dictionary member has trailing characters")
            bytes_consumed += 1
            bytes_consumed += discard_http_ows(data[bytes_consumed:])
            if not data[bytes_consumed:]:
                raise ValueError("Dictionary has trailing comma")

    def __setitem__(self, key: str, value: AllItemType) -> None:
        self.data[key] = itemise(value)

    def __str__(self) -> str:
        if len(self) == 0:
            raise ValueError("No contents; field should not be emitted")
        output = ""
        count = len(self)
        i = 0
        for member_name in self.keys():
            i += 1
            output += ser_key(member_name)
            if isinstance(self[member_name], Item) and self[member_name].value is True:
                output += str(self[member_name].params)
            else:
                output += "="
                output += str(self[member_name])
            if i < count:
                output += ", "
        return output

    def to_json(self) -> JsonType:
        return {k: v.to_json() for (k, v) in self.items()}

    def from_json(self, json_data: JsonType) -> None:
        for k, v in json_data.items():
            if isinstance(v[0], list):
                self[k] = InnerList()
            else:
                self[k] = Item()
            self[k].from_json(v)
