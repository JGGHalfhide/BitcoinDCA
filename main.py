import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import yfinance as yf

# Function to validate that selected date is not in the future
def validate_date(date):
    today = datetime.today().date()
    selected_date = datetime.strptime(date, "%m/%d/%y").date()
    return selected_date <= today

# Function to handle date validation
def on_date_change(event):
    selected_date = event.widget.get()
    if not validate_date(selected_date):
        error_label.config(text="Error: Date cannot be in the future!", fg="red")
    else:
        error_label.config(text="")

# Function to fetch historical Bitcoin prices from Yahoo Finance
def get_btc_price(date):
    btc = yf.Ticker("BTC-USD")
    hist = btc.history(start=date.strftime('%Y-%m-%d'), end=(date + timedelta(days=1)).strftime('%Y-%m-%d'))
    if not hist.empty and 'Close' in hist.columns:
        return hist['Close'].iloc[0]
    return None

# Function to initialize the DCA Sell Calculator
def dca_sell_calculator():
    for widget in root.winfo_children():
        widget.destroy()

    global start_date_entry, end_date_entry, btc_amount_entry, withdrawal_amount_entry, withdrawal_frequency, error_label, tree

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Start Date:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    start_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    start_date_entry.grid(row=0, column=1, padx=10, pady=10)
    start_date_entry.bind("<<DateEntrySelected>>", on_date_change)

    tk.Label(frame, text="End Date:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    end_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    end_date_entry.grid(row=1, column=1, padx=10, pady=10)
    end_date_entry.bind("<<DateEntrySelected>>", on_date_change)

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

    calculate_button = tk.Button(frame, text="Calculate Withdrawals", command=lambda: print("Withdrawal Calculation Not Implemented"))
    calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

    clear_button = tk.Button(frame, text="Clear", command=home_screen)
    clear_button.grid(row=6, column=0, columnspan=2, pady=10)

    error_label = tk.Label(frame, text="", fg="red")
    error_label.grid(row=7, column=0, columnspan=2, pady=10)

    tree = ttk.Treeview(root, columns=("Date", "BTC Remaining", "Total USD Withdrawn"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("BTC Remaining", text="BTC Remaining")
    tree.heading("Total USD Withdrawn", text="Total USD Withdrawn")
    tree.pack(fill="both", expand=True, pady=10)

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

    calculate_button = tk.Button(frame, text="Calculate Purchases", command=lambda: print("Purchase Calculation Not Implemented"))
    calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

    clear_button = tk.Button(frame, text="Clear", command=home_screen)
    clear_button.grid(row=5, column=0, columnspan=2, pady=10)

    tree = ttk.Treeview(root, columns=("Date", "BTC Purchased", "USD Invested", "BTC Value in USD"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("BTC Purchased", text="BTC Purchased")
    tree.heading("USD Invested", text="USD Invested")
    tree.heading("BTC Value in USD", text="BTC Value in USD")
    tree.pack(fill="both", expand=True, pady=10)

# Function to return to the home screen
def home_screen():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, pady=50)

    tk.Label(frame, text="Bitcoin DCA Calculator", font=("Arial", 16)).pack(pady=20)

    dca_buy_button = tk.Button(frame, text="DCA Buy Calculator", command=dca_buy_calculator)
    dca_buy_button.pack(pady=10)

    dca_sell_button = tk.Button(frame, text="DCA Sell Calculator", command=dca_sell_calculator)
    dca_sell_button.pack(pady=10)

# Initialize the main application window
root = tk.Tk()
root.title("Bitcoin DCA Calculator")
root.geometry("700x600")
root.configure(padx=20, pady=20)

home_screen()
root.mainloop()
