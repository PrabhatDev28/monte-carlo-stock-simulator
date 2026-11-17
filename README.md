# Monte Carlo Stock Price Simulator

Simulates thousands of possible future price paths for a stock using probability and random sampling.

**Tech:** Python, NumPy, pandas, Matplotlib
**Output:** 1,000+ simulated price paths, a scenario distribution, and confidence intervals.

## How it works

1. Download past prices for a stock (using `yfinance`).
2. Calculate the average daily return and the volatility (how much it jumps around).
3. Generate random daily returns from a normal distribution, 1,000 times.
4. Compound those returns into 1,000 possible price paths.
5. Summarize the final prices: average, best/worst case (5th–95th percentile), chance of profit.
6. Plot the paths and the distribution of final prices.

## Run in Google Colab (no installation needed)

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Click **File → Upload notebook** and choose `Monte_Carlo_Stock_Simulator.ipynb`
3. Click **Runtime → Run all**

(Once the repo is on GitHub, you can also open the notebook directly from **File → Open notebook → GitHub** tab.)

## Setup (run on your own computer)

```bash
git clone https://github.com/YOUR-USERNAME/monte-carlo-stock-simulator.git
cd monte-carlo-stock-simulator
pip install -r requirements.txt
```

## Run

```bash
python monte_carlo_simulator.py
```

Change `TICKER`, `DAYS` or `SIMULATIONS` at the top of the file to experiment.
If there is no internet, the program uses sample data so it still runs.

## Output

- Summary printed in the terminal
- `simulation_results.png` – charts of all paths and the final price distribution
- `simulated_paths.csv` – every simulated path

## Limitations

This is a learning project. It assumes returns are normally distributed and the past
average/volatility continue into the future, which real markets don't guarantee.
**Not financial advice.**
