import xml.etree.ElementTree as ET

import gen

from models import Message, MsgContent, Component, Field


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


class Lookup:
    def __init__(self, messages, msgcontents, fields, components):
        self._messages = messages
        self._msgcontents = msgcontents
        self._fields = fields
        self._components = components

    def msgcontents(self, id):
        import copy
        result = copy.deepcopy(self._msgcontents[id])
        for r in result:
            if not r.TagText.isdigit():
                r.FieldName = r.TagText
                r.DisplayTagText = 'Component'
                # Is this *really* keyed by name?
                # MsgContent -TagText-> Component -ComponentID-> MsgContent?
                if not self._components[r.TagText].NotReqXML:
                    r.AbbrName = self._components[r.TagText].AbbrName
            else:
                r.FieldName = self._fields[r.TagText].Name
                r.DisplayTagText = r.TagText
                # This seems backwards
                if not self._fields[r.TagText].NotReqXML:
                    r.AbbrName = "@" + self._fields[r.TagText].AbbrName
        return result


if __name__ == '__main__':
    messages = parse_messages('fix_repository_2010_edition_20140507/FIX.5.0SP2/Base/Messages.xml')
    msgcontents = parse_msgcontents('fix_repository_2010_edition_20140507/FIX.5.0SP2/Base/MsgContents.xml')
    fields = parse_fields('fix_repository_2010_edition_20140507/FIX.5.0SP2/Base/Fields.xml')
    components = parse_components('fix_repository_2010_edition_20140507/FIX.5.0SP2/Base/Components.xml')
    gen.render(messages.values(), Lookup(messages, msgcontents, fields, components))
