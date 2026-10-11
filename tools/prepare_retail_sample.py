"""Reproduce the bundled sample from UCI's downloaded online+retail.zip."""
import argparse
from decimal import Decimal, ROUND_HALF_EVEN
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile


def prepare(archive_path):
    with zipfile.ZipFile(archive_path) as archive:
        xlsx = archive.read(archive.namelist()[0])
    with zipfile.ZipFile(io.BytesIO(xlsx)) as book:
        namespace = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        strings = [''.join(node.itertext()) for node in
                   ET.fromstring(book.read('xl/sharedStrings.xml')).findall('s:si', namespace)]
        records = []
        for _, node in ET.iterparse(book.open('xl/worksheets/sheet1.xml'), events=('end',)):
            if node.tag.rsplit('}', 1)[-1] != 'row':
                continue
            index = int(node.attrib['r'])
            if index == 1:
                node.clear()
                continue
            values = {}
            for cell in node.findall('s:c', namespace):
                value = cell.find('s:v', namespace)
                if value is None:
                    continue
                text = value.text
                if cell.attrib.get('t') == 's':
                    text = strings[int(text)]
                values[''.join(c for c in cell.attrib['r'] if c.isalpha())] = text
            try:
                quantity = int(values['D'])
                price = int((Decimal(values['F']) * 100).quantize(Decimal('1'), rounding=ROUND_HALF_EVEN))
                if quantity == 0 or price < 0:
                    continue
                seconds = int((Decimal(values['E']) - Decimal('25569')) * 86400)
                records.append(dict(source='retail', id=f'row-{index}', rev=1,
                                    kind='return' if quantity < 0 else 'sale',
                                    customer=values.get('G'), sku=values['B'], timestamp=seconds,
                                    quantity=abs(quantity), price_minor=price, invoice=values['A']))
            except (KeyError, ValueError):
                continue
            node.clear()
            if len(records) >= 1200:
                break
    deliveries = []
    for index, record in enumerate(records):
        deliveries.append(record)
        if index % 31 == 0:
            deliveries.append(dict(record))
        if index % 47 == 0:
            deliveries.append({**record, 'rev': 2, 'quantity': record['quantity'] + 1})
        if index % 101 == 0:
            deliveries.append(dict(source=record['source'], id=record['id'], rev=3, kind='delete'))
        if index % 83 == 0:
            deliveries.extend([{**record, 'rev': 4, 'price_minor': record['price_minor'] + 1},
                               {**record, 'rev': 4, 'price_minor': record['price_minor'] + 2}])
    return ''.join(json.dumps(record, separators=(',', ':')) + '\n' for record in deliveries)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_zip')
    parser.add_argument('output')
    args = parser.parse_args()
    Path(args.output).write_text(prepare(args.source_zip), encoding='utf-8')
