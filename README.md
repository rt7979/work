=======================================================================  
內容：  

order_db         --------------------- db檔案  
order_demo_01.py --------------------- python主程式  
README.md        --------------------- 說明文件  


=======================================================================  
教學：  

1.下載python檔案後，要再外另外匯入PySide6函式庫  

2.DB可另外透過DB Browser for SQLite這支程式快速查看db內容並快速編輯  
  DB Browser for SQLite官方網站  
  https://sqlitebrowser.org/  

3.執行Power Shell或透過pyauto-py-to-exe，把python檔案打包成exe  

4.打包完成後，會生成出order_demo.exe和_internal資料夾  
  並把order_db放入_internal資料夾內  
  order ══╦═ order_demo.exe              --------------------- 主程式  
          ╚═ _internal/order_db/order.db --------------------- _internal資料夾和db位置  
