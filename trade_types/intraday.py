def calculate_intraday_returns(data, transaction_cost=0):
    returns = data["Close"] / data["Open"] - 1
    returns = returns - transaction_cost

    returns.name = "intraday_return"

    return returns
