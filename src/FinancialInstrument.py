import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use("seaborn")

class FinancialInstrument:
  """
  Class for analyzing Financial Instruments like stocks.

  Attributes
  ==========
  ticker: str
      ticker symbol with which to work with
  start: str
      start date for data retrieval
  end: str
      end date for data retrieval

  Methods
  =======
  get_data:
      retrieves daily price data (from yahoo finance) and prepares the data
  log_returns:
      calculates log returns
  plot_prices:
      creates a price chart
  plot_returns:
      plots log returns either as time series ("ts") or histogram ("hist")
  set_ticker:
      sets a new ticker
  mean_return:
      calculates mean return
  std_returns:
      calculates the standard deviation of returns (risk)
  annualized_perf:
      calculates annulized return and risk
  """

  def __init__(self, ticker, start, end):
    self._ticker = ticker
    self.start = start
    self.end = end
    self.get_data()
    self.log_returns()

  def __repr__(self):
    return f"FinancialInstrument(ticker = {self._ticker}, start = {self.start}, end = {self.end})"

  def get_data(self):
    """Retrieves (from yahoo finance) and prepares the data"""
    raw = yf.download(self._ticker, self.start, self.end).Close.to_frame()
    raw.rename(columns = { "Close": "price" }, inplace = True)
    self.data = raw

  def log_returns(self):
    """Calculates log returns"""
    self.data["log_returns"] = np.log(self.data.price / self.data.price.shift(1))

  def plot_prices(self):
    """Creates a price chart"""
    self.data.price.plot(figsize = (12, 8))
    plt.title(f"Price Chart: {self._ticker}", fontsize = 15)

  def plot_returns(self, kind = "ts"):
    """Plots log returns either as time series ("ts") or histogram ("hist")"""
    if kind == "ts":
      self.data.log_returns.plot(figsize = (12, 8))
      plt.title(f"Returns: {self._ticker}", fontsize = 15)
    elif kind == "hist":
      self.data.log_returns.hist(figsize = (12, 8), bins = int(np.sqrt(len(self.data))))
      plt.title(f"Frequency of Returns: {self._ticker}", fontsize = 15)

  def set_ticker(self, ticker = None):
    """Sets a new ticker"""
    if ticker is not None:
      self._ticker = ticker
      self.get_data()
      self.log_returns()

  def mean_return(self, freq = None):
    """Calculates mean return"""
    if freq is None:
      return self.data.log_returns.mean()
    else:
      resampled_price = self.data.price.resample(freq).last()
      resampled_returns = np.log(resampled_price / resampled_price.shift(1))
      return resampled_returns.mean()

  def std_returns(self, freq = None):
    """Calculates the standard deviation of returns (risk)"""
    if freq is None:
      return self.data.log_returns.std()
    else:
      resampled_price = self.data.price.resample(freq).last()
      resampled_returns = np.log(resampled_price / resampled_price.shift(1))
      return resampled_returns.std()

  def annualized_perf(self):
    """Calculates annulized return and risk"""
    mean_return = round(self.data.log_returns.mean() * 252, 3)
    risk = round(self.data.log_returns.std() * np.sqrt(252), 3)
    print(f"Return: {mean_return} | Risk: {risk}")
