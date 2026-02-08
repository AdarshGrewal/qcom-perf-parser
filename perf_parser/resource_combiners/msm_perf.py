from typing import List


def combine_msm_perf(values: List[str], path: str) -> str:
    sorted_values = sorted(values, key=lambda s: int(s.split(':')[0]))
    return ' '.join(v for v in sorted_values)
