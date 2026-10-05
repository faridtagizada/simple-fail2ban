"""Komanda sətri interfeysi."""
import argparse
import logging
import sys
import time

from . import __version__
from .firewall import block_ip, unblock_ip
from .monitor import follow, process_lines
from .tracker import FailureTracker

log = logging.getLogger("fail2ban_lite")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fail2ban_lite",
        description="SSH brute-force edən IP-ləri aşkarlayıb iptables ilə bloklayır.")
    p.add_argument("--log", default="/var/log/auth.log", help="Log faylı (default: /var/log/auth.log)")
    p.add_argument("--max-attempts", type=int, default=5, help="Bloklama həddi (default: 5)")
    p.add_argument("--window", type=int, default=300, help="Zaman pəncərəsi, saniyə (default: 300)")
    p.add_argument("--ban-time", type=int, default=600, help="Blok müddəti, saniyə (default: 600)")
    p.add_argument("--whitelist", nargs="*", default=["127.0.0.1"], help="Bloklanmayacaq IP-lər")
    p.add_argument("--apply", action="store_true",
                   help="Həqiqətən iptables tətbiq et (default: yalnız DRY-RUN, root lazımdır)")
    p.add_argument("--once", action="store_true",
                   help="Faylı əvvəldən bir dəfə oxu və çıx (test/demo üçün)")
    p.add_argument("-v", "--version", action="version", version=__version__)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    dry_run = not args.apply
    tracker = FailureTracker(args.max_attempts, args.window)
    whitelist = set(args.whitelist)
    bans = {}   # ip -> blok vaxtı

    def on_ban(ip: str) -> None:
        log.warning("Brute-force aşkarlandı: %s bloklanır", ip)
        block_ip(ip, dry_run)
        bans[ip] = time.time()

    def expire_bans() -> None:
        now = time.time()
        for ip in [i for i, t in bans.items() if now - t >= args.ban_time]:
            log.info("Blok müddəti bitdi: %s", ip)
            unblock_ip(ip, dry_run)
            del bans[ip]

    if not dry_run:
        log.warning("DİQQƏT: real iptables qaydaları tətbiq olunur!")
    try:
        if args.once:
            with open(args.log, errors="replace") as f:
                banned = process_lines(f, tracker, whitelist, on_ban)
            log.info("Bitdi. Bloklanan IP sayı: %d", len(banned))
            return 0
        log.info("İzlənir: %s (hədd=%d/%ds, dry_run=%s)", args.log,
                 args.max_attempts, args.window, dry_run)
        for line in follow(args.log):
            process_lines([line], tracker, whitelist, on_ban)
            expire_bans()
    except FileNotFoundError:
        print(f"Xəta: fayl tapılmadı: {args.log}", file=sys.stderr)
        return 1
    except PermissionError:
        print("Xəta: icazə yoxdur (log oxumaq/iptables üçün sudo lazım ola bilər)", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nDayandırıldı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
