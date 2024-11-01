import os

from jinja2 import Environment, FileSystemLoader

from macro_be import settings
from macro_sheet.service.i_template_render.i_template_render import ITemplateRender


class Jinja2TemplateRender(ITemplateRender):
    template_dir = os.path.join(settings.BASE_DIR, "macro_sheet", "infra", "templates")
    env = Environment(loader=FileSystemLoader(template_dir))

    def render_main_template(self, python_script: str) -> str:
        """
        main.py.jinja 템플릿을 렌더링하여 GUI 코드 문자열을 반환합니다.
        :param python_script: GUI에서 실행할 Python 스크립트 문자열
        :return: 렌더링된 GUI 코드 문자열
        """
        template = self.env.get_template("main.py.j2")
        return template.render(python_script=python_script)
