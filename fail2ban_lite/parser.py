"""auth.log sətirlərinin parse edilməsi."""
import re
import time
from datetime import datetime
from typing import Optional

SYSLOG_TS = re.compile(r"^([A-Z][a-z]{2})\s+(\d{1,2})\s+(\d{2}:\d{2}:\d{2})")


def parse_failed_login(line: str) -> Optional[str]:
    """Uğursuz SSH login sətrindən IP ünvanını qaytarır, əks halda None.

    TODO: özün yaz.

    Tanımalı olduğun sətirlər (nümunələr):
      Oct  8 11:21:59 srv sshd[1]: Failed password for root from 203.0.113.5 port 52114 ssh2
      Oct  8 11:22:03 srv sshd[1]: Failed password for invalid user admin from 198.51.100.7 port 4000 ssh2

    Tanımamalı olduğun sətirlər:
      Oct  8 11:23:00 srv sshd[1]: Accepted password for ali from 192.168.1.5 port 5000 ssh2
      Oct  8 11:24:00 srv CRON[9]: pam_unix(cron:session): session opened

    İpucu: `re` modulu, "Failed password" + "from <IP>" şablonu.
    """
    raise NotImplementedError("TODO: parse_failed_login")


def parse_timestamp(line: str) -> float:
    """Syslog vaxtını (məs. 'Oct  8 11:21:59') epoch saniyəyə çevirir.

    Sətirdə vaxt yoxdursa, cari vaxtı qaytarır. İl syslog-da olmur,
    ona görə cari il götürülür.
    """
    m = SYSLOG_TS.match(line)
    if not m:
        return time.time()
    month, day, hms = m.groups()
    year = datetime.now().year
    try:
        dt = datetime.strptime(f"{year} {month} {int(day)} {hms}", "%Y %b %d %H:%M:%S")
    except ValueError:
        return time.time()
    return dt.timestamp()
