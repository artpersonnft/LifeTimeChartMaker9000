# LifeTimeChartMaker9000
THIS BAD BOY MAKES CHARTS. LOTS OF CHARTS. THE LOTSEST OF CHARTS EVEN.

sorry for AI, but i asked AI to explain this shit. i dont wanna. it needs python, a few modules, and heres the guide:


How to Use the Stock Charting Script (ChartMaker.py)
This guide explains how to use stocks2.py, a Python script that downloads historical stock data and generates charts to visualize price trends or percentage increases. Follow these steps to set up, run, and interpret the results.
Step 1: Set Up Your Environment
Install Python 3.12:
Download and install Python 3.12 from python.org.

Verify the installation by running python --version in your terminal. It should show Python 3.12.x.

Install Required Libraries:
Open a terminal and install the necessary Python libraries using pip:

pip install yfinance pandas matplotlib plotly numpy

These libraries handle data downloading (yfinance), data processing (pandas, numpy), and charting (matplotlib, plotly).

Save the Script:
Copy the stocks2.py script into a file in an accessible directory (e.g., C:\Users\YourName\stocks2.py).

Step 2: Run the Script
Launch the Script:
Open a terminal, navigate to the script’s directory, and run:

python stocks2.py

Input Tickers:
The script prompts:

Input Tickers (comma-separated, 1-5 letters each, no suffix, or press Enter for default):

Enter tickers separated by commas (e.g., JNJ,KO,XOM). Each ticker must be 1–5 letters, with no suffixes (e.g., JNJ.TO is invalid).

Press Enter to use the default list of 28 tickers (e.g., AA, AEP, BA, etc.).

If you provide input, the script confirms with:

Using tickers: ['JNJ', 'KO', 'XOM']
or
Invalid input (e.g., JNJ.TO or TICKER) will prompt an error and ask you to try again.

Step 3: Download Stock Data
The script downloads historical stock data for each ticker from Yahoo Finance, from January 1, 1900, to the current date (April 6, 2025).

It calculates the percentage increase relative to the initial price.

You’ll see messages like:

Downloading data for JNJ...
Data for JNJ starts from 1962-01-02

Data downloading is parallelized across CPU cores for speed. If a ticker fails (e.g., invalid ticker), an error message appears, and the script continues.

Step 4: Select a Charting Option
The script prompts you to choose a charting option:

Choose a charting option:
1: Group by 5-year buckets from the earliest date
2: Group by majority start dates (10+ tickers per date)
3: Chart all tickers in one chart
4: Chart tickers in partitions of 100 (with price or percentage option)
Enter 1, 2, 3, or 4:

Option 1: Groups tickers by 5-year start date buckets (e.g., 1960–1965). Saves percentage increase charts as PNG files (e.g., chart_0_to_5_years.png).

Option 2: Groups tickers by start dates shared by 10+ tickers. Saves percentage increase charts as PNG files (e.g., chart_start_1962-01-02.png).

Option 3: Plots all tickers in one chart (percentage increase as a PNG, raw prices in an interactive Plotly chart in your browser).

Option 4: Splits tickers into batches of 100, with interactive Plotly charts. Choose P for raw prices or % for percentage increases.

Step 5: View and Interpret the Charts
Static Charts (Options 1, 2, 3): Saved as PNG files in the script’s directory, showing percentage increases over time.

