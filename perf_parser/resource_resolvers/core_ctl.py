from typing import Iterable

from perf_parser.models import ResolvedPair, ResourceContext
from perf_parser.utils.cpu import (
    get_cpu_index_for_cluster,
)


def resolve_lock_min_cores(ctx: ResourceContext) -> Iterable[ResolvedPair]:
    return [
        (
            f'/sys/devices/system/cpu/cpu{get_cpu_index_for_cluster(ctx.target_info, ctx.cluster)}/core_ctl/min_cpus',
            str(ctx.raw_value),
        )
    ]
