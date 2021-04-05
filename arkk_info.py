import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt

arkk = yf.Ticker("ARKK")


class Data:
    def __init__(self):
        pass

    def update(self):
        price_data = arkk.history(period='1m')
        return [price_data['High'][-1], price_data['Low'][-1], price_data['Close'][-1], price_data['High'].keys()[0]]

    def make_graph(self):
        price_data = arkk.history(period='max')
        all_dates = price_data['Close'].keys()
        oldest = dt.datetime(2018, 1, 1)
        newest = dt.datetime.now()
        relevant = price_data[(all_dates > oldest) & (all_dates < newest)]
        data = relevant['Close']
        dates = data.keys()
        vals = data.values

        ax = plt.axes()
        data.plot(label='Daily Close', xlim=(dates[0], dates[-1]), ylim=(vals.min(), max([160, vals.max()])))
        ax.plot(dates, np.full(len(dates), 150.19), color='black', label='USD$150.19')
        ax.set(xlabel="Date", ylabel="Price (USD)", title=f"ARKK Daily Close Stock Prices")
        ax.legend()
        plt.savefig("plot")
