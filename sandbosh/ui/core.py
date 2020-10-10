import tkinter as tk
from tkinter import ttk


class ShellUI(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # ウィンドータイトル
        self.master.title('SandBosh')

        # 初期画面の大きさ
        self.master.geometry('1000x600')

        # 背景色
        self.master.configure(background='black')

        self.pack()

        # コマンド入力用のラインを1行作成
        self.create_shell_line()

    # コマンド入力用のラインを1行作成
    def create_shell_line(self, i=1):
        def enter_key_handler(event):
            if (len(self.input_line.get().strip()) != 0):
                print(self.input_line.get().strip())
                self.input_line.configure(state='readonly')
                self.create_shell_line(i+1)

        def any_key_handler(event):
            self.input_line.focus_force()

        self.doller_mark = ttk.Label(self, text="$ ", font=("", 30))
        self.doller_mark.grid(row=i, column=1)

        self.input_line = ttk.Entry(self,  font=("", 30))
        self.input_line.bind('<Return>', enter_key_handler)
        self.input_line.bind('<KeyPress>', any_key_handler)
        self.input_line.grid(row=i, column=2)

        # カーソルを強制的に合わせる
        self.input_line.focus_force()


def ready_shell_ui():
    root = tk.Tk()
    app = ShellUI(master=root)
    app.mainloop()
