from datetime import datetime, date
from functools import cache
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use("seaborn")

@cache
def stockData(ticker: str, start: date, end: date) -> pd.DataFrame:
  return yf.download(ticker, start, end).Close.to_frame().rename(columns = { "Close": "price" })