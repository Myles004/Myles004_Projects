# map_app.py
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import requests
import mysql.connector
from polyline import decode
import traceback

class MapApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ER System - Hospitals Map")
        self.setGeometry(100, 100, 900, 700)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self.title_label = QLabel("Emergency Response Map")
        self.title_label.setStyleSheet("""
            font-size: 24px; font-weight: bold; color: #2C3E50; 
            padding: 10px; background-color: #ECF0F1; border-radius: 5px;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.map_view = QWebEngineView()
        html_path = r"C:\Users\Administrator\Desktop\python projects\maindocs"
        print(f"Loading map from: {html_path}")
        self.map_view.setUrl(QUrl.fromLocalFile(html_path))
        self.map_view.loadFinished.connect(self.on_load_finished)
        self.map_view.page().javaScriptConsoleMessage = self.log_js_message
        self.map_view.setStyleSheet("border: 2px solid #34495E; border-radius: 5px;")
        self.layout.addWidget(self.map_view, stretch=1)

        self.input_layout = QHBoxLayout()
        self.input_layout.setSpacing(10)

        self.label = QLabel("Enter Location:")
        self.label.setStyleSheet("font-size: 16px; color: #34495E; font-weight: bold;")
        self.input_layout.addWidget(self.label)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("e.g., Ngara, Nairobi, Kenya")
        self.input_field.setStyleSheet("""
            QLineEdit { font-size: 14px; padding: 8px; border: 2px solid #BDC3C7; 
                       border-radius: 5px; background-color: #FFFFFF; }
            QLineEdit:focus { border: 2px solid #3498DB; }
        """)
        self.input_field.setMinimumWidth(300)
        self.input_layout.addWidget(self.input_field)

        self.route_button = QPushButton("Find Nearest Hospital")
        self.route_button.setStyleSheet("""
            QPushButton { font-size: 14px; padding: 10px; background-color: #3498DB; 
                         color: white; border: none; border-radius: 5px; font-weight: bold; }
            QPushButton:hover { background-color: #2980B9; }
        """)
        self.route_button.clicked.connect(self.find_nearest_hospital)
        self.route_button.setCursor(Qt.PointingHandCursor)
        self.input_layout.addWidget(self.route_button)
        self.input_layout.addStretch()

        self.layout.addLayout(self.input_layout)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("font-size: 12px; color: #7F8C8D; padding: 5px; background-color: #ECF0F1; border-radius: 3px;")
        self.layout.addWidget(self.status_label)

        self.setStyleSheet("background-color: #F4F6F6;")
        self.setLayout(self.layout)

        self.init_db()

    def log_js_message(self, level, message, line, source):
        print(f"JS [Line {line}]: {message}")

    def on_load_finished(self, ok):
        if ok:
            print("Map HTML loaded successfully")
            self.status_label.setText("Map loaded")
            self.map_view.page().runJavaScript("console.log('Map initialized in Qt');")
        else:
            print("Failed to load map.html")
            self.status_label.setText("Failed to load map")

    def init_db(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="erdss_db")
            cursor = conn.cursor()
            cursor.execute("SELECT HospitalName, Latitude, Longitude, Capacity FROM hospitals")
            hospitals = cursor.fetchall()
            print(f"All hospitals in database ({len(hospitals)} total): {hospitals}")
            conn.close()
            print("MySQL database accessed successfully.")
            self.status_label.setText(f"Database connected ({len(hospitals)} hospitals)")
        except mysql.connector.Error as e:
            print(f"MySQL initialization error: {str(e)}")
            traceback.print_exc()
            self.status_label.setText("Database error")

    def find_nearest_hospital(self):
        try:
            location = self.input_field.text()
            print(f"Finding hospital for location: {location}")
            self.status_label.setText(f"Searching for {location}...")
            location_lat, location_lon = self.geocode_address(location)
            if location_lat is not None and location_lon is not None:
                nearest_hospital = self.get_nearest_hospital(location_lat, location_lon)
                if nearest_hospital:
                    print(f"Nearest hospital: {nearest_hospital['HospitalName']} at ({nearest_hospital['Latitude']}, {nearest_hospital['Longitude']})")
                    self.status_label.setText(f"Nearest: {nearest_hospital['HospitalName']}")
                    self.display_route_on_map(location_lat, location_lon, nearest_hospital['Latitude'], nearest_hospital['Longitude'])
                else:
                    print("No hospital found. Using fallback.")
                    self.status_label.setText("No hospital found, using fallback")
                    nearest_hospital = {'HospitalName': 'Nairobi Hospital', 'Latitude': -1.2833, 'Longitude': 36.8167, 'Capacity': 200}
                    self.display_route_on_map(location_lat, location_lon, nearest_hospital['Latitude'], nearest_hospital['Longitude'])
            else:
                print("Geocoding failed.")
                self.status_label.setText("Geocoding failed")
        except Exception as e:
            print(f"Error in find_nearest_hospital: {str(e)}")
            traceback.print_exc()
            self.status_label.setText("Error occurred")

    def geocode_address(self, address):
        geocode_api_url = f"https://api.geoapify.com/v1/geocode/search?text={address}&apiKey=eab03be52f944bc5992fc2a89e7f6d25"
        try:
            response = requests.get(geocode_api_url)
            if response.status_code == 200:
                geocode_data = response.json()
                if "features" in geocode_data and len(geocode_data["features"]) > 0:
                    lat = geocode_data["features"][0]["geometry"]["coordinates"][1]
                    lon = geocode_data["features"][0]["geometry"]["coordinates"][0]
                    print(f"Geocoded {address} to ({lat}, {lon})")
                    return lat, lon
                else:
                    print(f"No results found for address: {address}")
                    return None, None
            else:
                print(f"Geocoding API error: {response.status_code} - {response.text}")
                return None, None
        except requests.RequestException as e:
            print(f"Network error during geocoding: {str(e)}")
            return None, None

    def get_nearest_hospital(self, lat, lon):
        try:
            print("Connecting to MySQL...")
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="erdss_db")
            cursor = conn.cursor()
            query = """
            SELECT HospitalName, Latitude, Longitude, Capacity,
            (6371 * acos(cos(radians(%s)) * cos(radians(Latitude)) 
            * cos(radians(Longitude) - radians(%s)) 
            + sin(radians(%s)) * sin(radians(Latitude)))) AS distance
            FROM hospitals
            ORDER BY distance ASC
            LIMIT 1
            """
            print(f"Executing query with lat={lat}, lon={lon}")
            cursor.execute(query, (lat, lon, lat))
            result = cursor.fetchone()
            conn.close()
            print(f"Query result: {result}")
            if result:
                return {'HospitalName': result[0], 'Latitude': result[1], 'Longitude': result[2], 'Capacity': result[3]}
            print("No hospitals found in database.")
            return None
        except mysql.connector.Error as e:
            print(f"MySQL error: {str(e)}")
            traceback.print_exc()
            return None

    def display_route_on_map(self, start_lat, start_lon, end_lat, end_lon):
        try:
            print(f"Displaying route from ({start_lat}, {start_lon}) to ({end_lat}, {end_lon})")
            api_url = "https://api.openrouteservice.org/v2/directions/driving-car"
            api_key = "5b3ce3597851110001cf62486fe89220248c4016a5c67793cd7f8187"
            headers = {"Authorization": api_key, "Content-Type": "application/json"}
            body = {"coordinates": [[start_lon, start_lat], [end_lon, end_lat]]}
            print("Requesting route from OpenRouteService...")
            response = requests.post(api_url, json=body, headers=headers)
            print(f"API Response Status: {response.status_code}")
            if response.status_code == 200:
                route_data = response.json()
                if "routes" in route_data and len(route_data["routes"]) > 0:
                    route_geometry = route_data['routes'][0]['geometry']
                    decoded_coords = decode(route_geometry)
                    print(f"Decoded route coordinates (first 5): {decoded_coords[:5]}")
                    route_coords_str = str([[lat, lon] for lat, lon in decoded_coords]).replace("'", "")
                    js = f"""
                    console.log('Updating map with route');
                    map.eachLayer(layer => {{ if (layer instanceof L.Marker || layer instanceof L.Polyline) map.removeLayer(layer); }});
                    L.marker([{start_lat}, {start_lon}]).addTo(map).bindPopup('Your Location').openPopup();
                    L.marker([{end_lat}, {end_lon}]).addTo(map).bindPopup('Nearest Hospital').openPopup();
                    var routeCoords = {route_coords_str};
                    var routeLatLngs = routeCoords.map(coord => [coord[0], coord[1]]);
                    L.polyline(routeLatLngs, {{color: 'blue'}}).addTo(map);
                    map.fitBounds(routeLatLngs);
                    """
                    print(f"Running JS: {js[:100]}...")
                    self.map_view.page().runJavaScript(js)
                    self.status_label.setText("Route displayed")
                else:
                    print("No routes found. Showing markers only.")
                    self.status_label.setText("No route found")
                    js = f"""
                    console.log('Adding markers only');
                    map.eachLayer(layer => {{ if (layer instanceof L.Marker || layer instanceof L.Polyline) map.removeLayer(layer); }});
                    L.marker([{start_lat}, {start_lon}]).addTo(map).bindPopup('Your Location').openPopup();
                    L.marker([{end_lat}, {end_lon}]).addTo(map).bindPopup('Nearest Hospital').openPopup();
                    """
                    self.map_view.page().runJavaScript(js)
            else:
                print(f"Route error: {response.status_code} - {response.text}")
                self.status_label.setText("Routing error")
        except Exception as e:
            print(f"Error in display_route_on_map: {str(e)}")
            traceback.print_exc()
            self.status_label.setText("Error displaying route")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapApp()
    window.show()
    sys.exit(app.exec_())