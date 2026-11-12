import pytest
from log_parser.parser import parse_log_line


def test_parse_valid_log():
    line = (
        '192.168.1.10 - - [06/Nov/2026:10:15:32 +0100] "GET /login HTTP/1.1" 200 1536'
    )

    result = parse_log_line(line)

    assert result["ip"] == "192.168.1.10"
    assert result["method"] == "GET"
    assert result["path"] == "/login"
    assert result["status"] == 200
    assert result["size"] == 1536


def test_parse_invalid_log():
    with pytest.raises(ValueError, match="Invalid log format"):
        parse_log_line("invalid log")


def test_parse_invalid_request():
    line = '192.168.1.10 - - [06/Nov/2026:10:15:32 +0100] "GET /login" 200 1536'

    with pytest.raises(ValueError, match="Invalid HTTP request format"):
        parse_log_line(line)
