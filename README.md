# Minesweeper
授業課題で作成したマインスイーパーです。

Minesweeper created for a class assignment.

## CUIでプレイ（C言語）
2019/12 作成
```
gcc Minesweeper.c
./a.out
```

## CUIでプレイ（Python）
2021/10 作成
```
python Minesweeper.py (爆弾の数)
```
爆弾の数のデフォルトは10

### 動作テスト
```
python TestMinesweeper.py 
```

## GUIでプレイ
2021/11 作成
```
python Minesweeper_gui.py (爆弾の数)
```
### 課題以外に追加した機能
- ゲームクリア、ゲームオーバー時に地雷セルの位置を表示し、「再挑戦しますか？」のダイアログを表示
- フラグセルに旗のイラスト(flag.png)、地雷セルに爆弾のイラスト(bomb.png)を使用
- ゲームクリアのダイアログでクリアにかかった時間を表示


## 更新履歴
2023/05/01　C言語版を追加
