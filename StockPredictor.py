import FlaskServer
import RedditUtils
import pandas as pd
import datetime as datetime
import time
from flask import url_for
from prawcore.exceptions import Forbidden
import matplotlib.pyplot as plt


#gets dataframe of the combined searches for the ticker and the stock shortName
def getDataframe(arg1, arg2, arg3):
    return RedditUtils.getDataframe(arg3, arg1, arg2)


#Takes dataframe and a string as a stock ticker and returns a link to a image file of the chart
def getSentimentChart(arg1, arg2):
    df = arg1
    ticker_sentiment = df[['Time_Created', 'Overall_Post_Sentiment']]

    print(ticker_sentiment.to_string())
    #create the scatter plot
    scatter_Plot = ticker_sentiment.plot.scatter(x='Time_Created',
                                                 y='Overall_Post_Sentiment')

    fig = scatter_Plot.get_figure()
    filename = arg2 + str(int(time.time())) + ".png"
    filepath = "venv/static/" + filename
    fig.savefig(filepath)
    filepath = url_for('static', filename=filename)
    return filepath

def main():
    FlaskServer.getApp().run()

if __name__ == "__main__":
    main()
