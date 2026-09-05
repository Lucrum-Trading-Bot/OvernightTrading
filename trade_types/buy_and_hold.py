def calculate_buy_and_hold_returns(data, transaction_cost=0):
    returns = data["Close"].pct_change()

    returns.iloc[0] = (
        data["Close"].iloc[0]
        / data["Open"].iloc[0]
        / (1 + transaction_cost)
        - 1
    )

    returns.iloc[-1] = (
        (1 + returns.iloc[-1])
        * (1 - transaction_cost)
        - 1
    )

    returns.name = "buy_and_hold_return"

    return returns
