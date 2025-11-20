# Stock Outperformance Prediction – Machine Learning Pipeline

## Task Overview

We aim to predict whether a stock will outperform the S&P 500 index in the next 21 trading days (≈ 1 month).

This is framed as a **binary classification problem**:

**Target variable (y):**
- `y = 1` → Stock outperforms S&P 500
- `y = 0` → Stock underperforms or performs equally

**Formally,**

$$y_t = \begin{cases} 1 & \text{if } r_{t,t+21}^{\text{stock}} > r_{t,t+21}^{\text{S\&P}} \\ 0 & \text{otherwise} \end{cases}$$

where $r_{t,t+21}$ is the percentage return over the next 21 trading days.

---

## Input Features (X)

Each observation corresponds to a unique **(stock, date)** pair.

All features are computed using information available **up to that date** — no future leakage.

### Feature Groups

- **Momentum indicators** – rolling returns over 1 week, 1 month, 3 months
- **Volatility metrics** – 21-day rolling std of returns
- **Technical ratios** – price vs. moving averages (e.g., MA20, MA50), daily range, volume z-scores
- **Relative metrics** – stock returns and volatility relative to the S&P 500
- **Macro & sentiment variables** – VIX, Fed Funds Rate, CPI change, market breadth, put/call ratio
- **Sector performance** – sector ETF prices (XLK, XLF, XLV, XLE, XLI)
- **Technical indicators** – market (SPY, QQQ) RSI, moving averages

After preprocessing and normalization, these yield roughly **31 numerical features** per sample.

---

## Modeling Setup

**Task Type:** Supervised binary classification

**Input (X):** Engineered feature matrix (31 features)

**Output (y):** Binary label (1 = Outperform, 0 = Underperform)

**Training procedure:**
1. Construct features using data up to `t`
2. Construct labels using returns from `t` to `t + 21`
3. Split data chronologically (train → validation → test) to respect time ordering
4. Scaling: Standardize continuous features (e.g., z-score)

---

## End Goal

Once trained, the model can take a feature vector for any stock on a given date and output the probability that it will outperform the S&P 500 over the following month.
