from macro_sheet.service.i_code_generator.i_gui_code_generator import IGuiCodeGenerator


class GuiCodeGenerator(IGuiCodeGenerator):
    def __init__(self):
        pass

    def generate_gui_code(self):
        # GUI 코드 시작 부분 (예시로 만든거임)
        gui_code = """
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

class MacroApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Macro Runner")
        self.file_path = ""

    def select_file(self):
        self.file_path = filedialog.askdirectory(title="Select a Directory")
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, self.file_path)

    def start_macro(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "파일 경로를 선택하세요.")
            return
        self.run_macro()

    def run_macro(self):
        def task():
            # 여기에 블록 코드가 삽입됩니다
            {{ block_code }}
        threading.Thread(target=task).start()

    def create_widgets(self):
        self.file_entry = tk.Entry(self.root, width=50)
        self.file_entry.pack(padx=10, pady=5)

        file_button = tk.Button(self.root, text="파일 선택", command=self.select_file)
        file_button.pack(padx=10, pady=5)

        start_button = tk.Button(self.root, text="시작", command=self.start_macro)
        start_button.pack(padx=10, pady=5)

    def run(self):
        self.create_widgets()
        self.root.mainloop()

if __name__ == "__main__":
    app = MacroApp()
    app.run()
"""
        # 블록 코드 생성 및 삽입
        # block_code = "\n".join(
        #     self.block_generator.generate_block_code(block)
        #     for worksheet in workflow.worksheets
        #     for block in worksheet.blocks
        # )
        # full_gui_code = gui_code.replace("{{ block_code }}", block_code)
        # return full_gui_code
