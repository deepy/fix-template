import xml.etree.ElementTree as ET

import gen

from models import Message, MsgContent, Field


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
        fields[f.Tag] = f
    return fields


class Lookup:
    def __init__(self, messages, msgcontents, fields):
        self._messages = messages
        self._msgcontents = msgcontents
        self._fields = fields

    def msgcontents(self, id):
        import copy
        result = copy.deepcopy(self._msgcontents[id])
        # Field or Component	Field Name	FIXML name	Req'd	Comments	Depr.
        for r in result:
            if not r.TagText.isdigit():
                r.FieldName = r.TagText
                r.DisplayTagText = 'Component'
                r.AbbrName = 'NYI'
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
    gen.render([messages[11]], Lookup(messages, msgcontents, fields))
