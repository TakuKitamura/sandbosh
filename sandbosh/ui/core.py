# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkfont
from typing import Any, NewType, Tuple, List

# pylanceの設定
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false

# CreateWindow関数の返り値用の型
CreateWindowID = NewType('CreateWindowID', int)


class ShellUI(tk.Frame):
    """
        ShellのUI用のクラス
    """

    def __init__(self, root: tk.Tk):
        """
         クラスの初期化関数
        """

        super().__init__(root)
        self.window_width: int = 1000
        self.window_height: int = 600

        self.doller_mark_font: tkfont.Font = tkfont.Font(
            family='Monaco', size=35, weight='normal')
        self.input_line_font: tkfont.Font = tkfont.Font(
            family='Monaco', size=35, weight='normal')
        self.std_font: tkfont.Font = tkfont.Font(
            family='Monaco', size=35, weight='normal')

        self.comman_list: List[str] = []

        # 一番後ろ側の画面
        self.root: tk.Tk = self.setup_root(root)

        # rootの上にのる画面
        self.canvas: tk.Canvas = self.setup_canvas(self.root)

        # キャンバスがEnterもしくは, 文字列の折り返しによりcanvasの行数が増えた場合を検知するために利用
        # キャンバスの高さ
        self.canvas_height = self.canvas.winfo_height()

        # canvasの上にのるスクロールバー
        self.scrollbar: tk.Scrollbar = self.setup_scrollbar(self.canvas)

        # canvasの上にのるスクロール可能な画面
        self.scrollable_frame: tk.Frame = self.setup_scrollable_frame(
            self.canvas)

        self.scrollable_frame_window: CreateWindowID = self.setup_scrollable_frame_window(
            self.canvas, self.scrollable_frame)

        # コマンド入力用のラインを1行作成
        self.doller_mark: tk.Label = self.setup_doller_mark(
            self.scrollable_frame)
        self.input_line: tk.Text = self.setup_input_line(
            self.canvas, self.scrollable_frame)

        self.std: tk.Text = self.setup_std(self.scrollable_frame)

    def setup_root(self, root: tk.Tk) -> tk.Tk:
        """
        基礎画面のためのセットアップ関数
        """

        # ウィンドータイトル
        root.title('SandBosh')

        # 初期画面の大きさ
        root.geometry('{}x{}'.format(
            self.window_width, self.window_height))

        root.configure(background='blue')

        # 画面サイズの変更に合わせて拡張させる
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        return root

    def setup_canvas(self, root: tk.Tk) -> tk.Canvas:
        """
        キャンバスのためのセットアップ関数
        """
        # 基本的なパーツを載せるキャンバス
        canvas: tk.Canvas = tk.Canvas(
            root, background='green', borderwidth=0, highlightthickness=0, width=self.window_width, height=self.window_height)

        # 画面サイズの変更に合わせて拡張させ, 配置
        canvas.grid_rowconfigure(0, weight=1)
        canvas.grid_columnconfigure(0, weight=1)
        canvas.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        return canvas

    def setup_scrollbar(self, canvas: tk.Canvas) -> tk.Scrollbar:
        """
        スクロールバーのためのセットアップ関数
        """

        scrollbar: tk.Scrollbar = tk.Scrollbar(
            canvas, orient=tk.VERTICAL, command=canvas.yview
        )

        def on_mousewheel_callback(event: tk.Event):
            """
            マウスホイールで入力されたときに呼び出される関数
            """

            # 現在のスクロールバーの位置を更新
            scrollbar_pos: Tuple[float, float] = scrollbar.get()
            scrollbar.set(scrollbar_pos[0], scrollbar_pos[1])

            # スクロールが必要になるまでスクロールさせないための条件
            if (scrollbar_pos[0] != 0.0 or scrollbar_pos[1] != 1.0):
                # TODO: Mac以外も動作するようにする
                canvas.yview_scroll(-1*event.delta, tk.UNITS)
        canvas.bind_all("<MouseWheel>", on_mousewheel_callback)

        # スクロールバーとキャンバスを連携
        canvas.configure(yscrollcommand=scrollbar.set)
        return scrollbar

    def setup_scrollable_frame(self, canvas: tk.Canvas) -> tk.Frame:
        """
        スクロールできるフレームのためのセットアップ関数
        """
        scrollable_frame: tk.Frame = tk.Frame(
            canvas, background='red', width=self.window_width, height=self.window_height)

        # 画面サイズの変更に合わせて拡張させ, 配置
        scrollable_frame.grid_rowconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(2, weight=1)
        return scrollable_frame

    def setup_scrollable_frame_window(self, canvas: tk.Canvas, scrollable_frame: tk.Frame) -> CreateWindowID:
        """
        スクロールできるフレーム画面のためのセットアップ関数
        """

        scrollable_frame_window: CreateWindowID = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor=tk.N+tk.W)

        def canvas_configure_callback(event: tk.Event):
            """
            キャンバスが更新されるタイミングで呼び出される関数
            """
            # キャンバスのText子要素を取得し, 画面サイズに合わせて文字列を折り返す
            wigetd_children: List[Any] = scrollable_frame.winfo_children()
            i = 0
            for v in wigetd_children:
                if (v.winfo_class() == 'Text'):
                    text_child: tk.Text = v

                    # テキストのは場をWindowのは場に合わせて折り返す
                    line_count: int = text_child.count(
                        '1.0', tk.END, 'update', 'displaylines')
                    text_child.configure(height=line_count)
                    i += 1
            canvas.itemconfig(
                scrollable_frame_window, width=canvas.winfo_width())

            # スクロール範囲を更新
            canvas_pos: Tuple[int, int, int, int] = canvas.bbox('all')
            canvas.configure(scrollregion=canvas_pos)

            # キャンバスがEnterもしくは, 文字列の折り返しによりcanvasの行数が増えた場合に画面下部にスクロール
            if (self.canvas_height != event.height):
                # キャンバス最下部にスクロール
                canvas.yview_moveto(event.height)
                # キャンバスの高さを更新
                self.canvas_height = event.height

        scrollable_frame.bind('<Configure>', canvas_configure_callback)
        return scrollable_frame_window

    def setup_doller_mark(self, scrollable_frame: tk.Frame, i: int = 1) -> tk.Label:
        """
        コマンド入力のためのテキストエリアの一番左にあるドルマークのセットアップ関数
        """
        doller_mark: tk.Label = tk.Label(
            scrollable_frame, text='$', foreground='orange', background='black', borderwidth=0, font=self.doller_mark_font)

        # 画面サイズの変更に合わせて拡張させ, 配置
        doller_mark.grid(row=i, column=1, padx=0, sticky=tk.N)
        return doller_mark

    def setup_input_line(self, canvas: tk.Canvas, scrollable_frame: tk.Frame, i: int = 1) -> tk.Text:
        """
        コマンド入力のためのテキストエリアのセットアップ関数
        """
        input_line: tk.Text = tk.Text(
            scrollable_frame, wrap=tk.CHAR, height=1, foreground='white', background='purple', borderwidth=0, highlightthickness=0, selectbackground='skyblue', selectforeground='black', takefocus=True, font=self.input_line_font, pady=1, insertwidth=1, padx=10)

        # 画面サイズの変更に合わせて拡張させ, 配置
        input_line.grid(row=i, column=2, sticky=tk.E+tk.W)

        # カーソルを強制的に合わせる
        input_line.focus_force()

        def enter_key_callback(event: tk.Event):
            """
            Enter keyが押された際に呼び出される関数
            """
            # 末尾の改行は除く
            line: str = input_line.get('1.0', tk.END).strip()

            # コマンドの入力内容を標準出力
            print("command: '{}'".format(line))

            if len(line) > 0:
                self.comman_list.append(line)

            # 既に入力済みのテキストエリアを編集不可に変更
            input_line.configure(state=tk.DISABLED)

            self.std = self.setup_std(scrollable_frame, i+1)

            # TODO: ここでたぶんForkする
            self.std.insert('1.0', input())

            # 次のコマンド入力ラインを表示
            self.setup_doller_mark(scrollable_frame, i+2)
            self.setup_input_line(canvas, scrollable_frame, i+2)

            # キャンバスがEnterもしくは, 文字列の折り返しによりcanvasの行数が増えた場合を検知するために利用
            self.canvas_height = canvas.winfo_height()

        def key_callback(event: tk.Event):
            """
            keyが押された際に呼び出される関数
            """
            # 画面外に入力欄がある場合に, 最下部にスクロール
            canvas_height: int = canvas.winfo_height()
            canvas.yview_moveto(canvas_height)

        def input_key_release_callback(event: tk.Event):
            """
            keyを離した際に呼び出される関数
            """
            # 文字列を折り返すときに, コマンド入力エリアを1行追加
            line_count: int = input_line.count(
                '1.0', tk.END, 'update', 'displaylines')
            input_line.configure(height=line_count)

        input_line.bind('<Return>', enter_key_callback)
        input_line.bind('<Key>', key_callback)
        input_line.bind('<KeyRelease>', input_key_release_callback)
        return input_line

    def setup_std(self, scrollable_frame: tk.Frame, i: int = 1) -> tk.Text:
        std: tk.Text = tk.Text(
            scrollable_frame, wrap=tk.CHAR, height=1, foreground='white', background='gray', borderwidth=0, highlightthickness=0, selectbackground='skyblue', selectforeground='black', takefocus=True, font=self.std_font, pady=1, insertwidth=1, padx=10)

        # 初期化時は表示しない
        if i != 1:
            # 画面サイズの変更に合わせて拡張させ, 配置
            std.grid(row=i, column=2, sticky=tk.E+tk.W)

        def std_configure_callback(event: tk.Event):
            """
            stdのエリアが更新されたときに呼び出される関数
            """
            # insertに合わせて行数を更新
            line_count: int = std.count(
                '1.0', tk.END, 'update', 'displaylines')
            std.configure(height=line_count)
        std.bind('<Configure>', std_configure_callback)

        return std


def ready_shell_ui() -> None:
    """
    UIを呼び出す関数
    """
    root: tk.Tk = tk.Tk()
    app: ShellUI = ShellUI(root)

    # 画面を表示させたまま無限ループ
    app.mainloop()
