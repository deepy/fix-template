# FIX models


class Message:
    def parse_value(self, tag, text):
        if tag == 'NotReqXML':
            text = bool(int(text))
        elif tag == 'ComponentID':
            text = int(text)
        setattr(self, tag, text)


class MsgContent:
    def parse_value(self, tag, text):
        if tag == 'Reqd':
            text = bool(int(text))
        elif tag == 'ComponentID':
            text = int(text)
        setattr(self, tag, text)

    def __repr__(self):
        return '<MsgContent %s>' % self.TagText


class Component:
    def parse_value(self, tag, text):
        if tag == 'NotReqXML':
            text = bool(int(text))
        elif tag == 'ComponentID':
            text = int(text)
        setattr(self, tag, text)

    def __repr__(self):
        return '<MsgContent %s>' % self.TagText


class Field:
    # TODO: added/deprecated
    # <Field added="FIX.2.7" deprecated="FIXT.1.1">

    def parse_value(self, tag, text):
        if tag == 'NotReqXML':
            text = bool(int(text))
        setattr(self, tag, text)

    def __repr__(self):
        return '<Field %s>' % self.Name
