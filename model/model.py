from PyQt5.QtCore import QObject, pyqtSignal

class MapModel(QObject):
    # === Signals ===
    state_changed = pyqtSignal()
    emergency_stop_signal = pyqtSignal()
    rtl_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._center = {"lat": 25.033964, "lng": 121.564468}  # 預設中心（台北101）
        self._zoom = 14
        self._markers = []

        # 模擬無人機設定
        self.drone_count = 0
        self.formation = "Line"
        self.drone_configs = []

    # === Map 狀態 ===
    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, val):
        self._center = val
        self.state_changed.emit()

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, val):
        self._zoom = val
        self.state_changed.emit()

    @property
    def markers(self):
        return list(self._markers)

    def add_marker(self, marker):
        self._markers.append(marker)
        self.state_changed.emit()

    def clear_markers(self):
        self._markers = []
        self.state_changed.emit()

    # === 無人機控制 ===
    def emergency_stop(self):
        """觸發所有無人機緊急停止"""
        print("⚠️ 緊急停止")
        self.emergency_stop_signal.emit()

    def return_to_launch(self):
        """觸發所有無人機返回 Home"""
        print("所有無人機轉換為RTL模式")
        self.rtl_signal.emit()
