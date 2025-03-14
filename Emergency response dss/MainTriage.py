import sys
import mysql.connector
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QGroupBox, QCheckBox, QPushButton, QTextBrowser,
    QHBoxLayout, QLineEdit, QSizePolicy
)

class TriageInputApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Triage Input Form")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.WindowMaximizeButtonHint)
        self.init_ui()
        self.create_database()

    def init_ui(self):
        self.resize(850, 600)
        self.setStyleSheet("background-color: #f4f4f4;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        self.title_label = QLabel("Triage Input Form")
        self.title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #333;")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        self.case_id_input = QLineEdit()
        self.case_id_input.setReadOnly(True)
        self.case_id_input.setPlaceholderText("Auto-generated Case ID")
        self.case_id_input.setStyleSheet("padding: 8px; font-size: 12pt; background-color: #e0e0e0;")
        layout.addWidget(self.case_id_input)
        
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Enter your location (e.g., Nairobi, Kenya)")
        self.location_input.setStyleSheet("padding: 8px; font-size: 12pt;")
        layout.addWidget(self.location_input)
        
        self.symptoms_group = QGroupBox("Select Symptoms")
        self.symptoms_layout = QVBoxLayout()
        self.symptoms_group.setLayout(self.symptoms_layout)
        self.symptoms_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.symptom_checkboxes = {
            "Trouble Breathing": QCheckBox("Trouble Breathing"),
            "Uncontrolled Bleeding": QCheckBox("Uncontrolled Bleeding"),
            "No Sign of Life": QCheckBox("No Sign of Life"),
            "Severe Pain": QCheckBox("Severe Pain"),
            "Visible Fractures": QCheckBox("Visible Fractures"),
            "Dizziness": QCheckBox("Dizziness"),
            "Minor Injuries": QCheckBox("Minor Injuries"),
            "Chest Pain": QCheckBox("Chest Pain"),
            "Seizures": QCheckBox("Seizures"),
            "Burns": QCheckBox("Burns"),
            "Pregnancy Complications": QCheckBox("Pregnancy Complications"),
            "Unconcious": QCheckBox("Unconcious"),
        }
        
        for checkbox in self.symptom_checkboxes.values():
            checkbox.setStyleSheet("font-size: 12pt;")
            self.symptoms_layout.addWidget(checkbox)
        
        layout.addWidget(self.symptoms_group)
        
        self.button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 12pt;")
        self.submit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-size: 12pt;")
        self.reset_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.button_layout.addWidget(self.submit_button)
        self.button_layout.addWidget(self.reset_button)
        layout.addLayout(self.button_layout)
        
        self.result_display = QTextBrowser()
        self.result_display.setText("Triage Category: [Result will appear here]")
        self.result_display.setStyleSheet("font-size: 14pt; border: 1px solid #ccc; padding: 10px; background-color: #fff;")
        self.result_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.result_display)
        
        self.setLayout(layout)
        
        self.submit_button.clicked.connect(self.on_submit)
        self.reset_button.clicked.connect(self.on_reset)
        self.generate_case_id()
    
    def create_database(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="erdss_db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emergency_cases (
                id INT AUTO_INCREMENT PRIMARY KEY,
                case_id VARCHAR(20),
                emergency_type VARCHAR(255),
                location VARCHAR(255),
                severity VARCHAR(255),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def generate_case_id(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="erdss_db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM emergency_cases")
        count = cursor.fetchone()[0] + 1
        self.case_id_input.setText(f"CASE-{count:05d}")
        conn.close()
    
    def on_submit(self):
        selected_symptoms = [symptom for symptom, checkbox in self.symptom_checkboxes.items() if checkbox.isChecked()]
        emergency_type = ", ".join(selected_symptoms) if selected_symptoms else "Unknown"
        result = self.determine_priority(selected_symptoms)
        self.result_display.setText(result)
        self.save_case(emergency_type, result)
        self.generate_case_id()
    
    def save_case(self, emergency_type, severity):
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="erdss_db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO emergency_cases (case_id, emergency_type, location, severity)
            VALUES (%s, %s, %s, %s)
        """, (self.case_id_input.text(), emergency_type, self.location_input.text(), severity))
        conn.commit()
        conn.close()
    
    def on_reset(self):
        for checkbox in self.symptom_checkboxes.values():
            checkbox.setChecked(False)
        self.result_display.setText("Triage Category: [Result will appear here]")
        self.location_input.clear()
    
    def determine_priority(self, selected_symptoms):
        symptom_scores = {"Trouble Breathing": 10, "Uncontrolled Bleeding": 10, "No Sign of Life": 10, "Severe Pain": 7, "Visible Fractures": 7, "Dizziness": 5, "Minor Injuries": 3, "Chest Pain": 6, "Seizures": 10, "Burns": 6, "Pregnancy Complications": 15, "Unconcious": 7}
        total_score = sum([symptom_scores[symptom] for symptom in selected_symptoms])
        
        if total_score >= 15:
            return "High Priority"
        elif 8 <= total_score < 15:
            return "Medium Priority"
        else:
            return "Low Priority"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TriageInputApp()
    window.showMaximized()
    sys.exit(app.exec_())
