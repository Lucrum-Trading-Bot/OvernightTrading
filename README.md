# Overnight Trading

Compares three ways of holding the same asset over a selected period:

- **Overnight** — hold from one trading day's close to the next trading day's open.

- **Intraday** — hold from the open to the close of the same trading day.

- **Buy and hold** — hold continuously over the entire tested period.

## How to use

Install the requirements:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

Enter:

- **Ticker** — the asset's ticker, for example `AAPL`.

- **Start date** — first date of the analysis, in `YYYY-MM-DD` format.

- **End date** — last date of the analysis, in `YYYY-MM-DD` format.

- **Initial capital** — starting portfolio value.

- **Transaction cost (%)** — cost applied each time a position is opened or closed, entered as a percentage.

Click **Run comparison**.

## What it displays

The chart shows the portfolio value over time.

The vertical dashed lines mark **earnings dates**, which can help explain sudden changes in price behavior.

The small markers along the bottom compare overnight and intraday returns for each trading day:

- blue means Overnight performed better that day;

- orange means Intraday performed better that day.

The results table shows:

- total return;

- final value;

- best return;

- worst return;

- wins — trading days with a positive strategy return;

- losses — trading days with a negative strategy return;

- win rate — percentage of trading days with a positive strategy return;

- observations;

- max drawdown.

## Data

Market prices and earnings dates are fetched from Yahoo Finance through `yfinance`.

Market data is fetched at a **daily** interval and uses **adjusted prices**.
