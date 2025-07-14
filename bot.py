import MetaTrader5 as mt5
import pandas as pd
import time, os, datetime
from dotenv import load_dotenv
from telegram_alerts import send_alert

load_dotenv()

login = int(os.getenv("MT5_LOGIN"))
password = os.getenv("MT5_PASSWORD")
server = os.getenv("MT5_SERVER")
symbols = os.getenv("SYMBOLS").split(",")
max_trades = int(os.getenv("MAX_TRADES_PER_SYMBOL"))
risk = float(os.getenv("RISK_PER_TRADE_PERCENT"))

def connect_mt5():
    if not mt5.initialize():
        mt5.login(login, password=password, server=server)
    print("MT5 Connected:", mt5.last_error())

def get_data(symbol, timeframe, bars):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    return pd.DataFrame(rates)

def check_strategy(df):
    return df['close'].iloc[-1] > df['open'].iloc[-1]

def get_open_trades(symbol):
    trades = mt5.positions_get(symbol=symbol)
    return len(trades) if trades else 0

def trade(symbol):
    price = mt5.symbol_info_tick(symbol).ask
    sl = price - 5
    tp = price + 15
    volume = 0.01
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 100020,
        "comment": "MARVEL-TRADER",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result.retcode == 10009:
        send_alert(f"✅ Trade placed on {symbol} @ {price}")
    else:
        send_alert(f"❌ Trade failed on {symbol}: {result.retcode}")

def run_bot():
    connect_mt5()
    now = datetime.datetime.now()
    if now.weekday() == 5 and now.hour >= 23: return
    if now.weekday() == 6 and now.hour < 2: return

    for symbol in symbols:
        for tf in [mt5.TIMEFRAME_M3, mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_H1, mt5.TIMEFRAME_H4]:
            df = get_data(symbol, tf, 100)
            if check_strategy(df):
                if get_open_trades(symbol) < max_trades:
                    trade(symbol)
                    break

if __name__ == "__main__":
    while True:
        run_bot()
        time.sleep(60)
