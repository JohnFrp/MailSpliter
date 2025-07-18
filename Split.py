import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QFileDialog, QMessageBox,
    QComboBox, QCheckBox, QLineEdit
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from qt_material import apply_stylesheet


class EmailPasswordSplitter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email-Password Splitter")
        self.setMinimumSize(700, 600)
        
        self.setWindowIcon(QIcon("email.ico"))
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title label
        title_label = QLabel("Email-Password Splitter")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #6bff33;")
        layout.addWidget(title_label)
        
        # Filter controls
        filter_group = QWidget()
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.setContentsMargins(0, 0, 0, 0)
        
        self.filter_check = QCheckBox("Filter By Email Domain:             ")
        self.filter_check.setChecked(False)
        self.filter_check.stateChanged.connect(self.toggle_filter)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "custom"])
        self.filter_combo.setEnabled(False)
        
        self.custom_domain = QLineEdit()
        self.custom_domain.setPlaceholderText("Enter custom domain")
        self.custom_domain.setEnabled(False)
        self.custom_domain.setVisible(False)
        
        filter_layout.addWidget(self.filter_check)
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(self.custom_domain)
        filter_layout.addStretch()
        
        layout.addWidget(filter_group)
        
        # Remove domain controls
        remove_group = QWidget()
        remove_layout = QHBoxLayout(remove_group)
        remove_layout.setContentsMargins(0, 0, 0, 0)
        
        self.remove_check = QCheckBox("Remove Selected Domain:      ")
        self.remove_check.setChecked(False)
        self.remove_check.stateChanged.connect(self.toggle_remove)
        
        self.remove_combo = QComboBox()
        self.remove_combo.addItems(["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "custom"])
        self.remove_combo.setEnabled(False)
        
        self.remove_custom_domain = QLineEdit()
        self.remove_custom_domain.setPlaceholderText("Enter custom domain to remove")
        self.remove_custom_domain.setEnabled(False)
        self.remove_custom_domain.setVisible(False)
        
        remove_layout.addWidget(self.remove_check)
        remove_layout.addWidget(self.remove_combo)
        remove_layout.addWidget(self.remove_custom_domain)
        remove_layout.addStretch()
        
        layout.addWidget(remove_group)
        
        # Input area
        input_label = QLabel("")
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("example@gmail.com:password123\nanother@email.com:securepass")
        self.input_text.setMinimumHeight(150)
        layout.addWidget(input_label)
        layout.addWidget(self.input_text)
        
        # Button row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.process_btn = QPushButton("Save")
        self.process_btn.setFixedHeight(40)
        self.process_btn.clicked.connect(self.process_and_save)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedHeight(40)
        self.clear_btn.clicked.connect(self.clear_input)
        
        button_layout.addWidget(self.process_btn)
        button_layout.addWidget(self.clear_btn)
        layout.addLayout(button_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Apply styles
        self.apply_custom_styles()
        
        # Connect filter combo change
        self.filter_combo.currentTextChanged.connect(self.handle_combo_change)
        self.remove_combo.currentTextChanged.connect(self.handle_remove_combo_change)
    
    def apply_custom_styles(self):
        apply_stylesheet(self, theme='dark_teal.xml')
        
        self.setStyleSheet(self.styleSheet() + """
            QTextEdit, QPushButton, QComboBox, QLineEdit, QCheckBox {
                border-radius: 8px;
                padding: 8px;
                color: #6bff33;
            }
            QTextEdit, QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                width: 300px;
            }
            QPushButton {
                min-width: 100px;
                font-weight: bold;
            }
            QMainWindow {
                background-color: #1e1e1e;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QComboBox {
                width: 100px;
            }
        """)
        
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
    
    def toggle_filter(self, state):
        enabled = state == Qt.CheckState.Checked.value
        self.filter_combo.setEnabled(enabled)
        if enabled and self.filter_combo.currentText() == "custom":
            self.custom_domain.setEnabled(True)
            self.custom_domain.setVisible(True)
        else:
            self.custom_domain.setEnabled(False)
            self.custom_domain.setVisible(False)
    
    def toggle_remove(self, state):
        enabled = state == Qt.CheckState.Checked.value
        self.remove_combo.setEnabled(enabled)
        if enabled and self.remove_combo.currentText() == "custom":
            self.remove_custom_domain.setEnabled(True)
            self.remove_custom_domain.setVisible(True)
        else:
            self.remove_custom_domain.setEnabled(False)
            self.remove_custom_domain.setVisible(False)
    
    def handle_combo_change(self, text):
        if text == "custom":
            self.custom_domain.setEnabled(True)
            self.custom_domain.setVisible(True)
            self.custom_domain.setFocus()
        else:
            self.custom_domain.setEnabled(False)
            self.custom_domain.setVisible(False)
    
    def handle_remove_combo_change(self, text):
        if text == "custom":
            self.remove_custom_domain.setEnabled(True)
            self.remove_custom_domain.setVisible(True)
            self.remove_custom_domain.setFocus()
        else:
            self.remove_custom_domain.setEnabled(False)
            self.remove_custom_domain.setVisible(False)
    
    def get_domain_filter(self):
        if not self.filter_check.isChecked():
            return None
        
        if self.filter_combo.currentText() == "custom":
            domain = self.custom_domain.text().strip()
            if not domain:
                return None
            return domain
        
        return self.filter_combo.currentText()
    
    def get_domain_to_remove(self):
        if not self.remove_check.isChecked():
            return None
        
        if self.remove_combo.currentText() == "custom":
            domain = self.remove_custom_domain.text().strip()
            if not domain:
                return None
            return domain
        
        return self.remove_combo.currentText()
    
    def process_and_save(self):
        input_data = self.input_text.toPlainText().strip()
        if not input_data:
            QMessageBox.warning(self, "Warning", "Please enter some email:password pairs first!")
            return
        
        domain_filter = self.get_domain_filter()
        domain_to_remove = self.get_domain_to_remove()
        
        if domain_filter and domain_to_remove:
            QMessageBox.warning(self, "Warning", "You can't use both filter and remove domain at the same time!")
            return
        
        # First remove duplicates
        unique_lines = []
        seen = set()
        for line in input_data.split('\n'):
            if line.strip():  # Skip empty lines
                if line not in seen:
                    seen.add(line)
                    unique_lines.append(line.strip())
        
        # Process each line
        formatted_lines = []
        skipped_count = 0
        removed_count = 0
        duplicate_count = len(input_data.split('\n')) - len(unique_lines)
        
        for line in unique_lines:
            if ':' in line:
                email, password = line.split(':', 1)
                email = email.strip()
                password = password.strip()
                
                # Apply domain filter if enabled
                if domain_filter:
                    if not re.fullmatch(rf'.*@{re.escape(domain_filter)}$', email, re.IGNORECASE):
                        skipped_count += 1
                        continue
                
                # Apply domain removal if enabled
                if domain_to_remove:
                    if re.fullmatch(rf'.*@{re.escape(domain_to_remove)}$', email, re.IGNORECASE):
                        removed_count += 1
                        continue
                
                formatted_lines.append(email)
                formatted_lines.append(password)
                formatted_lines.append("")  # Empty line between entries
        
        # Show status messages
        status_messages = []
        if duplicate_count > 0:
            status_messages.append(f"Removed {duplicate_count} duplicates")
        if domain_filter and skipped_count > 0:
            status_messages.append(f"Filtered out {skipped_count} non-{domain_filter} entries")
        elif domain_to_remove and removed_count > 0:
            status_messages.append(f"Removed {removed_count} {domain_to_remove} entries")
        
        if status_messages:
            self.statusBar().showMessage(" | ".join(status_messages), 5000)
        
        if not formatted_lines:
            QMessageBox.warning(self, "Warning", "No valid email:password pairs found after filtering!")
            return
        
        # Save to file
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Output File",
            "output.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                # Use UTF-8 encoding to handle all characters
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(formatted_lines))
                self.statusBar().showMessage(f"Successfully saved to {file_path}", 5000)
                QMessageBox.information(self, "Success", "File saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
        
    def clear_input(self):
        self.input_text.clear()
        self.statusBar().showMessage("Cleared", 3000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    font = QFont()
    font.setFamily("Segoe UI" if sys.platform == "win32" else "Arial")
    font.setPointSize(10)
    app.setFont(font)

    window = EmailPasswordSplitter()
    window.show()
    
    sys.exit(app.exec())
