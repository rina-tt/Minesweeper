# Minesweeper GUI              
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
import time

MS_SIZE = 8         # ゲーム盤のサイズ
CLOSE, OPEN, FLAG = 0, 1, 2

# ★今までに作成したコードからGameクラスをコピー★

class Game:
    def __init__(self, number_of_mines = 10):
        """ ゲーム盤の初期化
        
        Arguments:
        number_of_mines -- 地雷の数のデフォルト値は10

        Side effects:
        mine_map[][] -- 地雷マップ(-1: 地雷，>=0 8近傍の地雷数)
        game_board[][] -- 盤面 (0: CLOSE(初期状態), 1: 開いた状態, 2: フラグ)

        """
        self.init_game_board()
        self.init_mine_map(number_of_mines)
        self.count_mines()

    def init_game_board(self):
        """ ゲーム盤を初期化 """
        # <-- (STEP 1) ここにコードを追加
        #オプション課題
        self.game_board = [[CLOSE for y in range(MS_SIZE)] for x in range(MS_SIZE)]
        
    def init_mine_map(self, number_of_mines):
        """ 地雷マップ(self->mine_map)の初期化
        Arguments:
        number_of_mines -- 地雷の数
        
        地雷セルに-1を設定する．      
        """
        # <-- (STEP 2) ここにコードを追加        
        #例外処理(地雷の数が負の値)
        if number_of_mines < 0:
            number_of_mines = 0
            
        #例外処理(地雷の数がゲーム盤のサイズより多い)
        if number_of_mines > MS_SIZE*MS_SIZE:
            number_of_mines = MS_SIZE*MS_SIZE
        
        self.mine_map = [[0 for y in range(MS_SIZE)] for x in range(MS_SIZE)]        
        mine = 0
        while mine < number_of_mines:
            y = random.randint(0,MS_SIZE-1)
            x = random.randint(0,MS_SIZE-1)
            #ランダムに選んだマスにまだ地雷が無い
            if self.mine_map[y][x] != -1:
                #地雷を置き、地雷の数を足す
                self.mine_map[y][x] = -1
                mine += 1
                 
    def count_mines(self):
        """ 8近傍の地雷数をカウントしmine_mapに格納 
        地雷数をmine_map[][]に設定する．
        """
        # <-- (STEP 3) ここにコードを追加
        for y in range(MS_SIZE):
            for x in range(MS_SIZE):
                if self.mine_map[y][x] != -1: # mine_map[y][x]が地雷でないとき
                    for i in range(-1,2,1): #-1,0,1
                        for j in range(-1,2,1):
                            if not (y+i<0 or x+j<0 or y+i>MS_SIZE-1 or x+j>MS_SIZE-1) : #端のセルは無視
                                if self.mine_map[y+i][x+j] == -1: #周りに地雷があるとき
                                    self.mine_map[y][x] += 1
                        

    
    def open_cell(self, x, y):
        """ セル(x, y)を開ける
        Arguments:
        x, y -- セルの位置
        
        Returns:
          True  -- 8近傍セルをOPENに設定．
                   ただし，既に開いているセルの近傍セルは開けない．
                   地雷セル，FLAGが設定されたセルは開けない．
          False -- 地雷があるセルを開けてしまった場合（ゲームオーバ）
        """
        # <-- (STEP 4) ここにコードを追加
        
        #フラグのあるセルを指定
        if self.game_board[y][x] == FLAG:
            return True
        
        #地雷があるセルを指定
        if self.mine_map[y][x] == -1: 
            return False
        
        #すでに開いているセルを指定
        if self.game_board[y][x] == OPEN:
            return True       
        
        #セルとその周囲を開く
        self.game_board[y][x] = OPEN
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                if not (y+i<0 or x+j<0 or y+i>MS_SIZE-1 or x+j>MS_SIZE-1) : #端のセルは無視
                    if self.mine_map[y+i][x+j] != -1: #捜査対象が地雷マスでないとき
                        if self.game_board[y+i][x+j] != FLAG: #フラグ状態でないとき
                            self.game_board[y+i][x+j] = OPEN

        return True
    
    def flag_cell(self, x, y):
        """
        セル(x, y)にフラグを設定する，既に設定されている場合はCLOSE状態にする
        """
        # <-- (STEP 5) ここにコードを追加
        if self.game_board[y][x] == FLAG: #すでにフラグの時
            self.game_board[y][x] = CLOSE
        elif self.game_board[y][x] == CLOSE: #しまっているとき
            self.game_board[y][x] = FLAG
            
           
    def is_finished(self):
        """ 地雷セル以外のすべてのセルが開かれたかチェック """
        # <-- (STEP 6) ここにコードを追加
        for y in range(MS_SIZE):
            for x in range(MS_SIZE):
                #地雷セル以外でかつ、開いていないセルを見つけたとき
                if self.mine_map[y][x] != -1 and self.game_board[y][x] != OPEN:
                    return False
                
        return True

        pass

