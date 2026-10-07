from fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("Order Management Server")

ORDERS_DB = {
    "ORD1001": {
        "Customer": "rahul Sharma",
        "Item": "wireless Earbuds",
        "Status": "Shipped",
        "Order_date": "2026-07-25",
        "Amount": 1899
    },
    "ORD1001": {
            "Customer": "Abhijit Singh",
            "Item": "Buds",
            "Status": "Delivered",
            "Order_date": "2026-08-12",
            "Amount": 1299
    },
}


@mcp.tool()
def get_order_status(order_id:str):
    order = ORDERS_DB.get(order_id.upper())
    if not order:
        return{"error": f"Order {order_id} not found..."}
    return order

@mcp.tool()
def check_refund_elegibilty(order_id:str):
    order = ORDERS_DB(order_id.upper())
    if not order:
        return {"error": f"Order {order_id} not found..."}

    order_date = datetime.strptime(order['order_date'], "%Y-%m-%d")
    days_passed = (datetime(2026,9,15) - order_date).days
    eligible = order['status'] == "DElivered" and days_passed <= 7
    return {
        "order_id ": order_id.upper(),
        "eligible": eligible,
        "days_since_order": days_passed,
        "reason": "Delivered with in 7 days" if eligible else "Not eliggible"
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001)