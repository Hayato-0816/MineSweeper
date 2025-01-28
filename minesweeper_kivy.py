from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
import random

# 日本語フォントの登録
LabelBase.register(name='ZenKakuGothicNew',
                fn_regular='./font/ZenKakuGothicNew-Regular.ttf')

class MinesweeperGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.setup_default_values()
        self.create_settings_ui()
        
    def setup_default_values(self):
        """デフォルト値の設定"""
        self.default_rows = "15"
        self.default_cols = "15"
        self.default_mines = "10"
        
    def create_settings_ui(self):
        """設定UI作成"""
        # 設定部分のレイアウト
        settings = BoxLayout(size_hint_y=0.1)
        
        # 行数設定
        settings.add_widget(Label(text='行数:', font_name='ZenKakuGothicNew'))
        self.rows_input = TextInput(
            text=self.default_rows,
            multiline=False,
            size_hint_x=0.2
        )
        settings.add_widget(self.rows_input)
        
        # 列数設定
        settings.add_widget(Label(text='列数:',font_name='ZenKakuGothicNew'))
        self.cols_input = TextInput(
            text=self.default_cols,
            multiline=False,
            size_hint_x=0.2
        )
        settings.add_widget(self.cols_input)
        
        # 地雷数設定
        settings.add_widget(Label(text='地雷数:',font_name='ZenKakuGothicNew'))
        self.mines_input = TextInput(
            text=self.default_mines,
            multiline=False,
            size_hint_x=0.2
        )
        settings.add_widget(self.mines_input)
        
        # スタートボタン
        start_button = Button(
            text='ゲーム開始',
            font_name='ZenKakuGothicNew',
            size_hint_x=0.3,
            on_press=self.start_game
        )
        settings.add_widget(start_button)
        
        self.add_widget(settings)
        
        # ゲーム盤用のコンテナ
        self.game_container = BoxLayout(orientation='vertical')
        self.add_widget(self.game_container)

    def start_game(self, instance):
        """ゲーム開始"""
        try:
            self.rows = int(self.create_settings_ui().rows_input.text)
            self.cols = int(self.create_settings_ui().cols_input.text)
            self.mines = int(self.create_settings_ui().mines_input.text)
            
            if not self.validate_settings():
                return
                
            self.create_game_board()
            
        except ValueError:
            self.show_error("数値を正しく入力してください")

    def validate_settings(self):
        """設定値の妥当性チェック"""
        if self.rows < 5 or self.cols < 5:
            self.show_error("行数と列数は5以上にしてください")
            return False
        if self.rows > 30 or self.cols > 50:
            self.show_error("行数は30以下、列数は50以下にしてください")
            return False
        if self.mines >= (self.rows * self.cols):
            self.show_error("地雷の数が多すぎます")
            return False
        return True

    def create_game_board(self):
        """ゲーム盤の作成"""
        self.game_container.clear_widgets()
        
        # ゲーム盤の初期化
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.buttons = [[None] * self.cols for _ in range(self.rows)]
        
        # 地雷の配置
        self.place_mines()
        
        # ボタングリッドの作成
        board = GridLayout(cols=self.cols, size_hint_y=0.9)
        for r in range(self.rows):
            for c in range(self.cols):
                btn = MineButton(
                    row=r,
                    col=c,
                    size_hint=(None, None),
                    size=(40, 40),
                    background_color=(0.6, 0.6, 0.6, 1)
                )
                btn.bind(on_release=self.on_button_click)
                btn.bind(on_right_click=self.on_right_click)
                self.buttons[r][c] = btn
                board.add_widget(btn)
        
        self.game_container.add_widget(board)
        
        # リトライボタン
        retry_button = Button(
            text='リトライ',
            size_hint_y=0.1,
            on_press=self.start_game
        )
        self.game_container.add_widget(retry_button)


    def show_error(self, message):
        """エラーポップアップ表示"""
        popup = Popup(
            title='エラー',
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

    def show_message(self, title, message):
        """メッセージポップアップ表示"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()







    def place_mines(self):
        """地雷の配置とマス目の数字設定"""
        # 地雷をランダムに配置
        mine_count = 0
        while mine_count < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.grid[r][c] != -1:
                self.grid[r][c] = -1
                mine_count += 1
        
        # 周囲の地雷数を計算
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] != -1:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if 0 <= r+dr < self.rows and 0 <= c+dc < self.cols:
                                if self.grid[r+dr][c+dc] == -1:
                                    count += 1
                    self.grid[r][c] = count

    def on_button_click(self, button):
        """マス目をクリックした時の処理"""
        r, c = button.row, button.col
        
        # 地雷をクリックした場合
        if self.grid[r][c] == -1:
            button.text = '💣'
            button.background_color = (1, 0, 0, 1)  # 赤色
            self.show_message('ゲームオーバー', '地雷を踏みました！')
            return
            
        # 数字のマスをクリックした場合
        if self.grid[r][c] > 0:
            button.text = str(self.grid[r][c])
            button.background_color = (0.8, 0.8, 0.8, 1)
            button.disabled = True
            return
            
        # 空白マスをクリックした場合（周囲の空白マスも開く）
        self.reveal_empty_cells(r, c)

    def on_right_click(self, button):
        """右クリックで旗を立てる処理"""
        if button.text == '🚩':
            button.text = ''
        else:
            button.text = '🚩'

    def reveal_empty_cells(self, row, col):
        """空白マスとその周囲を開く"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
            
        button = self.buttons[row][col]
        if button.disabled:
            return
            
        button.disabled = True
        button.background_color = (0.8, 0.8, 0.8, 1)
        
        if self.grid[row][col] > 0:
            button.text = str(self.grid[row][col])
            return
            
        # 周囲のマスも開く
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                self.reveal_empty_cells(row + dr, col + dc)


# カスタムボタンクラス（右クリック対応）
class MineButton(Button):
    def __init__(self, row, col, **kwargs):
        super().__init__(**kwargs)
        self.row = row
        self.col = col
        self.register_event_type('on_right_click')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'right':
                self.dispatch('on_right_click')
                return True
        return super().on_touch_down(touch)

    def on_right_click(self):
        pass

class MinesweeperApp(App):
    def build(self):
        return MinesweeperGame()

if __name__ == '__main__':
    MinesweeperApp().run()