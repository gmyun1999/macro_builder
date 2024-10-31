import os

from jinja2 import Environment, FileSystemLoader

from macro_be import settings
from macro_sheet.service.i_template_render.i_template_render import ITemplateRender


class Jinja2TemplateRender(ITemplateRender):
    template_dir = os.path.join(settings.BASE_DIR, "macro_sheet", "infra", "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
