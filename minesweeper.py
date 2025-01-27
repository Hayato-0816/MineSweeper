# マインスイーパーゲームの実装
# tkinterを使用してGUIを作成し、ランダムに地雷を配置して遊ぶゲーム
import random  # 地雷をランダムに配置するために使用
import tkinter as tk  # GUIライブラリ

class Minesweeper:
    def __init__(self, master):
        """
        ゲームの初期化を行う
        Parameters:
            master: tkinterのルートウィンドウ
        """
        self.master = master
        self.master.title("マインスイーパー")
        
        self.default_size()
        self.initial_setup()
        self.start_button()
        
        # ゲーム部フレーム
        self.game_frame = tk.Frame(self.master)
        self.game_frame.pack(expand=True)
    
    def default_size(self):
        """ゲームのサイズ設定を行うメソッド"""
        self.default_rows = tk.StringVar(value="15")
        self.default_cols = tk.StringVar(value="15")
        self.default_mines = tk.StringVar(value="10")
    
    def initial_setup(self):
        """ゲームの初期設定を行うメソッド"""
        # 設定用フレーム
        self.settings_frame = tk.Frame(self.master)
        self.settings_frame.pack(pady=10)
        
        # 行数設定
        tk.Label(self.settings_frame, text="行数:").grid(row=0, column=0, padx=5)
        tk.Entry(self.settings_frame, textvariable=self.default_rows, width=5).grid(row=0, column=1)
        
        # 列数設定
        tk.Label(self.settings_frame, text="列数:").grid(row=0, column=2, padx=5)
        tk.Entry(self.settings_frame, textvariable=self.default_cols, width=5).grid(row=0, column=3)
        
        # 地雷数設定
        tk.Label(self.settings_frame, text="地雷数:").grid(row=0, column=4, padx=5)
        tk.Entry(self.settings_frame, textvariable=self.default_mines, width=5).grid(row=0, column=5, padx=5)
        
    def start_button(self):
        """スタートボタン"""
        tk.Button(self.settings_frame, text="ゲーム開始", command=self.start_game).grid(row=1, column=0, columnspan=6, pady=10)

    def start_game(self):
        """設定値を取得してゲームを開始"""
        try:
            # 入力値を取得
            self.rows = int(self.default_rows.get())
            self.cols = int(self.default_cols.get())
            self.mines = int(self.default_mines.get())
            
            self.size_validation()
            self.clear_game()

            # ウィンドウサイズを調整（ボタンサイズに基づいて計算）
            button_size = 30  # ボタンの基本サイズ（ピクセル）
            window_width = self.cols * button_size + 40
            window_height = self.rows * button_size + 100  # 設定部分の高さを考慮
            
            # 画面の中央に表示されるように位置を計算
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            # ウィンドウサイズと位置を設定
            self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.master.resizable(False, False)
            
            # ゲーム盤の初期化
            self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
            
            # メインフレームを作成
            self.frame = tk.Frame(self.game_frame)
            self.frame.pack(expand=True)
            
            # リトライボタン
            self.retry = tk.Button(self.game_frame, text="リトライ", command=self.start_game)
            self.retry.pack(pady=10)
            
            self.setup()  # ゲーム盤のセットアップを実行
            
        except ValueError:
            tk.messagebox.showerror("エラー", "数値を正しく入力してください")

    def clear_game(self):
        """ゲーム盤のクリアを行うメソッド"""
        for widget in self.game_frame.winfo_children():
            widget.destroy()
    
    def size_validation(self):
        """ゲームのサイズ設定の妥当性チェックを行うメソッド"""
        if self.rows < 5 or self.cols < 5:
            tk.messagebox.showerror("エラー", "行数と列数は5以上にしてください")
            return
        if self.rows > 30 or self.cols > 50:
            tk.messagebox.showerror("エラー", "行数は30以下、列数は50以下にしてください")
            return
        if self.mines >= (self.rows * self.cols):
            tk.messagebox.showerror("エラー", "地雷の数が多すぎます")
            return

    def setup(self):
        """ゲーム盤の初期設定を行うメソッド"""
        # 地雷をランダムに配置
        for _ in range(self.mines):
            while True:
                r = random.randint(0, self.rows - 1)  # ランダムな行を選択
                c = random.randint(0, self.cols - 1)  # ランダムな列を選択
                if self.grid[r][c] == 0:  # まだ地雷が置かれていない場合
                    self.grid[r][c] = -1  # 地雷を配置
                    break
                    
        # 各マスの周囲の地雷数を計算
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] != -1:  # 地雷でないマスの場合
                    count = 0
                    # 周囲8マスをチェック
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            # 盤面の範囲内かチェック
                            if 0 <= r+dr < self.rows and 0 <= c+dc < self.cols:
                                if self.grid[r+dr][c+dc] == -1:  # 周囲のマスが地雷の場合
                                    count += 1
                    self.grid[r][c] = count  # 周囲の地雷数を記録

        # GUIのボタンを配置
        for r in range(self.rows):
            for c in range(self.cols):
                # 各マスにボタンを作成
                button = tk.Button(self.frame, width=2, height=1,
                                 command=lambda r=r, c=c: self.click(r, c))  # クリック時の動作を設定
                button.grid(row=r, column=c)  # グリッドレイアウトでボタンを配置
                button.config(bg='#A1A3A6', relief='raised')
                button.bind('<Button-3>', lambda e, r=r, c=c: self.right_click(e, r, c))
                self.buttons[r][c] = button  # ボタンを記録

    def click(self, r, c):
        """
        マスがクリックされた時の処理
        Parameters:
            r: クリックされた行
            c: クリックされた列
        """
        if self.buttons[r][c]['text'] == '🚩':
            return
        
        if self.grid[r][c] == -1:
            # 地雷をクリックした場合
            self.buttons[r][c].config(text='💣', bg='red')  # 地雷を表示して背景を赤く
            self.game_over()  # ゲームオーバー処理を実行
        else:
            # 安全なマスをクリックした場合
            self.reveal(r, c)  # マスを開く
    
    def right_click(self, event, r, c):
        """
        右クリック時の処理（旗を立てる/外す）
        Parameters:
            event: マウスイベント
            r: クリックされた行
            c: クリックされた列
        """
        button = self.buttons[r][c]
        if button['state'] != 'disabled':  # まだ開かれていないマスの場合
            if button['text'] == '🚩':  # 既に旗が立っている場合
                button.config(text='')  # 旗を外す
            else:
                button.config(text='🚩')  # 旗を立てる

    def reveal(self, r, c):
        """
        マスを開く処理（再帰的に空白マスを開く）
        Parameters:
            r: 開くマスの行
            c: 開くマスの列
        """
        # 盤面の範囲外または既に開いているマスの場合は処理しない
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
        if self.buttons[r][c]['state'] == 'disabled':
            return
            
        # マスを開く（ボタンを無効化）
        self.buttons[r][c].config(state='disabled')
        if self.grid[r][c] == 0:
            # 周囲に地雷がない場合
            self.buttons[r][c].config(text='',bg='#E1E1E1', relief='groove')  # 空白を表示
            # 周囲8マスも再帰的に開く
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    self.reveal(r+dr, c+dc)
        else:
            # 周囲に地雷がある場合は数字を表示
            self.buttons[r][c].config(text=str(self.grid[r][c]), bg='#E1E1E1', relief='groove')
        
        self.check_win()

    def game_over(self):
        """ゲームオーバー時の処理（全ての地雷を表示）"""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == -1:  # 地雷のマスを見つけた場合
                    self.buttons[r][c].config(text='💣')  # 地雷を表示

    def check_win(self):
        """ゲームクリア判定を行うメソッド"""
        unopened = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.buttons[r][c]['state'] != 'disabled' and self.grid[r][c] != -1:
                    unopened += 1
        
        if unopened == 0:
            # 地雷以外の全てのマスが開かれた場合
            tk.messagebox.showinfo("ゲームクリア", "おめでとうございます！クリアしました！")

# ゲームの実行
if __name__ == '__main__':
    root = tk.Tk()  # メインウィンドウを作成
    game = Minesweeper(root)  # ゲームインスタンスを作成
    root.mainloop()  # イベントループを開始