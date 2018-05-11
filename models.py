# FIX models


class Message:
    def parse_value(self, tag, text):
        if tag == 'NotReqXML':
            text = bool(int(text))
        elif tag == 'ComponentID':
            text = int(text)
        setattr(self, tag, text)

    def pretty_name(self):
        return self.Name

    def pretty_type(self):
        return self.MsgType

    def __repr__(self):
        return "<Message %s>" % self.pretty_name()


class MsgContent:
    def parse_value(self, tag, text):
        if tag == 'Reqd':
            text = bool(int(text))
        elif tag == 'ComponentID':
            text = int(text)
        setattr(self, tag, text)

    def pretty_name(self):
        return self.TagText

    def pretty_type(self):
        if self.TagText.isdigit():
            return self.TagText
        else:
            return "Component"

    def __repr__(self):
        return '<MsgContent %s>' % self.pretty_name()


class Component:
    def parse_value(self, tag, text):
        if tag == 'NotReqXML':
            text = bool(int(text))
        elif tag == 'ComponentID':
            text = int(text)
        setattr(self, tag, text)

    def pretty_name(self):
        return self.Name

    def pretty_type(self):
        return "Component"

    def __repr__(self):
        return '<Component %s>' % self.pretty_name()


class Field:
    # TODO: added/deprecated
    # <Field added="FIX.2.7" deprecated="FIXT.1.1">

    def parse_value(self, tag, text):
        if tag == 'NotReqXML':
            text = bool(int(text))
        setattr(self, tag, text)

    def __repr__(self):
        return '<Field %s>' % self.Name
