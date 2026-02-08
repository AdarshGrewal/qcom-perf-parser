import sys
import xml.etree.ElementTree as ET

from perf_parser.models import ResourceConfig, ResourceEntry, ResourceKey


def parse_base_config(filename: str) -> ResourceConfig:
    """
    Parse XML like:

    <PerfResources>
        <Major OpcodeValue="0x0" />
        <Minor OpcodeValue="0x0" Node="..."/>

        <Major OpcodeValue="0x1" />
        <Minor OpcodeValue="0x0" Node="..."/>
        <Minor OpcodeValue="0x1" Node="..."/>
        ...
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    resources = root.find('PerfResources')
    if not resources:
        print(f'PerfResources not found in {filename}')
        sys.exit()

    config: ResourceConfig = {}
    current_major: int = -1

    for elem in resources:
        if elem.tag == 'Major':
            current_major = int(elem.attrib['OpcodeValue'], 0)

        elif elem.tag == 'Minor':
            minor_val = int(elem.attrib['OpcodeValue'], 0)

            key: ResourceKey = (current_major, minor_val)
            config[key] = ResourceEntry(
                supported=elem.attrib.get('Supported', 'yes') != 'no',
                node=elem.attrib.get('Node'),
            )

    return config


def apply_overrides(config: ResourceConfig, filename: str) -> None:
    """
    Parse override XML like:

    <PerfResources>
        <Config MajorValue="0x1" MinorValue="0x1" Supported="no"/>
        <Config MajorValue="0x1" MinorValue="0x3" Supported="no"/>
        <Config MajorValue="0x1" MinorValue="0x4" Supported="no"/>
        <Config MajorValue="0x1" MinorValue="0x2" Node="..."/>
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    resources = root.find('PerfResources')
    if not resources:
        print(f'PerfResources not found in {filename}')
        sys.exit()

    for cfg in resources.findall('Config'):
        major_val = int(cfg.attrib['MajorValue'], 0)
        minor_val = int(cfg.attrib['MinorValue'], 0)

        key: ResourceKey = (major_val, minor_val)
        entry = config.get(key)
        if not entry:
            print(
                f'{filename} tries to overwrite ({major_val},{minor_val}) which does not exist in the base config'
            )
            sys.exit()

        if 'Node' in cfg.attrib:
            entry.node = cfg.attrib.get('Node')
        if 'Supported' in cfg.attrib:
            entry.supported = cfg.attrib.get('Supported', 'yes') != 'no'


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(
            'usage: python resourceconfigs.py commonresourceconfigs.xml targetresourceconfigs.xml'
        )
        sys.exit()

    cfg = parse_base_config(sys.argv[1])
    apply_overrides(cfg, sys.argv[2])

    for (maj, minr), entry in sorted(cfg.items()):
        print(f'(0x{maj:x}, 0x{minr:x}): node={entry.node!r}, supported={entry.supported}')
