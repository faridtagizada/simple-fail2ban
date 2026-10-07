from fail2ban_lite.tracker import FailureTracker


def test_ban_on_threshold():
    t = FailureTracker(max_attempts=3, window_seconds=60)
    assert t.record("1.1.1.1", 0) is False
    assert t.record("1.1.1.1", 1) is False
    assert t.record("1.1.1.1", 2) is True


def test_old_attempts_expire():
    t = FailureTracker(max_attempts=3, window_seconds=60)
    t.record("1.1.1.1", 0)
    t.record("1.1.1.1", 10)
    assert t.record("1.1.1.1", 100) is False   # ilk ikisi pəncərədən çıxıb


def test_ips_tracked_separately():
    t = FailureTracker(max_attempts=2, window_seconds=60)
    assert t.record("1.1.1.1", 0) is False
    assert t.record("2.2.2.2", 1) is False
    assert t.record("1.1.1.1", 2) is True


def test_history_cleared_after_ban():
    t = FailureTracker(max_attempts=2, window_seconds=60)
    t.record("1.1.1.1", 0)
    assert t.record("1.1.1.1", 1) is True
    assert t.record("1.1.1.1", 2) is False     # yenidən saymağa başlayır
