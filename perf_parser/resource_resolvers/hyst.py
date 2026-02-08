from typing import Iterable

from perf_parser.models import ResolvedPair, ResourceContext


def resolve_hyst_opt_path(ctx: ResourceContext) -> Iterable[ResolvedPair]:
    return [
        (f'{ctx.node}/{node_name}', str(ctx.raw_value))
        for node_name in ['hyst_length', 'hist_memory', 'hyst_trigger_count']
    ]
