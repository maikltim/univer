import sys
import requests
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QLabel, QWidget, 
                            QGridLayout, QPushButton, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt

OPERATORS = ["+", ".", "=", "/", "*", "-"]
ORANGE_STYLE = "background-color: orange; color: white;"
GRAY_STYLE = "background-color: lightgray; color: black;"


SERVICES = [
    "Локальный (http://localhost:8000)",
    "Удалённый (вставьте URL после деплоя)"
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SOA Calculator (PyQt5)")
        self.label = QLabel("0")
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.label.setStyleSheet("font-size: 24px; padding: 10px;")

        main_layout = QGridLayout()
        main_layout.addWidget(self.label, 0, 0, 1, 4)

        
        service_label = QLabel("Сервис:")
        self.service_combo = QComboBox()
        self.service_combo.addItems(SERVICES)
        
        service_layout = QHBoxLayout()
        service_layout.addWidget(service_label)
        service_layout.addWidget(self.service_combo)
        
        main_layout = QGridLayout()
        main_layout.addWidget(self.label, 0, 0, 1, 4)
        main_layout.addLayout(service_layout, 1, 0, 1, 4) 

        
        row_offset = 2 

        
        self._setup_button("AC", main_layout, row_offset + 0, 0, 1, 3, GRAY_STYLE)
        self._setup_button("/", main_layout, row_offset + 0, 3, 1, 1, ORANGE_STYLE)

       
        self._setup_button("7", main_layout, row_offset + 1, 0, 1, 1, GRAY_STYLE)
        self._setup_button("8", main_layout, row_offset + 1, 1, 1, 1, GRAY_STYLE)
        self._setup_button("9", main_layout, row_offset + 1, 2, 1, 1, GRAY_STYLE)
        self._setup_button("*", main_layout, row_offset + 1, 3, 1, 1, ORANGE_STYLE)

        
        self._setup_button("4", main_layout, row_offset + 2, 0, 1, 1, GRAY_STYLE)
        self._setup_button("5", main_layout, row_offset + 2, 1, 1, 1, GRAY_STYLE)
        self._setup_button("6", main_layout, row_offset + 2, 2, 1, 1, GRAY_STYLE)
        self._setup_button("-", main_layout, row_offset + 2, 3, 1, 1, ORANGE_STYLE)

        
        self._setup_button("1", main_layout, row_offset + 3, 0, 1, 1, GRAY_STYLE)
        self._setup_button("2", main_layout, row_offset + 3, 1, 1, 1, GRAY_STYLE)
        self._setup_button("3", main_layout, row_offset + 3, 2, 1, 1, GRAY_STYLE)
        self._setup_button("+", main_layout, row_offset + 3, 3, 1, 1, ORANGE_STYLE)

    
        self._setup_button("0", main_layout, row_offset + 4, 0, 1, 2, GRAY_STYLE)
        self._setup_button(".", main_layout, row_offset + 4, 2, 1, 1, GRAY_STYLE)
        self._setup_button("=", main_layout, row_offset + 4, 3, 1, 1, ORANGE_STYLE)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def _setup_button(self, text, layout, row, col, row_span=1, col_span=1, style=None):
        button = QPushButton(text)
        if style:
            button.setStyleSheet(style)
        button.clicked.connect(lambda: self.button_pressed(button))
        layout.addWidget(button, row, col, row_span, col_span)
        return button

    def button_pressed(self, button):
        current_text = self.label.text()
        button_text = button.text()

        if button_text == "=":
            self.send_to_service(current_text)
            
        elif button_text == "AC":
            self.label.setText("0")
            
        elif current_text == "0" and button_text not in OPERATORS:
            self.label.setText(button_text)
            
        else:
            if button_text == "." and "." in current_text and not any(op in current_text for op in OPERATORS if op != "."):
                pass 
            else:
                self.label.setText(current_text + button_text)

    def send_to_service(self, expression):
        """Отправляет выражение на Web-сервис и получает результат"""
        selected_service = self.service_combo.currentText()
        
        if selected_service == "Локальный (http://localhost:8000)":
            url = "http://localhost:8000/calculate"
        else:
            url_input = QMessageBox.getText(self, "Ввод URL", "Введите URL удаленного сервиса:")
            if not url_input[1]: 
                return
            url = url_input[0].strip()
            if not url.startswith("http"):
                QMessageBox.critical(self, "Ошибка", "URL должен начинаться с http:// или https://")
                return

        try:
            payload = {"expression": expression}
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status() 
            
            data = response.json()
            
            if data.get("error"):
                self.label.setText(f"Err: {data['error']}")
            else:
                self.label.setText(str(data["result"]))
                
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Ошибка соединения", "Не удалось подключиться к сервису.\nПроверьте, запущен ли Web-сервис.")
        except requests.exceptions.Timeout:
            QMessageBox.critical(self, "Ошибка", "Время ожидания ответа истекло.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 400)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
