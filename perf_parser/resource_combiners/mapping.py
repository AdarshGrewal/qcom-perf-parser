from typing import Dict

from perf_parser.models import ResourceCombiner, ResourceKey
from perf_parser.resource_combiners import msm_perf, sched_migrate

resource_combiners: Dict[ResourceKey, ResourceCombiner] = {
    # (major, minor): handler
    (0x2, 0x0): msm_perf.combine_msm_perf,
    (0x2, 0x1): msm_perf.combine_msm_perf,
    (0x3, 0x38): sched_migrate.combine_sched_migrate,  # sched - up/down migrate
}
