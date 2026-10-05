"""iptables ilə IP bloklama."""
import ipaddress
import logging
import subprocess
from typing import List

log = logging.getLogger("fail2ban_lite")


def is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def build_block_command(ip: str) -> List[str]:
    """IP-ni bloklayan iptables əmrini siyahı şəklində qaytarır.

    TODO: özün yaz.

    Gözlənilən nəticə (məs. ip='203.0.113.5'):
        ['iptables', '-I', 'INPUT', '-s', '203.0.113.5', '-j', 'DROP']

    TƏHLÜKƏSİZLİK: IP etibarsızdırsa `ValueError` at (is_valid_ip-dən istifadə et).
    Niyə? Log sətrindən gələn data etibarsızdır, əmrə birbaşa qoşmaq
    command injection riski yaradır. Bu səbəbdən də əmri string yox,
    siyahı kimi qururuq və shell=True istifadə etmirik.
    """
    raise NotImplementedError("TODO: build_block_command")


def build_unblock_command(ip: str) -> List[str]:
    """Blok qaydasını silən əmri qaytarır (-I əvəzinə -D).

    TODO: özün yaz. Eyni təhlükəsizlik qaydası keçərlidir.
    """
    raise NotImplementedError("TODO: build_unblock_command")


def _run(cmd: List[str], dry_run: bool) -> None:
    if dry_run:
        log.info("[DRY-RUN] %s", " ".join(cmd))
        return
    subprocess.run(cmd, check=True)


def block_ip(ip: str, dry_run: bool = True) -> None:
    _run(build_block_command(ip), dry_run)


def unblock_ip(ip: str, dry_run: bool = True) -> None:
    _run(build_unblock_command(ip), dry_run)
