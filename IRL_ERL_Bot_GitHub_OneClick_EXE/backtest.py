import json
from datetime import datetime
from utils import yf_load, resample
from strategy import detect_fvg, compute_factors, decide_direction
from journal import insert_trade, ensure_db

def run_backtest_symbol(symbol, db_path="trades.db", min_factors=3):
    df_ltf=yf_load(symbol, period="180d", interval="1h")
    if df_ltf.empty: return {"ok":False,"msg":"no data"}
    df_htf=resample(df_ltf,"4H")
    if df_htf.empty: return {"ok":False,"msg":"no htf data"}
    factors=compute_factors(df_htf)
    direction,votes=decide_direction(factors)
    ok_count=sum([1 for v in factors.values() if (v is True) or (v in ("long","short"))])
    if direction is None or ok_count<min_factors:
        return {"ok":False,"msg":f"confluence {ok_count}"}
    k=df_ltf.iloc[-1]; entry=float(k["Close"])
    if direction=="long":
        stop=float(k["Low"])*0.999; tp=entry+(entry-stop)*2
    else:
        stop=float(k["High"])*1.001; tp=entry-(stop-entry)*2
    result="no_hit"; pnl=0.0
    for _,r in df_ltf.tail(120).iterrows():
        if direction=="long":
            if r["Low"]<=stop: result="stop"; pnl=stop-entry; break
            if r["High"]>=tp:  result="tp";   pnl=tp-entry;   break
        else:
            if r["High"]>=stop: result="stop"; pnl=entry-stop; break
            if r["Low"]<=tp:   result="tp";   pnl=entry-tp;   break
    ensure_db(db_path)
    insert_trade(db_path, time=datetime.utcnow().isoformat(), symbol=symbol, direction=direction,
                 entry=entry, stop=stop, tp=tp, result=result, pnl=pnl, factors=json.dumps(factors), live=0)
    return {"ok":True,"msg":result,"pnl":pnl}
