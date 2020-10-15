# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkfont


class ShellUI(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.window_width = 1000
        self.window_height = 600

        # ウィンドータイトル
        self.root.title('SandBosh')

        # 初期画面の大きさ
        self.root.geometry('{}x{}'.format(
            self.window_width, self.window_height))

        self.root.configure(background='blue')

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        def root_configure(event):
            self.input_line.configure(height=self.get_input_line_count())
            self.canvas.itemconfig(
                self.create_scrollable_frame, width=self.root.winfo_width())

        self.root.bind('<Configure>', root_configure)

        self.font = tk.font.Font(family='Consolas', size=30, weight='normal')

        # 基本的なパーツを載せるキャンバス
        self.canvas = tk.Canvas(
            self.root, background='green', borderwidth=0, highlightthickness=0, width=self.window_width, height=self.window_height)

        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)

        # キャンバスの高さ
        self.canvas_height = 0

        # キャンバスが更新されるタイミング
        def canvas_configure(event):
            # キャンバスがEnterもしくは, 文字列の折り返しによりcanvasの行数が増えた場合
            if (self.canvas_height != event.height):
                self.canvas.configure(scrollregion=self.canvas.bbox('all'))
                self.canvas.yview_moveto(event.height)
                self.canvas_height = event.height

        def on_mousewheel(event):
            # 現在のスクロールバーの位置
            scrollbar_pos = self.scrollbar_y.get()
            self.scrollbar_y.set(scrollbar_pos[0], scrollbar_pos[1])

            # スクロールが必要になるまでスクロールさせないための条件
            if (scrollbar_pos[0] != 0.0 or scrollbar_pos[1] != 1.0):
                # TODO: Mac以外も動作するようにする
                self.canvas.yview_scroll(-1*event.delta, "units")

        # スクロールできるフレーム
        self.scrollable_frame = tk.Frame(
            self.canvas, background='red', width=self.window_width, height=self.window_height)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(2, weight=1)

        self.scrollable_frame.bind('<Configure>', canvas_configure)
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)

        self.create_scrollable_frame = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor=tk.N+tk.W)

        self.scrollbar_y = tk.Scrollbar(
            self.root, orient=tk.VERTICAL, command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # コマンド入力用のラインを1行作成
        self.create_shell_line()

        # スクロールバーと, キャンバスを描写
        self.scrollbar_y.grid(row=0, column=1, sticky=tk.S+tk.N)
        self.canvas.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

    def get_input_line(self):
        return self.input_line.get('1.0', tk.END).strip()

    def get_input_line_count(self):
        return self.input_line.count('1.0', tk.END, 'update', 'displaylines')

    # コマンド入力用のラインを1行作成する関数
    def create_shell_line(self, i=1, noWidget=False):
        def enter_key_handler(event):
            # 末尾の改行は除く
            line = self.get_input_line()
            print("command: '{}'".format(line))
            self.input_line.configure(state=tk.DISABLED)
            self.create_shell_line(i+1)
            self.canvas.yview_moveto(self.canvas.winfo_height())

        def input_key_press_handler(event):
            # pass
            self.canvas.yview_moveto(self.canvas.winfo_height())

        def input_key_release_handler(event):
            # 文字列を折り返すときに, コマンド入力エリアを1行追加
            self.input_line.configure(height=self.get_input_line_count())

            # 画面のふちまで文字列が埋まり, 行数が増加する前のキャンバスの高さ
            self.canvas_height = self.canvas.winfo_height()

        self.doller_mark = tk.Label(
            self.scrollable_frame, text='$', foreground='orange', background='black', borderwidth=0, font=self.font)
        self.doller_mark.grid(row=i, column=1, sticky=tk.N, padx=0)

        self.input_line = tk.Text(
            self.scrollable_frame, wrap=tk.CHAR, height=1, foreground='white', background='purple', borderwidth=0, highlightthickness=0, selectbackground='skyblue', selectforeground='black', takefocus=True, font=self.font, padx=0, pady=1, insertwidth=1, autoseparators=0)

        self.input_line.bind('<Return>', enter_key_handler)
        self.input_line.bind('<KeyPress>', input_key_press_handler)
        self.input_line.bind('<KeyRelease>', input_key_release_handler)

        self.input_line.grid(row=i, column=2, sticky=tk.E+tk.W)

        # カーソルを強制的に合わせる
        self.input_line.focus_force()


def ready_shell_ui():
    root = tk.Tk()
    app = ShellUI(root=root)
    app.mainloop()
