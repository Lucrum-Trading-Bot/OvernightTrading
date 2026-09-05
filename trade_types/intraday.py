def calculate_intraday_returns(data, transaction_cost=0):
    returns = (
        data["Close"]
        / data["Open"]
        * (1 - transaction_cost)
        / (1 + transaction_cost)
        - 1
    )

    returns.name = "intraday_return"

    return returns
