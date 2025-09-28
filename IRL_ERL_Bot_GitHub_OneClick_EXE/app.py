import streamlit as st, json, pandas as pd, matplotlib.pyplot as plt
from backtest import run_backtest_symbol
from journal import read_trades, ensure_db

st.set_page_config(page_title="IRL→ERL Bot", layout="wide")
st.title("IRL→ERL Trading Bot")

DEFAULT_SYMBOLS = ["GDAXI","GC=F","SI=F","EURUSD=X","GBPUSD=X","NZDUSD=X","AUDUSD=X","USDJPY=X","USDCHF=X","USDCAD=X",
                   "EURAUD=X","GBPAUD=X","EURGBP=X","GBPNZD=X","AUDJPY=X","NZDJPY=X","EURJPY=X","GBPJPY=X","CHFJPY=X","CADJPY=X",
                   "AUDCAD=X","NZDCAD=X","EURCAD=X","GBPCAD=X","AUDNZD=X","EURNZD=X"]

tab1, tab2 = st.tabs(["Backtest","Trades"])

with tab1:
    st.subheader("Backtest")
    sym = st.selectbox("Symbol", DEFAULT_SYMBOLS, index=0)
    minf = st.slider("Min. Faktoren", 1, 6, 3)
    if st.button("Backtest starten"):
        with st.spinner("Läuft..."):
            res=run_backtest_symbol(sym, db_path="trades.db", min_factors=minf)
        st.write(res)

with tab2:
    st.subheader("Journal")
    ensure_db("trades.db")
    df=read_trades("trades.db")
    if df.empty:
        st.info("Noch keine Trades gespeichert.")
    else:
        st.dataframe(df)
        df2=df.sort_values("time")
        df2["cum_pnl"]=df2["pnl"].cumsum()
        st.line_chart(df2.set_index("time")["cum_pnl"])
