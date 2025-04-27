import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="黃金即時多空建議系統", page_icon="💹")
st.title("💹 黃金即時多空建議系統（每3秒更新）")

placeholder = st.empty()

def fetch_data():
    data = yf.download('GC=F', period='1d', interval='1m', progress=False)
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA60'] = data['Close'].rolling(window=60).mean()
    return data

while True:
    data = fetch_data()

    if data.empty or pd.isna(data['MA60'].iloc[-1]):
        placeholder.warning("正在載入足夠資料進行分析，請稍候...")
        time.sleep(3)
        continue

    latest_price = data['Close'].iloc[-1]
    ma5 = data['MA5'].iloc[-1]
    ma20 = data['MA20'].iloc[-1]
    ma60 = data['MA60'].iloc[-1]

    if latest_price > ma5 > ma20 > ma60:
        advice = "📈 做多 ✅"
    elif latest_price < ma5 < ma20 < ma60:
        advice = "📉 做空 🔻"
    else:
        advice = "⚠️ 觀望"

    with placeholder.container():
        st.metric("最新即時金價 (XAU/USD)", f"{latest_price:.2f} USD")
        st.write("### 📊 移動平均線 (MA)")
        st.write(f"- **MA5**: {ma5:.2f}")
        st.write(f"- **MA20**: {ma20:.2f}")
        st.write(f"- **MA60**: {ma60:.2f}")
        st.write("---")
        st.write("## 🚨 操作建議：", advice)
        st.caption("每3秒自動刷新一次數據。")

    time.sleep(3)  # 每3秒更新一次
