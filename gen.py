from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)


def render_messages(base_path, messages, lookup):
    template = env.get_template('messages.html')

    import os
    path = os.path.join(base_path, 'messages')
    os.makedirs(path, exist_ok=True)

    for message in messages:
        with open(os.path.join(path, '{}.html'.format(message.MsgType)), 'w', encoding='utf-8') as outfile:
            result = template.render(message=message, lookup=lookup)
            outfile.write(result)
