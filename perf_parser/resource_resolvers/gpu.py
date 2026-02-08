from typing import Iterable

from perf_parser.models import ResolvedPair, ResourceContext
from perf_parser.utils.gpu import get_next_available_frequency


def resolve_next_gpu_freq(ctx: ResourceContext) -> Iterable[ResolvedPair]:
    return [(ctx.node, str(get_next_available_frequency(1000000 * ctx.raw_value)))]
