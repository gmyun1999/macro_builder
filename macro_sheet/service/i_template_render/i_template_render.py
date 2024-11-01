from abc import ABC, abstractmethod


class ITemplateRender(ABC):
    @abstractmethod
    def render_main_template(self, python_script: str) -> str:
        pass
