import tkinter as tk
from tkinter import ttk, messagebox

from visualization import show_results


def run_gui(run_analysis):
    root = tk.Tk()
    root.title("Overnight Trading")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=20)
    frame.grid()

    ttk.Label(
        frame,
        text="Overnight Trading Comparison",
        font=("Segoe UI", 14, "bold"),
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        pady=(0, 15),
    )

    ttk.Label(frame, text="Ticker").grid(row=1, column=0, sticky="w", pady=5)
    ttk.Label(frame, text="Start date").grid(row=2, column=0, sticky="w", pady=5)
    ttk.Label(frame, text="End date").grid(row=3, column=0, sticky="w", pady=5)
    ttk.Label(frame, text="Initial capital").grid(row=4, column=0, sticky="w", pady=5)
    ttk.Label(frame, text="Transaction cost (%)").grid(
        row=5,
        column=0,
        sticky="w",
        pady=5,
    )

    ticker_entry = ttk.Entry(frame, width=22)
    start_entry = ttk.Entry(frame, width=22)
    end_entry = ttk.Entry(frame, width=22)
    capital_entry = ttk.Entry(frame, width=22)
    cost_entry = ttk.Entry(frame, width=22)

    ticker_entry.grid(row=1, column=1, padx=(15, 0), pady=5)
    start_entry.grid(row=2, column=1, padx=(15, 0), pady=5)
    end_entry.grid(row=3, column=1, padx=(15, 0), pady=5)
    capital_entry.grid(row=4, column=1, padx=(15, 0), pady=5)
    cost_entry.grid(row=5, column=1, padx=(15, 0), pady=5)

    ticker_entry.insert(0, "AAPL")
    start_entry.insert(0, "2024-01-01")
    end_entry.insert(0, "2025-01-01")
    capital_entry.insert(0, "1000")
    cost_entry.insert(0, "0")

    status_label = ttk.Label(frame, text="Ready")
    status_label.grid(row=7, column=0, columnspan=2, pady=(10, 0))

    def calculate():
        run_button.config(state="disabled")
        status_label.config(text="Running...")
        root.update_idletasks()

        try:
            ticker = ticker_entry.get().strip().upper()
            initial_capital = float(capital_entry.get())
            transaction_cost = float(cost_entry.get()) / 100

            if not ticker:
                raise ValueError("Enter a ticker.")

            if initial_capital <= 0:
                raise ValueError("Initial capital must be greater than zero.")

            if transaction_cost < 0:
                raise ValueError("Transaction cost cannot be negative.")

            parameters = {
                "ticker": ticker,
                "start_date": start_entry.get().strip(),
                "end_date": end_entry.get().strip(),
                "initial_capital": initial_capital,
                "transaction_cost": transaction_cost,
            }

            results = run_analysis(parameters)

            status_label.config(text="Done")
            show_results(results)

        except Exception as error:
            status_label.config(text="Error")
            messagebox.showerror(
                "Could not run comparison",
                str(error),
            )

        finally:
            run_button.config(state="normal")

    run_button = ttk.Button(
        frame,
        text="Run comparison",
        command=calculate,
    )

    run_button.grid(
        row=6,
        column=0,
        columnspan=2,
        pady=(15, 0),
    )

    root.mainloop()
