import os

from fail2ban_lite.monitor import process_lines
from fail2ban_lite.tracker import FailureTracker

SAMPLE = os.path.join(os.path.dirname(__file__), "..", "samples", "auth_sample.log")


def run(whitelist=("127.0.0.1",)):
    banned_cb = []
    with open(SAMPLE) as f:
        result = process_lines(f, FailureTracker(5, 300), set(whitelist), banned_cb.append)
    return result, banned_cb


def test_attacker_banned():
    result, cb = run()
    assert result == ["203.0.113.5"]
    assert cb == result


def test_below_threshold_not_banned():
    result, _ = run()
    assert "198.51.100.7" not in result


def test_whitelist_respected():
    result, _ = run()
    assert "127.0.0.1" not in result


def test_without_whitelist_localhost_banned():
    result, _ = run(whitelist=())
    assert "127.0.0.1" in result
