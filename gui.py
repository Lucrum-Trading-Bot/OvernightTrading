import tkinter as tk
from tkinter import messagebox, ttk
from visualization import show_results


class OvernightTradingGUI:
    def __init__(self, run_analysis):
        self.run_analysis = run_analysis

        self.root = tk.Tk()
        self.root.title("Overnight Trading")
        self.root.resizable(False, False)

        self.ticker = tk.StringVar(value="MU")
        self.start_date = tk.StringVar(value="2024-01-01")
        self.end_date = tk.StringVar(value="2025-01-01")
        self.initial_capital = tk.StringVar(value="1000")
        self.transaction_cost = tk.StringVar(value="0")
        self.status = tk.StringVar(value="Ready")

        self.run_button = None
        self.build_gui()

    def build_gui(self):
        frame = ttk.Frame(self.root, padding=20)
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

        fields = (
            ("Ticker", self.ticker),
            ("Start date", self.start_date),
            ("End date", self.end_date),
            ("Initial capital", self.initial_capital),
            ("Transaction cost (%)", self.transaction_cost),
        )

        for row, (label, variable) in enumerate(fields, start=1):
            ttk.Label(
                frame,
                text=label,
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=5,
            )
            ttk.Entry(
                frame,
                textvariable=variable,
                width=22,
            ).grid(
                row=row,
                column=1,
                padx=(15, 0),
                pady=5,
            )

        self.run_button = ttk.Button(
            frame,
            text="Run comparison",
            command=self.calculate,
        )
        self.run_button.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=(15, 0),
        )

        ttk.Label(
            frame,
            textvariable=self.status,
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            pady=(10, 0),
        )

    def parameters(self):
        ticker = self.ticker.get().strip().upper()

        if not ticker:
            raise ValueError("Enter a ticker.")

        try:
            initial_capital = float(self.initial_capital.get())
            transaction_cost = float(self.transaction_cost.get()) / 100
        except ValueError as error:
            raise ValueError(
                "Initial capital and transaction cost must be numbers."
            ) from error

        if initial_capital <= 0:
            raise ValueError("Initial capital must be greater than zero.")

        if transaction_cost < 0:
            raise ValueError("Transaction cost cannot be negative.")

        return {
            "ticker": ticker,
            "start_date": self.start_date.get().strip(),
            "end_date": self.end_date.get().strip(),
            "initial_capital": initial_capital,
            "transaction_cost": transaction_cost,
        }

    def calculate(self):
        self.run_button.config(state="disabled")
        self.status.set("Running...")
        self.root.update_idletasks()

        try:
            results = self.run_analysis(self.parameters())
            self.status.set("Done")
            show_results(results)
        except Exception as error:
            self.status.set("Error")
            messagebox.showerror(
                "Could not run comparison",
                str(error),
            )
        finally:
            self.run_button.config(state="normal")

    def run(self):
        self.root.mainloop()


def run_gui(run_analysis):
    OvernightTradingGUI(run_analysis).run()
