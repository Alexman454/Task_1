import pytest
from terminal import uniq, head, wc

def test_uniq():
    lines = ["a\n", "a\n", "b\n", "b\n", "c\n"]
    result = uniq(lines)
    assert result == ["a\n", "b\n", "c\n"], f"Expected ['a\\n', 'b\\n', 'c\\n'], got {result}"
    print("test_uniq passed: uniq removes consecutive duplicate lines")

    lines = ["a\n", "a\n", "a\n"]
    result = uniq(lines)
    assert result == ["a\n"], f"Expected ['a\\n'], got {result}"
    print("test_uniq passed: uniq works for completely identical lines")

def test_head():
    lines = [f"{i}\n" for i in range(20)]
    result = head(lines, 5)
    assert result == ["0\n", "1\n", "2\n", "3\n", "4\n"], f"Expected first 5 lines, got {result}"
    print("test_head passed: head correctly returns the first N lines")

    result = head(lines, 0)
    assert result == [], f"Expected empty list for head(0), got {result}"
    print("test_head passed: head works when N=0")

def test_wc():
    lines = ["a b\n", "c d e\n"]
    result = wc(lines)
    assert result == {"lines": 2, "words": 5, "characters": 10}, f"Expected counts, got {result}"
    print("test_wc passed: wc calculates lines, words, and characters correctly")

    lines = []
    result = wc(lines)
    assert result == {"lines": 0, "words": 0, "characters": 0}, f"Expected zero counts, got {result}"
    print("test_wc passed: wc works for empty input")

if __name__ == "__main__":
    pytest.main(["-s", __file__])
