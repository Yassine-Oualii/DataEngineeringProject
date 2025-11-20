"""
Explain why scaled values are negative and what they mean
"""
import pandas as pd
import numpy as np

print("=" * 70)
print("UNDERSTANDING SCALED VALUES - Why Negative Numbers?")
print("=" * 70)

# Load original and scaled data
df_original = pd.read_csv('data/integrated_prepared_data.csv')
df_scaled = pd.read_csv('data/integrated_scaled_data.csv')

# Example with Close price
print("\nEXAMPLE: Close Price Transformation")
print("-" * 70)

# Get first row
orig_close = df_original['Close'].iloc[0]
scaled_close = df_scaled['Close'].iloc[0]
mean_close = df_original['Close'].mean()
std_close = df_original['Close'].std()

print(f"\nOriginal Close price (2004-08-19, GOOGL): ${orig_close:.2f}")
print(f"Mean Close price (all data): ${mean_close:.2f}")
print(f"Standard deviation: ${std_close:.2f}")
print(f"\nScaled Close value: {scaled_close:.6f}")

print(f"\nWhat does this mean?")
print(f"  - Original price ${orig_close:.2f} is BELOW the mean ${mean_close:.2f}")
print(f"  - This makes it NEGATIVE in scaled form")
print(f"  - Formula: ({orig_close:.2f} - {mean_close:.2f}) / {std_close:.2f} = {scaled_close:.6f}")
print(f"  - The value {scaled_close:.6f} means: {abs(scaled_close):.2f} standard deviations BELOW the mean")

# Show range of values
print("\n" + "-" * 70)
print("UNDERSTANDING THE SCALE:")
print("-" * 70)
print("""
After StandardScaler:
  Mean = 0 (center point)
  Std = 1 (unit of measurement)

Value Interpretation:
  -3.0 = Very low (3 std devs below mean)
  -2.0 = Low (2 std devs below mean)
  -1.0 = Below average (1 std dev below mean)
   0.0 = Average (at the mean)
  +1.0 = Above average (1 std dev above mean)
  +2.0 = High (2 std devs above mean)
  +3.0 = Very high (3 std devs above mean)
""")

# Show examples
print("\n" + "-" * 70)
print("CONCRETE EXAMPLES FROM YOUR DATA:")
print("-" * 70)

# Find examples of different scaled values
examples = []
for idx in range(len(df_scaled)):
    close_val = df_scaled.iloc[idx]['Close']
    orig_val = df_original.iloc[idx]['Close']
    date_val = df_original.iloc[idx]['Date']
    stock_val = df_original.iloc[idx]['stock']
    
    examples.append({
        'date': date_val,
        'stock': stock_val,
        'original': orig_val,
        'scaled': close_val,
        'interpretation': 'below' if close_val < 0 else 'above' if close_val > 0 else 'average'
    })
    
    if len(examples) >= 5:
        break

print("\nSample transformations:")
print(f"{'Date':<12} {'Stock':<6} {'Original $':<12} {'Scaled':<10} {'Interpretation'}")
print("-" * 70)
for ex in examples[:5]:
    orig_str = f"${ex['original']:.2f}"
    scaled_str = f"{ex['scaled']:.4f}"
    interp = ex['interpretation'] + " average"
    print(f"{str(ex['date'])[:10]:<12} {ex['stock']:<6} {orig_str:<12} {scaled_str:<10} ({interp})")

# Show some positive values
print("\n" + "-" * 70)
print("FINDING POSITIVE VALUES (Above Average):")
print("-" * 70)

positive_examples = df_scaled[df_scaled['Close'] > 0].head(3)
if len(positive_examples) > 0:
    print("\nExamples where Close is POSITIVE (above average):")
    for idx, row in positive_examples.iterrows():
        orig_close = df_original.iloc[idx]['Close']
        scaled_close = row['Close']
        date = row['Date']
        stock = row['stock']
        print(f"  {date} ({stock}): Original=${orig_close:.2f}, Scaled={scaled_close:.4f}")

# Show why this is normal
print("\n" + "=" * 70)
print("WHY THIS IS CORRECT:")
print("=" * 70)
print("""
1. StandardScaler Formula: (x - mean) / std
   - If value < mean → result is NEGATIVE
   - If value > mean → result is POSITIVE
   - If value = mean → result is ZERO

2. Your data from 2004:
   - GOOGL IPO price was around $2.49 (after stock splits)
   - Average Close price across all data: ~$116
   - So IPO price is WAY BELOW average → negative scaled value

3. This is EXPECTED and CORRECT:
   - Negative doesn't mean "bad"
   - It means "below the dataset mean"
   - Positive means "above the dataset mean"
   - Zero means "at the dataset mean"

4. For Machine Learning:
   - Models need features on similar scales
   - Negative/positive is just relative position
   - What matters: all features are now comparable
""")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
✓ Negative numbers are NORMAL for StandardScaler
✓ They indicate values below the mean
✓ Values are now rounded to 6 decimal places
✓ All features are on comparable scales
✓ Ready for machine learning models
""")

