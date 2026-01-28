from perf_parser.parsers import boostsconfig, resourceconfigs
from perf_parser.models import Boost, BoostKey, ResourceConfig, ResourceEntry
import sys
import os
import argparse
from typing import List, Tuple, Optional

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='QCOM perf config parser')
    parser.add_argument('dump_path', help='Path to dump')
    parser.add_argument(
        '-pbc', '--perfboostsconfig', help='Path to perfboostsconfig.xml', required=False
    )
    parser.add_argument('-ph', '--powerhint', help='Path to powerhint.xml', required=False)
    parser.add_argument(
        '-crc', '--commonresourceconfigs', help='Path to commonresourceconfigs.xml', required=False
    )
    parser.add_argument(
        '-trc', '--targetresourceconfigs', help='Path to targetresourceconfigs.xml', required=False
    )
    argument = parser.parse_args()

    perfboostsconfig_path = argument.perfboostsconfig or os.path.join(
        argument.dump_path, 'vendor/etc/perf/perfboostsconfig.xml'
    )
    powerhint_path = argument.powerhint or os.path.join(
        argument.dump_path, 'vendor/etc/powerhint.xml'
    )
    commonresourceconfigs_path = argument.commonresourceconfigs or os.path.join(
        argument.dump_path, 'vendor/etc/perf/commonresourceconfigs.xml'
    )
    targetresourceconfigs_path = argument.targetresourceconfigs or os.path.join(
        argument.dump_path, 'vendor/etc/perf/targetresourceconfigs.xml'
    )

    # perfboostsconfig.xml and powerhints.xml include all boosts with the resources and values to be set
    perfboosts = boostsconfig.parse_boost_xml(perfboostsconfig_path)
    powerhints = boostsconfig.parse_boost_xml(powerhint_path)

    # commonresourceconfigs.xml and targetresourceconfigs.xml map the resource major/minor to paths
    resource_config: ResourceConfig = resourceconfigs.parse_base_config(commonresourceconfigs_path)
    resourceconfigs.apply_overrides(resource_config, targetresourceconfigs_path)

    powerhint_map: List[Tuple[BoostKey, str]] = [
        # ((0x00001206, None, None), 'SUSTAINED_PERFORMANCE'),
        ((0x00001080, 1, 120), 'INTERACTION'),
        # ((0x00001081, 10, None), 'LAUNCH'),
    ]

    for bk, powerhint_name in powerhint_map:
        boost_id, boost_type, boost_fps = bk
        boost: Optional[Boost] = next(
            (
                b
                for b in perfboosts + powerhints
                if b.id == boost_id
                and (boost_type is None or b.type == boost_type)
                and (boost_fps is None or boost_fps in b.fps)
            ),
            None,
        )
        if not boost:
            print(
                f'Requested boost for {powerhint_name} not found! id: {boost_id}, type: {boost_type}, fps: {boost_fps}'
            )
            continue

        for opcode, value in boost.resources:
            major = (opcode & 0x1FC00000) >> 22
            minor = (opcode & 0x000FC000) >> 14
            cluster = (opcode & 0x00000F00) >> 8

            resource: ResourceEntry = resource_config[(major, minor)]
            print(f"set {value} on {resource} for cluster {cluster}")
