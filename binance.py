import websocket
import json

# WebSocket URL for Binance's BTC/USDT trade data
ws_url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# Variables to store buy and sell quantities
total_buy_qty = 0
total_sell_qty = 0

# Function to process the incoming WebSocket data
def on_message(ws, message):
    global total_buy_qty, total_sell_qty
    
    data = json.loads(message)  # Parse the received message (JSON format)

    # Extract price, quantity, and timestamp
    price = float(data['p'])  # Price of the trade
    quantity = float(data['q'])  # Quantity of the trade
    timestamp = data['T']  # Timestamp of the trade
    
    # Determine if it's a buy or sell trade
    is_sell = data['m']  # If 'true', it's a sell, if 'false', it's a buy

    # If it's a buy trade, add quantity to total_buy_qty
    if not is_sell:
        total_buy_qty += quantity
    else:
        total_sell_qty += quantity

    # Calculate the delta (difference between buy and sell quantities)
    delta = total_buy_qty - total_sell_qty

    # Print out the details
    print(f"Timestamp: {timestamp}, Price: {price}, Buy Quantity: {total_buy_qty}, Sell Quantity: {total_sell_qty}, Delta: {delta}")

    # Optional: You can store this data in a file, for example:
    with open("binance_trade_data.json", "a") as f:
        trade_data = {
            "timestamp": timestamp,
            "price": price,
            "buy_qty": total_buy_qty,
            "sell_qty": total_sell_qty,
            "delta": delta
        }
        json.dump(trade_data, f)
        f.write("\n")  # Newline for each entry

# Function to handle WebSocket connection opening
def on_open(ws):
    print("Connection established.")

# Function to handle WebSocket connection closing
def on_close(ws):
    print("Connection closed.")

# Create the WebSocket connection
ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_open=on_open, on_close=on_close)

# Run the WebSocket connection indefinitely
ws.run_forever()
