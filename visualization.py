import matplotlib.pyplot as plt


def show_results(results):
    plt.close("all")

    initial_capital = results["initial_capital"]

    overnight_values = (
        initial_capital
        * (1 + results["overnight_returns"]).cumprod()
    )
    intraday_values = (
        initial_capital
        * (1 + results["intraday_returns"]).cumprod()
    )
    buy_and_hold_values = (
        initial_capital
        * (1 + results["buy_and_hold_returns"]).cumprod()
    )

    figure, ax = plt.subplots(figsize=(10, 7))

    (overnight_line,) = ax.plot(overnight_values)
    (intraday_line,) = ax.plot(intraday_values)
    (buy_and_hold_line,) = ax.plot(buy_and_hold_values)

    overnight_returns, intraday_returns = results[
        "overnight_returns"
    ].align(
        results["intraday_returns"],
        join="inner",
    )

    overnight_better = overnight_returns > intraday_returns
    intraday_better = intraday_returns > overnight_returns

    y_min, y_max = ax.get_ylim()
    marker_y = y_min + (y_max - y_min) * 0.02

    ax.scatter(
        overnight_returns.index[overnight_better],
        [marker_y] * overnight_better.sum(),
        marker="|",
        s=60,
        color=overnight_line.get_color(),
    )
    ax.scatter(
        intraday_returns.index[intraday_better],
        [marker_y] * intraday_better.sum(),
        marker="|",
        s=60,
        color=intraday_line.get_color(),
    )

    for date in results["earnings_dates"]:
        ax.axvline(
            date,
            linestyle="--",
            linewidth=1,
            alpha=0.5,
            color="black",
        )

    ax.set_title(
        f"{results['ticker']} | "
        f"{results['start_date'].date()} to "
        f"{results['end_date'].date()}"
    )
    ax.set_ylabel("Portfolio value")
    ax.grid(alpha=0.3)

    overnight = results["overnight"]
    intraday = results["intraday"]
    buy_and_hold = results["buy_and_hold"]

    table_data = [
        [
            "Total return",
            f"{overnight['total_return']:.2%}",
            f"{intraday['total_return']:.2%}",
            f"{buy_and_hold['total_return']:.2%}",
        ],
        [
            "Final value",
            f"{overnight['final_value']:.2f}",
            f"{intraday['final_value']:.2f}",
            f"{buy_and_hold['final_value']:.2f}",
        ],
        [
            "Average return",
            f"{overnight['average_return']:.2%}",
            f"{intraday['average_return']:.2%}",
            "-",
        ],
        [
            "Median return",
            f"{overnight['median_return']:.2%}",
            f"{intraday['median_return']:.2%}",
            "-",
        ],
        [
            "Best return",
            f"{overnight['best_return']:.2%}",
            f"{intraday['best_return']:.2%}",
            "-",
        ],
        [
            "Worst return",
            f"{overnight['worst_return']:.2%}",
            f"{intraday['worst_return']:.2%}",
            "-",
        ],
        [
            "Wins",
            overnight["wins"],
            intraday["wins"],
            "-",
        ],
        [
            "Losses",
            overnight["losses"],
            intraday["losses"],
            "-",
        ],
        [
            "Win rate",
            f"{overnight['win_rate']:.2%}",
            f"{intraday['win_rate']:.2%}",
            "-",
        ],
        [
            "Observations",
            overnight["observations"],
            intraday["observations"],
            buy_and_hold["observations"],
        ],
        [
            "Max drawdown",
            f"{overnight['max_drawdown']:.2%}",
            f"{intraday['max_drawdown']:.2%}",
            f"{buy_and_hold['max_drawdown']:.2%}",
        ],
    ]

    table = ax.table(
        cellText=table_data,
        colLabels=[
            "Metric",
            "Overnight",
            "Intraday",
            "Buy and hold",
        ],
        cellLoc="center",
        bbox=[0, -0.78, 1, 0.62],
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)

    cells = table.get_celld()
    cells[(0, 0)].set_text_props(weight="bold")
    cells[(0, 1)].set_text_props(
        weight="bold",
        color=overnight_line.get_color(),
    )
    cells[(0, 2)].set_text_props(
        weight="bold",
        color=intraday_line.get_color(),
    )
    cells[(0, 3)].set_text_props(
        weight="bold",
        color=buy_and_hold_line.get_color(),
    )

    figure.subplots_adjust(bottom=0.45)
    plt.show(block=False)
