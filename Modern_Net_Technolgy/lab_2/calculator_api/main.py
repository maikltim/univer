from fastapi import FastAPI, Response
from pydantic import BaseModel
import ast
import operator

app = FastAPI()

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}

def safe_eval(expr):
    try:
        node = ast.parse(expr, mode='eval').body
        return _eval_node(node)
    except Exception:
        raise ValueError("Недопустимое выражение")

def _eval_node(node):
    if isinstance(node, ast.Num): 
        return node.n
    elif isinstance(node, ast.Constant): 
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Только числа")
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](left, right)
        else:
            raise ValueError("Оператор не разрешен")
    else:
        raise ValueError("Неподдерживаемая операция")

class CalcRequest(BaseModel):
    expression: str

class CalcResponse(BaseModel):
    result: float | int | None
    error: str | None = None

@app.post("/calculate", response_model=CalcResponse)
async def calculate(request: CalcRequest, response: Response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    result = None
    error = None

    try:
        res_val = safe_eval(request.expression)
        
        if isinstance(res_val, float) and res_val.is_integer():
            result = int(res_val)
        else:
            result = res_val
    except Exception as e:
        error = str(e)

    return CalcResponse(result=result, error=error)

@app.get("/")
async def root():
    return {"message": "SOA Calculator Service is running"}
