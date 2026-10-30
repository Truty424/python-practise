def is_palindrome(text: str) -> bool:
    text = text.lower()
    return text == text[::-1]


def count_words(text: str) -> int:
    return len(text.split())


def caesar_cipher(text: str, shift: int) -> str:
    result = ""
    for char in text:
        if "a" <= char <= "z":
            shifted = (ord(char) - 97 + shift) % 26 + 97
            result += chr(shifted)
        elif "A" <= char <= "Z":
            shifted = (ord(char) - 65 + shift) % 26 + 65
            result += chr(shifted)
        else:
            result += char
    return result
