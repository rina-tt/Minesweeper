/*マインスイーパの課題(version.2)*/

#include <stdio.h>
#include <stdlib.h> //rand関数
#include <time.h> //time関数

#define MS_SIZE 8 //ゲームボードのサイズ 変更不可
#define MINE -1 //地雷のセル
#define FLAG 2 //フラグを設置したセル
#define OPEN 1 //開いたセル

/////*表示に関する関数*/////

//ゲームの進行状況を表示
void print_game_board(int game_board[MS_SIZE][MS_SIZE],int mine_map[MS_SIZE][MS_SIZE]){

    int i,j;

    printf("x:開かれていないセル  0~8:開いたセル(近傍にある地雷の数)  P:フラグ\n");
    printf(" [y]\n");
    for(i=0;i<MS_SIZE;i++){
        printf("  %d |",i);
	for(j=0;j<MS_SIZE;j++){
	    if(game_board[i][j]==0){ //開けてない
                printf("  x");
	    }
	    if(game_board[i][j]==1){ //開けた
		printf("%3d",mine_map[i][j]);
	    }
	    if(game_board[i][j]==2){ //フラグ
		printf("  P");
	    }
	}
	printf("\n");
    }
    printf("     ");
    for(i=0;i<MS_SIZE;i++){
        printf("---");
    }
    printf("\n     ");
    for(i=0;i<MS_SIZE;i++){
        printf("%3d",i);
    }
    printf("[x]\n");
}
//答えを表示する関数
void print_mine_map(int mine_map[MS_SIZE][MS_SIZE]){
    int i,j;
    printf("-1:爆弾\n");
    printf(" [y]\n");
    for(i=0;i<MS_SIZE;i++){
        printf("  %d |",i);
        for(j=0;j<MS_SIZE;j++){
            printf("%3d",mine_map[i][j]);
        }
        printf("\n");
    }
    printf("     ");
    for(i=0;i<MS_SIZE;i++){
        printf("---");
    }
    printf("\n     ");
    for(i=0;i<MS_SIZE;i++){
        printf("%3d",i);
    }
    printf("[x]\n");
}

/////*ゲーム本体の関数*/////

//初期化する関数
void initialization(int *number_of_mines,int mine_map[MS_SIZE][MS_SIZE],int game_board[MS_SIZE][MS_SIZE]){

    int i,j;

    for(i=0;i<MS_SIZE;i++){
        for(j=0;j<MS_SIZE;j++){
            game_board[i][j]=0;
            mine_map[i][j]=0;
        }
    }
    *number_of_mines=10; //初期値
}

//ランダムに地雷をセットする関数
void set_mines(int number_of_mines,int mine_map[MS_SIZE][MS_SIZE]){
    int x,y,i;

//配置
    for(i=0;i<number_of_mines;i++){
	y=rand()%MS_SIZE; 
        x=rand()%MS_SIZE;
	if(mine_map[y][x]==MINE){//すでに地雷ならもう一回
	    i--;
        }
	else{
	mine_map[y][x]=MINE;
	}
    }
}

//周囲の地雷をカウントする関数
void mine_count(int mine_map[MS_SIZE][MS_SIZE]){
    int i,j,k,l;

    for(i=0;i<MS_SIZE;i++){
        for(j=0;j<MS_SIZE;j++){
	    if(mine_map[i][j]==MINE){//何もしない
	    }else{
		for(k=-1;k<2;k++){
		    for(l=-1;l<2;l++){
			if(i+k<0 || j+l<0 || i+k>7 || j+l>7){//端っこ 何もしない
			}else{
			    if(mine_map[i+k][j+l]==MINE){//周りに爆弾があれば[i][j]マスにプラス1
				mine_map[i][j] +=1;
			    }
			}
		    }
		}
	    }
	}
    }
}

//ユーザの入力を取得する関数
void select_cell(int *mode){

    printf("モードを選択してください。:セルを開く(1)、フラグを設置/除去する(2):");
    scanf("%d",mode);
    while(*mode!=1 && *mode!=2){
        printf("1か2を入力してください:");
	scanf("%d",mode);
    }
}

//選択したセルの8近傍を開く関数
void check_neighbors(int mine_map[MS_SIZE][MS_SIZE],int game_board[MS_SIZE][MS_SIZE],int X,int Y,int *win){
    int i,j;
    if(mine_map[Y][X]==MINE){
        printf("bomb!!");
	printf("地雷を踏みました\n");
	*win=1;
	//}else if(mine_map[Y+1][X+1]!=0){//開けたセルが0でないとき、そのセルしか開けない
	//    game_board[Y+1][X+1]=OPEN;
    }else{
	game_board[Y][X]=OPEN;//開けたセルが0のときは、周りの8マスも開ける
	for(i=-1;i<2;i++){
	    for(j=-1;j<2;j++){
		if(Y+i<0 || X+j<0 || Y+i>7 || X+j>7){ //ボード外
		}else{
	            if(mine_map[Y+i][X+j]==MINE){}//地雷マスには何もしない
		    else{game_board[Y+i][X+j]=OPEN;}//地雷マスでなければ開く
		}
	    }
	}
    }
} 


