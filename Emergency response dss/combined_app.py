from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, 
                             QLabel, QComboBox, QSpinBox, QTextEdit)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import requests
import mysql.connector
import traceback
import random
import string
from polyline import decode

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
        html_path = r"C:\Users\Administrator\Desktop\python projects\ERUI\map.html"
        print(f"Loading map from: {html_path}")
        self.map_view.setUrl(QUrl.fromLocalFile(html_path))
        self.map_view.loadFinished.connect(self.on_load_finished)
        self.map_view.page().javaScriptConsoleMessage = self.log_js_message
        self.map_view.setStyleSheet("border: 2px solid #34495E; border-radius: 5px;")
        self.layout.addWidget(self.map_view, stretch=1)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            font-size: 12px; color: #7F8C8D; padding: 5px;
            background-color: #ECF0F1; border-radius: 3px;
        """)
        self.layout.addWidget(self.status_label)

        self.setStyleSheet("background-color: #F4F6F6;")
        self.setLayout(self.layout)
        self.is_map_ready = False

    def log_js_message(self, level, message, line, source):
        print(f"JS [Line {line}]: {message}")

    def on_load_finished(self, ok):
        if ok:
            print("Map HTML loaded successfully")
            self.status_label.setText("Map loaded")
            self.map_view.page().runJavaScript("console.log('Map initialized in Qt');")
            self.is_map_ready = True
        else:
            print("Failed to load map.html")
            self.status_label.setText("Failed to load map")
            self.is_map_ready = False

    def display_route_on_map(self, start_lat, start_lon, end_lat, end_lon):
        try:
            if not self.is_map_ready:
                print("Map not ready yet, delaying route display...")
                QTimer.singleShot(1000, lambda: self.display_route_on_map(start_lat, start_lon, end_lat, end_lon))
                return

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
                    if (typeof map !== 'undefined') {{
                        map.eachLayer(layer => {{ if (layer instanceof L.Marker || layer instanceof L.Polyline) map.removeLayer(layer); }});
                        L.marker([{start_lat}, {start_lon}]).addTo(map).bindPopup('Your Location').openPopup();
                        L.marker([{end_lat}, {end_lon}]).addTo(map).bindPopup('Nearest Hospital').openPopup();
                        var routeCoords = {route_coords_str};
                        var routeLatLngs = routeCoords.map(coord => [coord[0], coord[1]]);
                        L.polyline(routeLatLngs, {{color: 'blue'}}).addTo(map);
                        map.fitBounds(routeLatLngs);
                        map.invalidateSize();
                    }} else {{
                        console.log('Map object not defined');
                    }}
                    """
                    print(f"Running JS: {js[:100]}...")
                    self.map_view.page().runJavaScript(js)
                    self.status_label.setText("Route displayed")
                else:
                    print("No routes found. Showing markers only.")
                    self.status_label.setText("No route found")
                    js = f"""
                    console.log('Adding markers only');
                    if (typeof map !== 'undefined') {{
                        map.eachLayer(layer => {{ if (layer instanceof L.Marker || layer instanceof L.Polyline) map.removeLayer(layer); }});
                        L.marker([{start_lat}, {start_lon}]).addTo(map).bindPopup('Your Location').openPopup();
                        L.marker([{end_lat}, {end_lon}]).addTo(map).bindPopup('Nearest Hospital').openPopup();
                        map.invalidateSize();
                    }}
                    """
                    self.map_view.page().runJavaScript(js)
            else:
                print(f"Route error: {response.status_code} - {response.text}")
                self.status_label.setText("Routing error")
                js = f"""
                console.log('Adding markers only due to API error');
                if (typeof map !== 'undefined') {{
                    map.eachLayer(layer => {{ if (layer instanceof L.Marker || layer instanceof L.Polyline) map.removeLayer(layer); }});
                    L.marker([{start_lat}, {start_lon}]).addTo(map).bindPopup('Your Location').openPopup();
                    L.marker([{end_lat}, {end_lon}]).addTo(map).bindPopup('Nearest Hospital').openPopup();
                    map.invalidateSize();
                }}
                """
                self.map_view.page().runJavaScript(js)
        except Exception as e:
            print(f"Error in display_route_on_map: {str(e)}")
            traceback.print_exc()
            self.status_label.setText("Error displaying route")

class TriageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emergency Triage System")
        self.setGeometry(200, 200, 650, 650)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(15)

        self.title_label = QLabel("Emergency Triage System")
        self.title_label.setStyleSheet("""
            font-size: 28px; font-weight: bold; color: #FFFFFF; 
            padding: 15px; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #3498DB, stop:1 #2980B9); 
            border-radius: 8px; border: 1px solid #2C3E50;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.input_layout = QHBoxLayout()
        self.input_layout.setSpacing(20)

        self.left_layout = QVBoxLayout()
        self.left_layout.setSpacing(10)
        self.name_label = QLabel("Patient Name:")
        self.name_label.setStyleSheet("font-size: 16px; color: #2C3E50; font-weight: bold;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter patient name")
        self.name_input.setStyleSheet("""
            QLineEdit { font-size: 14px; padding: 10px; border: 2px solid #BDC3C7; 
                       border-radius: 6px; background-color: #FFFFFF; }
            QLineEdit:focus { border: 2px solid #3498DB; }
        """)
        self.age_label = QLabel("Age:")
        self.age_label.setStyleSheet("font-size: 16px; color: #2C3E50; font-weight: bold;")
        self.age_input = QSpinBox()
        self.age_input.setRange(0, 150)
        self.age_input.setStyleSheet("font-size: 14px; padding: 5px; border: 2px solid #BDC3C7; border-radius: 6px;")
        self.gender_label = QLabel("Gender:")
        self.gender_label.setStyleSheet("font-size: 16px; color: #2C3E50; font-weight: bold;")
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        self.gender_input.setStyleSheet("font-size: 14px; padding: 5px; border: 2px solid #BDC3C7; border-radius: 6px;")
        self.location_label = QLabel("Location:")
        self.location_label.setStyleSheet("font-size: 16px; color: #2C3E50; font-weight: bold;")
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("e.g., Langata, Nairobi")
        self.location_input.setStyleSheet("""
            QLineEdit { font-size: 14px; padding: 10px; border: 2px solid #BDC3C7; 
                       border-radius: 6px; background-color: #FFFFFF; }
            QLineEdit:focus { border: 2px solid #3498DB; }
        """)
        self.left_layout.addWidget(self.name_label)
        self.left_layout.addWidget(self.name_input)
        self.left_layout.addWidget(self.age_label)
        self.left_layout.addWidget(self.age_input)
        self.left_layout.addWidget(self.gender_label)
        self.left_layout.addWidget(self.gender_input)
        self.left_layout.addWidget(self.location_label)
        self.left_layout.addWidget(self.location_input)
        self.input_layout.addLayout(self.left_layout)

        self.right_layout = QVBoxLayout()
        self.right_layout.setSpacing(10)
        self.condition_label = QLabel("Condition:")
        self.condition_label.setStyleSheet("font-size: 16px; color: #2C3E50; font-weight: bold;")
        self.condition_input = QComboBox()
        self.condition_input.addItems(["Breathing Difficulty", "Bleeding", "Chest Pain", "Unconscious", "Fever", "Other"])
        self.condition_input.setStyleSheet("font-size: 14px; padding: 5px; border: 2px solid #BDC3C7; border-radius: 6px;")
        self.severity_label = QLabel("Severity:")
        self.severity_label.setStyleSheet("font-size: 16px; color: #2C3E50; font-weight: bold;")
        self.severity_input = QComboBox()
        self.severity_input.addItems(["Mild", "Moderate", "Severe"])
        self.severity_input.setStyleSheet("font-size: 14px; padding: 5px; border: 2px solid #BDC3C7; border-radius: 6px;")
        self.details_label = QLabel("Details:")
        self.details_label.setStyleSheet("font-size: 16px; color: #2C3E50; font-weight: bold;")
        self.details_input = QTextEdit()
        self.details_input.setPlaceholderText("Additional symptoms or notes")
        self.details_input.setStyleSheet("""
            QTextEdit { font-size: 14px; padding: 10px; border: 2px solid #BDC3C7; 
                        border-radius: 6px; background-color: #FFFFFF; }
            QTextEdit:focus { border: 2px solid #3498DB; }
        """)
        self.right_layout.addWidget(self.condition_label)
        self.right_layout.addWidget(self.condition_input)
        self.right_layout.addWidget(self.severity_label)
        self.right_layout.addWidget(self.severity_input)
        self.right_layout.addWidget(self.details_label)
        self.right_layout.addWidget(self.details_input)
        self.input_layout.addLayout(self.right_layout)

        self.layout.addLayout(self.input_layout)

        self.assess_button = QPushButton("Assess Patient")
        self.assess_button.setStyleSheet("""
            QPushButton { font-size: 18px; padding: 12px; background-color: #27AE60; 
                         color: white; border: none; border-radius: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #219653; }
        """)
        self.assess_button.clicked.connect(self.assess_patient)
        self.assess_button.setCursor(Qt.PointingHandCursor)
        self.layout.addWidget(self.assess_button, alignment=Qt.AlignCenter)

        self.result_widget = QWidget()
        self.result_widget.setStyleSheet("""
            background-color: #ECF0F1; border-radius: 8px; padding: 10px;
        """)
        self.result_layout = QVBoxLayout(self.result_widget)
        self.result_layout.setSpacing(8)
        self.priority_label = QLabel("Triage Result: N/A")
        self.priority_label.setStyleSheet("font-size: 14px; color: #34495E;")
        self.recommendation_label = QLabel("Recommendation: N/A")
        self.recommendation_label.setStyleSheet("font-size: 14px; color: #34495E;")
        self.hospital_label = QLabel("Nearest Hospital: N/A")
        self.hospital_label.setStyleSheet("font-size: 14px; color: #34495E;")
        self.case_id_label = QLabel("Case ID: N/A")
        self.case_id_label.setStyleSheet("font-size: 14px; color: #34495E;")
        self.result_layout.addWidget(self.priority_label)
        self.result_layout.addWidget(self.recommendation_label)
        self.result_layout.addWidget(self.hospital_label)
        self.result_layout.addWidget(self.case_id_label)
        self.layout.addWidget(self.result_widget)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            font-size: 12px; color: #7F8C8D; padding: 8px; 
            background-color: #ECF0F1; border-radius: 5px;
        """)
        self.layout.addWidget(self.status_label)

        self.setStyleSheet("background-color: #F7F9FA;")
        self.setLayout(self.layout)

        self.map_window = None

    def generate_case_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def assess_patient(self):
        try:
            name = self.name_input.text().strip()
            age = self.age_input.value()
            gender = self.gender_input.currentText()
            location = self.location_input.text().strip()
            condition = self.condition_input.currentText()
            severity = self.severity_input.currentText()
            details = self.details_input.toPlainText().strip()

            print(f"Assessing patient: {name}, {age}, {gender}, {location}, {condition}, {severity}, {details}")

            if not location:
                self.status_label.setText("Please enter a location.")
                print("Missing location")
                return
            if not condition or not severity:
                self.status_label.setText("Please select condition and severity.")
                print("Missing condition or severity")
                return

            if severity == "Severe" and condition in ["Unconscious", "Chest Pain", "Bleeding"]:
                priority = "Critical"
                color = "#E74C3C"
                recommendation = "Seek immediate medical attention."
                if condition == "Bleeding":
                    recommendation = "Apply pressure to wound, seek immediate medical attention."
                elif condition == "Unconscious":
                    recommendation = "Check airway, call emergency services now."
            elif severity == "Moderate" or condition == "Breathing Difficulty":
                priority = "Urgent"
                color = "#F1C40F"
                recommendation = "Monitor closely, proceed to hospital soon."
            else:
                priority = "Stable"
                color = "#27AE60"
                recommendation = "Monitor condition, visit hospital if symptoms worsen."

            print(f"Triage result: {priority}, Recommendation: {recommendation}")
            self.priority_label.setText(f"Triage Result: {priority}")
            self.priority_label.setStyleSheet(f"font-size: 14px; color: #34495E; background-color: {color}; padding: 5px; border-radius: 3px;")
            self.recommendation_label.setText(f"Recommendation: {recommendation}")

            lat, lon = self.geocode_address(location)
            print(f"Geocoding returned: lat={lat}, lon={lon}")
            if lat is not None and lon is not None:
                print(f"Proceeding with coordinates: {lat}, {lon}")
                nearest_hospital = self.get_nearest_hospital(lat, lon)
                print(f"Nearest hospital result: {nearest_hospital}")
                if nearest_hospital:
                    self.hospital_label.setText(f"Nearest Hospital: {nearest_hospital['HospitalName']} ({nearest_hospital['Latitude']}, {nearest_hospital['Longitude']})")
                    case_id = self.generate_case_id()
                    self.log_to_database(case_id, condition, location, severity)
                    self.case_id_label.setText(f"Case ID: {case_id}")
                    self.status_label.setText("Assessment complete, opening map...")
                    print("Opening MapApp...")
                    if not self.map_window:
                        print("Creating new MapApp instance")
                        self.map_window = MapApp()
                    print(f"Calling display_route_on_map with {lat}, {lon}, {nearest_hospital['Latitude']}, {nearest_hospital['Longitude']}")
                    self.map_window.display_route_on_map(lat, lon, nearest_hospital['Latitude'], nearest_hospital['Longitude'])
                    print("Showing map window")
                    self.map_window.show()
                    self.map_window.raise_()
                    self.map_window.activateWindow()
                else:
                    self.hospital_label.setText("Nearest Hospital: Not found, using fallback")
                    self.status_label.setText("No hospital found, using fallback")
                    print("No hospital found, using fallback")
                    # Fallback to Nairobi Hospital
                    fallback_hospital = {'HospitalName': 'Nairobi Hospital', 'Latitude': -1.2955, 'Longitude': 36.8018}
                    case_id = self.generate_case_id()
                    self.log_to_database(case_id, condition, location, severity)
                    self.case_id_label.setText(f"Case ID: {case_id}")
                    print("Opening MapApp with fallback...")
                    if not self.map_window:
                        print("Creating new MapApp instance")
                        self.map_window = MapApp()
                    print(f"Calling display_route_on_map with {lat}, {lon}, {fallback_hospital['Latitude']}, {fallback_hospital['Longitude']}")
                    self.map_window.display_route_on_map(lat, lon, fallback_hospital['Latitude'], fallback_hospital['Longitude'])
                    print("Showing map window")
                    self.map_window.show()
                    self.map_window.raise_()
                    self.map_window.activateWindow()
            else:
                self.hospital_label.setText("Nearest Hospital: N/A")
                self.status_label.setText("Geocoding failed")
                print("Geocoding returned None")

        except Exception as e:
            print(f"Error in assess_patient: {str(e)}")
            traceback.print_exc()
            self.status_label.setText("Error during assessment")

    def geocode_address(self, address):
        geocode_api_url = f"https://api.geoapify.com/v1/geocode/search?text={address}&apiKey=eab03be52f944bc5992fc2a89e7f6d25"
        try:
            response = requests.get(geocode_api_url)
            print(f"Geocode API status: {response.status_code}")
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
            print("MySQL connection established")
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
            print("No hospitals found in database")
            return None
        except mysql.connector.Error as e:
            print(f"MySQL error in get_nearest_hospital: {str(e)}")
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"Unexpected error in get_nearest_hospital: {str(e)}")
            traceback.print_exc()
            return None

    def log_to_database(self, case_id, emergency_type, location, severity):
        try:
            print("Connecting to MySQL for logging...")
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="erdss_db")
            print("MySQL connection established for logging")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emergency_cases (
                    case_id VARCHAR(8) PRIMARY KEY,
                    emergency_type VARCHAR(50),
                    location VARCHAR(100),
                    severity VARCHAR(20)
                )
            """)
            query = "INSERT INTO emergency_cases (case_id, emergency_type, location, severity) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (case_id, emergency_type, location, severity))
            conn.commit()
            conn.close()
            print(f"Logged case: {case_id}, {emergency_type}, {location}, {severity}")
        except mysql.connector.Error as e:
            print(f"MySQL error during logging: {str(e)}")
            traceback.print_exc()
            self.status_label.setText("Error logging to database")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TriageApp()
    window.show()
    sys.exit(app.exec_())