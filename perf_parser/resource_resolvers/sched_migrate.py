from typing import Iterable, Tuple

from perf_parser.models import ResolvedPair, ResourceContext
from perf_parser.utils.constants import SCHED_MIGRATE_VALUE_UNSET


def _decode_raw_value(value: int) -> Tuple[int, int]:
    return ((value >> 16) & 0xFFFF, value & 0xFFFF)


def resolve_sched_group_migrate(ctx: ResourceContext) -> Iterable[ResolvedPair]:
    up, down = _decode_raw_value(ctx.raw_value)
    return [
        (ctx.node.replace('%s', 'sched_group_upmigrate'), str(up)),
        (ctx.node.replace('%s', 'sched_group_downmigrate'), str(down)),
    ]


def _migrate_value_string(cluster: int, numClusters: int, value: int) -> str:
    cluster = cluster - 1 if cluster > 0 else cluster
    return ' '.join(
        str(value) if i == cluster else SCHED_MIGRATE_VALUE_UNSET for i in range(0, numClusters - 1)
    )


def resolve_sched_migrate(ctx: ResourceContext) -> Iterable[ResolvedPair]:
    up, down = _decode_raw_value(ctx.raw_value)
    return [
        (
            ctx.node.replace('%s', 'sched_upmigrate'),
            _migrate_value_string(ctx.cluster, ctx.target_info.numClusters, up),
        ),
        (
            ctx.node.replace('%s', 'sched_downmigrate'),
            _migrate_value_string(ctx.cluster, ctx.target_info.numClusters, down),
        ),
    ]