int main(void){
    int mode;//モードを保持（モード：セルを開く、フラグを立てる・除去する）
    int number_of_mines; //地雷数のデフォルト値は10
    int mine_map[MS_SIZE][MS_SIZE]; //地雷セルと数字セルを記録
    int game_board[MS_SIZE][MS_SIZE]; //ゲームの進行を記録するためのゲームボード
    //ボード外のマスを考慮して、縦横ともに配列サイズを+2した
    int i,j;
    int X,Y; //ユーザーが指定したセルの位置
    int con=1; //ゲームを続行するか否か
    int win=0;//ゲームの勝利判定
    int sum;//開いたセルの合計

    while(con==1){
//配列とmode、地雷の数を初期化
	initialization(&number_of_mines,mine_map,game_board);

        srand((unsigned)time(NULL));//time関数で現在時刻を取得し、乱数を初期化する

        printf("マインスイーパを始めます。\n");
        printf("%dx%dのボードの各セルに配置された地雷を除去するゲームです。\n",MS_SIZE,MS_SIZE);

/*課題１ 地雷をランダムにセット*/

	//オプション課題1(地雷の数を指定)
	printf("設置する地雷数を入力してください:");
	scanf("%d",&number_of_mines);
	while(number_of_mines < 0 || number_of_mines > MS_SIZE*MS_SIZE){
	    printf("地雷数が正しくありません。\n");
	    printf("設置する地雷数を入力してください:");
	    scanf("%d",&number_of_mines);
	}

	set_mines(number_of_mines,mine_map);

/*課題２ 各セルの８近傍の地雷をカウント*/  
	mine_count(mine_map);

//全体を表示
        print_game_board(game_board,mine_map);

        while(win==0){//ゲームの継続条件 0=続ける 1=負け 2=勝ち
//モードを指定
            select_cell(&mode);
    
//ユーザがセルを指定
            if(mode==1){
                printf("開けたいセルの位置を指定してください。\n");
                printf("[x]と[y]を入力してください:");
                scanf("%d %d",&X,&Y);
	        while(X<0 || X>7 || Y<0 || Y>7){//セルがボード内にないとき
		    printf("0から7までの整数を入力してください。\n");
		    scanf("%d %d",&X,&Y);
	        }
//課題3 セルを開ける
		check_neighbors(mine_map,game_board,X,Y,&win);

	    }else{  //課題４ フラグを立てる
	        printf("フラグを設置/除去します。\n");
	        printf("すでにフラグを立てた位置を指定することで、フラグを除去できます。\n");
	        printf("[x]と[y]を入力してください:");
	        scanf("%d %d",&X,&Y);
                while(X<0 || X>7 || Y<0 || Y>7){//セルがボード内にないとき
                    printf("0から7までの整数を入力してください。\n");
                    scanf("%d %d",&X,&Y);
                }
	        if(game_board[Y][X]==FLAG){ //オプション課題2
		    game_board[Y][X]=0;
	        }else{
	            game_board[Y][X]=FLAG;
	        }	
	    }

//課題５ 開いたセルを数える
	    sum=0;//初期化
	    for(i=0;i<MS_SIZE;i++){
	        for(j=0;j<MS_SIZE;j++){
		    if(game_board[i][j]==OPEN){
		        sum +=1;
		    }
	        }
	    }
	    //確認用 printf("sum=%d\n",sum);

	    if(sum==(MS_SIZE*MS_SIZE)-number_of_mines){ //終了条件
	        win=2; //勝ち
            }

//ゲームの状況
            if(win==0){
		print_game_board(game_board,mine_map);
	    }

	    if(win==1 ||win==2){
                if(win==1){  //ゲームオーバー
	            printf("-----GAME OVER-----\n");
                }

                if(win==2){ //ゲームクリア
	            printf("Congratulation!!\n");
	        }
	        printf("答え\n");
		print_mine_map(mine_map); //mine_mapの表示

                //オプション課題3
	        printf("もう一度プレイしますか？(Yes = 1 No = 2):");
	        scanf("%d",&con);
	        while(con!=1 && con!=2){
	            printf("1か2を入力してください。\n");
	            printf("もう一度プレイしますか？(Yes = 1 No = 2):");
	            scanf("%d",&con);
	        }
	        if(con==2)
		    break;
	    }
        }//whileの閉じカッコ
    }//続行のカッコ

    return 0;
}
