from typing import Iterable

def combine_msm_perf(values: Iterable[str]) -> str:
    return " ".join(v for v in values)