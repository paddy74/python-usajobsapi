from enum import Enum
from typing import Annotated, List, Optional

import pytest
from pydantic import BaseModel, Field

from usajobsapi.utils import _dump_by_alias

# _dump_by_alias


class Color(str, Enum):
    RED = "red"
    BLUE = "blue"


class QueryModel(BaseModel):
    # scalars
    a_str: Annotated[Optional[str], Field(serialization_alias="A")] = None
    a_int: Annotated[Optional[int], Field(serialization_alias="D")] = None

    # bools and enums
    a_bool: Annotated[Optional[bool], Field(serialization_alias="B")] = None
    enum_field: Annotated[Optional[Color], Field(serialization_alias="E")] = None

    # lists
    a_list_str: List[str] = Field(default_factory=list, serialization_alias="C")
    a_list_int: List[int] = Field(default_factory=list, serialization_alias="H")

    # outliers
    empty_list: List[str] = Field(default_factory=list, serialization_alias="F")
    none_field: Annotated[Optional[str], Field(serialization_alias="G")] = None


def test_uses_alias_names():
    m = QueryModel(a_str="hello", a_int=42)
    out = _dump_by_alias(m)
    assert out == {"A": "hello", "D": "42"}


@pytest.mark.parametrize("val,expected", [(True, "True"), (False, "False")])
def test_boolean_formatting(val, expected):
    m = QueryModel(a_bool=val)
    out = _dump_by_alias(m)
    assert out == {"B": expected}


def test_list_join_semicolon_for_strings_and_ints():
    m = QueryModel(a_list_str=["x", "y", "z"], a_list_int=[1, 2, 3])
    out = _dump_by_alias(m)
    assert out["C"] == "x;y;z"
    assert out["H"] == "1;2;3"


def test_empty_list_and_none_omitted():
    m = QueryModel(a_list_str=[], none_field=None)
    out = _dump_by_alias(m)
    assert "C" not in out
    assert "G" not in out


def test_zero_and_false_are_preserved():
    m = QueryModel(a_int=0, a_bool=False)
    out = _dump_by_alias(m)
    # "0" and "False" should not be dropped
    assert out["D"] == "0"
    assert out["B"] == "False"


def test_enum_serialization():
    m = QueryModel(enum_field=Color.BLUE)  # pyright: ignore[reportCallIssue]
    out = _dump_by_alias(m)
    assert out == {"E": "Color.BLUE"}


def test_empty_string_is_omitted():
    m = QueryModel(a_str="")
    out = _dump_by_alias(m)
    assert "A" not in out


def test_idempotent_and_no_side_effects():
    m = QueryModel(a_str="a", a_bool=True, a_list_str=["p", "q"])
    out1 = _dump_by_alias(m)
    out2 = _dump_by_alias(m)  # calling twice should produce identical results
    assert out1 == out2
    # ensure model fields weren't mutated
    assert m.a_list_str == ["p", "q"]
