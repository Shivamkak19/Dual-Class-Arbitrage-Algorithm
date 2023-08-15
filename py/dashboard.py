from tickers import tickers

import pandas as pd
import streamlit as st

ticker = tickers()
stock_df = ticker.getStock()

st.write(stock_df)