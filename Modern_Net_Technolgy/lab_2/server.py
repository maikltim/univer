import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc
import ast
import uuid
import time

VALID_USERS = {
    "admin": "12345",
    "user": "password"
}

active_sessions = {}

def safe_eval(expr):
    """Безопасное вычисление через AST"""
    try:
        node = ast.parse(expr, mode='eval')
        for node in ast.walk(node):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp, 
                                     ast.Num, ast.Constant, ast.operator, ast.unaryop)):
                raise ValueError("Запрещенные операции")
        return eval(compile(node, filename="", mode="eval"))
    except Exception as e:
        return None

class CalculatorServicer(calculator_pb2_grpc.CalculatorServiceServicer):
    
    def Login(self, request, context):
        username = request.username
        password = request.password
        
        if username in VALID_USERS and VALID_USERS[username] == password:
            session_id = str(uuid.uuid4())
            active_sessions[session_id] = time.time() + 600 
            
            return calculator_pb2.LoginResponse(
                session_id=session_id,
                success=True,
                message="Авторизация успешна"
            )
        else:
            return calculator_pb2.LoginResponse(
                session_id="",
                success=False,
                message="Неверный логин или пароль"
            )

    def Calculate(self, request, context):
        session_id = request.session_id
        expression = request.expression
        
        if session_id not in active_sessions:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Сессия истекла или не найдена. Пожалуйста, войдите снова.")
            return calculator_pb2.CalculateResponse(result=0.0, error="Сессия невалидна")
        
    
        if time.time() > active_sessions[session_id]:
            del active_sessions[session_id]
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Время сессии истекло.")
            return calculator_pb2.CalculateResponse(result=0.0, error="Сессия истекла")
        
    
        result = safe_eval(expression)
        
        if result is None:
            return calculator_pb2.CalculateResponse(result=0.0, error="Ошибка вычисления выражения")
            
        return calculator_pb2.CalculateResponse(result=result, error="")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServiceServicer_to_server(CalculatorServicer(), server)
    
    server.add_inet_address('[::]', 50051)
    print("gRPC сервер запущен на порту 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
