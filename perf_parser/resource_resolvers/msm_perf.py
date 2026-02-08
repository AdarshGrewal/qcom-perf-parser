from typing import Iterable

from perf_parser.models import ResolvedPair, ResourceContext
from perf_parser.utils.cpu import get_cpus_for_cluster, get_next_available_frequency_for_cluster


def resolve_msm_perf(ctx: ResourceContext) -> Iterable[ResolvedPair]:
    value = get_next_available_frequency_for_cluster(
        ctx.target_info, ctx.cluster, 1000 * ctx.raw_value
    )
    return [
        (
            ctx.node,
            ' '.join(
                f'{cpu}:{value}' for cpu in get_cpus_for_cluster(ctx.target_info, ctx.cluster)
            ),
        )
    ]
