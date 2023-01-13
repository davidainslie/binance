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
  """Retrieves (from yahoo finance) and prepares the data"""
  return yf.download(fi.ticker, fi.start, fi.end).Close.to_frame().rename(columns = { "Close": "price" })

# TODO - Ignore this first iteration of `logReturns` but keeping as an example of higher order function with currying (all a tad awkward in Python)
# def logReturns(f: Callable[[pd.DataFrame], pd.DataFrame]) -> Callable[[pd.DataFrame], pd.DataFrame]:
#   def logReturns(f: Callable[[pd.DataFrame], pd.DataFrame], df: pd.DataFrame):
#     return df.assign(logReturns = np.log(f(df)))
#
#   return partial(logReturns, f)

def pricesWithLogReturns(fi: FinancialInstrument) -> pd.DataFrame:
  """Calculates log returns"""
  def pricesWithLogReturns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.assign(logReturns = np.log(prices.price / prices.price.shift(1)))

  return pricesWithLogReturns(prices(fi))

def plotPrices(fi: FinancialInstrument):
  """Creates a price chart"""
  prices(fi).price.plot(figsize = (12, 8))
  plt.title(f"Price Chart: {fi.ticker}", fontsize = 15)

def plotReturns(fi: FinancialInstrument, kind = "ts"):
  """Plots log returns either as time series ("ts") or histogram ("hist")"""
  if kind == "ts":
    pricesWithLogReturns(fi).logReturns.plot(figsize = (12, 8))
    plt.title(f"Returns: {fi.ticker}", fontsize = 15)
  elif kind == "hist":
    pricesWithLogReturns(fi).logReturns.hist(figsize = (12, 8), bins = int(np.sqrt(len(pricesWithLogReturns(fi)))))
    plt.title(f"Frequency of Returns: {fi.ticker}", fontsize = 15)

def meanReturn(fi: FinancialInstrument, frequency: int = None):
  """Calculates mean return"""
  if frequency is None:
    return pricesWithLogReturns(fi).logReturns.mean() # Mean return based on daily data by default
  else:
    resampledPrice = prices(fi).price.resample(frequency).last()
    resampledReturns = np.log(resampledPrice / resampledPrice.shift(1))

    return resampledReturns.mean()

def standardReturns(fi: FinancialInstrument, frequency: int = None):
  """Calculates the standard deviation of returns (risk)"""
  if frequency is None:
    return pricesWithLogReturns(fi).logReturns.std()
  else:
    resampledPrice = prices(fi).price.resample(frequency).last()
    resampledReturns = np.log(resampledPrice / resampledPrice.shift(1))
    return resampledReturns.std()

def annualisedPerformance(fi: FinancialInstrument):
  """Calculates annulized return and risk"""
  meanReturn = round(pricesWithLogReturns(fi).logReturns.mean() * 252, 3) # 252 trading days in a year
  risk = round(pricesWithLogReturns(fi).logReturns.std() * np.sqrt(252), 3)
  print(f"Return: {meanReturn} | Risk: {risk}")