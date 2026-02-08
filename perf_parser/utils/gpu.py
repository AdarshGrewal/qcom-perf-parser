import subprocess
from typing import Iterable


def get_available_frequencies() -> Iterable[int]:
    available_frequencies = subprocess.check_output(
        [
            'adb',
            'shell',
            'cat',
            '/sys/class/kgsl/kgsl-3d0/devfreq/available_frequencies',
        ],
        text=True,
    )

    return [int(f, 0) for f in available_frequencies.split(' ') if f.strip()]


def get_next_available_frequency(requested_frequency: int) -> int:
    return min(get_available_frequencies(), key=lambda x: abs(x - requested_frequency))
