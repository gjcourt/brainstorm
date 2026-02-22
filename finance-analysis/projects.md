# Finance & Analysis Projects (15)

This category focuses on EDGAR parsing, DCF modeling, and personal finance tracking.

### 51. Automated EDGAR 10-K/10-Q XBRL Parser
*   **Difficulty:** Hard
*   **Time Commitment:** Months
*   **Target Skills:** Go, XML/XBRL Parsing, SEC EDGAR API, Database Design
*   **Description:** Build a Go service that automatically downloads and parses XBRL data from the SEC EDGAR database. Extract key financial metrics (Revenue, Net Income, Free Cash Flow) from 10-K and 10-Q filings and store them in a structured PostgreSQL database.

### 52. Discounted Cash Flow (DCF) Model Generator
*   **Difficulty:** Hard
*   **Time Commitment:** Months
*   **Target Skills:** Financial Modeling, WACC Calculation, Terminal Value, Go/Python
*   **Description:** Create an application that takes the parsed EDGAR data (from Project 51) and automatically generates a baseline Discounted Cash Flow (DCF) model for a given ticker. Allow users to tweak assumptions (growth rates, discount rates) via a web interface.

### 53. Self-Hosted Personal Balance Sheet Tracker
*   **Difficulty:** Medium
*   **Time Commitment:** 1-4 weeks
*   **Target Skills:** Plaid API, React, Go, Double-Entry Accounting
*   **Description:** Build a custom, self-hosted application to track your personal net worth. Integrate with the Plaid API to pull live bank and brokerage balances, categorize assets and liabilities, and calculate personal financial ratios (e.g., debt-to-equity).

### 54. Options Pricing Model (Black-Scholes) in Go
*   **Difficulty:** Medium
*   **Time Commitment:** 1-4 weeks
*   **Target Skills:** Go, Quantitative Finance, Statistical Math
*   **Description:** Implement the Black-Scholes-Merton options pricing model from scratch in Go. Calculate the theoretical price of European call and put options, as well as the "Greeks" (Delta, Gamma, Theta, Vega, Rho).

### 55. SEC Filing Sentiment Analysis using LLMs
*   **Difficulty:** Hard
*   **Time Commitment:** Months
*   **Target Skills:** NLP, Local LLMs (Llama 3), Python, Text Extraction
*   **Description:** Build a pipeline that downloads the "Management's Discussion and Analysis" (MD&A) section of 10-K filings. Use a locally hosted LLM to perform sentiment analysis, identifying shifts in management tone (optimistic vs. pessimistic) over time.

### 56. Portfolio Rebalancing Algorithm
*   **Difficulty:** Medium
*   **Time Commitment:** 1-4 weeks
*   **Target Skills:** Modern Portfolio Theory (MPT), Optimization Algorithms, Brokerage APIs
*   **Description:** Write a script that connects to your brokerage account (e.g., Interactive Brokers or Alpaca API), compares your current asset allocation against a target portfolio, and generates the optimal buy/sell orders to rebalance while minimizing tax impact.

### 57. Historical Stock Data Backtesting Engine
*   **Difficulty:** Hard
*   **Time Commitment:** Months
*   **Target Skills:** Time-Series Databases (TimescaleDB), Event-Driven Architecture, Go
*   **Description:** Build a high-performance backtesting engine in Go. Ingest historical OHLCV (Open, High, Low, Close, Volume) data into TimescaleDB and write an event-driven system to test custom trading strategies against historical data, accounting for slippage and commissions.

### 58. Real-time Market Data Pipeline via WebSockets
*   **Difficulty:** Medium
*   **Time Commitment:** 1-4 weeks
*   **Target Skills:** WebSockets, Redis Pub/Sub, Go Concurrency
*   **Description:** Connect to a real-time market data provider (like Polygon.io or Alpaca) via WebSockets. Ingest the live tick data, calculate moving averages or VWAP in real-time using Go channels, and broadcast the results to a frontend dashboard via Redis Pub/Sub.

### 59. Financial Terminology Flashcard App
*   **Difficulty:** Easy
*   **Time Commitment:** 1-2 days
*   **Target Skills:** React Native/Flutter, Spaced Repetition Algorithms
*   **Description:** Build a simple mobile or web app using a spaced repetition algorithm (like SuperMemo-2) to memorize complex financial terminology, accounting principles, and valuation formulas.

### 60. Macro-Economic Indicator Dashboard
*   **Difficulty:** Medium
*   **Time Commitment:** 1-4 weeks
*   **Target Skills:** FRED API, Data Visualization (D3.js/Grafana), Data Pipelines
*   **Description:** Create a dashboard that automatically pulls key macroeconomic indicators from the Federal Reserve Economic Data (FRED) API (e.g., Yield Curve, CPI, Unemployment Rate, M2 Money Supply) and visualizes their historical trends and correlations.

### 61. Insider Trading Tracker and Alert System
*   **Difficulty:** Medium
*   **Time Commitment:** 1-4 weeks
*   **Target Skills:** SEC Form 4 Parsing, Web Scraping, Notification Systems (Slack/Discord)
*   **Description:** Build a scraper that monitors the SEC EDGAR database for Form 4 filings (Statement of Changes in Beneficial Ownership). Parse the data to identify significant insider buying or selling and send real-time alerts to a Slack or Discord channel.

### 62. Dividend Yield and Growth Screener
*   **Difficulty:** Medium
*   **Time Commitment:** 1-4 weeks
*   **Target Skills:** Financial APIs (FMP/Alpha Vantage), SQL, Data Filtering
*   **Description:** Create a stock screener focused on dividend investing. Pull historical dividend payout data, calculate the Dividend Yield, Payout Ratio, and 5-year Dividend Growth Rate (CAGR), and filter for companies that meet specific criteria (e.g., Dividend Aristocrats).

### 63. Cryptocurrency Arbitrage Bot
*   **Difficulty:** Hard
*   **Time Commitment:** Months
*   **Target Skills:** High-Frequency Trading Concepts, Multiple Exchange APIs, Low Latency Go
*   **Description:** Write a bot in Go that connects to multiple cryptocurrency exchanges (e.g., Binance, Coinbase, Kraken) simultaneously. Monitor order books for price discrepancies across exchanges and execute triangular or spatial arbitrage trades when profitable.

### 64. Personal Expense Categorization using ML
*   **Difficulty:** Medium
*   **Time Commitment:** 1-4 weeks
*   **Target Skills:** Python, Scikit-Learn, NLP, CSV Parsing
*   **Description:** Export your credit card and bank statements as CSVs. Train a machine learning model (like a Naive Bayes classifier or a simple neural network) to automatically categorize transactions (e.g., Groceries, Dining, Utilities) based on the merchant name and amount.

### 65. Peer-to-Peer Lending Portfolio Analyzer
*   **Difficulty:** Medium
*   **Time Commitment:** 1-4 weeks
*   **Target Skills:** API Integration, Risk Modeling, Data Visualization
*   **Description:** If you use P2P lending platforms (like Prosper or LendingClub), build a tool that downloads your loan portfolio via their API. Analyze the default rates, calculate your true annualized return (XIRR), and visualize the risk distribution of your notes.
