from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.core.window import Window

# アプリ起動前に設定
Window.resizable = True

# 日本語フォントの登録
LabelBase.register(name='ZenKakuGothicNew',
                  fn_regular='./font/ZenKakuGothicNew-Regular.ttf')


class TestBox(BoxLayout):
    def __init__(self, **kwargs):
        super(TestBox, self).__init__(**kwargs)
        self.test = BoxLayout(orientation='horizontal')
        self.test.add_widget(Label(text='行数'))
        self.rows = TextInput(text='15')
        self.test.add_widget(self.rows)
        self.test.add_widget(Label(text='列数'))
        self.cols = TextInput(text='15')
        self.test.add_widget(self.cols)
        self.add_widget(self.test)
        self.test.add_widget(Button(text='button', on_press=self.test_button))
    
    def test_button(self, *args):
        print(self.rows.text)
        print(self.cols.text)


class MinesweeperApp(App):
    def build(self):
        return TestBox()


if __name__ == '__main__':
    MinesweeperApp().run()