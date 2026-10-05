"""Log faylını izləyib bloklama qərarını verir."""
import os
import time
from typing import Callable, Iterable, List, Set

from .parser import parse_failed_login, parse_timestamp
from .tracker import FailureTracker


def process_lines(lines: Iterable[str], tracker: FailureTracker,
                  whitelist: Set[str], on_ban: Callable[[str], None]) -> List[str]:
    """Sətirləri emal edir, bloklanan IP-lərin siyahısını qaytarır."""
    banned: List[str] = []
    for line in lines:
        ip = parse_failed_login(line)
        if ip is None or ip in whitelist or ip in banned:
            continue
        if tracker.record(ip, parse_timestamp(line)):
            banned.append(ip)
            on_ban(ip)
    return banned


def follow(path: str, poll: float = 0.5):
    """`tail -f` kimi: faylın sonundan yeni sətirləri verir (generator)."""
    with open(path, "r", errors="replace") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                yield line
            else:
                time.sleep(poll)
