import json
from PyQt5.QtCore import QObject
from view.settings_view import SettingsView

class MapController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        # connect UI buttons (top_bar 隱藏但按鈕物件存在)
        try:
            self.view.add_btn.clicked.connect(self.on_add_marker_clicked)
            self.view.center_btn.clicked.connect(self.on_center_clicked)
            self.view.clear_btn.clicked.connect(self.on_clear_markers)

            # 新增：緊急停止 / 返回Home
            self.view.stop_btn.clicked.connect(self.on_emergency_stop)
            self.view.rtl_btn.clicked.connect(self.on_rtl)
        except Exception:
            # 如果 top_bar 被完全移除，這裡會發生例外，我們安全忽略
            pass

        # connect from JS (右鍵航點) -> Bridge slot emits waypointAdded signal
        self.view.bridge.waypointAdded.connect(self.on_waypoint_added)

        # IMPORTANT: 等 WebView 載入完成後再 sync（避免 setCenter 等函式尚未定義）
        self.view.webview.page().loadFinished.connect(self.sync_model_to_view)

    def sync_model_to_view(self, reset_center=False):
        """把 model 同步到 view (JS)"""
        c = self.model.center
        z = self.model.zoom

        # set center and clear markers
        if reset_center:
            self.view.run_js(f"setCenter({c['lat']}, {c['lng']}, {z});")
        self.view.run_js("clearMarkers();")

        coords = []
        for m in self.model.markers:
            label = (m.get("label") or "").replace("'", "\\'")
            js = f"addMarker('{m['id']}', {m['lat']}, {m['lng']}, '{label}');"
            self.view.run_js(js)
            coords.append([m['lat'], m['lng']])

        if len(coords) > 1:
            coord_js = json.dumps(coords)
            self.view.run_js(f"drawPath({coord_js});")

    def on_add_marker_clicked(self):
        try:
            lat = float(self.view.lat_input.text())
            lng = float(self.view.lng_input.text())
        except Exception:
            return
        marker = {
            "id": f"m{len(self.model.markers)+1}",
            "lat": lat, "lng": lng,
            "label": f"第{len(self.model.markers)+1}航點"
        }
        self.model.add_marker(marker)
        self.sync_model_to_view()

    def on_center_clicked(self):
        try:
            lat = float(self.view.lat_input.text())
            lng = float(self.view.lng_input.text())
        except Exception:
            return
        self.model.center = {"lat": lat, "lng": lng}

    def on_clear_markers(self):
        self.model.clear_markers()

    def on_waypoint_added(self, lat, lng):
        """由地圖右鍵新增航點時呼叫（Bridge.emit -> 這裡接收）"""
        marker = {
            "id": f"m{len(self.model.markers)+1}",
            "lat": lat, "lng": lng,
            "label": f"第{len(self.model.markers)+1}航點"
        }
        self.model.add_marker(marker)
        self.sync_model_to_view()

    # === 新增：控制按鈕事件 ===
    def on_emergency_stop(self):
        """緊急停止所有無人機"""
        print("⚠️ 按下緊急停止")
        self.model.emergency_stop()

    def on_rtl(self):
        """所有無人機返回Home"""
        print("🟢 按下返回Home")
        self.model.return_to_launch()


class SettingsController:
    def __init__(self, model):
        self.model = model
        self.view = SettingsView()

        # 綁定 "確認" 按鈕
        self.view.confirm_btn.clicked.connect(self.apply_settings)

    def apply_settings(self):
        # 讀取選項
        index_count = self.view.combo_drone_count.currentIndex()
        if index_count == 0:
            self.model.drone_count = 3
        elif index_count == 1:
            self.model.drone_count = 5

        formations = ["Line", "Wedge", "Square"]
        self.model.formation = formations[self.view.combo_formation.currentIndex()]
        self.view.close()
