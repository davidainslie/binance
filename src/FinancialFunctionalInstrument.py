from dataclasses import dataclass
from datetime import datetime, date
from functools import cache
from functools import partial
from typing import Callable

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use("seaborn")

@dataclass(frozen = True)
class FinancialInstrument:
  ticker: str
  start: date
  end: date

# TODO - Ignore this first iteration of `stock` giving all prices for given dates.
# @cache
# def stock(ticker: str, start: date, end: date) -> pd.DataFrame:
#   return yf.download(ticker, start, end).Close.to_frame().rename(columns = { "Close": "price" })

@cache
def prices(fi: FinancialInstrument) -> pd.DataFrame:
  return yf.download(fi.ticker, fi.start, fi.end).Close.to_frame().rename(columns = { "Close": "price" })

# TODO - Ignore this first iteration of `logReturns` but keeping as an example of higher order function with currying (all a tad awkward in Python)
# def logReturns(f: Callable[[pd.DataFrame], pd.DataFrame]) -> Callable[[pd.DataFrame], pd.DataFrame]:
#   def logReturns(f: Callable[[pd.DataFrame], pd.DataFrame], df: pd.DataFrame):
#     return df.assign(logReturns = np.log(f(df)))
#
#   return partial(logReturns, f)

def pricesWithLogReturns(fi: FinancialInstrument) -> pd.DataFrame:
  def pricesWithLogReturns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.assign(logReturns = np.log(prices.price / prices.price.shift(1)))

  return pricesWithLogReturns(prices(fi))

def plotPrices(fi: FinancialInstrument):
  prices(fi).price.plot(figsize = (12, 8))
  plt.title(f"Price Chart: {fi.ticker}", fontsize = 15)

def plotReturns(fi: FinancialInstrument, kind = "ts"):
  if kind == "ts":
    pricesWithLogReturns(fi).logReturns.plot(figsize = (12, 8))
    plt.title(f"Returns: {fi.ticker}", fontsize = 15)
  elif kind == "hist":
    pricesWithLogReturns(fi).logReturns.hist(figsize = (12, 8), bins = int(np.sqrt(len(pricesWithLogReturns(fi)))))
    plt.title(f"Frequency of Returns: {fi.ticker}", fontsize = 15)