from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('messages.html')


def render(messages, lookup):
    with open('out/messages.html', 'w') as outfile:
        result = template.render(messages=messages, lookup=lookup)
        outfile.write(result)
        # print("\n".join([s for s in result.split("\n") if s]))
