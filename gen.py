from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)


class Stylify:
    @staticmethod
    def linkify(obj):
        if obj.pretty_type().isdigit():
            return "../{}/{}.html".format('fields', obj.pretty_name())
        return "../{}s/{}.html".format(obj.pretty_type().lower(), obj.pretty_name())

    @staticmethod
    def boldify(obj, text):
        if obj.pretty_type() == 'Component':
            return "<b>{}</b>".format(text)
        else:
            return text


def render_pages(base_path, subdir, messages, lookup):
    template = env.select_template([subdir+'.html', 'messages.html'])

    import os
    path = os.path.join(base_path, subdir)
    os.makedirs(path, exist_ok=True)

    for message in messages:
        filename = '{}.html'.format(message.filename())
        with open(os.path.join(path, filename), 'w', encoding='utf-8') as outfile:
            result = template.render(message=message, lookup=lookup, stylify=Stylify)
            outfile.write(result)
