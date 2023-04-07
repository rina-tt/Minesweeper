# Minesweeper
2021/11に授業課題で作成したマインスイーパーです。/Minesweeper created for a class assignment.

動作確認していません。

追加機能

(1)ゲームクリア、ゲームオーバー時に地雷セルの位置を表示し、「再挑戦しますか？」のダイアログを表示
- MinesweeperWindowクラスにshow_mine_map()を追加、全セルを探査して地雷セルならOPENにする
- MinesweeperWindowクラスにresult()を追加、UIの初期化をしてshow_mine_map()を実行
- 「No」ならcloseして終了、「Yes」なら再挑戦(一度closeしてから__init__()を実行)

(2)フラグセルに旗のイラスト(flag.png)、地雷セルに爆弾のイラスト(bomb.png)を使用
- 自作
- MinesweeperWindowクラスのshow_cell_status()でsetIcon(QIcon("ファイル名"))を使用

(3)ゲームクリアのダイアログでクリアにかかった時間を表示する
- timeモジュールをインポート
- MinesweeperWindowのインスタンスの初期化で開始時刻(start)を取得
- MyPushButtonクラスのon_click()においてゲームクリアと判定されたとき、現在時刻から開始時刻(start)を引いてクリアにかかった時間(clear_time)を取得
