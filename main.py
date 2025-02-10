import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import yfinance as yf

# Function to fetch historical Bitcoin prices from Yahoo Finance
def get_btc_price(date):
    btc = yf.Ticker("BTC-USD")
    hist = btc.history(start=date.strftime('%Y-%m-%d'), end=(date + timedelta(days=1)).strftime('%Y-%m-%d'))
    if not hist.empty and 'Close' in hist.columns:
        return hist['Close'].iloc[0]
    return None

# Function to compute DCA Buy with cumulative totals
def calculate_dca_buy():
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    purchase_amount = float(purchase_amount_entry.get())
    frequency = purchase_frequency.get()

    date_intervals = {"Daily": 1, "Weekly": 7, "Biweekly": 14, "Monthly": 30}
    interval = date_intervals.get(frequency, 1)

    total_btc_purchased = 0
    total_usd_invested = 0
    purchases = []

    date = start_date
    while date <= end_date:
        btc_price = get_btc_price(date)
        if btc_price:
            btc_bought = purchase_amount / btc_price
            total_btc_purchased += btc_bought
            total_usd_invested += purchase_amount
            purchases.append((date.strftime("%Y-%m-%d"), total_btc_purchased, total_usd_invested, total_btc_purchased * btc_price))
        date += timedelta(days=interval)

    # Populate the treeview
    for row in tree.get_children():
        tree.delete(row)

    for purchase in purchases:
        tree.insert("", "end", values=purchase)

# Function to compute DCA Sell
def calculate_dca_sell():
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    btc_amount = float(btc_amount_entry.get())
    withdrawal_amount = float(withdrawal_amount_entry.get())
    frequency = withdrawal_frequency.get()

    date_intervals = {"Daily": 1, "Weekly": 7, "Biweekly": 14, "Monthly": 30}
    interval = date_intervals.get(frequency, 1)

    btc_remaining = btc_amount
    total_usd_withdrawn = 0
    withdrawals = []

    date = start_date
    while date <= end_date and btc_remaining > 0:
        btc_price = get_btc_price(date)
        if btc_price:
            btc_sold = withdrawal_amount / btc_price
            if btc_sold > btc_remaining:
                btc_sold = btc_remaining
            btc_remaining -= btc_sold
            total_usd_withdrawn += btc_sold * btc_price
            withdrawals.append((date.strftime("%Y-%m-%d"), btc_remaining, total_usd_withdrawn))
        date += timedelta(days=interval)

    # Populate the treeview
    for row in tree.get_children():
        tree.delete(row)

    for withdrawal in withdrawals:
        tree.insert("", "end", values=withdrawal)

# Function to initialize the DCA Buy Calculator
def dca_buy_calculator():
    for widget in root.winfo_children():
        widget.destroy()

    global start_date_entry, end_date_entry, purchase_amount_entry, purchase_frequency, tree

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Start Date:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    start_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    start_date_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame, text="End Date:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    end_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    end_date_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(frame, text="Purchase Amount ($):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    purchase_amount_entry = tk.Entry(frame)
    purchase_amount_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(frame, text="Purchase Frequency:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    purchase_frequency = ttk.Combobox(frame, values=["Daily", "Weekly", "Biweekly", "Monthly"])
    purchase_frequency.grid(row=3, column=1, padx=10, pady=10)
    purchase_frequency.current(0)

    tk.Button(frame, text="Calculate Purchases", command=calculate_dca_buy).grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(frame, text="Back", command=home_screen).grid(row=5, column=0, columnspan=2, pady=10)

    tree = ttk.Treeview(root, columns=("Date", "BTC Purchased", "USD Invested", "BTC Value in USD"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("BTC Purchased", text="BTC Purchased")
    tree.heading("USD Invested", text="USD Invested")
    tree.heading("BTC Value in USD", text="BTC Value in USD")
    tree.pack(fill="both", expand=True, pady=10)

# Function to initialize the DCA Sell Calculator
def dca_sell_calculator():
    for widget in root.winfo_children():
        widget.destroy()

    global start_date_entry, end_date_entry, btc_amount_entry, withdrawal_amount_entry, withdrawal_frequency, tree

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Start Date:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    start_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    start_date_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame, text="End Date:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    end_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    end_date_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(frame, text="Starting Bitcoin Amount:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    btc_amount_entry = tk.Entry(frame)
    btc_amount_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(frame, text="Withdrawal Amount ($):").grid(row=3, column=0, padx=10, pady=10, sticky="w")
    withdrawal_amount_entry = tk.Entry(frame)
    withdrawal_amount_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(frame, text="Withdrawal Frequency:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
    withdrawal_frequency = ttk.Combobox(frame, values=["Daily", "Weekly", "Biweekly", "Monthly"])
    withdrawal_frequency.grid(row=4, column=1, padx=10, pady=10)
    withdrawal_frequency.current(0)

    tk.Button(frame, text="Calculate Withdrawals", command=calculate_dca_sell).grid(row=5, column=0, columnspan=2, pady=10)
    tk.Button(frame, text="Back", command=home_screen).grid(row=6, column=0, columnspan=2, pady=10)  # Added Back button

    tree = ttk.Treeview(root, columns=("Date", "BTC Remaining", "Total USD Withdrawn"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("BTC Remaining", text="BTC Remaining")
    tree.heading("Total USD Withdrawn", text="Total USD Withdrawn")
    tree.pack(fill="both", expand=True, pady=10)

# Home Screen
def home_screen():
    for widget in root.winfo_children():
        widget.destroy()
    tk.Button(root, text="DCA Buy", command=dca_buy_calculator).pack(pady=10)
    tk.Button(root, text="DCA Sell", command=dca_sell_calculator).pack(pady=10)

# Initialize the GUI
root = tk.Tk()
root.title("Bitcoin DCA Calculator")
home_screen()
root.mainloop()