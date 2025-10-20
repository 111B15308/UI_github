# view/startup_dialog.py
from PyQt5 import QtWidgets, QtGui

class StartupDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("啟動設定")
        self.resize(300, 100)

        layout = QtWidgets.QFormLayout(self)

        # Port (改成 QLineEdit + 驗證器)
        self.port_input = QtWidgets.QLineEdit()
        self.port_input.setPlaceholderText("輸入 Port (1000~10000)預設:5760")
        self.port_input.setValidator(QtGui.QIntValidator(1, 99999))

        # 高度 (1~30 公尺)
        self.alt_input = QtWidgets.QSpinBox()
        self.alt_input.setRange(1, 30)
        self.alt_input.setValue(15)

        # 速度 (1~10 m/s)
        self.speed_input = QtWidgets.QDoubleSpinBox()
        self.speed_input.setRange(1, 10)
        self.speed_input.setValue(5)
        self.speed_input.setDecimals(1)

        layout.addRow("Port:", self.port_input)
        layout.addRow("高度 (m):", self.alt_input)
        layout.addRow("速度 (m/s):", self.speed_input)

        # 確認按鈕
        self.confirm_btn = QtWidgets.QPushButton("確認")
        self.confirm_btn.clicked.connect(self.validate_and_accept)
        layout.addRow(self.confirm_btn)

    def validate_and_accept(self):
        """檢查輸入值是否在範圍內，否則跳出小視窗"""
        # 檢查 Port
        try:
            port = int(self.port_input.text())
        except ValueError:
            self.show_error("Port 必須是數字!")
            return

        altitude = self.alt_input.value()
        speed = self.speed_input.value()

        if not (1000 <= port <= 10000):
            self.show_error("Port 超出輸入範圍!! (1000 ~ 10000)")
            return
        if not (1 <= altitude <= 30):
            self.show_error("高度超出輸入範圍!! (1 ~ 30)")
            return
        if not (1 <= speed <= 10):
            self.show_error("速度超出輸入範圍!! (1 ~ 10)")
            return

        # 如果全部合法，就關閉視窗
        self.accept()

    def show_error(self, message):
        """跳出錯誤提示小視窗"""
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("錯誤")
        msg.setText(message)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
