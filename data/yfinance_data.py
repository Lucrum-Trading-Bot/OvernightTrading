import pandas as pd
import yfinance as yf


def get_market_data(ticker, start_date, end_date):
    end_date = pd.Timestamp(end_date) + pd.Timedelta(days=1)

    try:
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            interval="1d",
            auto_adjust=True,
            progress=False,
            multi_level_index=False,
        )
    except Exception as error:
        raise RuntimeError(f"Could not load market data for {ticker}") from error

    if data.empty:
        raise RuntimeError(f"No market data found for {ticker}")

    data = data[[
        "Open",
        "Close",
    ]].dropna()

    if data.empty:
        raise RuntimeError(f"No usable market data found for {ticker}")

    data.index.name = "date"

    return data


def get_earnings_dates(ticker, start_date, end_date):
    try:
        earnings = yf.Ticker(ticker).get_earnings_dates(limit=100)
    except Exception:
        return pd.DatetimeIndex([])

    if earnings is None or earnings.empty:
        return pd.DatetimeIndex([])

    dates = pd.DatetimeIndex(earnings.index)

    if dates.tz is not None:
        dates = dates.tz_localize(None)

    dates = dates.normalize()

    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)

    dates = dates[
        (dates >= start_date)
        & (dates <= end_date)
    ]

    return dates.unique().sort_values()
