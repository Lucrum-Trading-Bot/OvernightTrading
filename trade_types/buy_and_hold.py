def calculate_buy_and_hold_returns(data):
    returns = data["Close"].pct_change()

    returns.iloc[0] = data["Close"].iloc[0] / data["Open"].iloc[0] - 1
    returns.name = "buy_and_hold_return"

    return returns
