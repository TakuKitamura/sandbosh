# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkfont
import math

WIDTH = 1000
HEIGHT = 600


class ExpandoText(tk.Text):
    def insert(self, *args, **kwargs):
        result = tk.Text.insert(self, *args, **kwargs)
        self.reset_height()
        return result

    def reset_height(self):
        height = self.tk.call(
            (self._w, "count", "-update", "-displaylines", "1.0", "end"))
        print(height)
        self.configure(height=height)


class ShellUI(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root

        # ウィンドータイトル
        self.root.title('SandBosh')

        # 初期画面の大きさ
        self.root.geometry('{}x{}'.format(WIDTH, HEIGHT))

        self.font = tk.font.Font(family="Consolas", size=30, weight="normal")

        # 基本的なパーツを載せるキャンバス
        self.canvas = tk.Canvas(
            self.root, background='black', borderwidth=0, highlightthickness=0)

        # スクロールできるフレーム
        self.scrollable_frame = tk.Frame(self.root)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw")

        self.scroll_y = tk.Scrollbar(
            self.root, orient="vertical", command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # コマンド入力用のラインを1行作成
        self.create_shell_line()

        # スクロールバーと, キャンバスを描写
        self.scroll_y.pack(side=tk.RIGHT, fill="y")
        self.canvas.pack(side=tk.LEFT, fill="both", expand=True)

    # コマンド入力用のラインを1行作成する関数
    def create_shell_line(self, i=1):
        def enter_key_handler(event):
            if (len(self.input_line.get('1.0', 'end -1c').strip()) != 0):

                print(self.input_line.get('1.0', 'end -1c').strip())
                self.input_line.configure(state='disabled')
                self.create_shell_line(i+1)

        def any_key_handler(event):
            self.input_line.focus_force()

        def keyRelease(event):
            self.input_line['height'] = self.tk.call((self.input_line, "count", "-update",
                                                      "-displaylines", "1.0", "end"))

        self.doller_mark = tk.Label(
            self.scrollable_frame, text="$", foreground='white', background='black', borderwidth=0, font=self.font)
        self.doller_mark.grid(row=i, column=1, sticky=tk.N)

        self.input_line = tk.Text(
            self.scrollable_frame, wrap=tk.WORD, height=1, width=(WIDTH//self.font.measure('A'))+1, foreground='white', background='black',   insertbackground='white', borderwidth=0, highlightthickness=0, selectbackground='skyblue', selectforeground='black', takefocus=False, font=self.font, padx=0, pady=0, insertwidth=0, autoseparators=0)

        self.input_line.bind('<Return>', enter_key_handler)
        self.input_line.bind('<KeyPress>', any_key_handler)
        self.input_line.bind('<KeyRelease>', keyRelease)
        self.input_line.bind('')
        self.input_line.grid(row=i, column=2)

        # カーソルを強制的に合わせる
        self.input_line.focus_force()


def ready_shell_ui():
    root = tk.Tk()
    app = ShellUI(root=root)
    app.mainloop()
