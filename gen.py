from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('messages.html')


def render(messages, lookup):
    for message in messages:
        with open('out/messages/{}.html'.format(message.MsgType), 'w', encoding='utf-8') as outfile:
            result = template.render(message=message, lookup=lookup)
            outfile.write(result)
