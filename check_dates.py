import pandas as pd

# Read GOOGL data
df_googl = pd.read_csv('data/GOOGL_raw.csv', skiprows=2)
df_googl.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
df_googl['Date'] = pd.to_datetime(df_googl['Date'])
df_googl = df_googl.set_index('Date').sort_index()

# Read SP500 data
df_sp = pd.read_csv('data/^GSPC_raw.csv', skiprows=2)
df_sp.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
df_sp['Date'] = pd.to_datetime(df_sp['Date'])
df_sp = df_sp.set_index('Date').sort_index()

print("=" * 60)
print("DATE RANGE ANALYSIS")
print("=" * 60)
print(f"\nGOOGL:")
print(f"  Start: {df_googl.index.min()}")
print(f"  End: {df_googl.index.max()}")
print(f"  Total rows: {len(df_googl)}")

print(f"\nSP500:")
print(f"  Start: {df_sp.index.min()}")
print(f"  End: {df_sp.index.max()}")
print(f"  Total rows: {len(df_sp)}")

# Check for gaps in trading days (Mon-Fri)
print("\n" + "=" * 60)
print("TRADING DAY GAPS (within date ranges)")
print("=" * 60)

# Create business day range for GOOGL
bday_range_googl = pd.bdate_range(start=df_googl.index.min(), end=df_googl.index.max())
missing_bdays_googl = bday_range_googl[~bday_range_googl.isin(df_googl.index)]
print(f"\nGOOGL:")
print(f"  Expected trading days: {len(bday_range_googl)}")
print(f"  Actual data points: {len(df_googl)}")
print(f"  Missing trading days: {len(missing_bdays_googl)}")
if len(missing_bdays_googl) > 0:
    print(f"  First 10 missing trading days: {missing_bdays_googl[:10].tolist()}")

# Create business day range for SP500
bday_range_sp = pd.bdate_range(start=df_sp.index.min(), end=df_sp.index.max())
missing_bdays_sp = bday_range_sp[~bday_range_sp.isin(df_sp.index)]
print(f"\nSP500:")
print(f"  Expected trading days: {len(bday_range_sp)}")
print(f"  Actual data points: {len(df_sp)}")
print(f"  Missing trading days: {len(missing_bdays_sp)}")
if len(missing_bdays_sp) > 0:
    print(f"  First 10 missing trading days: {missing_bdays_sp[:10].tolist()}")

# Check date alignment
print("\n" + "=" * 60)
print("DATE ALIGNMENT BETWEEN GOOGL AND SP500")
print("=" * 60)
common_dates = df_googl.index.intersection(df_sp.index)
googl_only = df_googl.index.difference(df_sp.index)
sp_only = df_sp.index.difference(df_googl.index)

print(f"\nCommon dates (both have data): {len(common_dates)}")
print(f"GOOGL-only dates: {len(googl_only)}")
if len(googl_only) > 0:
    print(f"  Examples: {googl_only[:5].tolist()}")
print(f"SP500-only dates: {len(sp_only)}")
if len(sp_only) > 0:
    print(f"  Examples: {sp_only[:5].tolist()}")

# Check for consecutive missing days
print("\n" + "=" * 60)
print("CONSECUTIVE MISSING DAYS (potential data quality issues)")
print("=" * 60)

def find_consecutive_gaps(dates, date_range):
    """Find gaps of 3+ consecutive trading days"""
    gaps = []
    prev_date = None
    gap_start = None
    for date in date_range:
        if date not in dates:
            if gap_start is None:
                gap_start = date
            prev_date = date
        else:
            if gap_start is not None and prev_date is not None:
                gap_length = (prev_date - gap_start).days
                if gap_length >= 3:  # More than just a weekend
                    gaps.append((gap_start, prev_date, gap_length))
            gap_start = None
            prev_date = date
    return gaps

gaps_googl = find_consecutive_gaps(df_googl.index, bday_range_googl)
gaps_sp = find_consecutive_gaps(df_sp.index, bday_range_sp)

print(f"\nGOOGL - Gaps of 3+ trading days: {len(gaps_googl)}")
for start, end, length in gaps_googl[:5]:
    print(f"  {start.date()} to {end.date()} ({length} days)")

print(f"\nSP500 - Gaps of 3+ trading days: {len(gaps_sp)}")
for start, end, length in gaps_sp[:5]:
    print(f"  {start.date()} to {end.date()} ({length} days)")

