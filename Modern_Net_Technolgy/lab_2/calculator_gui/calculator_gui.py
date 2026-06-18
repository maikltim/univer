import sys
import grpc
import calculator_pb2
import calculator_pb2_grpc
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.session_id = None
        self.channel = None
        self.stub = None
        self.init_ui()
        self.connect_to_server()

    def connect_to_server(self):
        try:
            self.channel = grpc.insecure_channel('localhost:50051')
            self.stub = calculator_pb2_grpc.CalculatorServiceStub(self.channel)
            print("Подключено к gRPC серверу")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось подключиться к серверу:\n{e}")
            sys.exit(1)

    def init_ui(self):
        self.setWindowTitle('gRPC Калькулятор с Авторизацией')
        self.layout = QVBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите выражение (например, 2+2)")
        self.layout.addWidget(self.input_field)
        self.btn_login = QPushButton("Войти в систему")
        self.btn_login.clicked.connect(self.show_login_dialog)
        self.layout.addWidget(self.btn_login)
        self.status_label = QLabel("Статус: Не авторизован")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.layout.addWidget(self.status_label)
        self.btn_calc = QPushButton("Вычислить")
        self.btn_calc.clicked.connect(self.perform_calculation)
        self.btn_calc.setEnabled(False) 
        self.layout.addWidget(self.btn_calc)

        self.result_label = QLabel("Результат: ")
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def show_login_dialog(self):
        from PyQt5.QtWidgets import QInputDialog
        username, ok1 = QInputDialog.getText(self, 'Авторизация', 'Логин:')
        if not ok1 or not username: return
        
        password, ok2 = QInputDialog.getText(self, 'Авторизация', 'Пароль:', QLineEdit.Password)
        if not ok2 or not password: return

        try:
            response = self.stub.Login(calculator_pb2.LoginRequest(username=username, password=password))
            if response.success:
                self.session_id = response.session_id
                self.status_label.setText(f"Статус: Авторизован (Session ID: {self.session_id[:8]}...)")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                self.btn_login.setText("Сменить пользователя")
                self.btn_calc.setEnabled(True)
                QMessageBox.information(self, "Успех", response.message)
            else:
                QMessageBox.warning(self, "Ошибка входа", response.message)
        except grpc.RpcError as e:
            QMessageBox.critical(self, "Ошибка связи", str(e.details()))

    def perform_calculation(self):
        expression = self.input_field.text()
        if not expression:
            return

        if not self.session_id:
            QMessageBox.warning(self, "Внимание", "Сначала выполните вход!")
            return

        try:
            req = calculator_pb2.CalculateRequest(expression=expression, session_id=self.session_id)
            response = self.stub.Calculate(req)
            
            if response.error:
                QMessageBox.warning(self, "Ошибка вычисления", response.error)
                if "Сессия" in response.error:
                    self.logout() # Сброс сессии при ошибке авторизации
            else:
                self.result_label.setText(f"Результат: {response.result}")
                
        except grpc.RpcError as e:
            QMessageBox.critical(self, "Ошибка RPC", str(e.details()))
            self.logout()

    def logout(self):
        self.session_id = None
        self.status_label.setText("Статус: Не авторизован")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.btn_login.setText("Войти в систему")
        self.btn_calc.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())
