from jinja2 import Environment
from j2tools import YamlLoader


jinja = Environment(loader=YamlLoader('templates.yml'))
