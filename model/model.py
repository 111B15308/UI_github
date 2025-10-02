from PyQt5.QtCore import QObject, pyqtSignal

class MapModel(QObject):
    state_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._center = {"lat": 25.033964, "lng": 121.564468}  # 預設台北101
        self._zoom = 14
        self._markers = []

        # 無人機參數
        self.drone_settings = {
            "port": "",
            "ip": "",
            "spacing": "",
            "alt_step": "",
            "rtl_height": "",
            "speed": "",
        }
        self._drone_count = 3
        self._formation = "Line"

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

    def set_drone_settings(self, settings: dict):
        """存放無人機設定"""
        self.drone_settings.update(settings)
        self.state_changed.emit()
    
    @property
    def drone_count(self):
        return self._drone_count
    
    @drone_count.setter
    def drone_count(self, val):
        self._drone_count = val
        self.state_changed.emit()
    
    @property
    def formation(self):
        return self._formation
    
    @formation.setter
    def formation(self, val):
        self._formation = val
        self.state_changed.emit()
