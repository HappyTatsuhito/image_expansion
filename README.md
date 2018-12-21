<<<<<<< HEAD
# 準備  
    $ cd src/tm_image_expantion  
imageの中にフォルダ(名前は数字(例：000)でお願いします)を作成し、中に画像を入れてください  
background_imageには拡張する時の背景画像を入れてください。  

# 操作方法  
image_expansion.pyを実行します  
キーボード入力の説明：  
　1枚目(白背景の画像)：  
　　切り取る範囲の決定  
　　　s：決定  
　　明るさ  
　　　r：増加    
　　　f：減少  
　　lowerの数値  
　　　t：増加  
　　　g：減少  
　　upperの色の範囲  
　　　y：増加  
　　　h：減少  
　　lowerの彩度の範囲  
　　　u：増加  
　　　j：減少  
　　upperの彩度の範囲  
　　　i：増加  
　　　k：減少  
　　lowerの明度の範囲  
　　　o：増加  
　　　l：減少  
　　upperの明度の範囲  
　　　p：増加  
　　　;：減少  
	
　2枚目(青背景でbounding boxが表示されている画像)：  
　　s：データ拡張の開始  
　　d：元画像の削除  
　　c：プログラムの終了  
　　b：画像編集(1枚目)に戻る  
　　other(その他のキーボード入力)：拡張せずに次の画像に進む

# その他  
learningにデータ拡張した画像、座標テキストが生成されます  
textにtrain.txtとtest.txtが生成されます  

=======
# 概要  
RoboCup@HomeリーグStoringGroceries用  

# 実行方法  
  $ rosrun tm_storing_groceries sg_start.sh  
  $ roslaunch realsense_camera r200_nodelet_rgbd.launch  
  $ roslaunch darknet_ros darknet_ros_gdb.launch  
  $ rosrun tm_storing_groceries Navigation.py  
  $ rosrun tm_storing_groceries Storing_Groceries.py  

# その他  
Navigation.pyとStoring_Groceries.pyは毎回立ち上げ直してください  
>>>>>>> 9ff50d0b57b02d0be79cdb00b72e38eb0041780f
