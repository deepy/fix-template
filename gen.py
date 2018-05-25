from jinja2 import Environment, FileSystemLoader, select_autoescape, evalcontextfilter, Markup


class Stylify:
    def __init__(self, conf):
        self.conf = conf

    @evalcontextfilter
    def linkify(self, eval_ctx, obj):
        result = "../{}.html".format(self.conf.get_http_path(obj))
        if eval_ctx.autoescape:
            return Markup(result)
        return result

    @evalcontextfilter
    def boldify(self, eval_ctx, obj, text):
        if obj.pretty_type() == 'Component':
            result = "<b>{}</b>".format(text)
            if eval_ctx.autoescape:
                return Markup(result)
            return result
        else:
            return text


def fiximate(conf, subdir, messages, lookup, repo, copyright=None):
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html'])
    )

    import os
    path = conf.get_paths(subdir)
    os.makedirs(path, exist_ok=True)

    stylify = Stylify(conf)

    env.filters['boldify'] = stylify.boldify
    env.filters['linkify'] = stylify.linkify

    template = env.select_template([subdir + '.html', 'messages.html'])

    for message in messages:
        filename = '{}.html'.format(conf.get_filename(message))
        with open(os.path.join(path, filename), 'w', encoding='utf-8') as outfile:
            result = template.render(message=message, lookup=lookup, copyright=copyright, repository=repo)
            outfile.write(result)
