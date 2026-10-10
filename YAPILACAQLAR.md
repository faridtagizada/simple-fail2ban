# Sənin işin (GitHub-a yükləməzdən əvvəl bu faylı sil)

Layihənin çərçivəsi hazırdır. Əsas məntiqi sən yazırsan. Testlər sənə düzgün olub-olmadığını göstərir.

## Yazılacaq funksiyalar (bu ardıcıllıqla)
1. `fail2ban_lite/parser.py` → `parse_failed_login`  (test: `pytest tests/test_parser.py`)
2. `fail2ban_lite/tracker.py` → `FailureTracker.record`  (test: `pytest tests/test_tracker.py`)
3. `fail2ban_lite/firewall.py` → `build_block_command`, `build_unblock_command`  (test: `pytest tests/test_firewall.py`)
4. Hamısı bitəndə: `pytest -v` və `python -m fail2ban_lite --log samples/auth_sample.log --once`

Hər funksiyanın docstring-ində ipucu var. Ilişsən, yazdığın kodu mənə göndər, səhvlərini birlikdə tapaq.

## Özünü yoxla (müsahibə sualları)
- Niyə sürüşən pəncərə istifadə edirik, sadə sayğac niyə kifayət etmir?
- Niyə əmri string yox, siyahı ilə qururuq? `shell=True` nə təhlükə yaradır?
- `iptables -I` ilə `-A` fərqi nədir? Niyə `-I` seçdik?
- Hücumçu IP-ni saxtalaşdırsa (spoofing) və whitelist IP-sini göndərsə nə olar?
- Öz IP-ni səhvən bloklasan serverə necə qayıdarsan?

## Sonra əlavə et (layihəni öz layihənə çevirən hissə)
- IPv6 dəstəyi və ya `ban-time` bitəndə log
- Ubuntu VM-də real `--apply` ilə sına, `sudo iptables -L -n` ilə yoxla, Kali-dən `hydra` ilə öz VM-ə hücum edib bloklanmanı müşahidə et
