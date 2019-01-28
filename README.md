# 準備  
    $ cd src/tm_image_expantion/image  
imageの中にフォルダ(名前は数字(例：000)でお願いします)を作成し、中に拡張させる元の画像を入れてください。  
    例：$ mkdir 000  
background_imageには拡張する時の背景画像を入れて下さい。  

# 概要(expansion)  
このデータ拡張スクリプトはHSV色空間で背景を取り除きます。取り除く色の範囲はCOLOR_LOWERからCOLOR_UPPERまでの範囲が対象となります。  
拡張を開始するとexpanded_image, learning, textのフォルダが生成されます。  
拡張を終えた元画像はimageからexpanded_imageに移動し、拡張された学習用データと座標はlearningに生成されます。textにはall.txt, train.txt, test.txtが生成されます。all.txtには学習用データの全てのパスが、train.txtとtest.txtには設定した割合でパスがランダムに振り分けられます。  

# 概要(trimming)  
このスクリプトはデータ拡張はせず、背景を単色にするスクリプトです。  
拡張したデータを学習用パソコンに移すとなると多大な時間がかかってしまうため、拡張をすぐに行える前段階のデータ(単色の背景のデータ)を作成するために使用します。  
基本はexpansionと変わりませんが、トリムを開始するとexpanded_image, trimed_imageのフォルダが生成されます。  
expanded_imageはexpansionと同様で、単色の背景になったデータはtrimed_imageに生成されます。  

# 操作方法(expansion)  
image_expansion.pyを実行します  
※ 実行する場合はscriptsの中で実行して下さい。  
キーボード入力の説明：  
　1枚目(白背景の画像)：  
　　切り取る範囲の決定  
　　　s ： 決定  

　　明るさ  
　　　r ： 増加    
　　　f ： 減少  
	
　　　　　　色相の範囲(H)　彩度の範囲(S)　明度の範囲(V)  

　　LOWER　　t ： 増加　　　　y ： 増加　　　　u ： 増加  
　　　　　　　　g ： 減少　　　　h ： 減少　　　　j ： 減少  

　　UPPER　　i ： 増加　　　　o ： 増加　　　　p ： 増加  
　　　　　　　　k ： 減少　　　　l ： 減少　　　　; ： 減少  



　2枚目(青背景でbounding boxが表示されている画像)：  
　　s ： データ拡張の開始  
　　d ： 元画像の削除  
　　c ： プログラムの終了  
　　b ： 画像編集(1枚目)に戻る  
　　other(その他のキーボード入力)：拡張せずに次の画像に進む  

# 操作方法(trimming)  
基本操作はexpansionと変わりません。  
2枚目のbounding boxが表示されている画像の時に矢印キーの左か右をタイプすると背景を赤, 青, 緑の何れかに変更ができます。  


# その他  
１から拡張し直す場合はimageの中に作成した(数字の)フォルダと同じ名前のフォルダをlearning,textのフォルダから削除して下さい。(expanded_imageはどちらでも可)  

