import xml.etree.ElementTree as ET

import gen

from models import Message, MsgContent, Component, Field


def parse_messages(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    messages = {}
    for message in root:
        m = Message()
        for tag in message:
            m.parse_value(tag.tag, tag.text)
        messages[m.ComponentID] = m
    return messages


def parse_msgcontents(xml):
    from collections import defaultdict

    tree = ET.parse(xml)
    root = tree.getroot()

    msgcontent = defaultdict(list)

    for message in root:
        m = MsgContent()
        for tag in message:
            m.parse_value(tag.tag, tag.text)
        for attrib in message.attrib:
            m.parse_value('attr_' + attrib, message.attrib[attrib])
        msgcontent[m.ComponentID].append(m)
    return msgcontent


def parse_fields(xml):
    tree = ET.parse(xml)
    root = tree.getroot()

    fields = {}

    for message in root:
        f = Field()
        for tag in message:
            f.parse_value(tag.tag, tag.text)
        for attrib in message.attrib:
            f.parse_value('attr_' + attrib, message.attrib[attrib])
        fields[f.Tag] = f
    return fields


def parse_components(xml):
    tree = ET.parse(xml)
    root = tree.getroot()

    components = {}

    for message in root:
        c = Component()
        for tag in message:
            c.parse_value(tag.tag, tag.text)
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
    gen.render([messages[14]], Lookup(messages, msgcontents, fields, components))
    # gen.render([messages[11]], Lookup(messages, msgcontents, fields, components))
