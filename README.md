LifeTimeChartMaker9000THIS BAD BOY MAKES CHARTS. LOTS OF CHARTS. THE LOTSEST OF CHARTS EVEN.LifeTimeChartMaker9000 is a powerful Python-based tool designed to download historical stock data from Yahoo Finance and generate a variety of visualizations for analyzing price trends and percentage increases over time. It supports grouping stocks by start dates, bucketing by years, and rendering both static PNG charts (using Matplotlib) and interactive HTML charts (using Plotly). The tool is optimized for efficiency, using parallel processing for data downloads, and handles a wide range of tickers (up to 28 defaults or custom inputs). It's ideal for financial analysts, investors, or anyone interested in long-term stock performance visualization.FeaturesHistorical Data Download: Fetches data from January 1, 1900 (or earliest available) to the current date using yfinance.
Percentage Calculations: Computes percentage increases relative to the initial price for each stock.
Multiple Charting Options:Group by 5-year buckets from the earliest start date.
Group by shared start dates (for 10+ tickers).
Single comprehensive chart for all tickers.
Partitioned charts in batches of 100 (with price or percentage views).

Output Formats: Static PNG images for quick views; interactive Plotly HTML files for detailed exploration.
Error Handling: Validates ticker inputs, skips invalid data, and continues processing.
Parallel Processing: Leverages CPU cores for faster downloads.

PrerequisitesPython 3.12 (tested; earlier versions may work but are not guaranteed).
Internet connection for downloading data from Yahoo Finance.
No additional setup beyond library installation.

InstallationInstall Python 3.12:Download from python.org.
Verify installation: Open a terminal and run python --version. It should output Python 3.12.x.

Install Required Libraries:Open a terminal and run:
pip install yfinance pandas matplotlib plotly numpy
These libraries provide:yfinance: Stock data retrieval.
pandas & numpy: Data manipulation.
matplotlib: Static chart generation.
plotly: Interactive charts.

Clone or Download the Repository:Clone via Git: git clone https://github.com/artpersonnft/LifeTimeChartMaker9000.git
Or download the ZIP from the GitHub repo and extract it.
Navigate to the project directory in your terminal.

Usage
The main script is ChartMaker.py (internally referenced as stocks2.py in some documentation). Follow these steps to run it:Step 1: Launch the ScriptOpen a terminal, navigate to the project directory, and run:
python ChartMaker.py

Step 2: Input TickersThe script prompts:
Input Tickers (comma-separated, 1-5 letters each, no suffix, or press Enter for default):
Custom Input: Enter tickers separated by commas (e.g., JNJ, KO, XOM). Each must be 1–5 uppercase letters, no suffixes (e.g., avoid JNJ.TO).
Default: Press Enter to use the built-in list of 28 tickers (e.g., AA, AEP, BA, ... – full list shown in script output).
Validation: Invalid inputs (e.g., suffixes or non-alphabetic) trigger an error and reprompt. Confirmed input shows: Using tickers: ['JNJ', 'KO', 'XOM'].

Step 3: Download Stock DataThe script automatically downloads historical data for each ticker (from ~1900 to present).
Progress messages: Downloading data for JNJ... Data for JNJ starts from 1962-01-02.
Downloads are parallelized across CPU cores for speed.
Notes:Data starts from the ticker's earliest available date (e.g., many begin post-1960).
Failed downloads (e.g., invalid ticker) are logged, but processing continues.
Percentage increases are calculated relative to the first available price.

Step 4: Select Charting OptionAfter downloads, choose from the menu:
Choose a charting option:
1: Group by 5-year buckets from the earliest date
2: Group by majority start dates (10+ tickers per date)
3: Chart all tickers in one chart
4: Chart tickers in partitions of 100 (with price or percentage option)
Enter 1, 2, 3, or 4:
Option 1: 5-Year BucketsGroups tickers by 5-year start date ranges (e.g., 1960–1965).
Generates and saves PNG charts of percentage increases (e.g., chart_0_to_5_years.png).

Option 2: Majority Start DatesGroups by exact start dates shared by 10+ tickers.
Saves PNG percentage increase charts (e.g., chart_start_1962-01-02.png).

Option 3: All-in-One ChartCreates a single PNG for percentage increases.
Opens an interactive Plotly chart in your default browser for raw prices.

Option 4: Partitioned ChartsSplits tickers into batches of ~100.
Prompts: P for raw prices or % for percentage increases.
Generates interactive Plotly HTML files (viewable in browser).

Step 5: View ResultsStatic Charts (Options 1, 2, 3 PNGs): Saved in the project directory. Show percentage increases over time (x-axis: date, y-axis: % change).
Interactive Charts (Options 3, 4): HTML files auto-open in browser or saved locally. Hover for details, zoom/pan enabled.
Interpretation:Positive trends indicate growth; compare across groups for cohort analysis.
Early data may be sparse; charts normalize to starting price = 0%.

Example OutputFor default tickers, expect 5–10 PNG/HTML files depending on option.
Sample filename: partition_1_prices.html (interactive price chart for first 100 tickers).

TroubleshootingDownload Errors: Check internet; ensure tickers are valid (e.g., via Yahoo Finance search). Rerun for retries.
Library Issues: Reinstall with pip install --upgrade yfinance pandas matplotlib plotly numpy.
Memory/Performance: For 100+ custom tickers, Option 4 is recommended to avoid overload.
Date Range: Fixed to historical full; edit script for custom end dates if needed.
No Data for Ticker: Script skips and notifies (e.g., delisted stocks).

Repository Structure
LifeTimeChartMaker9000/
├── ChartMaker.py          # Main script (core logic for data and charts)
├── README.md              # This file
└── requirements.txt       # (Optional: Add for pip install -r)
(Note: Currently minimal; future additions may include sample data or configs.)Contributing
Contributions welcome! Fork the repo, make changes, and submit a pull request. Focus areas: More chart types, CSV export, GUI interface.Fork the project.
Create a feature branch (git checkout -b feature/AmazingFeature).
Commit changes (git commit -m 'Add some AmazingFeature').
Push to branch (git push origin feature/AmazingFeature).
Open a Pull Request.

License
This project is licensed under the MIT License - see the LICENSE file for details. (Add a LICENSE file if not present.)AcknowledgmentsBuilt with open-source libraries: yfinance, pandas, matplotlib, plotly, numpy.
Inspired by stock market visualization needs.
Thanks to Yahoo Finance for free historical data access.

ContactRepository: artpersonnft/LifeTimeChartMaker9000
Issues: Report bugs or request features via GitHub Issues.

