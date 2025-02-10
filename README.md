# Bitcoin DCA Calculator

## Overview
The Bitcoin DCA (Dollar-Cost Averaging) Calculator is a Python-based GUI application that helps users simulate and analyze Bitcoin purchases and withdrawals over a specified time period. The application provides two main functionalities:
- **DCA Buy Calculator**: Simulates periodic Bitcoin purchases over a date range.
- **DCA Sell Calculator**: Simulates periodic Bitcoin withdrawals over a date range.
- Note: the Yahoo Finance API limits requests to 2000 per hour. If the application is failing to generate data, this is the likely issue. 

## Features
- User-friendly GUI built with Tkinter.
- Date selection using `tkcalendar.DateEntry`.
- Fetches real Bitcoin historical prices using Yahoo Finance (`yfinance` module).
- Displays results in a tabular format using `ttk.Treeview`.
- Clear button to reset inputs and return to the home screen.

## Installation
### Prerequisites
Ensure you have Python installed (Python 3.x recommended). The following dependencies are required:
```sh
pip install tkinter tkcalendar yfinance
```

## Usage
Run the script with:
```sh
python script_name.py
```

### Home Screen
- **DCA Buy Calculator**: Opens a form to input a date range, purchase amount, and frequency.
- **DCA Sell Calculator**: Opens a form to input a date range, Bitcoin amount, withdrawal amount, and frequency.

### DCA Buy Calculator
1. Enter a start and end date.
2. Enter a fixed USD purchase amount.
3. Select a purchase frequency (Daily, Weekly, Biweekly, Monthly).
4. Click **"Calculate Purchases"** to display the simulated Bitcoin investments.

### DCA Sell Calculator
1. Enter a start and end date.
2. Enter an initial Bitcoin amount.
3. Enter a fixed withdrawal amount in USD.
4. Select a withdrawal frequency.
5. Click **"Calculate Withdrawals"** to display the simulated Bitcoin sales.

### Returning to Home Screen
Click the **"Clear"** button to reset and return to the main menu.

## Future Improvements
- Add data visualization (e.g., graphs for price trends).
- Improve error handling and input validation.

## License
This project is open-source under the MIT License.

## Author
Developed by JGGHalfhide.

