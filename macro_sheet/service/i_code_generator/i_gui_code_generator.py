from abc import ABC, abstractmethod


class IGuiCodeGenerator(ABC):
    @abstractmethod
    def generate_gui_code(self):
        # 워크시트 소스코드 받아서 최종적으로 gui 코드를 반환해야함
        pass
