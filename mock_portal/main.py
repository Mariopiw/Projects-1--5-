from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()
ORDERS = {
    "ORD-1001": {"status": "READY", "quantity": 10},
    "ORD-1002": {"status": "HOLD", "quantity": 7},
    "ORD-1003": {"status": "READY", "quantity": -2},
}

LOGIN = """<html><body><form method='post' action='/login'><input id='username' name='username'><input id='password' name='password' type='password'><button type='submit'>Login</button></form></body></html>"""
DASHBOARD = """<html><body><form method='get' action='/search'><input id='order-search' name='order_id'><button id='search-button' type='submit'>Search</button></form></body></html>"""

@app.get("/", response_class=HTMLResponse)
def root():
    return LOGIN

@app.post("/login", response_class=HTMLResponse)
def login(username: str = Form(...), password: str = Form(...)):
    if username != "demo" or password != "demo-password":
        raise HTTPException(401, "Invalid credentials")
    return DASHBOARD

@app.get("/search", response_class=HTMLResponse)
def search(order_id: str):
    order = ORDERS.get(order_id)
    if order is None:
        raise HTTPException(404, "Order not found")
    return f"<html><body><div id='order-status'>{order['status']}</div><div id='order-quantity'>{order['quantity']}</div></body></html>"
