import pytest

from fail2ban_lite.firewall import build_block_command, build_unblock_command


def test_block_command():
    cmd = build_block_command("203.0.113.5")
    assert cmd[0] == "iptables"
    assert "203.0.113.5" in cmd
    assert "DROP" in cmd
    assert "-I" in cmd or "-A" in cmd


def test_unblock_command():
    cmd = build_unblock_command("203.0.113.5")
    assert cmd[0] == "iptables"
    assert "-D" in cmd and "203.0.113.5" in cmd


@pytest.mark.parametrize("bad", ["abc", "1.1.1.1; rm -rf /", "999.1.1.1", ""])
def test_invalid_ip_rejected(bad):
    with pytest.raises(ValueError):
        build_block_command(bad)
    with pytest.raises(ValueError):
        build_unblock_command(bad)


def test_command_is_list_not_string():
    assert isinstance(build_block_command("1.2.3.4"), list)
