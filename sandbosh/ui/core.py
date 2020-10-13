# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkfont

WIDTH = 1000
HEIGHT = 600


class ShellUI(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root

        # ウィンドータイトル
        self.root.title('SandBosh')

        # 初期画面の大きさ
        self.root.geometry('{}x{}'.format(WIDTH, HEIGHT))

        self.root.configure(background='black')

        self.font = tk.font.Font(family='Consolas', size=30, weight='normal')

        # 基本的なパーツを載せるキャンバス
        self.canvas = tk.Canvas(
            self.root, background='black', borderwidth=0, highlightthickness=0)

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
            # TODO: Mac以外も動作するようにする

            # Mac
            self.canvas.yview_scroll(-1*event.delta, "units")

        # スクロールできるフレーム
        self.scrollable_frame = tk.Frame(self.root)
        self.scrollable_frame.bind('<Configure>', canvas_configure)
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)

        self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor='nw')

        self.scroll_y = tk.Scrollbar(
            self.root, orient='vertical', command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        # コマンド入力用のラインを1行作成
        self.create_shell_line()

        # スクロールバーと, キャンバスを描写
        self.scroll_y.pack(side=tk.RIGHT, fill='y')
        self.canvas.pack(side=tk.LEFT, fill='both', expand=True)

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
            self.input_line.configure(state='disabled')
            self.create_shell_line(i+1)

        def input_key_press_handler(event):
            pass

        def input_key_release_handler(event):
            # 文字列を折り返すときに, コマンド入力エリアを1行追加
            self.input_line.configure(height=self.get_input_line_count())

            # 画面のふちまで文字列が埋まり, 行数が増加する前のキャンバスの高さ
            self.canvas_height = self.canvas.bbox('all')[3]

        self.doller_mark = tk.Label(
            self.scrollable_frame, text='$', foreground='white', background='black', borderwidth=0, font=self.font)
        self.doller_mark.grid(row=i, column=1, sticky=tk.N, padx=0)

        self.input_line = tk.Text(
            self.scrollable_frame, wrap=tk.CHAR, height=1, width=(WIDTH//self.font.measure('A'))+1, foreground='white', background='black', borderwidth=0, highlightthickness=0, selectbackground='skyblue', selectforeground='black', takefocus=True, font=self.font, padx=0, pady=1, insertwidth=1, autoseparators=0)

        self.input_line.bind('<Return>', enter_key_handler)
        self.input_line.bind('<KeyPress>', input_key_press_handler)
        self.input_line.bind('<KeyRelease>', input_key_release_handler)
        self.input_line.grid(row=i, column=2)

        # カーソルを強制的に合わせる
        self.input_line.focus_force()


def ready_shell_ui():
    root = tk.Tk()
    app = ShellUI(root=root)
    app.mainloop()
