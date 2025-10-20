import sys
from PyQt5.QtWidgets import QApplication, QDialog

from model.model import MapModel
from view.view import MapView
from controller.controller import MapController

# 設定視窗 (無人機數量 / 隊形)
from view.settings_dialog import SettingsDialog
# 每台無人機的詳細參數設定
from view.drone_config_dialog import DroneConfigDialog

def main():
    app = QApplication(sys.argv)

    # --- 1. 先顯示無人機數量 + 隊形設定 ---
    settings_dialog = SettingsDialog()
    if settings_dialog.exec_() != QDialog.Accepted:
        sys.exit(0)

    settings = settings_dialog.get_settings()
    drone_count = settings["drone_count"]

    # --- 2. 根據數量，依序顯示每台無人機的設定視窗 ---
    drone_configs = []
    for i in range(drone_count):
        dlg = DroneConfigDialog(i + 1)  # 第1台、第2台…
        if dlg.exec_() == QDialog.Accepted:
            config = {
                "port": int(dlg.port_input.text()),
                "altitude": dlg.alt_input.value(),
                "speed": dlg.speed_input.value()
            }
            drone_configs.append(config)
        else:
            sys.exit(0)  # 使用者取消 → 直接退出程式

    # --- 3. 建立 Model 並存入設定 ---
    model = MapModel()
    model.drone_count = drone_count
    model.formation = settings.get("formation", "Line")
    model.drone_configs = drone_configs

    # --- 4. 顯示地圖 ---
    view = MapView(model)
    controller = MapController(model, view)
    view.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()