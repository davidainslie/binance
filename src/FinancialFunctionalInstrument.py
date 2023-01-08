from datetime import datetime, date
from functools import cache
from functools import partial
from typing import Callable

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use("seaborn")

@cache
def stock(ticker: str, start: date, end: date) -> pd.DataFrame:
  return yf.download(ticker, start, end).Close.to_frame().rename(columns = { "Close": "price" })

# TODO - Ignore this first iteration of `logReturns` but keeping as an example of higher order function with currying (all a tad awkward in Python)
# def logReturns(f: Callable[[pd.DataFrame], pd.DataFrame]) -> Callable[[pd.DataFrame], pd.DataFrame]:
#   def logReturns(f: Callable[[pd.DataFrame], pd.DataFrame], df: pd.DataFrame):
#     return df.assign(logReturns = np.log(f(df)))
#
#   return partial(logReturns, f)

def logReturns(stock: pd.DataFrame) -> pd.DataFrame:
  return stock.assign(logReturns = np.log(stock.price / stock.price.shift(1)))