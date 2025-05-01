import requests
import time
import json
import websocket
from datetime import datetime, timedelta

symbol = "BTCUSDT"
limit = 1000

# ---------- Step 1: Fetch historical aggTrades for last 24 hours ----------
def fetch_historical_trades():
    print("🕰️ Fetching historical data for last 24 hours...")
    end_time = int(time.time() * 1000)
    start_time = end_time - (24 * 60 * 60 * 1000)  # 24 hours in milliseconds

    all_trades = []
    from_id = None

    while True:
        params = {
            "symbol": symbol,
            "limit": limit,
            "startTime": start_time,
            "endTime": end_time
        }
        if from_id:
            params["fromId"] = from_id

        response = requests.get("https://api.binance.com/api/v3/aggTrades", params=params)
        data = response.json()

        if not data:  # Check if the list is empty
            print("No more data available.")
            break

        all_trades.extend(data)
        from_id = data[-1]["a"] + 1  # Access the last trade ID safely
        if len(data) < limit:  # If fewer trades are returned, stop the loop
            break

    return all_trades

# ---------- Helper to calculate buy/sell quantities ----------
def classify_trade(trade):
    price = float(trade["p"])
    qty = float(trade["q"])
    ts = int(trade["T"])
    maker = trade["m"]  # if True → SELL; if False → BUY

    buy_qty = qty if not maker else 0
    sell_qty = qty if maker else 0
    delta = buy_qty - sell_qty

    print(f"Timestamp: {ts}, Price: {price}, Buy Quantity: {buy_qty}, Sell Quantity: {sell_qty}, Delta: {delta}")

# ---------- Step 2: WebSocket Live Feed ----------
def on_message(ws, message):
    trade = json.loads(message)
    price = float(trade["p"])
    qty = float(trade["q"])
    ts = int(trade["T"])
    maker = trade["m"]

    buy_qty = qty if not maker else 0
    sell_qty = qty if maker else 0
    delta = buy_qty - sell_qty

    print(f"Timestamp: {ts}, Price: {price}, Buy Quantity: {buy_qty}, Sell Quantity: {sell_qty}, Delta: {delta}")

def on_open(ws):
    print("🚀 Live WebSocket connection started")

def on_close(ws):
    print("❌ WebSocket closed")

# ---------- Main ----------
if __name__ == "__main__":
    # Historical data
    trades = fetch_historical_trades()
    for t in trades:
        classify_trade(t)

    # Real-time data
    ws_url = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@trade"
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_open=on_open, on_close=on_close)
    ws.run_forever()
