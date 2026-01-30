from perf_parser.models import ResourceKey, ResourceResolver
from perf_parser.resource_resolvers import msm_perf
from typing import Dict

resource_resolvers: Dict[ResourceKey, ResourceResolver] = {
    # (major, minor): handler
    (0x2, 0x0): msm_perf.resolve_msm_perf,
    (0x2, 0x1): msm_perf.resolve_msm_perf,
}