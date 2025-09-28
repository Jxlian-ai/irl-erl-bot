import yfinance as yf, pandas as pd
def yf_load(symbol, period="180d", interval="1h"):
    df = yf.download(symbol, period=period, interval=interval, progress=False)
    if df is None or df.empty: return pd.DataFrame()
    cols = ["Open","High","Low","Close","Volume"]
    for c in cols:
        if c not in df.columns and c.lower() in df.columns:
            df.rename(columns={c.lower(): c}, inplace=True)
    if not set(cols).issubset(df.columns): return pd.DataFrame()
    df.index = pd.to_datetime(df.index)
    return df[cols].dropna()
def resample(df, rule="4H"):
    if df.empty: return df
    return df.resample(rule).agg({"Open":"first","High":"max","Low":"min","Close":"last","Volume":"sum"}).dropna()
