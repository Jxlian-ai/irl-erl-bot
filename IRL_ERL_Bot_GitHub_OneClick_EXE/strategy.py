import pandas as pd
from utils import resample
def detect_fvg(df):
    out=[]
    for i in range(len(df)-2):
        c1,c2,c3=df.iloc[i],df.iloc[i+1],df.iloc[i+2]
        if c3["Low"]>c1["High"]: out.append((df.index[i+2],"bull",float(c1["High"]),float(c3["Low"])))
        elif c3["High"]<c1["Low"]: out.append((df.index[i+2],"bear",float(c3["High"]),float(c1["Low"])))
    if not out: return pd.DataFrame(columns=["type","top","bottom"]).set_index(pd.Index([]))
    return pd.DataFrame(out, columns=["time","type","top","bottom"]).set_index("time")
def trend_direction(df_htf, lookback=20):
    if len(df_htf)<lookback+1: return None
    recent=df_htf.tail(lookback)
    return "long" if recent["Close"].iloc[-1] > recent["Close"].mean() else "short"
def compute_factors(df_htf):
    f={}
    td=trend_direction(df_htf)
    if td: f["trend"]=td
    fvg=detect_fvg(df_htf)
    if not fvg.empty:
        last=fvg.iloc[-1]
        f["fvg_bias"]="long" if last["type"]=="bull" else "short"
    if len(df_htf)>51:
        hi=df_htf["High"].rolling(50).max().iloc[-2]
        lo=df_htf["Low"].rolling(50).min().iloc[-2]
        last=df_htf.iloc[-1]
        if last["High"]>=hi: f["sweep_bias"]="short"
        elif last["Low"]<=lo: f["sweep_bias"]="long"
    return f
def decide_direction(factors):
    votes={"long":0,"short":0}
    for k in ("trend","fvg_bias","sweep_bias"):
        v=factors.get(k)
        if v in ("long","short"): votes[v]+=1
    if votes["long"]==votes["short"]==0: return None, votes
    return ("long" if votes["long"]>=votes["short"] else "short"), votes
