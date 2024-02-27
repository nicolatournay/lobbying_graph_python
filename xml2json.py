import xml.etree.ElementTree as ET
import json
from collections import defaultdict

def etree_to_dict(t):
    tag = t.tag.split('}')[-1]  # Supprime l'espace de noms
    d = {tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[tag]['#text'] = text
        else:
            d[tag] = text
    return d

def xml_to_json(xml_file, json_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = etree_to_dict(root)

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

xml_to_json('eu_transparency_register_jan_2024.xml', 'eu_transparency_register_jan_2024.json')