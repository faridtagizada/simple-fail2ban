"""IP başına uğursuz cəhdlərin sürüşən zaman pəncərəsində sayılması."""


class FailureTracker:
    """Hər IP üçün cəhdlərin vaxtını saxlayır.

    max_attempts: pəncərə daxilində neçə cəhddən sonra IP bloklanmalıdır
    window_seconds: pəncərənin uzunluğu (saniyə)
    """

    def __init__(self, max_attempts: int = 5, window_seconds: int = 300):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self.attempts = {}   # ip -> [vaxt1, vaxt2, ...]

    def record(self, ip: str, timestamp: float) -> bool:
        """Uğursuz cəhdi qeyd edir. Hədd aşılıbsa True qaytarır.

        TODO: özün yaz.

        Qaydalar:
          1. Bu IP-nin siyahısına `timestamp`-i əlavə et.
          2. `window_seconds`-dən köhnə vaxtları siyahıdan sil.
          3. Qalan cəhdlərin sayı >= max_attempts olarsa True qaytar
             və həmin IP-nin tarixçəsini təmizlə (təkrar bloklanmasın).
          4. Əks halda False qaytar.

        İpucu: dict + list kifayətdir. (Əlavə: `collections.deque` ilə necə olar?)
        """
        raise NotImplementedError("TODO: FailureTracker.record")
