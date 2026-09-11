from data.yfinance_data import get_earnings_dates, get_market_data
from gui import run_gui
from trade_types.buy_and_hold import calculate_buy_and_hold_returns
from trade_types.intraday import calculate_intraday_returns
from trade_types.overnight import calculate_overnight_returns


def summarize(returns, initial_capital):
    returns = returns.dropna()

    total_return = (1 + returns).prod() - 1
    final_value = initial_capital * (1 + total_return)

    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax().clip(lower=1)
    drawdown = cumulative / peak - 1

    return {
        "total_return": total_return,
        "final_value": final_value,
        "average_return": returns.mean(),
        "median_return": returns.median(),
        "best_return": returns.max(),
        "worst_return": returns.min(),
        "wins": (returns > 0).sum(),
        "losses": (returns < 0).sum(),
        "win_rate": (returns > 0).mean(),
        "observations": len(returns),
        "max_drawdown": drawdown.min(),
    }


def run_analysis(parameters):
    data = get_market_data(
        parameters["ticker"],
        parameters["start_date"],
        parameters["end_date"],
    )

    earnings_dates = get_earnings_dates(
        parameters["ticker"],
        parameters["start_date"],
        parameters["end_date"],
    )

    transaction_cost = parameters["transaction_cost"]

    overnight_returns = calculate_overnight_returns(
        data,
        transaction_cost,
    )
    intraday_returns = calculate_intraday_returns(
        data,
        transaction_cost,
    )
    buy_and_hold_returns = calculate_buy_and_hold_returns(
        data,
        transaction_cost,
    )

    initial_capital = parameters["initial_capital"]

    return {
        "ticker": parameters["ticker"],
        "start_date": data.index[0],
        "end_date": data.index[-1],
        "initial_capital": initial_capital,
        "transaction_cost": transaction_cost,
        "earnings_dates": earnings_dates,
        "overnight_returns": overnight_returns,
        "intraday_returns": intraday_returns,
        "buy_and_hold_returns": buy_and_hold_returns,
        "overnight": summarize(
            overnight_returns,
            initial_capital,
        ),
        "intraday": summarize(
            intraday_returns,
            initial_capital,
        ),
        "buy_and_hold": summarize(
            buy_and_hold_returns,
            initial_capital,
        ),
    }


def main():
    run_gui(run_analysis)


if __name__ == "__main__":
    main()
