from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtSql import (QSqlDatabase, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate,
                           QSqlTableModel, QSqlQueryModel, QSqlQuery)
import sys
import os
os.chdir(os.path.dirname(__file__))


class Qtablewidgetdemo(QMainWindow):
    def __init__(self, parent=None):
        super(Qtablewidgetdemo, self).__init__(parent)
        self.orderid = 0    # 客戶訂單
        self.initmodel()
        self.setwindow()
        self.set_right_layout()
        self.add_tableview_widget()
        self.add_ordertableview_widget()
        self.current_time()

    def current_time(self):
        self.datetimeedit = QDateTimeEdit(QDateTime.currentDateTime())
        currtime = self.datetimeedit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.text.appendPlainText(currtime)

    def initmodel(self):
        # 建立model，菜單
        self.model = QSqlQueryModel()
        Query = (f"SELECT A.套餐名稱, B.餐點名稱, C.餐點名稱, D.飲料名稱, (B.價格+C.價格+D.價格+E.價格-10) AS 售價 "
                 f"FROM 套餐 AS A, 主餐 AS B, 點心 AS C, 飲料 AS D, 飲料大小 AS E "
                 f"WHERE A.主餐 = B.id AND A.點心 = C.id AND A.飲料 = D.id AND E.id = 1;")
        self.model.setQuery(Query)

        # 建立標題
        title = ["套餐名稱", "主餐", "點心", "飲料", "售價"]
        for i in range(len(title)):
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, title[i])

        # 建立modelc，查詢結果
        self.modelc = QSqlQueryModel()

        # 建立modeld，取代modelb
        self.modeld = QSqlTableModel()
        self.modeld.setTable("客戶訂單_套餐")
        self.modeld.setHeaderData(0, Qt.Orientation.Horizontal, "訂單編號")
        self.modeld.select()

    def setwindow(self):
        self.resize(900, 700)
        self.setWindowTitle("點餐系統")

        # widget和layout
        widget = QWidget()
        self.setCentralWidget(widget)
        self.big_layout = QHBoxLayout()
        widget.setLayout(self.big_layout)

        left_layout = QVBoxLayout()
        left_layout.sizeConstraint()
        self.right_all_layout = QVBoxLayout()
        self.big_layout.addLayout(left_layout)
        self.big_layout.addLayout(self.right_all_layout)
        self.big_layout.setStretchFactor(left_layout, 3)
        self.big_layout.setStretchFactor(self.right_all_layout, 1)

        # 顧客資料和購物車
        customerlayout = QHBoxLayout()
        self.namelabel = QLabel("客戶名稱(手機號碼)：")
        self.customer_name = QLineEdit("0939-222-333")
        self.addcar = QPushButton("加入購物車")
        customerlayout.addWidget(self.namelabel)
        customerlayout.addWidget(self.customer_name)
        customerlayout.addWidget(self.addcar)
        self.addcar.setEnabled(False)

        # 建立tableview
        self.tableview = QTableView()
        self.tableview.setModel(self.model)

        # 調整表格寬度
        # 第一行：根據程式本身視窗大小自動改變欄位寬度，但是欄位基本寬度，所以有可能產生超出程式預設的範圍(出現多餘的橫軸)
        # 第二行：根據程式本身視窗大小平均分配欄位寬度，但無法調整
        # 第三行：表格最後一筆資料黏到程式視窗邊邊
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableview.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.tableview.horizontalHeader().setStretchLastSection(True)  # 最後一格黏在畫面左邊

        # 客戶訂單表格order_tableview
        # 建立和設定委託
        self.order_tableview = QTableView()
        self.order_tableview.setModel(self.modeld)
        self.order_tableview.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # 禁止編輯
        self.order_tableview.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)   # 一次選一行

        # modelb用的
        # self.delegate = QSqlRelationalDelegate(self.order_tableview)
        # self.order_tableview.setItemDelegate(self.delegate)
        # self.order_tableview.setItemDelegate(QSqlRelationalDelegate(self.order_tableview))

        # 調整order_tableview表格寬度
        self.order_tableview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.order_tableview.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.order_tableview.horizontalHeader().setStretchLastSection(True)

        # 其他工具
        # 建立新增和清除的button
        buttonlayout = QHBoxLayout()
        self.edit_button = QPushButton('修改')
        self.del_button = QPushButton('刪除')
        self.button_text_clear = QPushButton("清除文字訊息")
        self.price_button = QPushButton("計算金額")
        buttonlayout.addWidget(self.edit_button)
        buttonlayout.addWidget(self.del_button)
        buttonlayout.addWidget(self.button_text_clear)
        buttonlayout.addWidget(self.price_button)

        # groupbox，框框內放第二張表格和文字框
        self.groupbox = QGroupBox()
        self.groupbox.setTitle("確認結果")
        self.text = QPlainTextEdit('')

        # layout排版
        layoutb = QVBoxLayout(self.groupbox)
        layoutb.addWidget(self.order_tableview)
        layoutb.addWidget(self.text)

        # 左layout部分
        left_layout.addLayout(customerlayout)
        left_layout.addWidget(self.tableview)
        left_layout.addLayout(buttonlayout)
        left_layout.addWidget(self.groupbox)

        # 按鈕設定
        self.addcar.clicked.connect(self.add_order)
        self.button_text_clear.clicked.connect(self.text.clear)
        self.edit_button.clicked.connect(self.order_edit)               # ------------------------
        self.del_button.clicked.connect(self.del_order)
        self.price_button.clicked.connect(self.cele_price)
        # self.tableview.setShowGrid(False)

    # 右邊要做修改動作的畫面，使用修改並選擇要修改的項目會出現
    def set_right_layout(self):
        # 右layout部分
        self.r_groupbox = QGroupBox()
        self.r_groupbox.setTitle("更換餐點")
        self.grobox_layout = QFormLayout(self.r_groupbox)

        self.right_button_layout = QHBoxLayout()
        self.right_ok = QPushButton("確認送出")
        self.right_cancel = QPushButton("取消修改")
        self.right_button_layout.addWidget(self.right_ok)
        self.right_button_layout.addWidget(self.right_cancel)

        self.right_all_layout.addWidget(self.r_groupbox)
        self.right_all_layout.addLayout(self.right_button_layout)

        self.customer = QLineEdit()
        self.combo = QComboBox()
        self.drink = QComboBox()
        self.drink_size = QComboBox()
        self.count = QSpinBox()
        self.price = QLineEdit()
        self.grobox_layout.addRow('客戶代號', self.customer)
        self.grobox_layout.addRow('餐點名稱', self.combo)
        self.grobox_layout.addRow('飲料', self.drink)
        self.grobox_layout.addRow('飲料大小', self.drink_size)
        self.grobox_layout.addRow('數量', self.count)
        self.grobox_layout.addRow('價格', self.price)

        self.customer.setEnabled(False)

        self.r_groupbox.hide()
        self.right_ok.hide()
        self.right_cancel.hide()

        # 按鈕訊號設定
        self.right_ok.clicked.connect(self.update_sql)
        self.right_cancel.clicked.connect(self.order_edit_cancel)

    # 上面表格內增加"數量"和"確認"的小工具
    def add_tableview_widget(self):
        # 新增二個有按鍵的欄位
        column = self.model.columnCount()
        title = ["數量", "確認"]

        for i in range(2):
            self.model.insertColumn(column)
            self.model.setHeaderData(column + i, Qt.Orientation.Horizontal, title[i])

        # 加小工具
        row = self.model.rowCount()
        column = self.model.columnCount()
        self.count_sb = []
        self.add_check = []

        for i in range(row):
            # 新增數量和設定範圍
            self.count_sb.append(QSpinBox())
            self.tableview.setIndexWidget(self.model.index(i, column-2), self.count_sb[i])
            self.count_sb[i].setRange(0, 10)

            # 新增勾選方塊
            self.add_check.append(QCheckBox())
            self.tableview.setIndexWidget(self.model.index(i, column-1), self.add_check[i])

            # 數量和勾選連動
            self.count_sb[i].valueChanged.connect(self.val_changed)
            self.add_check[i].stateChanged.connect(self.button_enable)

    # 每一筆訂單旁邊增加"修改"按鈕
    def add_ordertableview_widget(self):
        row = self.modeld.rowCount()
        column = self.modeld.columnCount()

        # 新增"修改"標題
        self.modeld.insertColumn(column)
        self.modeld.setHeaderData(column, Qt.Orientation.Horizontal, "修改")

        # 新增"選擇"內容
        select_button = []
        if row != 0:
            for i in range(row):
                select_button.append(QPushButton('選擇'))
                self.order_tableview.setIndexWidget(self.modeld.index(i, column), select_button[i])
                select_button[i].clicked.connect(self.order_edit2)
        """self.select_button = []
        if row != 0:
            for i in range(row):
                self.select_button.append(QPushButton('選擇'))
                self.order_tableview.setIndexWidget(self.modeld.index(i, column), self.select_button[i])
                self.select_button[i].clicked.connect(self.order_edit2)"""

        # 把這一列隱藏起來
        self.order_tableview.hideColumn(column)


    # 數量和勾選連動的函數
    def val_changed(self):
        curr_row = self.tableview.currentIndex().row()
        if self.count_sb[curr_row].value() == 0:
            self.add_check[curr_row].setChecked(False)
        else:
            self.add_check[curr_row].setChecked(True)

    # 勾選和購物車按鈕連動函數
    def button_enable(self):
        # 當前"欄"位
        curr_row = self.tableview.currentIndex().row()

        # 數量和選擇連動
        if self.add_check[curr_row].isChecked() is True and self.count_sb[curr_row].value() == 0:
            self.count_sb[curr_row].setValue(1)
        elif self.add_check[curr_row].isChecked() is False:
            self.count_sb[curr_row].setValue(0)

        # 紀錄選擇，且紀錄次數和哪一欄
        addrow = []
        for i in range(len(self.add_check)):
            if self.add_check[i].isChecked() is True:
                addrow.append(i)

        # 根據選擇的次數和欄位，紀錄數量
        addcount = []
        for i in addrow:
            addcount.append(self.count_sb[i].value())

        # 選擇和按鈕連動，只要有項目被選擇，解鎖按鈕
        if addrow:
            self.addcar.setEnabled(True)
        else:
            self.addcar.setEnabled(False)

    # 新增訂單，顯示下面表格用
    def add_order(self):
        # 訂單資料
        row_count = self.modeld.rowCount()
        column_count = self.modeld.columnCount()
        curr_row = self.tableview.currentIndex().row()

        customer = self.customer_name.text()
        combo = self.model.record(curr_row).value(0)
        drink = self.model.record(curr_row).value(3)
        count = self.count_sb[curr_row].value()
        size = "小"

        # 訂單流水號
        Query = (f'SELECT MAX(id) '
                 f'FROM 客戶訂單_套餐;')

        self.modelc.setQuery(QSqlQuery(Query))
        search_id = self.modelc.record(0).value(0)

        if not self.orderid:
            self.orderid = 0

        if not search_id:
            self.orderid += 1
        else:
            if self.orderid >= search_id:
                self.orderid += 1
            else:
                self.orderid = search_id + 1

        # 價格
        Query = (f'SELECT (a.NO_drink + b.價格 + c.價格)*{count} '
                 f'FROM 套餐 as a, 飲料 as b, 飲料大小 as c '
                 f'WHERE a.套餐名稱 = "{combo}" AND b.飲料名稱 = "{drink}" AND c.大小 = "{size}";')
        self.modelc.setQuery(QSqlQuery(Query))

        price = self.modelc.record(0).value(0)

        if self.add_check[curr_row].isChecked() is True:
            # 訂單、數量、價格
            Query = (f'INSERT INTO 客戶訂單_套餐  (id, 客戶代號, 套餐名稱, 飲料, 飲料大小, 數量, 價格) '
                     f'VALUES ({self.orderid}, "{customer}", "{combo}", "{drink}", "{size}", {count}, {price});')
            self.modeld.setQuery(QSqlQuery(Query))
            self.text.appendPlainText(f'訂單  {self.orderid}  號，已加入購物車')
        else:
            self.text.appendPlainText('新增失敗，請選擇正確項目')

        # 刷新畫面
        self.moded_update()

    # 計算"最終價格"
    def cele_price(self):
        Query = (f'SELECT SUM(價格) '
                 f'FROM 客戶訂單_套餐;')
        self.modelc.setQuery(QSqlQuery(Query))

        price = self.modelc.record(0).value(0)
        self.text.appendPlainText(f'總計: {price} 元')

    # 啟動"修改"按鈕
    def order_edit(self):
        row = self.modeld.rowCount()
        column = self.modeld.columnCount()
        if row > 0:
            self.order_tableview.showColumn(column-1)
        else:
            self.text.appendPlainText("沒有訂單")

    # 點選"選擇"後，開啟右邊視窗做修改
    def order_edit2(self):
        self.r_groupbox.show()
        self.right_ok.show()
        self.right_cancel.show()

        # 改尺寸，好像沒用
        self.order_tableview.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.order_tableview.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.order_tableview.horizontalHeader().setStretchLastSection(True)

        # 選擇的"哪一列"，選擇那一列的"總欄位數量"
        curr_row = self.order_tableview.currentIndex().row()
        curr_record = self.modeld.record(curr_row)
        column_count = self.modeld.columnCount()

        # 訂單資料
        order_title = []
        order_data = []
        for i in range(column_count):
            order_title.append(self.modeld.headerData(i, Qt.Orientation.Horizontal))
            order_data.append(curr_record.value(i))

        # 客戶資料_建修改檔，不用改資料
        self.customer.setText(order_data[1])

        # 套餐名稱_建修改檔
        Query = (f"SELECT 套餐名稱 "
                 f"FROM 套餐;")
        self.modelc.setQuery(Query)
        combos = []
        for i in range(self.modelc.rowCount()):
            combos.append(self.modelc.record(i).value(0))
        self.combo.clear()
        self.combo.addItems(combos)
        self.combo.setCurrentText(order_data[2])

        # 飲料_建修改檔
        Query = (f"SELECT 飲料名稱 "
                 f"FROM 飲料;")
        self.modelc.setQuery(Query)
        drinks = []
        for i in range(self.modelc.rowCount()):
            drinks.append(self.modelc.record(i).value(0))
        self.drink.clear()
        self.drink.addItems(drinks)
        self.drink.setCurrentText(order_data[3])

        # 飲料大小_建修改檔
        Query = (f"SELECT 大小 "
                 f"FROM 飲料大小;")
        self.modelc.setQuery(Query)
        drink_sizes = []
        for i in range(self.modelc.rowCount()):
            drink_sizes.append(self.modelc.record(i).value(0))
        self.drink_size.clear()
        self.drink_size.addItems(drink_sizes)
        self.drink_size.setCurrentText(order_data[4])

        # 數量_建修改檔
        self.count.setRange(1, 10)
        self.count.setValue(order_data[5])

        # 連接訊號
        self.combo.currentIndexChanged.connect(self.update_price)
        self.drink.currentIndexChanged.connect(self.update_price)
        self.drink_size.currentIndexChanged.connect(self.update_price)
        self.count.valueChanged.connect(self.update_price)

        # 價格_建修改檔
        self.price.setText(f'{order_data[6]}')

    # 根據右邊訂單，更新價格
    def update_price(self):
        # 斷訊號
        self.combo.currentIndexChanged.disconnect()
        self.drink.currentIndexChanged.disconnect()
        self.drink_size.currentIndexChanged.disconnect()
        self.count.valueChanged.disconnect()

        # 連接訊號
        self.combo.currentIndexChanged.connect(self.update_price)
        self.drink.currentIndexChanged.connect(self.update_price)
        self.drink_size.currentIndexChanged.connect(self.update_price)
        self.count.valueChanged.connect(self.update_price)

        combo = self.combo.itemText(self.combo.currentIndex())
        drink = self.drink.itemText(self.drink.currentIndex())
        drink_size = self.drink_size.itemText(self.drink_size.currentIndex())
        count = self.count.text()

        Query = (f"SELECT (a.NO_drink + b.價格 + c.價格)*{count} "
                 f"FROM 套餐 as a, 飲料 as b, 飲料大小 as c "
                 f"WHERE a.套餐名稱 = '{combo}' AND b.飲料名稱 = '{drink}' AND c.大小 = '{drink_size}';")
        self.modelc.setQuery(Query)

        price = self.modelc.record(0).value(0)
        self.price.setText(f'{price}')
        # print(f'price側:{combo, drink, drink_size, count, price}')


    # 修改餐點後，更新訂單表格
    def update_sql(self):
        customerid = self.modeld.record(self.order_tableview.currentIndex().row()).value(0)
        customer = self.customer.text()
        combo = self.combo.itemText(self.combo.currentIndex())
        drink = self.drink.itemText(self.drink.currentIndex())
        drink_size = self.drink_size.itemText(self.drink_size.currentIndex())
        count = self.count.text()
        price = self.price.text()

        # print(f'sql側:{customerid, customer, combo, drink, drink_size, count, price}')

        Query = (f"UPDATE 客戶訂單_套餐 "
                 f"SET 套餐名稱 = '{combo}', 飲料 = '{drink}', 飲料大小 = '{drink_size}', 數量 = {count}, 價格 = {price} "
                 f"WHERE id = {customerid};")
        self.modelc.setQuery(Query)

        self.moded_update()
        self.text.appendPlainText(f'訂單  {customerid}  號，修改完成')


    # 取消修改
    def order_edit_cancel(self):
        # 斷訊號
        self.combo.currentIndexChanged.disconnect()
        self.drink.currentIndexChanged.disconnect()
        self.drink_size.currentIndexChanged.disconnect()
        self.count.valueChanged.disconnect()

        # 清資料
        self.customer.clear()
        self.combo.clear()
        self.drink.clear()
        self.drink_size.clear()
        self.count.setValue(0)
        self.price.clear()

        # 隱藏
        self.r_groupbox.hide()
        self.right_ok.hide()
        self.right_cancel.hide()
        self.order_tableview.hideColumn(7)
        # self.modeld.removeColumns()
        self.text.appendPlainText('取消修改')


    # 刪除訂單
    def del_order(self):
        row = self.modeld.rowCount()

        # 紀錄訂單流水號
        Query = (f'SELECT MAX(id) '
                 f'FROM 客戶訂單_套餐;')
        self.modelc.setQuery(QSqlQuery(Query))
        self.orderid = self.modelc.record(0).value(0)

        # 當前欄位並刪除
        curr_row = self.order_tableview.currentIndex().row()
        customerid = self.modeld.record(curr_row).value(0)

        if row == 0:
            self.text.appendPlainText("沒有訂單")
        else:
            if customerid == 0:
                self.text.appendPlainText(f'請選擇訂單')
            else:
                self.modeld.removeRows(curr_row, 1)
                self.text.appendPlainText(f'訂單  {customerid}  號，已刪除')

        # 刷新畫面
        self.moded_update()

    # 刷新畫面
    def moded_update(self):
        self.modeld.setTable("客戶訂單_套餐")
        self.modeld.setHeaderData(0, Qt.Orientation.Horizontal, "訂單編號")
        self.modeld.select()

        # self.modeld.select()後會把最後一列的修改刪掉，這邊補上最後一列
        self.add_ordertableview_widget()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('./order_db/order.db')
    if db.open() is not True:
        QMessageBox.critical(QWidget(), "警告", "連接失敗")
        exit()
    demo = Qtablewidgetdemo()
    demo.show()
    sys.exit(app.exec())
