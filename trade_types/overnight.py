def calculate_overnight_returns(data, transaction_cost=0):
    returns = data["Open"] / data["Close"].shift(1) - 1
    returns = returns.dropna() - transaction_cost

    returns.name = "overnight_return"

    return returns
