from fail2ban_lite.parser import parse_failed_login, parse_timestamp


def test_failed_password_root():
    line = "Oct  8 11:21:59 srv sshd[1]: Failed password for root from 203.0.113.5 port 52114 ssh2"
    assert parse_failed_login(line) == "203.0.113.5"


def test_failed_password_invalid_user():
    line = "Oct  8 11:22:03 srv sshd[1]: Failed password for invalid user admin from 198.51.100.7 port 4000 ssh2"
    assert parse_failed_login(line) == "198.51.100.7"


def test_accepted_login_ignored():
    line = "Oct  8 11:23:00 srv sshd[1]: Accepted password for ali from 192.168.1.5 port 5000 ssh2"
    assert parse_failed_login(line) is None


def test_unrelated_line_ignored():
    assert parse_failed_login("Oct  8 11:24:00 srv CRON[9]: pam_unix(cron:session): session opened") is None


def test_empty_line():
    assert parse_failed_login("") is None


def test_timestamp_parsed_and_ordered():
    a = parse_timestamp("Oct  8 11:21:59 srv x")
    b = parse_timestamp("Oct  8 11:22:59 srv x")
    assert b - a == 60
