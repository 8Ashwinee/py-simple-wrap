import pytest

from py_simple_package.src.py_simple import extract_hashtag_names as public_extract
from py_simple_package.src.py_simple.easy_regex import (
    extract_hashtag_names,
    extract_hashtags,
)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello #Python and #coding", ["Python", "coding"]),
        ("#hello_world #123 #_", ["hello_world", "123", "_"]),
        ("#Python #Python #python", ["Python", "Python", "python"]),
        ("", []),
        ("No hashtags here", []),
        ("# ## ### #!", []),
        ("word#tag _#tag 1#tag ##tag ###tag", []),
        ("(#one), #two! #three-four", ["one", "two", "three"]),
        ("#one\n#two\t#three", ["one", "two", "three"]),
        ("#caf\u00e9 #\u6771\u4eac", ["caf\u00e9", "\u6771\u4eac"]),
        ("\u00e9#tag", []),
        ("#cafe\u0301", ["cafe"]),
        ("#one#two", ["one"]),
        ("#\U0001f600", []),
    ],
)
def test_extract_hashtag_names(text, expected):
    assert extract_hashtag_names(text) == expected


def test_public_export():
    assert public_extract is extract_hashtag_names


def test_existing_regex_hashtags_keep_hash_symbols():
    assert extract_hashtags("#Python #coding") == ["#Python", "#coding"]
