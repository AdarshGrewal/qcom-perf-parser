from perf_parser.models import ResourceKey, ResourceCombiner
from perf_parser.resource_combiners import msm_perf
from typing import Dict

resource_combiners: Dict[ResourceKey, ResourceCombiner] = {
    # (major, minor): handler
    (0x2, 0x0): msm_perf.combine_msm_perf,
    (0x2, 0x1): msm_perf.combine_msm_perf,
}