from collections import UserString
from decimal import Decimal
from typing import Union, Dict, List, Tuple
from typing_extensions import TypeAlias


class Token(UserString):
    def __init__(self, seq: str):
        self.data = seq

    def __repr__(self) -> str:
        return f'Token("{self.data}")'


BareItemType: TypeAlias = Union[int, float, str, bool, Decimal, bytes, Token]
ParamsType: TypeAlias = Dict[str, BareItemType]
ItemType: TypeAlias = Union[BareItemType, Tuple[BareItemType, ParamsType]]
InnerListType: TypeAlias = Union[List[ItemType], Tuple[List[ItemType], ParamsType]]
ItemOrInnerListType: TypeAlias = Union[ItemType, InnerListType]
ListType: TypeAlias = List[Union[ItemType, InnerListType]]
DictionaryType: TypeAlias = Dict[str, Union[ItemType, InnerListType]]
StructuredType: TypeAlias = Union[ItemType, ListType, DictionaryType]
