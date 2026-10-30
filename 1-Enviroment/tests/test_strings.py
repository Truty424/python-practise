import pytest
from strings import caesar_cipher, count_words, is_palindrome


@pytest.fixture
def sample_text() -> str:
    return "Hello World"


@pytest.mark.parametrize(
    "text, expected",
    [
        ("kayak", True),
        ("hello", False),
        ("Kayak", True),
        ("racecar", True),
        ("python", False),
    ],
)
def test_is_palindrome(text: str, expected: bool):
    assert is_palindrome(text) is expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello World", 2),
        ("", 0),
        (" Python ", 1),
    ],
)
def test_count_words(text: str, expected: int):
    assert count_words(text) == expected


@pytest.mark.parametrize(
    "text, shift, expected",
    [
        ("abc", 3, "def"),
        ("ABC", 3, "DEF"),
        ("xyz", 3, "abc"),
        ("Hello World!", 3, "Khoor Zruog!"),
        ("abc", -3, "xyz"),
    ],
)
def test_caesar_cipher(text: str, shift: int, expected: str):
    assert caesar_cipher(text, shift) == expected


def test_count_words_with_fixture(sample_text: str):
    assert count_words(sample_text) == 2
