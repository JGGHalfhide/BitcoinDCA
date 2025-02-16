from flask import Flask, render_template, request
from datetime import datetime, timedelta
import yfinance as yf
import sqlite3

app = Flask(__name__)


# connect and initialize sqlite3 db for visitor counter
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS visitor_counter (
id INTEGER PRIMARY KEY,
count INTEGER NOT NULL)''')
    conn.execute('INSERT OR IGNORE INTO visitor_counter (id, count) VALUES (1, 0)')
    conn.commit()
    conn.close()


def increment_visitor_count():
    conn = get_db_connection()
    conn.execute('UPDATE visitor_counter SET count = count + 1 WHERE id = 1')
    conn.commit()
    count = conn.execute('SELECT count FROM visitor_counter WHERE id = 1').fetchone()['count']
    conn.close()
    return count


# Function to fetch historical Bitcoin prices
def get_btc_price(date):
    btc = yf.Ticker("BTC-USD")
    hist = btc.history(start=date.strftime('%Y-%m-%d'), end=(date + timedelta(days=1)).strftime('%Y-%m-%d'))
    return hist['Close'].iloc[0] if not hist.empty and 'Close' in hist.columns else None


# DCA Buy Calculator Route
@app.route('/dca-buy', methods=['GET', 'POST'])
def dca_buy():
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        purchase_amount = float(request.form['purchase_amount'])
        frequency = request.form['purchase_frequency']

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
                purchases.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "btc_purchased": round(total_btc_purchased, 6),
                    "usd_invested": round(total_usd_invested, 2),
                    "btc_value": round(total_btc_purchased * btc_price, 2)
                })
            date += timedelta(days=interval)

        return render_template("dca_buy.html", purchases=purchases)

    return render_template("dca_buy.html", purchases=None)


# DCA Sell Calculator Route
@app.route('/dca-sell', methods=['GET', 'POST'])
def dca_sell():
    sell_transactions = []

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        btc_amount = float(request.form['btc_amount'])  # Starting BTC balance
        withdrawal_amount = float(request.form['withdrawal_amount'])  # USD to withdraw per sale
        withdrawal_frequency = request.form['withdrawal_frequency']

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        current_date = start_date
        btc_remaining = btc_amount
        total_usd_withdrawn = 0  # Cumulative USD withdrawn
        total_btc_sold = 0  # Cumulative BTC sold

        while current_date <= end_date and btc_remaining > 0:
            btc_price = 50000  # Placeholder BTC price

            # Determine BTC sold based on available balance
            btc_sold = min(withdrawal_amount / btc_price, btc_remaining)
            usd_received = btc_sold * btc_price

            # Update running totals
            btc_remaining -= btc_sold
            total_btc_sold += btc_sold
            total_usd_withdrawn += usd_received

            print(
                f"Date: {current_date.strftime('%Y-%m-%d')}, BTC Sold: {btc_sold}, Total USD Withdrawn: {usd_received}, BTC Remaining: {btc_remaining}, Total USD Withdrawn: {total_usd_withdrawn}")

            sell_transactions.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "btc_sold": round(total_btc_sold, 6),  # Running total
                "usd_received": round(total_usd_withdrawn, 2),  # Running total
                "btc_remaining": round(btc_remaining, 8)  # Running total
            })

            # Stop if all BTC has been sold
            if btc_remaining <= 0:
                break

            # Move to the next withdrawal date
            if withdrawal_frequency == "Daily":
                current_date += timedelta(days=1)
            elif withdrawal_frequency == "Weekly":
                current_date += timedelta(weeks=1)
            elif withdrawal_frequency == "Biweekly":
                current_date += timedelta(weeks=2)
            elif withdrawal_frequency == "Monthly":
                current_date += timedelta(weeks=4)

    return render_template("dca_sell.html", sell_transactions=sell_transactions)


# Home Page Route
@app.route('/')
def home():
    count = increment_visitor_count()

    return render_template("home.html", visitor_count=count)


if __name__ == '__main__':
    initialize_db()  # Ensure database is set up before the app starts
    app.run(debug=True)
