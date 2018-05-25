import models


def is_message(target):
    return isinstance(target, models.Message)


def is_field(target):
    return isinstance(target, models.Field)


def is_component(target):
    if isinstance(target, models.Component):
        return True
    elif hasattr(target, 'TagText') and not target.TagText.isdigit():
        return True
    return False
