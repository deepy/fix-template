from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)


class Stylify:
    def __init__(self, conf):
        self.conf = conf

    def linkify(self, obj):
        return "../{}.html".format(self.conf.get_http_path(obj))

    def boldify(self, obj, text):
        if obj.pretty_type() == 'Component':
            return "<b>{}</b>".format(text)
        else:
            return text


def fiximate(conf, subdir, messages, lookup, repo, copyright=None):
    template = env.select_template([subdir+'.html', 'messages.html'])

    import os
    path = conf.get_paths(subdir)
    os.makedirs(path, exist_ok=True)

    stylify = Stylify(conf)

    for message in messages:
        filename = '{}.html'.format(conf.get_filename(message))
        with open(os.path.join(path, filename), 'w', encoding='utf-8') as outfile:
            result = template.render(message=message, lookup=lookup, stylify=stylify, copyright=copyright, repository=repo)
            outfile.write(result)
