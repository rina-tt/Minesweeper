# Minesweeper python
import random
import numpy as np

MS_SIZE = 8          # ゲーム盤のサイズ
CLOSE, OPEN, FLAG = 0, 1, 2

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
        
        #地雷があるセルを指定
        if self.mine_map[y][x] == -1: 
            return False
        
        #すでに開いているセルを指定
        if self.game_board[y][x] == OPEN:
            return True
        
        #フラグのあるセルを指定
        if self.game_board[y][x] == FLAG:
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

        
    def print_header(self):
        print("=====================================")
        print("===  MineSweeper Python Ver. 1  =====")
        print("=====================================")

    def print_footer(self):
        print("   ", end="")
        for x in range(MS_SIZE):
            print("---", end="")
        print("[x]\n   ", end="")
        for x in range(MS_SIZE):
            print(f"{x:3d}", end="")
        print("")
        
    def print_mine_map(self):
        print(" [y]")
        for y in range(MS_SIZE):
            print(f"{y:2d}|", end="")
            for x in range(MS_SIZE):
                print(f"{self.mine_map[y][x]:2d}", end="")
            print("")
        
    def print_game_board(self):
        marks = ['x', ' ', 'P']
        self.print_header()
        print("[y]")
        for y in range(MS_SIZE):
            print(f"{y:2d}|", end="")
            for x in range(MS_SIZE):
                if self.game_board[y][x] == OPEN and self.mine_map[y][x] > 0:
                    print(f"{self.mine_map[y][x]:3d}", end="")
                else:
                    print(f"{marks[self.game_board[y][x]]:>3}", end="")
            print("")
        self.print_footer()

if __name__ == '__main__':
    b = Game()
    quitGame = False
    while not quitGame:
        b.print_game_board()
        print("o x y: セルを開く，f x y: フラグ設定/解除, q: 終了 -->", end="")
        command_str = input()

        try:
            cmd = command_str.split(" ")
            if cmd[0] == 'o':
                x, y = cmd[1:]
                if b.open_cell(int(x), int(y)) == False:
                    print("ゲームオーバー!")
                    quitGame = True
            elif cmd[0] == 'f':
                x, y = cmd[1:]
                b.flag_cell(int(x), int(y))
            elif cmd[0] == 'q':
                print("ゲームを終了します．")
                quitGame = True
                break
            else:
                print("コマンドはo, f, qのいずれかを指定してください．")
        except:
            print("もう一度，コマンドを入力してください．")
            
        if b.is_finished():
            b.print_game_board()
            print("ゲームクリア!")
            quitGame = True
