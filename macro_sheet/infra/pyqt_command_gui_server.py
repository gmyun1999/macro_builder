from macro_sheet.service.i_command_gui_server.i_command_gui_server import (
    ICommandGuiServer,
)


class PyQtCommandGuiServer(ICommandGuiServer):
    def __init__(self):
        pass

    def send_total_script_to_command_gui(self):
        """
        나중에 데스크톱 앱이 생성이되면 패키징 서버가 아닌 데스크톱 앱으로 직접 스크립트를 보내야함.
        """
        pass
