import xml.etree.ElementTree as ET

import gen

from models import Message, MsgContent, Component, Field, Enum


def extract_xml(constructor, element):
    r = constructor()
    for tag in element:
        r.parse_value(tag.tag, tag.text)
    for attrib in element.attrib:
        r.parse_value('attr_' + attrib, element.attrib[attrib])
    return r


def parse_messages(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    messages = {}
    for element in root:
        m = extract_xml(Message, element)
        messages[m.ComponentID] = m
    return messages


def parse_msgcontents(xml):
    from collections import defaultdict

    tree = ET.parse(xml)
    root = tree.getroot()

    msgcontent = defaultdict(list)

    for element in root:
        m = extract_xml(MsgContent, element)
        msgcontent[m.ComponentID].append(m)
    return msgcontent


def parse_fields(xml):
    tree = ET.parse(xml)
    root = tree.getroot()

    fields = {}

    for element in root:
        f = extract_xml(Field, element)
        fields[f.Tag] = f
    return fields


def parse_components(xml):
    tree = ET.parse(xml)
    root = tree.getroot()

    components = {}

    for element in root:
        c = extract_xml(Component, element)
        components[c.Name] = c
    return components


def parse_enums(xml):
    from collections import defaultdict

    tree = ET.parse(xml)
    root = tree.getroot()

    enums = defaultdict(list)

    for element in root:
        c = extract_xml(Enum, element)
        enums[c.Tag].append(c)
    return enums


# noinspection SqlNoDataSourceInspection
class Lookup:
    def _init_db(self):
        import sqlite3

        self._db = sqlite3.connect(":memory:")
        cur = self._db.cursor()
        cur.execute('CREATE TABLE messages (type varchar, name varchar, component_id int)')
        cur.execute('CREATE TABLE msgcontents (component_id int, tag_text varchar)')
        cur.execute('CREATE TABLE fields (tag int, name varchar)')
        cur.execute('CREATE TABLE components (component_id int, name varchar)')
        cur.close()
        self._db.commit()

    def _index(self):
        cur = self._db.cursor()
        # Insert messages
        cur.executemany('INSERT INTO messages values(?, ?, ?)',
                        [(x.MsgType, x.Name, x.ComponentID) for x in self._messages.values()])

        # Insert msgcontents
        import itertools
        cur.executemany('INSERT INTO msgcontents values(?, ?)',
                        [(x.ComponentID, x.TagText) for x in itertools.chain.from_iterable(self._msgcontents.values())])

        # Insert fields
        cur.executemany('INSERT INTO fields values(?, ?)',
                        [(x.Tag, x.Name) for x in self._fields.values()])

        # Insert components
        cur.executemany('INSERT INTO components values(?, ?)',
                        [(x.ComponentID, x.Name) for x in self._components.values()])

        cur.close()
        self._db.commit()

    def __init__(self, messages, msgcontents, fields, components, enums):
        self._messages = messages
        self._msgcontents = msgcontents
        self._fields = fields
        self._components = components
        self._enums = enums

        self._init_db()
        self._index()

    def msgcontents(self, id):
        import copy

        result = sorted(copy.deepcopy(self._msgcontents[id]), key=lambda res: float(res.Position))

        for r in result:
            if not r.TagText.isdigit():
                r.FieldName = r.TagText
                # Is this *really* keyed by name?
                # MsgContent -TagText-> Component -ComponentID-> MsgContent?
                if not self._components[r.TagText].NotReqXML:
                    r.AbbrName = self._components[r.TagText].AbbrName
            else:
                r.FieldName = self._fields[r.TagText].Name
                # This seems backwards
                if not self._fields[r.TagText].NotReqXML:
                    r.AbbrName = "@" + self._fields[r.TagText].AbbrName
        return result

    def fields_in(self, tag):
        result = {}

        cur = self._db.cursor()
        res = cur.execute('SELECT f.name, group_concat(c.name) '
                          'FROM fields f '
                           
                          'LEFT JOIN msgcontents mc ON f.tag == mc.tag_text '
                          'LEFT JOIN components c ON mc.component_id == c.component_id '
                           
                          'WHERE f.name = ? '
                           
                          'ORDER BY f.tag', (tag,)).fetchone()
        if res and res[1]:
            result['components'] = sorted(zip(res[1].split(','), res[1].split(',')))

        res = cur.execute('SELECT f.name, group_concat(m.name), group_concat(m.type) '
                          'FROM fields f '
                           
                          'LEFT JOIN msgcontents mc ON f.tag == mc.tag_text '
                          'LEFT JOIN messages m ON mc.component_id == m.component_id '
                           
                          'WHERE f.name = ? '
                           
                          'ORDER BY f.tag', (tag,)).fetchone()
        if res and res[1]:
            result['messages'] = sorted(zip(res[1].split(','), res[2].split(',')), key=lambda x: x[0])

        cur.close()

        return result

    def get_enums(self, tag_id):
        return self._enums.get(tag_id)


if __name__ == '__main__':
    import os

    base = 'fix_repository_2010_edition_20140507'

    for version in next(os.walk(base))[1]:
        if not version.startswith('FIX') or version == 'FIX.4.3':  # Looks for field 465, which seems to be an enum.
            continue
        output = os.path.join('out', version)

        try:
            messages = parse_messages(os.path.join(base, version, 'Base/Messages.xml'))
            msgcontents = parse_msgcontents(os.path.join(base, version, 'Base/MsgContents.xml'))
            fields = parse_fields(os.path.join(base, version, 'Base/Fields.xml'))
            components = parse_components(os.path.join(base, version, 'Base/Components.xml'))
            enums = parse_enums(os.path.join(base, version, 'Base/Enums.xml'))
            lookup = Lookup(messages, msgcontents, fields, components, enums)
            gen.render_pages(output, 'messages', messages.values(), lookup)
            gen.render_pages(output, 'components', components.values(), lookup)
            gen.render_pages(output, 'fields', fields.values(), lookup)
        except:
            print("Exception while processing: %s" % version)
            raise
