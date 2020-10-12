# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkfont
import math

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

        self.font = tk.font.Font(family='Consolas', size=30, weight='normal')

        # 基本的なパーツを載せるキャンバス
        self.canvas = tk.Canvas(
            self.root, background='black', borderwidth=0, highlightthickness=0)

        # スクロールできるフレーム
        self.scrollable_frame = tk.Frame(self.root)
        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox('all')
            )
        )

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
        self.input_line.after(100, self.welcome_message)

    def welcome_message(self):
        self.input_line.insert(1.0, '@Rinzler: the only documentation that would be useful is the tcl/tk documentation. When you call call, it literally just directly translates the arguments to a tcl command (tcl statements are simply lists made up of a command and zero or more arguments). tcl.tk/man – Bryan Oakley Mar 18 \'15 at 18: 12')
        self.input_line.configure(height=self.get_input_line_count())

        self.input_line.configure(state='disabled')
        self.create_shell_line(2)

    def get_input_line(self):
        return self.input_line.get('1.0', tk.END).strip()

    def get_input_line_count(self):
        return self.input_line.count('1.0', tk.END, 'update', 'displaylines')

    # コマンド入力用のラインを1行作成する関数
    def create_shell_line(self, i=1, noWidget=False):
        def enter_key_handler(event):
            # 末尾の改行は除く
            line = self.get_input_line()
            if (len(line) != 0):
                print(line)
                self.input_line.configure(state='disabled')
                self.create_shell_line(i+1)

        def input_key_release_handler(event):
            if event.keysym != 'Return':
                self.input_line.configure(height=self.get_input_line_count())

        self.doller_mark = tk.Label(
            self.scrollable_frame, text='$', foreground='white', background='black', borderwidth=0, font=self.font)
        self.doller_mark.grid(row=i, column=1, sticky=tk.N)

        self.input_line = tk.Text(
            self.scrollable_frame, wrap=tk.CHAR, height=1, width=(WIDTH//self.font.measure('A'))+1, foreground='white', background='black',   insertbackground='white', borderwidth=0, highlightthickness=0, selectbackground='skyblue', selectforeground='black', takefocus=False, font=self.font, padx=0, pady=0, insertwidth=0, autoseparators=0)

        self.input_line.bind('<Return>', enter_key_handler)
        self.input_line.bind('<KeyRelease>', input_key_release_handler)
        self.input_line.bind('')
        self.input_line.grid(row=i, column=2)

        # カーソルを強制的に合わせる
        self.input_line.focus_force()


def ready_shell_ui():
    root = tk.Tk()
    app = ShellUI(root=root)
    app.mainloop()