class MyPushButton(QPushButton):
    
    def __init__(self, text, x, y, parent):
        """ セルに対応するボタンを生成 """
        super(MyPushButton, self).__init__(text, parent)
        self.parent = parent
        self.x = x
        self.y = y
        self.setMinimumSize(25, 25)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, 
            QSizePolicy.MinimumExpanding)
        
    def set_bg_color(self, colorname):
        """ セルの色を指定する
        Arguments:
            self
            colorname: 文字列 -- 色名 (例, "white")
        """
        self.setStyleSheet("MyPushButton{{background-color: {}}}".format(colorname))

    def on_click(self):
        """ セルをクリックしたときの動作 """
        # ★以下，コードを追加★
        #Shift同時押しの時 = フラグ立てる
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.parent.game.flag_cell(self.x,self.y)
        else:
            #地雷セル押したとき
            if self.parent.game.open_cell(self.x,self.y) == False:
                QMessageBox.information(self, "Game Over", "ゲームオーバー！")
                self.parent.show_cell_status()
                #地雷表示 and 再挑戦するか否か
                self.parent.result()
            #その他
            else:
                self.parent.game.open_cell(self.x,self.y)
        self.parent.show_cell_status()
        
        #ゲームクリアしているか
        if self.parent.game.is_finished() == True:
            #クリアタイム = 現在時刻 - 開始時刻
            self.clear_time = time.time() - self.parent.start
            QMessageBox.information(self, "Game Clear", "ゲームクリア！(クリアタイム：{:.1f}".format(self.clear_time) + "秒)")
            self.parent.show_cell_status()
            #地雷表示 and 再挑戦するか否か
            self.parent.result()
                    
        pass
            
class MinesweeperWindow(QMainWindow):
    
    def __init__(self):
        """ インスタンスが生成されたときに呼び出されるメソッド """
        super(MinesweeperWindow, self).__init__()
        self.game = Game()
        self.initUI()
        #開始時刻を取得
        self.start = time.time()
    
    def initUI(self):
        """ UIの初期化 """        
        self.resize(500, 500) 
        self.setWindowTitle('Minesweeper')
        
        # ★以下，コードを追加★
        #(1)ステータスバー
        self.statusBar().showMessage("Shift+クリックでフラグをセット")
        
        #(2)ボード構築        
        self.button = [[0 for y in range(MS_SIZE)] for x in range(MS_SIZE)] #8x8初期化
        vbox = QVBoxLayout(spacing = 0) #縦方向
        for y in range(MS_SIZE):
            hbox = QHBoxLayout(spacing = 0) #横方向
            for x in range(MS_SIZE):
                self.button[y][x] = MyPushButton(None,x,y,self)
                self.button[y][x].clicked.connect(self.button[y][x].on_click)  
                hbox.addWidget(self.button[y][x])
            vbox.addLayout(hbox)
            
        container = QWidget()        
        container.setLayout(vbox)
        self.setCentralWidget(container)
        
        self.show_cell_status()
        
        self.show()
    
    def show_cell_status(self):
        """ ゲームボードを表示 """
        # ★以下，コードを追加★
        for y in range(MS_SIZE):
            for x in range(MS_SIZE):
                if self.game.game_board[y][x] == CLOSE:
                    self.button[y][x].set_bg_color("gray")
                    self.button[y][x].setText("x")
                    self.button[y][x].setIcon(QIcon(None))
                elif self.game.game_board[y][x] == OPEN:
                    self.button[y][x].set_bg_color("green")
                    self.button[y][x].setIcon(QIcon(None))
                    num = self.game.mine_map[y][x]
                    if num == 0:
                        self.button[y][x].setText(" ")
                    else:
                        self.button[y][x].setText(str(num))
                        self.button[y][x].setFont(QFont("Times", 12, QFont.Bold))
                    #空きセルが爆弾の時
                    if self.game.mine_map[y][x] == -1:
                        self.button[y][x].set_bg_color("green")
                        self.button[y][x].setIcon(QIcon('bomb.png'))
                        self.button[y][x].setText(" ")

                else:
                    self.button[y][x].set_bg_color("yellow")
                    self.button[y][x].setIcon(QIcon('flag.png'))
                    self.button[y][x].setText(" ")
    
    #地雷セルを表示するための関数                          
    def show_mine_map(self):
        for y in range(MS_SIZE):
            for x in range(MS_SIZE):
                #もし地雷セルなら開ける
                if self.game.mine_map[y][x] == -1:
                    self.game.game_board[y][x] = OPEN

        self.show_cell_status()
    
    #地雷マスを表示し再挑戦判定をする関数
    def result(self):
        #元のウィンドウを閉じる
        self.close()
        #地雷の位置
        self.initUI()
        self.show_mine_map()
        result = QMessageBox.question(self, 'Restart', "再挑戦しますか？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) 
        if result == QMessageBox.Yes:
            self.close()
            #ゲームを初期化
            self.__init__()
        else:
            self.close()
                      
def main():
    app = QApplication(sys.argv)
    w = MinesweeperWindow()
    app.exec_()
            
if __name__ == '__main__':
    main()