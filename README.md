# Simple Fail2ban (fail2ban-lite)

Python ilə yazılmış sadə fail2ban analoqu. `/var/log/auth.log` faylını izləyir, qısa zamanda çoxlu uğursuz SSH login edən IP-ləri aşkarlayır və `iptables` ilə bloklayır. Müəyyən müddətdən sonra blokdan çıxarır.

> ⚠️ Defolt olaraq **DRY-RUN** rejimində işləyir (heç nəyi bloklamır, yalnız log yazır). Real bloklama üçün `--apply` və root lazımdır. Öz IP-ni whitelist-ə əlavə et, yoxsa özünü serverdən kənarda qoya bilərsən.

## Funksiyalar
- Uğursuz SSH login sətirlərinin parse edilməsi (`Failed password`, `invalid user`)
- Sürüşən zaman pəncərəsi ilə brute-force aşkarlanması (default: 5 dəqiqədə 5 cəhd)
- `iptables` ilə bloklama və blok müddəti bitəndə avtomatik açma
- Whitelist dəstəyi
- DRY-RUN rejimi (təhlükəsiz test)
- Command injection-a qarşı: IP yoxlanılır, əmrlər `shell=True` olmadan, siyahı kimi icra edilir
- `pytest` testləri

## Quraşdırma
```bash
git clone https://github.com/<istifadəçi_adın>/simple-fail2ban.git
cd simple-fail2ban
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
Əlavə kitabxana lazım deyil (yalnız testlər üçün `pytest`). Python 3.8+, Linux, `iptables`.

## İstifadə
```bash
# Nümunə log üzərində demo (heç nə bloklamır)
python -m fail2ban_lite --log samples/auth_sample.log --once

# Canlı izləmə, DRY-RUN
python -m fail2ban_lite --log /var/log/auth.log

# Real bloklama (root lazımdır), öz IP-ni whitelist-ə əlavə et
sudo python -m fail2ban_lite --apply --whitelist 127.0.0.1 <sənin_IP> \
     --max-attempts 5 --window 300 --ban-time 900
```

| Parametr | Təsvir | Default |
|---|---|---|
| `--log` | Log faylı | `/var/log/auth.log` |
| `--max-attempts` | Bloklama həddi | 5 |
| `--window` | Pəncərə (san.) | 300 |
| `--ban-time` | Blok müddəti (san.) | 600 |
| `--whitelist` | Bloklanmayan IP-lər | `127.0.0.1` |
| `--apply` | Real iptables | söndürülüb |
| `--once` | Faylı bir dəfə oxu | söndürülüb |

### Nümunə çıxış
```
WARNING Brute-force aşkarlandı: 203.0.113.5 bloklanır
INFO [DRY-RUN] iptables -I INPUT -s 203.0.113.5 -j DROP
INFO Bitdi. Bloklanan IP sayı: 1
```
> Real çıxışın ekran görüntüsü ilə əvəz et.

## Layihə strukturu
```
simple-fail2ban/
├── fail2ban_lite/
│   ├── parser.py     # log sətirlərinin parse edilməsi
│   ├── tracker.py    # sürüşən pəncərə ilə cəhd sayğacı
│   ├── firewall.py   # iptables əmrləri
│   ├── monitor.py    # log izləmə və qərar məntiqi
│   └── cli.py
├── samples/auth_sample.log
└── tests/
```

## Testlər
```bash
pytest -v
```

## Məhdudiyyətlər
- Yalnız SSH `Failed password` sətirləri (public key və PAM xətaları yox)
- Yalnız IPv4 üçün `iptables` (IPv6 üçün `ip6tables` lazımdır)
- Yenidən başladıqda aktiv bloklar yadda qalmır

## Gələcək planlar
- [ ] IPv6 (`ip6tables`) və `nftables` dəstəyi
- [ ] `systemd` servis faylı
- [ ] Blokların fayla yazılıb bərpası
- [ ] Digər servislər (Nginx, FTP) üçün filtrlər

## Lisenziya
MIT
