"""
Monte Carlo Stock Price Simulator
---------------------------------
Simulates thousands of possible future price paths for a stock
using probability and random sampling.

Libraries: NumPy, pandas, Matplotlib (+ yfinance for real stock data)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# SETTINGS - change these to experiment!
# ------------------------------------------------------------
TICKER = "AAPL"          # Stock symbol (e.g. "TSLA", "MSFT", "RELIANCE.NS")
HISTORY_PERIOD = "2y"    # How much past data to learn from
DAYS = 252               # Days to simulate (252 trading days = 1 year)
SIMULATIONS = 1000       # Number of possible futures to simulate


# ------------------------------------------------------------
# STEP 1: Get historical stock prices
# ------------------------------------------------------------
def get_prices(ticker, period):
    """Download past prices. If download fails, use fake sample data."""
    try:
        import yfinance as yf
        data = yf.download(ticker, period=period, progress=False)
        prices = data["Close"].squeeze().dropna()
        if len(prices) < 30:
            raise ValueError("Not enough data")
        print(f"Downloaded {len(prices)} days of {ticker} prices.")
        return prices
    except Exception as error:
        print(f"Could not download data ({error}).")
        print("Using sample data instead so the program still works.\n")
        np.random.seed(1)
        fake_returns = np.random.normal(0.0005, 0.015, 500)
        return pd.Series(100 * np.cumprod(1 + fake_returns))


# ------------------------------------------------------------
# STEP 2: Learn from history (average move and volatility)
# ------------------------------------------------------------
def get_daily_stats(prices):
    daily_returns = prices.pct_change().dropna()   # % change each day
    average = daily_returns.mean()                 # typical daily move
    volatility = daily_returns.std()               # how much it jumps around
    return average, volatility


# ------------------------------------------------------------
# STEP 3: Run the Monte Carlo simulation
# ------------------------------------------------------------
def simulate(start_price, average, volatility, days, simulations):
    # Random daily returns: one column per simulation
    random_returns = np.random.normal(average, volatility, (days, simulations))

    # Turn returns into prices (compounding day after day)
    paths = start_price * np.cumprod(1 + random_returns, axis=0)

    # Put the starting price on the first row
    start_row = np.full((1, simulations), start_price)
    return np.vstack([start_row, paths])


# ------------------------------------------------------------
# STEP 4: Summarize the results
# ------------------------------------------------------------
def summarize(paths, start_price):
    final_prices = paths[-1]                       # price at the end of each path
    summary = {
        "Starting price": start_price,
        "Average final price": final_prices.mean(),
        "Median final price": np.median(final_prices),
        "Worst case (5th percentile)": np.percentile(final_prices, 5),
        "Best case (95th percentile)": np.percentile(final_prices, 95),
        "Chance of profit (%)": (final_prices > start_price).mean() * 100,
    }
    return final_prices, summary


# ------------------------------------------------------------
# STEP 5: Draw the charts
# ------------------------------------------------------------
def make_charts(paths, final_prices, start_price, ticker):
    fig, (left, right) = plt.subplots(1, 2, figsize=(14, 5))

    # Chart 1: all simulated price paths
    left.plot(paths, alpha=0.1, linewidth=0.7)
    left.plot(paths.mean(axis=1), color="black", linewidth=2, label="Average path")
    left.set_title(f"{paths.shape[1]} Simulated Price Paths for {ticker}")
    left.set_xlabel("Days")
    left.set_ylabel("Price")
    left.legend()

    # Chart 2: distribution of final prices + confidence interval
    low = np.percentile(final_prices, 5)
    high = np.percentile(final_prices, 95)
    right.hist(final_prices, bins=50, color="skyblue", edgecolor="white")
    right.axvline(start_price, color="black", linestyle="--", label="Start price")
    right.axvline(low, color="red", linestyle="--", label="5th percentile")
    right.axvline(high, color="green", linestyle="--", label="95th percentile")
    right.set_title("Distribution of Final Prices (90% Confidence Interval)")
    right.set_xlabel("Final price")
    right.set_ylabel("Number of simulations")
    right.legend()

    plt.tight_layout()
    plt.savefig("simulation_results.png", dpi=150)
    print("Chart saved as simulation_results.png")
    plt.show()


# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------
def main():
    prices = get_prices(TICKER, HISTORY_PERIOD)
    start_price = float(prices.iloc[-1])
    average, volatility = get_daily_stats(prices)

    paths = simulate(start_price, average, volatility, DAYS, SIMULATIONS)
    final_prices, summary = summarize(paths, start_price)

    print(f"\n--- Results after {DAYS} days ({SIMULATIONS} simulations) ---")
    for name, value in summary.items():
        print(f"{name}: {value:.2f}")

    # Save results to a CSV file
    pd.DataFrame(paths).to_csv("simulated_paths.csv", index=False)
    print("\nAll paths saved as simulated_paths.csv")

    make_charts(paths, final_prices, start_price, TICKER)


if __name__ == "__main__":
    main()
